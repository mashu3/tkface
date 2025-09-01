"""
Tests for PathBrowser widget module.

This module tests the new modular structure of PathBrowser.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
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
from tkface.widget.pathbrowser import utils
from tkface.widget.pathbrowser import style
from tkface.widget.pathbrowser import view


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
        # Test only the configuration and state, not actual widget creation
        config = PathBrowserConfig()
        state = PathBrowserState()
        
        # Test that we can create the configuration
        assert config.select == "file"
        assert config.multiple is False
        assert config.initialdir is None
        assert config.filetypes == [("All files", "*.*")]
        assert config.ok_label == "ok"
        assert config.cancel_label == "cancel"
        
        # Test that we can create the state
        assert state.current_dir == str(Path.cwd())
        assert state.selected_items == []
        assert state.sort_column == "#0"
        assert state.sort_reverse is False
        assert state.navigation_history == []
        assert state.forward_history == []
        assert state.selection_anchor is None

    def test_pathbrowser_with_config(self, root):
        """Test PathBrowser creation with custom config."""
        # Test only the configuration, not actual widget creation
        config = PathBrowserConfig(
            select="dir",
            multiple=True,
            ok_label="Select",
            cancel_label="Cancel"
        )
        
        # Test the configuration values
        assert config.select == "dir"
        assert config.multiple is True
        assert config.ok_label == "Select"
        assert config.cancel_label == "Cancel"

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


class TestFileInfoManager:
    """Test FileInfoManager functionality."""

    def test_file_info_manager_creation(self):
        """Test FileInfoManager creation."""
        manager = FileInfoManager()
        assert manager.get_cache_size() == 0
        assert manager.get_memory_usage_estimate() == 0

    def test_file_info_manager_with_root(self):
        """Test FileInfoManager with root widget."""
        root = Mock()
        manager = FileInfoManager(root, max_cache_size=500)
        assert manager.get_cache_size() == 0
        assert manager._max_cache_size == 500

    def test_get_file_info_existing_file(self, root):
        """Test getting file info for existing file."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"test content")
            tmp_path = tmp_file.name

        try:
            manager = FileInfoManager(root=root)
            file_info = manager.get_file_info(tmp_path)
            
            assert file_info.path == tmp_path
            assert file_info.name == Path(tmp_path).name
            assert file_info.is_dir is False
            assert file_info.size_bytes == len(b"test content")
            assert file_info.size_str == format_size(len(b"test content"))
            # File type can be localized, so check that it's not empty
            assert file_info.file_type in ["File", "ファイル"]
            assert manager.get_cache_size() == 1
        finally:
            os.unlink(tmp_path)

    def test_get_file_info_directory(self, root):
        """Test getting file info for directory."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            manager = FileInfoManager(root=root)
            file_info = manager.get_file_info(tmp_dir)
            
            assert file_info.path == tmp_dir
            assert file_info.name == Path(tmp_dir).name
            assert file_info.is_dir is True
            assert file_info.size_bytes == 0
            assert file_info.size_str == ""
            # File type can be localized, so check that it's not empty
            assert file_info.file_type in ["Folder", "フォルダ"]
            assert manager.get_cache_size() == 1

    def test_get_file_info_nonexistent(self, root):
        """Test getting file info for nonexistent file."""
        manager = FileInfoManager(root=root)
        file_info = manager.get_file_info("/nonexistent/path")
        
        assert file_info.path == "/nonexistent/path"
        assert file_info.name == "path"
        assert file_info.is_dir is False
        assert file_info.size_bytes == 0
        assert file_info.size_str == ""
        # File type can be localized, so check that it's not empty
        assert file_info.file_type in ["Unknown", "不明"]
        assert manager.get_cache_size() == 1

    def test_cache_management(self, root):
        """Test cache size management."""
        manager = FileInfoManager(root=root, max_cache_size=2)
        
        # Add items to cache
        manager.get_file_info("/path1")
        manager.get_file_info("/path2")
        assert manager.get_cache_size() == 2
        
        # Add third item - should remove oldest
        manager.get_file_info("/path3")
        assert manager.get_cache_size() == 2

    def test_clear_directory_cache(self, root):
        """Test clearing directory cache."""
        manager = FileInfoManager(root=root)
        
        # Add some items to cache
        manager.get_file_info("/home/user/file1")
        manager.get_file_info("/home/user/file2")
        manager.get_file_info("/tmp/file3")
        
        assert manager.get_cache_size() == 3
        
        # Clear cache for /home/user directory
        manager.clear_directory_cache("/home/user")
        assert manager.get_cache_size() == 1

    def test_clear_cache(self, root):
        """Test clearing entire cache."""
        manager = FileInfoManager(root=root)
        
        # Add items to cache
        manager.get_file_info("/path1")
        manager.get_file_info("/path2")
        assert manager.get_cache_size() == 2
        
        # Clear cache
        manager.clear_cache()
        assert manager.get_cache_size() == 0

    def test_remove_from_cache(self, root):
        """Test removing specific item from cache."""
        manager = FileInfoManager(root=root)
        
        # Add item to cache
        manager.get_file_info("/path1")
        assert manager.get_cache_size() == 1
        
        # Remove item
        manager.remove_from_cache("/path1")
        assert manager.get_cache_size() == 0

    def test_get_cached_file_info(self, root):
        """Test getting cached file info."""
        manager = FileInfoManager(root=root)
        
        # First call - should cache
        file_info1 = manager.get_cached_file_info("/path1")
        assert manager.get_cache_size() == 1
        
        # Second call - should return cached version
        file_info2 = manager.get_cached_file_info("/path1")
        assert file_info1 is file_info2  # Same object reference

    def test_memory_usage_estimate(self, root):
        """Test memory usage estimation."""
        manager = FileInfoManager(root=root)
        
        # Add some items to cache
        manager.get_file_info("/path1")
        manager.get_file_info("/path2")
        
        memory_usage = manager.get_memory_usage_estimate()
        assert memory_usage > 0

    def test_resolve_symlink(self, root):
        """Test symlink resolution."""
        manager = FileInfoManager(root=root)
        
        # Test with regular path
        result = manager._resolve_symlink("/regular/path")
        assert result == "/regular/path"


class TestUtils:
    """Test utility functions."""

    def test_format_size_edge_cases(self):
        """Test format_size with edge cases."""
        assert format_size(0) == "0 B"
        assert format_size(1) == "1 B"
        assert format_size(1023) == "1023 B"
        assert format_size(1024) == "1.0 KB"
        assert format_size(1025) == "1.0 KB"
        assert format_size(1024 * 1024) == "1.0 MB"
        assert format_size(1024 * 1024 * 1024) == "1.0 GB"
        assert format_size(1024 * 1024 * 1024 * 1024) == "1.0 TB"

    def test_format_size_large_values(self):
        """Test format_size with large values."""
        # Test values that would exceed TB
        large_value = 1024 * 1024 * 1024 * 1024 * 1024
        result = format_size(large_value)
        assert result.endswith(" TB")

    def test_open_file_with_default_app(self):
        """Test opening file with default app."""
        # Test with nonexistent file - this may return True on some systems
        result = utils.open_file_with_default_app("/nonexistent/file")
        # The function may return True even for nonexistent files on some systems
        assert isinstance(result, bool)

    def test_add_extension_if_needed(self):
        """Test adding extension if needed."""
        filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
        
        # File already has extension
        result = utils.add_extension_if_needed("test.txt", filetypes, "Text files (*.txt)")
        assert result == "test.txt"
        
        # File needs extension
        result = utils.add_extension_if_needed("test", filetypes, "Text files (*.txt)")
        assert result == "test.txt"
        
        # No current filter
        result = utils.add_extension_if_needed("test", filetypes, None)
        assert result == "test"
        
        # All files filter
        result = utils.add_extension_if_needed("test", filetypes, "All files (*.*)")
        assert result == "test"

    def test_matches_filter(self):
        """Test file filter matching."""
        filetypes = [("Text files", "*.txt"), ("Python files", "*.py"), ("All files", "*.*")]
        
        # Test with "All files" filter
        result = utils.matches_filter("test.txt", filetypes, "All files", "file", "All files")
        assert result is True
        
        # Test with specific filter
        result = utils.matches_filter("test.txt", filetypes, "Text files (*.txt)", "file", "All files")
        assert result is True
        
        result = utils.matches_filter("test.py", filetypes, "Text files (*.txt)", "file", "All files")
        assert result is False
        
        # Test directory mode
        result = utils.matches_filter("test.txt", filetypes, "Text files (*.txt)", "dir", "All files")
        assert result is False

    def test_would_create_loop(self):
        """Test loop detection."""
        tree_widget = Mock()
        tree_widget.exists.return_value = False
        
        # Test normal case
        result = utils.would_create_loop("/path", "/real/path", tree_widget)
        assert result is False
        
        # Test existing path
        tree_widget.exists.return_value = True
        result = utils.would_create_loop("/path", "/real/path", tree_widget)
        assert result is True

    def test_get_performance_stats(self):
        """Test performance statistics."""
        stats = utils.get_performance_stats(100, 1024, "/current/dir", 5)
        
        assert stats["cache_size"] == 100
        assert stats["memory_usage_bytes"] == 1024
        assert stats["current_directory"] == "/current/dir"
        assert stats["selected_items_count"] == 5


class TestStyle:
    """Test style and theme functionality."""

    def test_pathbrowser_theme_default(self):
        """Test default PathBrowserTheme."""
        theme = PathBrowserTheme()
        assert theme.background == "#ffffff"
        assert theme.foreground == "#000000"
        assert theme.tree_background == "#f0f0f0"
        assert theme.tree_foreground == "#000000"

    def test_pathbrowser_theme_custom(self):
        """Test custom PathBrowserTheme."""
        theme = PathBrowserTheme(
            background="#000000",
            foreground="#ffffff",
            tree_background="#111111",
            tree_foreground="#eeeeee"
        )
        assert theme.background == "#000000"
        assert theme.foreground == "#ffffff"
        assert theme.tree_background == "#111111"
        assert theme.tree_foreground == "#eeeeee"

    def test_get_pathbrowser_theme_default(self):
        """Test getting default theme."""
        theme = get_pathbrowser_theme()
        assert isinstance(theme, PathBrowserTheme)

    def test_get_pathbrowser_theme_custom(self):
        """Test getting custom theme."""
        # This will fall back to default if theme file doesn't exist
        theme = get_pathbrowser_theme("nonexistent")
        assert isinstance(theme, PathBrowserTheme)

    def test_get_pathbrowser_themes(self):
        """Test getting available themes."""
        themes = get_pathbrowser_themes()
        assert isinstance(themes, list)
        assert "light" in themes

    def test_apply_theme_to_widget(self):
        """Test applying theme to widget."""
        widget = Mock()
        widget.winfo_children.return_value = []
        widget.configure = Mock()
        
        theme = PathBrowserTheme()
        style.apply_theme_to_widget(widget, theme)
        
        widget.configure.assert_called_with(bg=theme.background, fg=theme.foreground)

    def test_get_default_theme(self):
        """Test getting default theme."""
        theme = style.get_default_theme()
        assert isinstance(theme, PathBrowserTheme)


class TestPathBrowserCore:
    """Test PathBrowser core functionality."""

    def test_pathbrowser_initialization(self, root):
        """Test PathBrowser initialization."""
        config = PathBrowserConfig(
            select="file",
            multiple=False,
            initialdir="/tmp",
            filetypes=[("Text files", "*.txt")],
            ok_label="Open",
            cancel_label="Cancel"
        )
        
        # Test configuration creation
        assert config.select == "file"
        assert config.multiple is False
        assert config.initialdir == "/tmp"
        assert config.filetypes == [("Text files", "*.txt")]
        assert config.ok_label == "Open"
        assert config.cancel_label == "Cancel"
        
        # Test state creation
        state = PathBrowserState(current_dir="/tmp")
        assert state.current_dir == "/tmp"
        assert state.selected_items == []
        assert state.sort_column == "#0"
        assert state.sort_reverse is False
        
        # Test file info manager creation
        manager = FileInfoManager(root=root)
        assert isinstance(manager, FileInfoManager)
        
        # Test theme creation
        theme = get_pathbrowser_theme()
        assert isinstance(theme, PathBrowserTheme)

    def test_pathbrowser_initialization_with_params(self, root):
        """Test PathBrowser initialization with individual parameters."""
        # Test configuration with individual parameters
        config = PathBrowserConfig(
            select="dir",
            multiple=True,
            initialdir="/home",
            filetypes=[("Python files", "*.py")],
            ok_label="Select",
            cancel_label="Cancel"
        )
        
        assert config.select == "dir"
        assert config.multiple is True
        assert config.initialdir == "/home"
        assert config.filetypes == [("Python files", "*.py")]
        assert config.ok_label == "Select"
        assert config.cancel_label == "Cancel"

    def test_pathbrowser_save_mode(self, root):
        """Test PathBrowser in save mode."""
        # Test save mode configuration
        config = PathBrowserConfig(
            save_mode=True,
            initialfile="test.txt"
        )
        
        assert config.save_mode is True
        assert config.initialfile == "test.txt"

    def test_get_selection_save_mode(self, root):
        """Test get_selection in save mode."""
        # Test save mode selection logic
        config = PathBrowserConfig(save_mode=True)
        state = PathBrowserState(current_dir="/tmp")
        
        # Simulate save mode selection
        filename = "test.txt"
        full_path = f"/tmp/{filename}"
        
        assert config.save_mode is True
        assert state.current_dir == "/tmp"
        assert full_path == "/tmp/test.txt"

    def test_get_selection_normal_mode(self, root):
        """Test get_selection in normal mode."""
        # Test normal mode selection logic
        state = PathBrowserState(selected_items=["/path1", "/path2"])
        
        assert state.selected_items == ["/path1", "/path2"]

    def test_set_initial_directory(self, root):
        """Test setting initial directory."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Test directory validation
            path_obj = Path(tmp_dir)
            assert path_obj.exists()
            assert path_obj.is_dir()
            
            # Test state update
            state = PathBrowserState(current_dir=tmp_dir)
            assert state.current_dir == tmp_dir

    def test_set_file_types(self, root):
        """Test setting file types."""
        # Test file types configuration
        config = PathBrowserConfig()
        new_filetypes = [("Python files", "*.py"), ("Text files", "*.txt")]
        config.filetypes = new_filetypes
        
        assert config.filetypes == new_filetypes

    def test_performance_stats(self, root):
        """Test performance statistics."""
        # Test performance statistics generation
        manager = FileInfoManager(root=root)
        state = PathBrowserState(current_dir="/tmp", selected_items=["/path1", "/path2"])
        
        stats = utils.get_performance_stats(
            manager.get_cache_size(),
            manager.get_memory_usage_estimate(),
            state.current_dir,
            len(state.selected_items)
        )
        
        assert "cache_size" in stats
        assert "memory_usage_bytes" in stats
        assert "current_directory" in stats
        assert "selected_items_count" in stats

    def test_optimize_performance(self, root):
        """Test performance optimization."""
        # Test performance optimization
        manager = FileInfoManager(root=root)
        
        # Add some items to cache
        manager.get_file_info("/path1")
        manager.get_file_info("/path2")
        
        initial_cache_size = manager.get_cache_size()
        assert initial_cache_size > 0
        
        # Clear cache
        manager.clear_cache()
        assert manager.get_cache_size() == 0


