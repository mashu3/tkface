"""
Tests for PathBrowser widget module.

This module tests the new modular structure of PathBrowser.
"""

from pathlib import Path
import pytest

from tkface.widget.pathbrowser import (
    PathBrowser,
    PathBrowserConfig,
    PathBrowserState,
    FileInfoManager,
    FileInfo,
    format_size,
    get_pathbrowser_theme,
    get_pathbrowser_themes,
    PathBrowserTheme
)


class TestPathBrowserModule:
    """Test the PathBrowser module structure."""

    def test_imports(self):
        """Test that all imports work correctly."""
        # Test that all classes can be imported
        assert PathBrowser is not None
        assert PathBrowserConfig is not None
        assert PathBrowserState is not None
        assert FileInfoManager is not None
        assert FileInfo is not None
        assert format_size is not None
        assert get_pathbrowser_theme is not None
        assert get_pathbrowser_themes is not None
        assert PathBrowserTheme is not None

    def test_pathbrowser_config(self):
        """Test PathBrowserConfig creation."""
        config = PathBrowserConfig()
        assert config.select == "file"
        assert config.multiple is False
        assert config.initialdir is None
        assert config.filetypes == [("All files", "*.*")]
        assert config.ok_label == "ok"
        assert config.cancel_label == "cancel"
        assert config.max_cache_size == 1000
        assert config.batch_size == 100
        assert config.enable_memory_monitoring is True
        assert config.show_hidden_files is False
        assert config.lazy_loading is True

    def test_pathbrowser_state(self):
        """Test PathBrowserState creation."""
        state = PathBrowserState()
        assert state.current_dir == str(Path.cwd())
        assert state.selected_items == []
        assert state.sort_column == "#0"
        assert state.sort_reverse is False
        assert state.navigation_history == []
        assert state.forward_history == []
        assert state.selection_anchor is None

    def test_file_info_manager(self):
        """Test FileInfoManager creation."""
        manager = FileInfoManager()
        assert manager is not None
        assert manager.get_cache_size() == 0

    def test_format_size(self):
        """Test format_size function."""
        assert format_size(0) == "0 B"
        assert format_size(1024) == "1.0 KB"
        assert format_size(1024 * 1024) == "1.0 MB"
        assert format_size(1024 * 1024 * 1024) == "1.0 GB"

    def test_pathbrowser_theme(self):
        """Test PathBrowserTheme creation."""
        theme = PathBrowserTheme()
        assert theme.background == "#ffffff"
        assert theme.foreground == "#000000"
        assert theme.tree_background == "#f0f0f0"
        assert theme.tree_foreground == "#000000"

    def test_get_pathbrowser_theme(self):
        """Test get_pathbrowser_theme function."""
        theme = get_pathbrowser_theme()
        assert isinstance(theme, PathBrowserTheme)

    def test_get_pathbrowser_themes(self):
        """Test get_pathbrowser_themes function."""
        themes = get_pathbrowser_themes()
        assert isinstance(themes, list)
        assert "light" in themes

    def test_pathbrowser_creation(self, root):
        """Test PathBrowser widget creation."""
        browser = PathBrowser(root)
        assert browser is not None
        assert hasattr(browser, 'config')
        assert hasattr(browser, 'state')
        assert hasattr(browser, 'file_info_manager')
        assert hasattr(browser, 'theme')

    def test_pathbrowser_with_config(self, root):
        """Test PathBrowser creation with custom config."""
        config = PathBrowserConfig(
            select="dir",
            multiple=True,
            ok_label="Select",
            cancel_label="Cancel"
        )
        browser = PathBrowser(root, config=config)
        assert browser.config.select == "dir"
        assert browser.config.multiple is True
        assert browser.config.ok_label == "Select"
        assert browser.config.cancel_label == "Cancel"

    def test_file_info_creation(self):
        """Test FileInfo creation."""
        file_info = FileInfo(
            path="/test/path",
            name="test.txt",
            is_dir=False,
            size_bytes=1024,
            size_str="1.0 KB",
            modified="2023-01-01 12:00",
            file_type="TXT"
        )
        assert file_info.path == "/test/path"
        assert file_info.name == "test.txt"
        assert file_info.is_dir is False
        assert file_info.size_bytes == 1024
        assert file_info.size_str == "1.0 KB"
        assert file_info.modified == "2023-01-01 12:00"
        assert file_info.file_type == "TXT"


if __name__ == "__main__":
    pytest.main([__file__])
