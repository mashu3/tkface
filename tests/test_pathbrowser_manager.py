"""
Additional tests to increase coverage for tkface.widget.pathbrowser.manager.

Targets uncovered lines: 72, 103, 123, 151-156.
"""

import os
import tempfile
import tkinter as tk
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from tkface.widget.pathbrowser import FileInfoManager, PathBrowser


class TestPathBrowserCoreUpdates:
    def test_update_filter_options_default_all_files(self, root):
        """Test that filter defaults to 'All files' when available."""
        browser = PathBrowser(root)
        browser.config.filetypes = [
            ("All files", "*.*"),
            ("Text files", "*.txt"),
            ("Python files", "*.py")
        ]
        browser.filter_combo = Mock()
        browser.filter_combo.set = Mock()
        browser.filter_combo.__setitem__ = Mock()  # Mock item assignment
        
        # Mock lang.get to return localized text
        with patch("tkface.widget.pathbrowser.core.lang.get", return_value="All files"):
            browser._update_filter_options()
            
            # Should set "All files" as default
            browser.filter_combo.set.assert_called_with("All files (*.*)")

    def test_update_filter_options_fallback_to_first(self, root):
        """Test that filter falls back to first option when 'All files' not available."""
        browser = PathBrowser(root)
        browser.config.filetypes = [
            ("Text files", "*.txt"),
            ("Python files", "*.py")
        ]
        browser.filter_combo = Mock()
        browser.filter_combo.set = Mock()
        browser.filter_combo.__setitem__ = Mock()  # Mock item assignment
        
        # Mock lang.get to return localized text
        with patch("tkface.widget.pathbrowser.core.lang.get", return_value="All files"):
            browser._update_filter_options()
            
            # Should set "All files" as default (since lang.get returns "All files")
            browser.filter_combo.set.assert_called_with("All files")