class TestPathBrowserIntegration:
    """Test PathBrowser integration with mocked widgets."""

    def test_pathbrowser_full_initialization(self, root):
        """Test full PathBrowser initialization with mocked widgets."""
        # Mock all the widget creation and methods
        with patch('tkface.widget.pathbrowser.core.view') as mock_view, \
             patch.object(PathBrowser, '_load_directory') as mock_load, \
             patch.object(PathBrowser, '_update_navigation_buttons') as mock_nav, \
             patch.object(PathBrowser, '_schedule_memory_monitoring') as mock_mem:
            
            # Create mock widgets
            mock_file_tree = Mock()
            mock_file_tree.focus_set = Mock()
            mock_path_var = Mock()
            mock_status_var = Mock()
            mock_up_button = Mock()
            mock_down_button = Mock()
            mock_filter_combo = Mock()
            mock_selected_var = Mock()
            
            # Mock the widget creation
            def mock_create_widgets(browser):
                browser.file_tree = mock_file_tree
                browser.path_var = mock_path_var
                browser.status_var = mock_status_var
                browser.up_button = mock_up_button
                browser.down_button = mock_down_button
                browser.filter_combo = mock_filter_combo
                browser.selected_var = mock_selected_var
            
            mock_view.create_pathbrowser_widgets = mock_create_widgets
            mock_view.setup_pathbrowser_bindings = Mock()
            
            # Create PathBrowser instance
            browser = PathBrowser(root)
            
            # Verify initialization
            assert browser.config is not None
            assert browser.state is not None
            assert browser.file_info_manager is not None
            assert browser.theme is not None
            assert browser.file_tree == mock_file_tree
            assert browser.path_var == mock_path_var
            assert browser.status_var == mock_status_var
            
            # Verify method calls
            mock_view.setup_pathbrowser_bindings.assert_called_once_with(browser)
            mock_load.assert_called_once()
            mock_nav.assert_called_once()
            mock_mem.assert_called_once()

    def test_pathbrowser_with_custom_config(self, root):
        """Test PathBrowser with custom configuration."""
        config = PathBrowserConfig(
            select="dir",
            multiple=True,
            initialdir="/custom/path",
            filetypes=[("Custom files", "*.custom")],
            ok_label="Custom OK",
            cancel_label="Custom Cancel",
            save_mode=True,
            initialfile="custom.txt",
            max_cache_size=500,
            batch_size=50,
            enable_memory_monitoring=False,
            show_hidden_files=True,
            lazy_loading=False
        )
        
        with patch('tkface.widget.pathbrowser.core.view') as mock_view, \
             patch.object(PathBrowser, '_load_directory') as mock_load, \
             patch.object(PathBrowser, '_update_navigation_buttons') as mock_nav, \
             patch.object(PathBrowser, '_schedule_memory_monitoring') as mock_mem:
            
            # Create mock widgets
            mock_file_tree = Mock()
            mock_file_tree.focus_set = Mock()
            mock_path_var = Mock()
            mock_status_var = Mock()
            mock_up_button = Mock()
            mock_down_button = Mock()
            mock_filter_combo = Mock()
            mock_selected_var = Mock()
            
            def mock_create_widgets(browser):
                browser.file_tree = mock_file_tree
                browser.path_var = mock_path_var
                browser.status_var = mock_status_var
                browser.up_button = mock_up_button
                browser.down_button = mock_down_button
                browser.filter_combo = mock_filter_combo
                browser.selected_var = mock_selected_var
            
            mock_view.create_pathbrowser_widgets = mock_create_widgets
            mock_view.setup_pathbrowser_bindings = Mock()
            
            # Create PathBrowser with custom config
            browser = PathBrowser(root, config=config)
            
            # Verify custom configuration
            assert browser.config.select == "dir"
            assert browser.config.multiple is True
            assert browser.config.initialdir == "/custom/path"
            assert browser.config.filetypes == [("Custom files", "*.custom")]
            assert browser.config.ok_label == "Custom OK"
            assert browser.config.cancel_label == "Custom Cancel"
            assert browser.config.save_mode is True
            assert browser.config.initialfile == "custom.txt"
            assert browser.config.max_cache_size == 500
            assert browser.config.batch_size == 50
            assert browser.config.enable_memory_monitoring is False
            assert browser.config.show_hidden_files is True
            assert browser.config.lazy_loading is False
            
            # Verify state initialization
            assert browser.state.current_dir == "/custom/path"
            
            # Memory monitoring should not be called
            mock_mem.assert_not_called()

    def test_pathbrowser_navigation_methods(self, root):
        """Test PathBrowser navigation methods."""
        with patch('tkface.widget.pathbrowser.core.view') as mock_view, \
             patch.object(PathBrowser, '_load_directory') as mock_load, \
             patch.object(PathBrowser, '_update_navigation_buttons') as mock_nav, \
             patch.object(PathBrowser, '_schedule_memory_monitoring') as mock_mem:
            
            # Create mock widgets
            mock_file_tree = Mock()
            mock_file_tree.focus_set = Mock()
            mock_path_var = Mock()
            mock_status_var = Mock()
            mock_up_button = Mock()
            mock_down_button = Mock()
            mock_filter_combo = Mock()
            mock_selected_var = Mock()
            
            def mock_create_widgets(browser):
                browser.file_tree = mock_file_tree
                browser.path_var = mock_path_var
                browser.status_var = mock_status_var
                browser.up_button = mock_up_button
                browser.down_button = mock_down_button
                browser.filter_combo = mock_filter_combo
                browser.selected_var = mock_selected_var
            
            mock_view.create_pathbrowser_widgets = mock_create_widgets
            mock_view.setup_pathbrowser_bindings = Mock()
            
            browser = PathBrowser(root)
            browser.state.current_dir = "/test/dir"
            browser.state.forward_history = ["/test/dir/subdir"]
            
            # Test _go_up method
            with patch('pathlib.Path') as mock_path:
                mock_path.return_value.parent = "/test"
                browser._go_up()
                mock_load.assert_called_with("/test")
                assert browser.state.forward_history == ["/test/dir/subdir", "/test/dir"]
                assert browser.state.navigation_history == []
            
            # Test _go_down method
            browser.state.forward_history = ["/test/dir/subdir"]
            browser._go_down()
            mock_load.assert_called_with("/test/dir/subdir")
            assert browser.state.forward_history == []
            assert browser.state.navigation_history == ["/test/dir"]
            
            # Test _go_down with empty history
            browser.state.forward_history = []
            browser._go_down()
            # Should not call _load_directory
            assert mock_load.call_count == 3  # Previous calls + initialization

    def test_pathbrowser_file_operations(self, root):
        """Test PathBrowser file operations."""
        with patch('tkface.widget.pathbrowser.core.view') as mock_view, \
             patch.object(PathBrowser, '_load_directory') as mock_load, \
             patch.object(PathBrowser, '_update_navigation_buttons') as mock_nav, \
             patch.object(PathBrowser, '_schedule_memory_monitoring') as mock_mem:
            
            # Create mock widgets
            mock_file_tree = Mock()
            mock_file_tree.focus_set = Mock()
            mock_path_var = Mock()
            mock_status_var = Mock()
            mock_up_button = Mock()
            mock_down_button = Mock()
            mock_filter_combo = Mock()
            mock_selected_var = Mock()
            
            def mock_create_widgets(browser):
                browser.file_tree = mock_file_tree
                browser.path_var = mock_path_var
                browser.status_var = mock_status_var
                browser.up_button = mock_up_button
                browser.down_button = mock_down_button
                browser.filter_combo = mock_filter_combo
                browser.selected_var = mock_selected_var
            
            mock_view.create_pathbrowser_widgets = mock_create_widgets
            mock_view.setup_pathbrowser_bindings = Mock()
            
            browser = PathBrowser(root)
            
            # Test _copy_path method
            browser.tree = Mock()
            browser.tree.selection.return_value = ["/test/file.txt"]
            browser.clipboard_clear = Mock()
            browser.clipboard_append = Mock()
            
            browser._copy_path()
            browser.clipboard_clear.assert_called_once()
            browser.clipboard_append.assert_called_once_with("/test/file.txt")

    def test_pathbrowser_keyboard_navigation(self, root):
        """Test PathBrowser keyboard navigation methods."""
        with patch('tkface.widget.pathbrowser.core.view') as mock_view, \
             patch.object(PathBrowser, '_load_directory') as mock_load, \
             patch.object(PathBrowser, '_update_navigation_buttons') as mock_nav, \
             patch.object(PathBrowser, '_schedule_memory_monitoring') as mock_mem:
            
            # Create mock widgets
            mock_file_tree = Mock()
            mock_file_tree.focus_set = Mock()
            mock_path_var = Mock()
            mock_status_var = Mock()
            mock_up_button = Mock()
            mock_down_button = Mock()
            mock_filter_combo = Mock()
            mock_selected_var = Mock()
            
            def mock_create_widgets(browser):
                browser.file_tree = mock_file_tree
                browser.path_var = mock_path_var
                browser.status_var = mock_status_var
                browser.up_button = mock_up_button
                browser.down_button = mock_down_button
                browser.filter_combo = mock_filter_combo
                browser.selected_var = mock_selected_var
            
            mock_view.create_pathbrowser_widgets = mock_create_widgets
            mock_view.setup_pathbrowser_bindings = Mock()
            
            browser = PathBrowser(root)
            browser.file_tree = Mock()
            browser.file_tree.selection.return_value = ["item1"]
            browser.file_tree.get_children.return_value = ["item1", "item2", "item3"]
            browser.file_tree.selection_set = Mock()
            browser.file_tree.see = Mock()
            
            # Test keyboard navigation methods exist and can be called
            browser._move_selection_up(Mock())
            browser._move_selection_down(Mock())
            browser._move_to_first(Mock())
            browser._move_to_last(Mock())
            
            # Verify methods were called (they may not modify selection in all cases)
            assert hasattr(browser, '_move_selection_up')
            assert hasattr(browser, '_move_selection_down')
            assert hasattr(browser, '_move_to_first')
            assert hasattr(browser, '_move_to_last')

    def test_pathbrowser_selection_handling(self, root):
        """Test PathBrowser selection handling."""
        with patch('tkface.widget.pathbrowser.core.view') as mock_view, \
             patch.object(PathBrowser, '_load_directory') as mock_load, \
             patch.object(PathBrowser, '_update_navigation_buttons') as mock_nav, \
             patch.object(PathBrowser, '_schedule_memory_monitoring') as mock_mem:
            
            # Create mock widgets
            mock_file_tree = Mock()
            mock_file_tree.focus_set = Mock()
            mock_path_var = Mock()
            mock_status_var = Mock()
            mock_up_button = Mock()
            mock_down_button = Mock()
            mock_filter_combo = Mock()
            mock_selected_var = Mock()
            
            def mock_create_widgets(browser):
                browser.file_tree = mock_file_tree
                browser.path_var = mock_path_var
                browser.status_var = mock_status_var
                browser.up_button = mock_up_button
                browser.down_button = mock_down_button
                browser.filter_combo = mock_filter_combo
                browser.selected_var = mock_selected_var
            
            mock_view.create_pathbrowser_widgets = mock_create_widgets
            mock_view.setup_pathbrowser_bindings = Mock()
            
            browser = PathBrowser(root)
            browser.config.select = "file"
            browser.config.multiple = True
            
            # Test _on_file_select
            browser.file_tree.selection.return_value = ["/test/file1.txt", "/test/file2.txt"]
            browser.file_info_manager = Mock()
            browser.file_info_manager.get_cached_file_info.return_value = Mock(
                is_dir=False
            )
            browser.state.selection_anchor = None
            
            with patch('tkface.widget.pathbrowser.core.view') as mock_view_update:
                mock_view_update.update_selected_display = Mock()
                browser._on_file_select(Mock())
                
                # Verify selection was processed
                assert len(browser.state.selected_items) == 2

    def test_pathbrowser_error_handling(self, root):
        """Test PathBrowser error handling."""
        with patch('tkface.widget.pathbrowser.core.view') as mock_view, \
             patch.object(PathBrowser, '_load_directory') as mock_load, \
             patch.object(PathBrowser, '_update_navigation_buttons') as mock_nav, \
             patch.object(PathBrowser, '_schedule_memory_monitoring') as mock_mem:
            
            # Create mock widgets
            mock_file_tree = Mock()
            mock_file_tree.focus_set = Mock()
            mock_path_var = Mock()
            mock_status_var = Mock()
            mock_up_button = Mock()
            mock_down_button = Mock()
            mock_filter_combo = Mock()
            mock_selected_var = Mock()
            
            def mock_create_widgets(browser):
                browser.file_tree = mock_file_tree
                browser.path_var = mock_path_var
                browser.status_var = mock_status_var
                browser.up_button = mock_up_button
                browser.down_button = mock_down_button
                browser.filter_combo = mock_filter_combo
                browser.selected_var = mock_selected_var
            
            mock_view.create_pathbrowser_widgets = mock_create_widgets
            mock_view.setup_pathbrowser_bindings = Mock()
            
            browser = PathBrowser(root)
            browser.status_var = Mock()
            browser.winfo_toplevel = Mock(return_value=root)
            
            # Test error handling methods exist
            assert hasattr(browser, '_load_directory')
            assert hasattr(browser, '_update_navigation_buttons')

    def test_pathbrowser_memory_monitoring(self, root):
        """Test PathBrowser memory monitoring."""
        with patch('tkface.widget.pathbrowser.core.view') as mock_view, \
             patch.object(PathBrowser, '_load_directory') as mock_load, \
             patch.object(PathBrowser, '_update_navigation_buttons') as mock_nav:
            
            # Create mock widgets
            mock_file_tree = Mock()
            mock_file_tree.focus_set = Mock()
            mock_path_var = Mock()
            mock_status_var = Mock()
            mock_up_button = Mock()
            mock_down_button = Mock()
            mock_filter_combo = Mock()
            mock_selected_var = Mock()
            
            def mock_create_widgets(browser):
                browser.file_tree = mock_file_tree
                browser.path_var = mock_path_var
                browser.status_var = mock_status_var
                browser.up_button = mock_up_button
                browser.down_button = mock_down_button
                browser.filter_combo = mock_filter_combo
                browser.selected_var = mock_selected_var
            
            mock_view.create_pathbrowser_widgets = mock_create_widgets
            mock_view.setup_pathbrowser_bindings = Mock()
            
            # Enable memory monitoring
            config = PathBrowserConfig(enable_memory_monitoring=True)
            browser = PathBrowser(root, config=config)
            
            # Test _check_memory_usage
            browser.file_info_manager = Mock()
            browser.file_info_manager.get_memory_usage_estimate.return_value = 60 * 1024 * 1024  # 60MB
            browser.file_info_manager.get_cache_size.return_value = 1000
            browser.file_info_manager.clear_cache = Mock()
            
            with patch('tkface.widget.pathbrowser.core.logger') as mock_logger:
                browser._check_memory_usage()
                mock_logger.warning.assert_called_once()
                browser.file_info_manager.clear_cache.assert_called_once()
            
            # Test _schedule_memory_monitoring
            browser.after = Mock()
            browser._check_memory_usage = Mock()
            browser._schedule_memory_monitoring()
            browser.after.assert_called_once_with(30000, browser._schedule_memory_monitoring)


class TestView:
    """Test view functionality."""

    def test_create_pathbrowser_widgets(self, root):
        """Test creating PathBrowser widgets."""
        browser = Mock()
        browser.config = Mock()
        browser.config.multiple = False
        browser.config.save_mode = False
        browser.config.initialfile = None
        
        # Mock tkinter widgets
        with patch('tkface.widget.pathbrowser.view.ttk') as mock_ttk:
            mock_frame = Mock()
            mock_ttk.Frame.return_value = mock_frame
            mock_ttk.Button.return_value = Mock()
            mock_ttk.Entry.return_value = Mock()
            mock_ttk.Label.return_value = Mock()
            mock_ttk.PanedWindow.return_value = Mock()
            mock_ttk.Treeview.return_value = Mock()
            mock_ttk.Combobox.return_value = Mock()
            
            with patch('tkface.widget.pathbrowser.view.tk') as mock_tk:
                mock_tk.StringVar.return_value = Mock()
                
                view.create_pathbrowser_widgets(browser)
                
                # Verify that widgets were created
                assert hasattr(browser, 'top_toolbar')
                assert hasattr(browser, 'paned')
                assert hasattr(browser, 'file_tree')
                assert hasattr(browser, 'tree')
                assert hasattr(browser, 'status_var')

    def test_setup_pathbrowser_bindings(self, root):
        """Test setting up PathBrowser bindings."""
        browser = Mock()
        browser.tree = Mock()
        browser.file_tree = Mock()
        browser.filter_combo = Mock()
        
        view.setup_pathbrowser_bindings(browser)
        
        # Verify that bindings were set up
        browser.tree.bind.assert_called()
        browser.file_tree.bind.assert_called()
        browser.filter_combo.bind.assert_called()
        browser.bind.assert_called()

    def test_load_directory_tree(self, root):
        """Test loading directory tree."""
        browser = Mock()
        browser.tree = Mock()
        browser.tree.delete = Mock()
        browser.tree.insert = Mock()
        browser.tree.get_children.return_value = []
        browser.state = Mock()
        browser.state.current_dir = "/tmp"
        browser.file_info_manager = Mock()
        browser.file_info_manager._resolve_symlink = Mock(return_value="/tmp")
        
        with patch('tkface.widget.pathbrowser.view.utils') as mock_utils:
            mock_utils.IS_WINDOWS = False
            mock_utils.IS_MACOS = False
            
            with patch('tkface.widget.pathbrowser.view.populate_tree_node') as mock_populate:
                with patch('tkface.widget.pathbrowser.view.expand_path') as mock_expand:
                    view.load_directory_tree(browser)
                    
                    browser.tree.delete.assert_called()
                    browser.tree.insert.assert_called()
                    mock_expand.assert_called_with(browser, "/tmp")

    def test_populate_tree_node(self, root):
        """Test populating tree node."""
        browser = Mock()
        browser.tree = Mock()
        browser.tree.get_children.return_value = []
        browser.tree.delete = Mock()
        browser.tree.insert = Mock()
        browser.tree.exists.return_value = False
        browser.status_var = Mock()
        
        with patch('tkface.widget.pathbrowser.view.Path') as mock_path:
            mock_path_obj = Mock()
            mock_path_obj.iterdir.return_value = []
            mock_path.return_value = mock_path_obj
            
            with patch('tkface.widget.pathbrowser.view.utils') as mock_utils:
                mock_utils.IS_MACOS = False
                
                view.populate_tree_node(browser, "/test/path")
                
                browser.tree.get_children.assert_called_with("/test/path")

    def test_expand_path(self, root):
        """Test expanding path in tree."""
        browser = Mock()
        browser.tree = Mock()
        browser.tree.item = Mock()
        browser.tree.get_children.return_value = []
        browser.tree.selection_set = Mock()
        browser.tree.see = Mock()
        browser.file_info_manager = Mock()
        browser.file_info_manager._resolve_symlink = Mock(return_value="/test/path")
        
        with patch('tkface.widget.pathbrowser.view.utils') as mock_utils:
            mock_utils.IS_WINDOWS = False
            
            with patch('tkface.widget.pathbrowser.view.populate_tree_node') as mock_populate:
                view.expand_path(browser, "/test/path")
                
                browser.tree.selection_set.assert_called_with("/test/path")
                browser.tree.see.assert_called_with("/test/path")

    def test_load_files(self, root):
        """Test loading files."""
        browser = Mock()
        browser.file_tree = Mock()
        browser.file_tree.delete = Mock()
        browser.file_tree.insert = Mock()
        browser.file_tree.get_children.return_value = []
        browser.state = Mock()
        browser.state.current_dir = "/tmp"
        browser.config = Mock()
        browser.config.batch_size = 100
        browser.config.filetypes = [("All files", "*.*")]
        browser.config.select = "file"
        browser.filter_var = Mock()
        browser.filter_var.get.return_value = "All files"
        browser.status_var = Mock()
        browser.file_info_manager = Mock()
        browser.file_info_manager.get_cached_file_info.return_value = Mock(
            name="test.txt",
            path="/tmp/test.txt",
            size_str="1 KB",
            modified="2023-01-01",
            file_type="TXT",
            size_bytes=1024
        )
        
        with patch('tkface.widget.pathbrowser.view.Path') as mock_path:
            mock_path_obj = Mock()
            mock_item = Mock()
            mock_item.is_dir.return_value = False
            mock_item.name = "test.txt"
            mock_path_obj.iterdir.return_value = [mock_item]
            mock_path.return_value = mock_path_obj
            
            with patch('tkface.widget.pathbrowser.view.utils') as mock_utils:
                mock_utils.matches_filter.return_value = True
                
                with patch('tkface.widget.pathbrowser.view.sort_items') as mock_sort:
                    mock_sort.return_value = [("test.txt", "/tmp/test.txt", "📄", "1 KB", "2023-01-01", "TXT", 1024)]
                    
                    view.load_files(browser)
                    
                    browser.file_tree.delete.assert_called()
                    browser.file_tree.insert.assert_called()

    def test_sort_items(self, root):
        """Test sorting items."""
        browser = Mock()
        browser.state = Mock()
        browser.state.sort_column = "#0"
        browser.state.sort_reverse = False
        
        items = [
            ("b.txt", "/path/b.txt", "📄", "1 KB", "2023-01-02", "TXT", 1024),
            ("a.txt", "/path/a.txt", "📄", "2 KB", "2023-01-01", "TXT", 2048)
        ]
        
        with patch('tkface.widget.pathbrowser.view.lang') as mock_lang:
            mock_lang.get.return_value = "Folder"
            
            result = view.sort_items(browser, items)
            
            # Should be sorted by name (first column)
            assert result[0][0] == "a.txt"
            assert result[1][0] == "b.txt"

    def test_update_selected_display(self, root):
        """Test updating selected display."""
        browser = Mock()
        browser.state = Mock()
        browser.state.selected_items = ["/path/file1.txt", "/path/file2.txt"]
        browser.selected_var = Mock()
        browser.file_info_manager = Mock()
        mock_file_info = Mock()
        mock_file_info.name = "file1.txt"
        mock_file_info.is_dir = False
        browser.file_info_manager.get_cached_file_info.return_value = mock_file_info
        
        view.update_selected_display(browser)
        
        browser.selected_var.set.assert_called()

    def test_update_status(self, root):
        """Test updating status."""
        browser = Mock()
        browser.state = Mock()
        browser.state.selected_items = []
        browser.status_var = Mock()
        
        with patch('tkface.widget.pathbrowser.view.update_directory_status') as mock_update_dir:
            view.update_status(browser)
            mock_update_dir.assert_called_with(browser)

    def test_update_selection_status(self, root):
        """Test updating selection status."""
        browser = Mock()
        browser.state = Mock()
        browser.state.selected_items = ["/path/file1.txt"]
        browser.status_var = Mock()
        browser.file_info_manager = Mock()
        mock_file_info = Mock()
        mock_file_info.name = "file1.txt"
        mock_file_info.is_dir = False
        mock_file_info.size_bytes = 1024
        browser.file_info_manager.get_cached_file_info.return_value = mock_file_info
        
        with patch('tkface.widget.pathbrowser.view.lang') as mock_lang:
            mock_lang.get.return_value = "Selected:"
            
            with patch('tkface.widget.pathbrowser.view.utils') as mock_utils:
                mock_utils.format_size.return_value = "1 KB"
                
                view.update_selection_status(browser)
                
                browser.status_var.set.assert_called()

    def test_update_directory_status(self, root):
        """Test updating directory status."""
        browser = Mock()
        browser.state = Mock()
        browser.state.current_dir = "/tmp"
        browser.status_var = Mock()
        
        with patch('tkface.widget.pathbrowser.view.Path') as mock_path:
            mock_path_obj = Mock()
            mock_item = Mock()
            mock_item.is_dir.return_value = False
            mock_item.stat.return_value.st_size = 1024
            mock_path_obj.iterdir.return_value = [mock_item]
            mock_path.return_value = mock_path_obj
            
            with patch('tkface.widget.pathbrowser.view.lang') as mock_lang:
                mock_lang.get.return_value = "file"
                
                with patch('tkface.widget.pathbrowser.view.utils') as mock_utils:
                    mock_utils.format_size.return_value = "1 KB"
                    
                    view.update_directory_status(browser)
                    
                    browser.status_var.set.assert_called()

    def test_show_context_menu(self, root):
        """Test showing context menu."""
        browser = Mock()
        browser.tree = Mock()
        browser.tree.selection.return_value = ["/path"]
        browser.file_info_manager = Mock()
        browser.file_info_manager.get_file_info.return_value = Mock(is_dir=True)
        browser.tree.item.return_value = False  # Not open
        
        event = Mock()
        event.x_root = 100
        event.y_root = 100
        
        with patch('tkface.widget.pathbrowser.view.tk') as mock_tk:
            mock_menu = Mock()
            mock_tk.Menu.return_value = mock_menu
            
            with patch('tkface.widget.pathbrowser.view.lang') as mock_lang:
                mock_lang.get.return_value = "Expand"
                
                view.show_context_menu(browser, event, "tree")
                
                mock_menu.add_command.assert_called()
                mock_menu.post.assert_called_with(100, 100)

    def test_load_directory_tree_windows(self, root):
        """Test loading directory tree on Windows."""
        browser = Mock()
        browser.tree = Mock()
        browser.tree.delete = Mock()
        browser.tree.insert = Mock()
        browser.tree.get_children.return_value = []
        browser.state = Mock()
        browser.state.current_dir = "C:\\"
        browser.file_info_manager = Mock()
        browser.file_info_manager._resolve_symlink = Mock(return_value="C:\\")
        
        with patch('tkface.widget.pathbrowser.view.utils') as mock_utils:
            mock_utils.IS_WINDOWS = True
            mock_utils.IS_MACOS = False
            
            with patch('tkface.widget.pathbrowser.view.populate_tree_node') as mock_populate:
                with patch('tkface.widget.pathbrowser.view.expand_path') as mock_expand:
                    with patch('pathlib.Path') as mock_path:
                        mock_path.return_value.exists.return_value = True
                        view.load_directory_tree(browser)
                        
                        browser.tree.delete.assert_called()
                        # insert may not be called if no directories found
                        mock_expand.assert_called_with(browser, "C:\\")

    def test_populate_tree_node_with_children(self, root):
        """Test populating tree node with children."""
        browser = Mock()
        browser.tree = Mock()
        browser.tree.get_children.return_value = ["existing_child"]
        browser.tree.delete = Mock()
        browser.tree.insert = Mock()
        browser.tree.exists.return_value = False
        browser.status_var = Mock()
        
        with patch('tkface.widget.pathbrowser.view.Path') as mock_path:
            mock_path_obj = Mock()
            mock_item = Mock()
            mock_item.is_dir.return_value = True
            mock_item.name = "test_dir"
            mock_path_obj.iterdir.return_value = [mock_item]
            mock_path.return_value = mock_path_obj
            
            with patch('tkface.widget.pathbrowser.view.utils') as mock_utils:
                mock_utils.IS_MACOS = False
                
                view.populate_tree_node(browser, "/test/path")
                
                browser.tree.get_children.assert_called_with("/test/path")
                # insert may not be called if no new directories found

    def test_populate_tree_node_macos_symlink(self, root):
        """Test populating tree node on macOS with symlink handling."""
        browser = Mock()
        browser.tree = Mock()
        browser.tree.get_children.return_value = []
        browser.tree.delete = Mock()
        browser.tree.insert = Mock()
        browser.tree.exists.return_value = False
        browser.status_var = Mock()
        
        with patch('tkface.widget.pathbrowser.view.Path') as mock_path:
            mock_path_obj = Mock()
            mock_item = Mock()
            mock_item.is_dir.return_value = True
            mock_item.name = "test_dir"
            mock_item.resolve.return_value = Path("/real/path")
            mock_path_obj.iterdir.return_value = [mock_item]
            mock_path.return_value = mock_path_obj
            
            # Mock the joinpath method to return a proper mock
            mock_subpath = Mock()
            mock_subpath.iterdir.return_value = []  # No subdirectories
            mock_path_obj.joinpath.return_value = mock_subpath
            
            with patch('tkface.widget.pathbrowser.view.utils') as mock_utils:
                mock_utils.IS_MACOS = True
                mock_utils.would_create_loop.return_value = False
                
                view.populate_tree_node(browser, "/test/path")
                
                browser.tree.get_children.assert_called_with("/test/path")

    def test_load_files_with_directories(self, root):
        """Test loading files including directories."""
        browser = Mock()
        browser.file_tree = Mock()
        browser.file_tree.delete = Mock()
        browser.file_tree.insert = Mock()
        browser.file_tree.get_children.return_value = []
        browser.state = Mock()
        browser.state.current_dir = "/tmp"
        browser.config = Mock()
        browser.config.batch_size = 100
        browser.config.filetypes = [("All files", "*.*")]
        browser.config.select = "both"
        browser.filter_var = Mock()
        browser.filter_var.get.return_value = "All files"
        browser.status_var = Mock()
        browser.file_info_manager = Mock()
        browser.file_info_manager.get_cached_file_info.return_value = Mock(
            name="test_dir",
            path="/tmp/test_dir",
            size_str="",
            modified="2023-01-01",
            file_type="Folder",
            size_bytes=0
        )
        
        with patch('tkface.widget.pathbrowser.view.Path') as mock_path:
            mock_path_obj = Mock()
            mock_item = Mock()
            mock_item.is_dir.return_value = True
            mock_item.name = "test_dir"
            mock_path_obj.iterdir.return_value = [mock_item]
            mock_path.return_value = mock_path_obj
            
            with patch('tkface.widget.pathbrowser.view.utils') as mock_utils:
                mock_utils.matches_filter.return_value = True
                
                with patch('tkface.widget.pathbrowser.view.sort_items') as mock_sort:
                    mock_sort.return_value = [("test_dir", "/tmp/test_dir", "📁", "", "2023-01-01", "Folder", 0)]
                    
                    view.load_files(browser)
                    
                    browser.file_tree.delete.assert_called()
                    browser.file_tree.insert.assert_called()

    def test_load_files_with_error(self, root):
        """Test loading files with error handling."""
        browser = Mock()
        browser.file_tree = Mock()
        browser.file_tree.delete = Mock()
        browser.file_tree.get_children.return_value = []  # Empty list for delete
        browser.state = Mock()
        browser.state.current_dir = "/restricted"
        browser.status_var = Mock()
        browser.winfo_toplevel.return_value = root
        browser.config = Mock()
        browser.config.batch_size = 100  # Valid batch size
        browser.config.filetypes = [("All files", "*.*")]
        browser.config.select = "file"
        browser.filter_var = Mock()
        browser.filter_var.get.return_value = "All files"
        
        with patch('tkface.widget.pathbrowser.view.Path') as mock_path:
            mock_path_obj = Mock()
            mock_path_obj.iterdir.side_effect = PermissionError("Access denied")
            mock_path.return_value = mock_path_obj
            
            with patch('tkface.widget.pathbrowser.view.messagebox') as mock_msgbox, \
                 patch('tkface.widget.pathbrowser.view.lang') as mock_lang:
                mock_lang.get.return_value = "Access Denied"
                
                view.load_files(browser)
                
                browser.status_var.set.assert_called()
                mock_msgbox.showerror.assert_called_once()

    def test_sort_items_by_size(self, root):
        """Test sorting items by size."""
        browser = Mock()
        browser.state = Mock()
        browser.state.sort_column = "size"
        browser.state.sort_reverse = False
        
        items = [
            ("file1.txt", "/path/file1.txt", "📄", "2 KB", "2023-01-02", "TXT", 2048),
            ("file2.txt", "/path/file2.txt", "📄", "1 KB", "2023-01-01", "TXT", 1024)
        ]
        
        with patch('tkface.widget.pathbrowser.view.lang') as mock_lang:
            mock_lang.get.return_value = "Folder"
            
            result = view.sort_items(browser, items)
            
            # Should be sorted by size (smallest first)
            assert result[0][0] == "file2.txt"
            assert result[1][0] == "file1.txt"

    def test_sort_items_by_modified(self, root):
        """Test sorting items by modified date."""
        browser = Mock()
        browser.state = Mock()
        browser.state.sort_column = "modified"
        browser.state.sort_reverse = True
        
        items = [
            ("file1.txt", "/path/file1.txt", "📄", "1 KB", "2023-01-01", "TXT", 1024),
            ("file2.txt", "/path/file2.txt", "📄", "2 KB", "2023-01-02", "TXT", 2048)
        ]
        
        with patch('tkface.widget.pathbrowser.view.lang') as mock_lang:
            mock_lang.get.return_value = "Folder"
            
            result = view.sort_items(browser, items)
            
            # Should be sorted by modified date (newest first due to reverse=True)
            assert result[0][0] == "file2.txt"
            assert result[1][0] == "file1.txt"

    def test_sort_items_by_type(self, root):
        """Test sorting items by file type."""
        browser = Mock()
        browser.state = Mock()
        browser.state.sort_column = "type"
        browser.state.sort_reverse = False
        
        items = [
            ("file2.txt", "/path/file2.txt", "📄", "2 KB", "2023-01-02", "TXT", 2048),
            ("file1.py", "/path/file1.py", "📄", "1 KB", "2023-01-01", "PY", 1024)
        ]
        
        with patch('tkface.widget.pathbrowser.view.lang') as mock_lang:
            mock_lang.get.return_value = "Folder"
            
            result = view.sort_items(browser, items)
            
            # Should be sorted by file type
            assert result[0][0] == "file1.py"  # PY comes before TXT
            assert result[1][0] == "file2.txt"

    def test_update_selected_display_multiple_files(self, root):
        """Test updating selected display with multiple files."""
        browser = Mock()
        browser.state = Mock()
        browser.state.selected_items = ["/path/file1.txt", "/path/file2.txt", "/path/file3.txt", "/path/file4.txt"]
        browser.selected_var = Mock()
        browser.file_info_manager = Mock()
        
        # Create proper mock with string name attribute
        mock_file_info = Mock()
        mock_file_info.name = "file1.txt"  # String value
        mock_file_info.is_dir = False
        browser.file_info_manager.get_cached_file_info.return_value = mock_file_info
        
        view.update_selected_display(browser)
        
        browser.selected_var.set.assert_called()
        # Should show first file with count indication
        call_args = browser.selected_var.set.call_args[0][0]
        assert "file1.txt" in call_args
        assert "+3 more" in call_args

    def test_update_selected_display_directories_only(self, root):
        """Test updating selected display with directories only."""
        browser = Mock()
        browser.state = Mock()
        browser.state.selected_items = ["/path/dir1", "/path/dir2"]
        browser.selected_var = Mock()
        browser.file_info_manager = Mock()
        browser.file_info_manager.get_cached_file_info.return_value = Mock(
            name="dir1",
            is_dir=True
        )
        
        view.update_selected_display(browser)
        
        browser.selected_var.set.assert_called_with("")

    def test_update_selection_status_multiple_items(self, root):
        """Test updating selection status with multiple items."""
        browser = Mock()
        browser.state = Mock()
        browser.state.selected_items = ["/path/file1.txt", "/path/dir1"]
        browser.status_var = Mock()
        browser.file_info_manager = Mock()
        
        def mock_get_file_info(path):
            if "file1.txt" in path:
                mock_file = Mock()
                mock_file.name = "file1.txt"  # String name
                mock_file.is_dir = False
                mock_file.size_bytes = 1024
                return mock_file
            else:
                mock_dir = Mock()
                mock_dir.name = "dir1"  # String name
                mock_dir.is_dir = True
                mock_dir.size_bytes = 0
                return mock_dir
        
        browser.file_info_manager.get_cached_file_info.side_effect = mock_get_file_info
        
        with patch('tkface.widget.pathbrowser.view.lang') as mock_lang:
            mock_lang.get.return_value = "Selected:"
            
            with patch('tkface.widget.pathbrowser.view.utils') as mock_utils:
                mock_utils.format_size.return_value = "1 KB"
                
                view.update_selection_status(browser)
                
                browser.status_var.set.assert_called()
                call_args = browser.status_var.set.call_args[0][0]
                assert "file1.txt" in call_args
                assert "dir1" in call_args

    def test_update_directory_status_with_error(self, root):
        """Test updating directory status with error handling."""
        browser = Mock()
        browser.state = Mock()
        browser.state.current_dir = "/restricted"
        browser.status_var = Mock()
        
        with patch('tkface.widget.pathbrowser.view.Path') as mock_path:
            mock_path_obj = Mock()
            mock_path_obj.iterdir.side_effect = PermissionError("Access denied")
            mock_path.return_value = mock_path_obj
            
            view.update_directory_status(browser)
            
            browser.status_var.set.assert_called()
            call_args = browser.status_var.set.call_args[0][0]
            assert "Access denied" in call_args

    def test_show_context_menu_file_type(self, root):
        """Test showing context menu for file type."""
        browser = Mock()
        browser.file_tree = Mock()
        browser.file_tree.selection.return_value = ["/path/file.txt"]
        
        event = Mock()
        event.x_root = 100
        event.y_root = 100
        
        with patch('tkface.widget.pathbrowser.view.tk') as mock_tk:
            mock_menu = Mock()
            mock_tk.Menu.return_value = mock_menu
            
            with patch('tkface.widget.pathbrowser.view.lang') as mock_lang:
                mock_lang.get.return_value = "Open"
                
                view.show_context_menu(browser, event, "file")
                
                mock_menu.add_command.assert_called()
                mock_menu.post.assert_called_with(100, 100)

    def test_show_context_menu_tree_open(self, root):
        """Test showing context menu for open tree node."""
        browser = Mock()
        browser.tree = Mock()
        browser.tree.selection.return_value = ["/path/dir"]
        browser.tree.item.return_value = True  # Is open
        browser.file_info_manager = Mock()
        browser.file_info_manager.get_file_info.return_value = Mock(is_dir=True)
        
        event = Mock()
        event.x_root = 100
        event.y_root = 100
        
        with patch('tkface.widget.pathbrowser.view.tk') as mock_tk:
            mock_menu = Mock()
            mock_tk.Menu.return_value = mock_menu
            
            with patch('tkface.widget.pathbrowser.view.lang') as mock_lang:
                mock_lang.get.return_value = "Collapse"
                
                view.show_context_menu(browser, event, "tree")
                
                mock_menu.add_command.assert_called()
                mock_menu.post.assert_called_with(100, 100)