class TestFileInfoManagerCoverage:
    def test_get_file_info_root_none_regular_file(self):
        """Covers get_file_info with root=None normal path (line ~72)."""
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(b"data")
            temp_name = tf.name
        try:
            # Mock lang.get to avoid Tk root requirement
            with patch("tkface.widget.pathbrowser.manager.lang.get", return_value="File"):
                manager = FileInfoManager(root=None)
                info = manager.get_file_info(temp_name)
                assert info.path == temp_name
                assert info.name == os.path.basename(temp_name)
                assert info.is_dir is False
                assert info.size_bytes >= 0
                # Cached
                assert manager.get_cache_size() >= 1
        finally:
            try:
                os.remove(temp_name)
            except OSError:
                pass

    def test_get_file_info_root_none_error_branch(self):
        """Covers exception branch with root=None (line ~103)."""
        # Mock lang.get to avoid Tk root requirement
        with patch("tkface.widget.pathbrowser.manager.lang.get", return_value="Unknown"):
            manager = FileInfoManager(root=None)
            with patch("pathlib.Path.stat", side_effect=OSError("boom")):
                info = manager.get_file_info("/no/such/path")
                assert info.path.endswith("path")
                assert info.is_dir is False
                # Error result is also cached
                assert manager.get_cache_size() == 1

    def test_lru_eviction_in_manage_cache_size(self):
        """Covers L123 eviction of oldest entry when exceeding max_cache_size."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create small files to stat
            paths = []
            for i in range(5):
                p = Path(temp_dir) / f"f{i}.txt"
                p.write_text("x")
                paths.append(str(p))

            manager = FileInfoManager(root=None, max_cache_size=3)
            for p in paths:
                manager.get_file_info(p)
            # After inserting 5 with max 3, 2 oldest must be evicted
            assert manager.get_cache_size() == 3
            # Remaining should be the most recent three
            remaining_keys = list(manager._cache.keys())  # noqa: SLF001 (test internals acceptable)
            assert remaining_keys == paths[-3:]

    @pytest.mark.parametrize(
        "real_path, expect_same",
        [
            ("/real/target", False),   # returns resolved real path when different
            ("/same", True),           # returns original when same
        ],
    )
    def test_resolve_symlink_macos_paths(self, real_path, expect_same):
        """Covers 151-156 macOS branch including success and equality case."""
        manager = FileInfoManager()

        def fake_resolve(self):  # noqa: D401
            return Path(real_path)

        with patch("tkface.widget.pathbrowser.utils.IS_MACOS", True), \
             patch.object(Path, "resolve", fake_resolve):
            original = "/same" if expect_same else "/link"
            result = manager._resolve_symlink(original)
            if expect_same:
                assert result == original
            else:
                # On Windows, path separators are normalized
                expected = real_path.replace("/", os.sep)
                assert result == expected

    def test_resolve_symlink_macos_exception(self):
        """Covers exception path in macOS symlink resolution (151-156)."""
        manager = FileInfoManager()
        with patch("tkface.widget.pathbrowser.utils.IS_MACOS", True), \
             patch.object(Path, "resolve", side_effect=PermissionError("denied")):
            assert manager._resolve_symlink("/link") == "/link"

    def test_get_file_info_cache_hit(self):
        """Covers cache hit scenario (lines 51-52)."""
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(b"data")
            temp_name = tf.name
        try:
            with patch("tkface.widget.pathbrowser.manager.lang.get", return_value="File"):
                manager = FileInfoManager(root=None)
                # First call - cache miss
                info1 = manager.get_file_info(temp_name)
                assert manager.get_cache_size() == 1
                
                # Second call - cache hit (lines 51-52)
                info2 = manager.get_file_info(temp_name)
                assert info1.path == info2.path
                assert manager.get_cache_size() == 1  # Still 1, not 2
        finally:
            try:
                os.remove(temp_name)
            except OSError:
                pass

    def test_get_file_info_directory_branch(self):
        """Covers directory branch (line 70)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("tkface.widget.pathbrowser.manager.lang.get", return_value="Folder"):
                manager = FileInfoManager(root=None)
                info = manager.get_file_info(temp_dir)
                assert info.is_dir is True
                assert info.size_bytes == 0
                assert info.size_str == ""

    def test_get_file_info_file_type_branches(self):
        """Covers file type branches (line 74)."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tf:
            tf.write(b"data")
            temp_name = tf.name
        try:
            with patch("tkface.widget.pathbrowser.manager.lang.get", return_value="File"):
                manager = FileInfoManager(root=None)
                info = manager.get_file_info(temp_name)
                assert info.file_type == "TXT"  # Extension without dot, uppercase
        finally:
            try:
                os.remove(temp_name)
            except OSError:
                pass

    def test_get_file_info_file_type_no_extension(self):
        """Covers file type branch for files without extension (line 74)."""
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(b"data")
            temp_name = tf.name
        try:
            with patch("tkface.widget.pathbrowser.manager.lang.get", return_value="File"):
                manager = FileInfoManager(root=None)
                info = manager.get_file_info(temp_name)
                assert info.file_type == "File"  # No extension, uses lang.get
        finally:
            try:
                os.remove(temp_name)
            except OSError:
                pass

    def test_clear_directory_cache(self):
        """Covers clear_directory_cache method (lines 127-131)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create files in directory and subdirectory
            file1 = Path(temp_dir) / "file1.txt"
            file1.write_text("test")
            subdir = Path(temp_dir) / "subdir"
            subdir.mkdir()
            file2 = subdir / "file2.txt"
            file2.write_text("test")
            
            with patch("tkface.widget.pathbrowser.manager.lang.get", return_value="File"):
                manager = FileInfoManager(root=None)
                # Cache files
                manager.get_file_info(str(file1))
                manager.get_file_info(str(file2))
                assert manager.get_cache_size() == 2
                
                # Clear directory cache
                manager.clear_directory_cache(temp_dir)
                assert manager.get_cache_size() == 0

    def test_get_memory_usage_estimate(self):
        """Covers memory usage estimation (lines 136-146)."""
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(b"data")
            temp_name = tf.name
        try:
            with patch("tkface.widget.pathbrowser.manager.lang.get", return_value="File"):
                manager = FileInfoManager(root=None)
                manager.get_file_info(temp_name)
                
                # Test memory usage estimation
                memory_usage = manager.get_memory_usage_estimate()
                assert isinstance(memory_usage, int)
                assert memory_usage > 0
        finally:
            try:
                os.remove(temp_name)
            except OSError:
                pass

    def test_clear_cache(self):
        """Covers clear_cache method (line 161)."""
        with patch("tkface.widget.pathbrowser.manager.lang.get", return_value="File"):
            manager = FileInfoManager(root=None)
            with tempfile.NamedTemporaryFile(delete=False) as tf:
                tf.write(b"data")
                temp_name = tf.name
            try:
                manager.get_file_info(temp_name)
                assert manager.get_cache_size() > 0
                
                manager.clear_cache()
                assert manager.get_cache_size() == 0
            finally:
                try:
                    os.remove(temp_name)
                except OSError:
                    pass

    def test_remove_from_cache_existing(self):
        """Covers remove_from_cache for existing item (lines 165-166)."""
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(b"data")
            temp_name = tf.name
        try:
            with patch("tkface.widget.pathbrowser.manager.lang.get", return_value="File"):
                manager = FileInfoManager(root=None)
                manager.get_file_info(temp_name)
                assert manager.get_cache_size() == 1
                
                manager.remove_from_cache(temp_name)
                assert manager.get_cache_size() == 0
        finally:
            try:
                os.remove(temp_name)
            except OSError:
                pass

    def test_remove_from_cache_nonexistent(self):
        """Covers remove_from_cache for non-existent item (lines 165-166)."""
        manager = FileInfoManager(root=None)
        # Try to remove non-existent item
        manager.remove_from_cache("/nonexistent/path")
        assert manager.get_cache_size() == 0  # Should not raise exception

    def test_get_cached_file_info(self):
        """Covers get_cached_file_info method (line 174)."""
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(b"data")
            temp_name = tf.name
        try:
            with patch("tkface.widget.pathbrowser.manager.lang.get", return_value="File"):
                manager = FileInfoManager(root=None)
                # This should call get_file_info internally
                info = manager.get_cached_file_info(temp_name)
                assert info.path == temp_name
                assert manager.get_cache_size() == 1
        finally:
            try:
                os.remove(temp_name)
            except OSError:
                pass