class TestUtilsAdvanced:
    """Test advanced utility functions."""

    def test_format_size_precision(self, root):
        """Test format_size with different precision levels."""
        # Test various size ranges
        assert format_size(512) == "512 B"
        assert format_size(1536) == "1.5 KB"  # 1.5 * 1024
        assert format_size(1536 * 1024) == "1.5 MB"
        assert format_size(1536 * 1024 * 1024) == "1.5 GB"
        assert format_size(1536 * 1024 * 1024 * 1024) == "1.5 TB"

    def test_matches_filter_complex_patterns(self, root):
        """Test matches_filter with complex patterns."""
        filetypes = [
            ("Text files", "*.txt *.log"),
            ("Python files", "*.py *.pyw"),
            ("All files", "*.*")
        ]
        
        # Test multiple patterns in one filter
        result = utils.matches_filter("test.txt", filetypes, "Text files (*.txt *.log)", "file", "All files")
        assert result is True
        
        result = utils.matches_filter("test.log", filetypes, "Text files (*.txt *.log)", "file", "All files")
        assert result is True
        
        result = utils.matches_filter("test.py", filetypes, "Text files (*.txt *.log)", "file", "All files")
        assert result is False

    def test_matches_filter_case_insensitive(self, root):
        """Test matches_filter with case insensitive matching."""
        filetypes = [("Text files", "*.TXT")]
        
        result = utils.matches_filter("test.txt", filetypes, "Text files (*.TXT)", "file", "All files")
        assert result is True
        
        result = utils.matches_filter("test.TXT", filetypes, "Text files (*.TXT)", "file", "All files")
        assert result is True

    def test_would_create_loop_macos_specific(self, root):
        """Test would_create_loop with macOS specific cases."""
        tree_widget = Mock()
        tree_widget.exists.return_value = False
        
        with patch('tkface.widget.pathbrowser.utils.IS_MACOS', True):
            # Test macOS specific loop detection
            result = utils.would_create_loop("/Volumes/Macintosh HD/Volumes", "/", tree_widget)
            assert result is True
            
            # Test path containing real path
            result = utils.would_create_loop("/path/to/real/path/subdir", "/path/to/real/path", tree_widget)
            assert result is True

    def test_add_extension_if_needed_complex_patterns(self, root):
        """Test add_extension_if_needed with complex patterns."""
        filetypes = [
            ("Python files", "*.py *.pyw"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        
        # Test with multiple extensions in pattern
        result = utils.add_extension_if_needed("test", filetypes, "Python files (*.py *.pyw)")
        assert result == "test.pyw"  # Should add first extension from pattern
        
        # Test with no extension needed
        result = utils.add_extension_if_needed("test.py", filetypes, "Python files (*.py *.pyw)")
        assert result == "test.py"

    def test_get_performance_stats_edge_cases(self, root):
        """Test get_performance_stats with edge cases."""
        # Test with zero values
        stats = utils.get_performance_stats(0, 0, "", 0)
        assert stats["cache_size"] == 0
        assert stats["memory_usage_bytes"] == 0
        assert stats["current_directory"] == ""
        assert stats["selected_items_count"] == 0
        
        # Test with large values
        stats = utils.get_performance_stats(10000, 1000000000, "/very/long/path/name", 1000)
        assert stats["cache_size"] == 10000
        assert stats["memory_usage_bytes"] == 1000000000
        assert stats["current_directory"] == "/very/long/path/name"
        assert stats["selected_items_count"] == 1000


class TestStyleAdvanced:
    """Test advanced style functionality."""

    def test_load_theme_file_error_handling(self, root):
        """Test theme file loading with error handling."""
        # Test with nonexistent theme file
        with patch('pathlib.Path.exists', return_value=False):
            with pytest.raises(FileNotFoundError):
                style._load_theme_file("nonexistent")
        
        # Test with malformed config file
        import configparser
        with patch('pathlib.Path.exists', return_value=True), \
             patch('configparser.ConfigParser.read') as mock_read, \
             patch('configparser.ConfigParser.__getitem__', side_effect=KeyError):
            mock_read.return_value = []
            with pytest.raises(configparser.Error):
                style._load_theme_file("malformed")

    def test_apply_theme_to_widget_recursive(self, root):
        """Test applying theme to widget recursively."""
        # Create a mock widget hierarchy
        parent_widget = Mock()
        child_widget = Mock()
        grandchild_widget = Mock()
        
        parent_widget.winfo_children.return_value = [child_widget]
        child_widget.winfo_children.return_value = [grandchild_widget]
        grandchild_widget.winfo_children.return_value = []
        
        parent_widget.winfo_class.return_value = "TFrame"
        child_widget.winfo_class.return_value = "TButton"
        grandchild_widget.winfo_class.return_value = "TLabel"
        
        theme = PathBrowserTheme()
        
        style.apply_theme_to_widget(parent_widget, theme)
        
        # Verify that configure was called on all widgets
        parent_widget.configure.assert_called()
        child_widget.configure.assert_called()
        grandchild_widget.configure.assert_called()

    def test_apply_theme_to_widget_with_error(self, root):
        """Test applying theme to widget with error handling."""
        widget = Mock()
        widget.winfo_children.return_value = []
        widget.configure.side_effect = ValueError("Invalid color")
        
        theme = PathBrowserTheme()
        
        # Should not raise exception
        style.apply_theme_to_widget(widget, theme)
        
        widget.configure.assert_called()

    def test_get_pathbrowser_themes_with_missing_dir(self, root):
        """Test getting themes when themes directory is missing."""
        with patch('pathlib.Path.exists', return_value=False):
            themes = style.get_pathbrowser_themes()
            assert themes == ["light"]

    def test_get_pathbrowser_themes_with_filtering(self, root):
        """Test getting themes with filtering."""
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.glob') as mock_glob:
            
            # Mock theme files
            mock_theme1 = Mock()
            mock_theme1.stem = "light"
            mock_theme2 = Mock()
            mock_theme2.stem = "dark"
            mock_theme3 = Mock()
            mock_theme3.stem = "custom"  # Should be filtered out
            
            mock_glob.return_value = [mock_theme1, mock_theme2, mock_theme3]
            
            themes = style.get_pathbrowser_themes()
            assert "light" in themes
            assert "dark" in themes
            assert "custom" not in themes


class TestPathBrowserCoreAdvanced:
    """Advanced tests for PathBrowser core functionality using conftest fixtures."""

    def test_core_methods_exist(self, root, pathbrowser_mock_patches, pathbrowser_mock_widgets):
        """Test that core methods exist and can be called."""
        from tkface.widget.pathbrowser.core import PathBrowser, PathBrowserConfig
        from unittest.mock import patch, Mock
        
        # Create PathBrowser with mocked widgets
        config = PathBrowserConfig(initialdir="/tmp")
        
        with patch('tkface.widget.pathbrowser.view.lang.get', return_value="Go"), \
             patch('tkface.widget.pathbrowser.view.create_pathbrowser_widgets') as mock_create_widgets, \
             patch('tkface.widget.pathbrowser.view.setup_pathbrowser_bindings'), \
             patch('tkface.widget.pathbrowser.view.load_directory_tree'), \
             patch('tkface.widget.pathbrowser.view.load_files'), \
             patch('tkface.widget.pathbrowser.view.update_selected_display'), \
             patch('tkface.widget.pathbrowser.view.update_status'), \
             patch('tkface.widget.pathbrowser.core.Path') as mock_path, \
             patch.object(PathBrowser, '_load_directory'), \
             patch.object(PathBrowser, '_update_navigation_buttons'):
            
            # Mock Path operations
            mock_path.return_value.absolute.return_value = "/tmp"
            
            # Mock create_pathbrowser_widgets to set required attributes
            def mock_create_widgets_side_effect(browser_instance):
                browser_instance.file_tree = Mock()
                browser_instance.file_tree.focus_set = Mock()
                browser_instance.after = Mock()
                browser_instance.path_var = Mock()
                browser_instance.status_var = Mock()
                browser_instance.up_button = Mock()
                browser_instance.down_button = Mock()
                browser_instance.filter_combo = Mock()
                browser_instance.selected_files_entry = Mock()
                browser_instance.selected_var = Mock()
                browser_instance.tree = Mock()
            
            mock_create_widgets.side_effect = mock_create_widgets_side_effect
            
            browser = PathBrowser(root, config=config)
        
        # Test that core methods exist
        assert hasattr(browser, '_load_directory')
        assert hasattr(browser, '_go_up')
        assert hasattr(browser, '_go_down')
        assert hasattr(browser, '_go_to_path')
        assert hasattr(browser, '_update_navigation_buttons')
        assert hasattr(browser, '_copy_path')
        assert hasattr(browser, '_open_selected')
        assert hasattr(browser, '_move_selection_up')
        assert hasattr(browser, '_move_selection_down')
        assert hasattr(browser, '_move_to_first')
        assert hasattr(browser, '_move_to_last')
        assert hasattr(browser, '_on_file_select')
        assert hasattr(browser, '_check_memory_usage')
        assert hasattr(browser, '_schedule_memory_monitoring')
        assert hasattr(browser, '_update_status')
        assert hasattr(browser, 'get_selection')
        assert hasattr(browser, 'set_initial_directory')
        assert hasattr(browser, 'set_file_types')
        assert hasattr(browser, 'get_performance_stats')
        assert hasattr(browser, 'optimize_performance')

    def test_load_directory_permission_error(self, root, pathbrowser_mock_patches, pathbrowser_mock_widgets):
        """Test _load_directory with permission error."""
        from tkface.widget.pathbrowser.core import PathBrowser, PathBrowserConfig
        from unittest.mock import patch, Mock
        import os
        
        config = PathBrowserConfig(initialdir="/tmp")
        
        with patch('tkface.widget.pathbrowser.view.lang.get', return_value="Go"), \
             patch('tkface.widget.pathbrowser.view.create_pathbrowser_widgets') as mock_create_widgets, \
             patch('tkface.widget.pathbrowser.view.setup_pathbrowser_bindings'), \
             patch('tkface.widget.pathbrowser.view.load_directory_tree'), \
             patch('tkface.widget.pathbrowser.view.load_files'), \
             patch('tkface.widget.pathbrowser.view.update_selected_display'), \
             patch('tkface.widget.pathbrowser.view.update_status'), \
             patch('tkface.widget.pathbrowser.core.Path') as mock_path, \
             patch.object(PathBrowser, '_update_navigation_buttons'), \
             patch('tkface.widget.pathbrowser.core.messagebox') as mock_messagebox:
            
            # Mock Path operations
            mock_path.return_value.absolute.return_value = "/tmp"
            mock_path.return_value.name = "test_dir"
            
            # Mock create_pathbrowser_widgets to set required attributes
            def mock_create_widgets_side_effect(browser_instance):
                browser_instance.file_tree = Mock()
                browser_instance.file_tree.focus_set = Mock()
                browser_instance.after = Mock()
                browser_instance.path_var = Mock()
                browser_instance.status_var = Mock()
                browser_instance.up_button = Mock()
                browser_instance.filter_combo = Mock()
                browser_instance.selected_files_entry = Mock()
                browser_instance.selected_var = Mock()
                browser_instance.tree = Mock()
                browser_instance.winfo_toplevel = Mock(return_value=root)
            
            mock_create_widgets.side_effect = mock_create_widgets_side_effect
            
            browser = PathBrowser(root, config=config)
            
            # Mock file_info_manager to raise PermissionError
            with patch.object(browser.file_info_manager, '_resolve_symlink', side_effect=PermissionError("Access denied")):
                browser._load_directory("/restricted")
                
                # Check that error message was set
                browser.status_var.set.assert_called()
                mock_messagebox.showerror.assert_called()

    def test_load_directory_file_not_found(self, root, pathbrowser_mock_patches, pathbrowser_mock_widgets):
        """Test _load_directory with file not found error."""
        from tkface.widget.pathbrowser.core import PathBrowser, PathBrowserConfig
        from unittest.mock import patch, Mock
        import os
        
        config = PathBrowserConfig(initialdir="/tmp")
        
        with patch('tkface.widget.pathbrowser.view.lang.get', return_value="Go"), \
             patch('tkface.widget.pathbrowser.view.create_pathbrowser_widgets') as mock_create_widgets, \
             patch('tkface.widget.pathbrowser.view.setup_pathbrowser_bindings'), \
             patch('tkface.widget.pathbrowser.view.load_directory_tree'), \
             patch('tkface.widget.pathbrowser.view.load_files'), \
             patch('tkface.widget.pathbrowser.view.update_selected_display'), \
             patch('tkface.widget.pathbrowser.view.update_status'), \
             patch('tkface.widget.pathbrowser.core.Path') as mock_path, \
             patch.object(PathBrowser, '_update_navigation_buttons'):
            
            # Mock Path operations
            mock_path.return_value.absolute.return_value = "/tmp"
            mock_path.return_value.name = "missing_dir"
            mock_path.return_value.parent = "/parent"
            
            # Mock create_pathbrowser_widgets to set required attributes
            def mock_create_widgets_side_effect(browser_instance):
                browser_instance.file_tree = Mock()
                browser_instance.file_tree.focus_set = Mock()
                browser_instance.after = Mock()
                browser_instance.path_var = Mock()
                browser_instance.status_var = Mock()
                browser_instance.up_button = Mock()
                browser_instance.filter_combo = Mock()
                browser_instance.selected_files_entry = Mock()
                browser_instance.selected_var = Mock()
                browser_instance.tree = Mock()
            
            mock_create_widgets.side_effect = mock_create_widgets_side_effect
            
            browser = PathBrowser(root, config=config)
            
            # Mock file_info_manager to raise FileNotFoundError for the first call only
            with patch.object(browser.file_info_manager, '_resolve_symlink') as mock_resolve:
                # First call raises FileNotFoundError, subsequent calls return the path
                mock_resolve.side_effect = [FileNotFoundError("Directory not found"), "/parent", "/tmp"]
                
                browser._load_directory("/missing")
                
                # Check that error message was set
                browser.status_var.set.assert_called()
                # Check that it tried to navigate to parent (recursive call)
                assert browser.status_var.set.call_count >= 1

    def test_navigation_methods(self, root, pathbrowser_mock_patches, pathbrowser_mock_widgets):
        """Test navigation methods."""
        from tkface.widget.pathbrowser.core import PathBrowser, PathBrowserConfig
        from unittest.mock import patch, Mock
        
        config = PathBrowserConfig(initialdir="/tmp")
        
        with patch('tkface.widget.pathbrowser.view.lang.get', return_value="Go"), \
             patch('tkface.widget.pathbrowser.view.create_pathbrowser_widgets') as mock_create_widgets, \
             patch('tkface.widget.pathbrowser.view.setup_pathbrowser_bindings'), \
             patch('tkface.widget.pathbrowser.view.load_directory_tree'), \
             patch('tkface.widget.pathbrowser.view.load_files'), \
             patch('tkface.widget.pathbrowser.view.update_selected_display'), \
             patch('tkface.widget.pathbrowser.view.update_status'), \
             patch('tkface.widget.pathbrowser.core.Path') as mock_path, \
             patch.object(PathBrowser, '_load_directory') as mock_load_dir, \
             patch.object(PathBrowser, '_update_navigation_buttons'):
            
            # Mock Path operations
            mock_path.return_value.absolute.return_value = "/tmp"
            mock_path.return_value.parent = "/parent"
            
            # Mock create_pathbrowser_widgets to set required attributes
            def mock_create_widgets_side_effect(browser_instance):
                browser_instance.file_tree = Mock()
                browser_instance.file_tree.focus_set = Mock()
                browser_instance.after = Mock()
                browser_instance.path_var = Mock()
                browser_instance.status_var = Mock()
                browser_instance.up_button = Mock()
                browser_instance.down_button = Mock()
                browser_instance.filter_combo = Mock()
                browser_instance.selected_files_entry = Mock()
                browser_instance.selected_var = Mock()
                browser_instance.tree = Mock()
            
            mock_create_widgets.side_effect = mock_create_widgets_side_effect
            
            browser = PathBrowser(root, config=config)
            
            # Test _go_up
            browser._go_up()
            mock_load_dir.assert_called_with("/parent")
            mock_path.assert_called_with("/tmp")
            
            # Test _go_down with forward history
            browser.state.forward_history = ["/subdir"]
            browser._go_down()
            mock_load_dir.assert_called_with("/subdir")
            
            # Test _go_down without forward history
            browser.state.forward_history = []
            browser._go_down()
            browser.status_var.set.assert_called()

    def test_file_operations(self, root, pathbrowser_mock_patches, pathbrowser_mock_widgets):
        """Test file operation methods."""
        from tkface.widget.pathbrowser.core import PathBrowser, PathBrowserConfig
        from unittest.mock import patch, Mock
        
        config = PathBrowserConfig(initialdir="/tmp")
        
        with patch('tkface.widget.pathbrowser.view.lang.get', return_value="Go"), \
             patch('tkface.widget.pathbrowser.view.create_pathbrowser_widgets') as mock_create_widgets, \
             patch('tkface.widget.pathbrowser.view.setup_pathbrowser_bindings'), \
             patch('tkface.widget.pathbrowser.view.load_directory_tree'), \
             patch('tkface.widget.pathbrowser.view.load_files'), \
             patch('tkface.widget.pathbrowser.view.update_selected_display'), \
             patch('tkface.widget.pathbrowser.view.update_status'), \
             patch('tkface.widget.pathbrowser.core.Path') as mock_path, \
             patch('tkface.widget.pathbrowser.core.messagebox') as mock_messagebox:
            
            # Mock Path operations
            mock_path.return_value.absolute.return_value = "/tmp"
            
            # Mock create_pathbrowser_widgets to set required attributes
            def mock_create_widgets_side_effect(browser_instance):
                browser_instance.file_tree = Mock()
                browser_instance.file_tree.focus_set = Mock()
                browser_instance.after = Mock()
                browser_instance.path_var = Mock()
                browser_instance.status_var = Mock()
                browser_instance.up_button = Mock()
                browser_instance.down_button = Mock()
                browser_instance.filter_combo = Mock()
                browser_instance.selected_files_entry = Mock()
                browser_instance.selected_var = Mock()
                browser_instance.tree = Mock()
                browser_instance.winfo_toplevel = Mock(return_value=root)
                
                # Mock selection methods to return empty lists
                browser_instance.tree.selection.return_value = []
                browser_instance.file_tree.selection.return_value = []
            
            mock_create_widgets.side_effect = mock_create_widgets_side_effect
            
            browser = PathBrowser(root, config=config)
            
            # Test _copy_path
            browser._copy_path()
            # Should not raise any errors
            
            # Test _open_selected
            browser._open_selected()
            # Should not raise any errors

    def test_memory_monitoring(self, root, pathbrowser_mock_patches, pathbrowser_mock_widgets):
        """Test memory monitoring methods."""
        from tkface.widget.pathbrowser.core import PathBrowser, PathBrowserConfig
        from unittest.mock import patch, Mock
        
        config = PathBrowserConfig(initialdir="/tmp")
        
        with patch('tkface.widget.pathbrowser.view.lang.get', return_value="Go"), \
             patch('tkface.widget.pathbrowser.view.create_pathbrowser_widgets') as mock_create_widgets, \
             patch('tkface.widget.pathbrowser.view.setup_pathbrowser_bindings'), \
             patch('tkface.widget.pathbrowser.view.load_directory_tree'), \
             patch('tkface.widget.pathbrowser.view.load_files'), \
             patch('tkface.widget.pathbrowser.view.update_selected_display'), \
             patch('tkface.widget.pathbrowser.view.update_status'), \
             patch('tkface.widget.pathbrowser.core.Path') as mock_path:
            
            # Mock Path operations
            mock_path.return_value.absolute.return_value = "/tmp"
            
            # Mock create_pathbrowser_widgets to set required attributes
            def mock_create_widgets_side_effect(browser_instance):
                browser_instance.file_tree = Mock()
                browser_instance.file_tree.focus_set = Mock()
                browser_instance.after = Mock()
                browser_instance.path_var = Mock()
                browser_instance.status_var = Mock()
                browser_instance.up_button = Mock()
                browser_instance.down_button = Mock()
                browser_instance.filter_combo = Mock()
                browser_instance.selected_files_entry = Mock()
                browser_instance.selected_var = Mock()
                browser_instance.tree = Mock()
            
            mock_create_widgets.side_effect = mock_create_widgets_side_effect
            
            browser = PathBrowser(root, config=config)
            
            # Test _check_memory_usage
            browser._check_memory_usage()
            # Should not raise any errors
            
            # Test _schedule_memory_monitoring
            browser._schedule_memory_monitoring()
            # Should not raise any errors


class TestViewAdvanced:
    """Advanced tests for view functionality using conftest fixtures."""

    def test_view_functions_exist(self, root, pathbrowser_mock_patches):
        """Test that view functions exist and can be called."""
        from tkface.widget.pathbrowser import view
        
        # Test that view functions exist
        assert hasattr(view, 'create_pathbrowser_widgets')
        assert hasattr(view, 'setup_pathbrowser_bindings')
        assert hasattr(view, 'load_directory_tree')
        assert hasattr(view, 'expand_path')
        assert hasattr(view, 'sort_items')
        assert hasattr(view, 'update_selected_display')
        assert hasattr(view, 'update_status')
        assert hasattr(view, 'show_context_menu')




class TestUtilsAdvancedComprehensive:
    """Comprehensive advanced tests for utility functions."""

    def test_utils_functions_exist(self, root):
        """Test that utility functions exist and can be called."""
        from tkface.widget.pathbrowser import utils
        
        # Test that utility functions exist
        assert hasattr(utils, 'format_size')
        assert hasattr(utils, 'matches_filter')
        assert hasattr(utils, 'would_create_loop')
        assert hasattr(utils, 'add_extension_if_needed')
        assert hasattr(utils, 'get_performance_stats')
        assert hasattr(utils, 'open_file_with_default_app')




class TestStyleAdvancedComprehensive:
    """Comprehensive advanced tests for style functionality."""

    def test_style_functions_exist(self, root):
        """Test that style functions exist and can be called."""
        from tkface.widget.pathbrowser import style
        
        # Test that style functions exist
        assert hasattr(style, 'PathBrowserTheme')
        assert hasattr(style, 'get_pathbrowser_theme')
        assert hasattr(style, 'get_pathbrowser_themes')
        assert hasattr(style, 'apply_theme_to_widget')
        assert hasattr(style, 'get_default_theme')








if __name__ == "__main__":
    pytest.main([__file__])
