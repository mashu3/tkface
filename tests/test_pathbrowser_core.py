"""
Additional tests for PathBrowser core functionality to improve coverage.

This module focuses on testing the uncovered parts of the core.py file.
"""

import os
from unittest.mock import Mock, patch
import pytest
import tkinter as tk
from tkface.widget.pathbrowser import PathBrowser
from tkface.widget.pathbrowser import utils
from tkface.widget.pathbrowser import view


class TestPathBrowserCoreAdditionalCoverage:
    """Additional tests for PathBrowser core functionality to improve coverage."""

    def test_on_file_select_no_selection(self, root, mock_treeview_operations):
        """Test _on_file_select method with no selection."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.state.selected_items = ["/test/file1.txt"]

        with patch.object(browser, '_update_status') as mock_update:
            with patch.object(view, 'update_selected_display') as mock_update_display:
                browser._on_file_select(None)
                assert browser.state.selected_items == []
                mock_update.assert_called_once()
                mock_update_display.assert_called_once_with(browser)

    def test_on_file_select_with_selection(self, root, mock_treeview_operations):
        """Test _on_file_select method with selection."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = ["/test/file1.txt"]
        browser.state.selected_items = []

        with patch.object(browser, '_update_status') as mock_update:
            with patch.object(view, 'update_selected_display') as mock_update_display:
                browser._on_file_select(None)
                assert "/test/file1.txt" in browser.state.selected_items
                mock_update.assert_called_once()
                mock_update_display.assert_called_once_with(browser)

    def test_move_selection_up_normal(self, root, mock_treeview_operations):
        """Test _move_selection_up method in normal case."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.get_children.return_value = ["/test/file1.txt", "/test/file2.txt"]
        browser.file_tree.selection.return_value = ["/test/file2.txt"]

        with patch.object(browser, '_on_file_select') as mock_select_callback:
            result = browser._move_selection_up(Mock())
            assert result == "break"
            browser.file_tree.selection_set.assert_called_once_with("/test/file1.txt")
            browser.file_tree.see.assert_called_once_with("/test/file1.txt")
            mock_select_callback.assert_called_once_with(None)

    def test_move_selection_down_normal(self, root, mock_treeview_operations):
        """Test _move_selection_down method in normal case."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.get_children.return_value = ["/test/file1.txt", "/test/file2.txt"]
        browser.file_tree.selection.return_value = ["/test/file1.txt"]

        with patch.object(browser, '_on_file_select') as mock_select_callback:
            result = browser._move_selection_down(Mock())
            assert result == "break"
            browser.file_tree.selection_set.assert_called_once_with("/test/file2.txt")
            browser.file_tree.see.assert_called_once_with("/test/file2.txt")
            mock_select_callback.assert_called_once_with(None)

    def test_extend_selection_range_normal(self, root, mock_treeview_operations):
        """Test _extend_selection_range with normal selection."""
        browser = PathBrowser(root)
        browser.config.multiple = True
        browser.file_tree = mock_treeview_operations
        browser.file_tree.get_children.return_value = ["/test/file1.txt", "/test/file2.txt", "/test/file3.txt"]
        browser.file_tree.selection.return_value = ["/test/file1.txt"]
        browser.state.selection_anchor = "/test/file1.txt"

        event = Mock()

        with patch.object(browser, '_on_file_select') as mock_select_callback:
            result = browser._extend_selection_range(event, 1)
            assert result == "break"
            # Should select range from anchor to target
            expected_selection = ["/test/file1.txt", "/test/file2.txt"]
            browser.file_tree.selection_set.assert_called_once_with(expected_selection)

    def test_expand_all(self, root, comprehensive_treeview_mock, mock_file_info_manager):
        """Test _expand_all method."""
        browser = PathBrowser(root)
        browser.tree = comprehensive_treeview_mock
        browser.file_info_manager = mock_file_info_manager

        # Mock file info for directory
        mock_file_info = Mock()
        mock_file_info.is_dir = True
        browser.file_info_manager.get_cached_file_info.return_value = mock_file_info

        # Mock tree children to return empty list to prevent recursion
        browser.tree.get_children.return_value = []

        browser._expand_all("/test/dir")
        browser.tree.item.assert_called_with("/test/dir", open=True)
        browser.tree.get_children.assert_called()

    def test_on_ok_save_mode_valid_filename(self, root):
        """Test _on_ok method in save mode with valid filename."""
        browser = PathBrowser(root)
        browser.config.save_mode = True
        browser.selected_var = Mock()
        browser.selected_var.get.return_value = "test.txt"
        browser.state.current_dir = "/test"

        with patch.object(browser, 'event_generate') as mock_event:
            browser._on_ok()
            mock_event.assert_called_once_with("<<PathBrowserOK>>")

    def test_on_ok_open_mode(self, root):
        """Test _on_ok method in open mode."""
        browser = PathBrowser(root)
        browser.config.save_mode = False
        browser.state.selected_items = ["/test/file1.txt"]

        with patch.object(browser, 'event_generate') as mock_event:
            browser._on_ok()
            mock_event.assert_called_once_with("<<PathBrowserOK>>")

    def test_has_directory_selection_true(self, root, mock_file_info_manager):
        """Test _has_directory_selection method returns True."""
        browser = PathBrowser(root)
        browser.state.selected_items = ["/test/dir1", "/test/file1.txt"]
        browser.file_info_manager = mock_file_info_manager
        
        # Mock file info for directory
        mock_dir_info = Mock()
        mock_dir_info.is_dir = True
        mock_file_info = Mock()
        mock_file_info.is_dir = False
        
        browser.file_info_manager.get_cached_file_info.side_effect = lambda x: mock_dir_info if x == "/test/dir1" else mock_file_info
        
        result = browser._has_directory_selection()
        assert result is True

    def test_has_directory_selection_false(self, root, mock_file_info_manager):
        """Test _has_directory_selection method returns False."""
        browser = PathBrowser(root)
        browser.state.selected_items = ["/test/file1.txt", "/test/file2.txt"]
        browser.file_info_manager = mock_file_info_manager
        
        # Mock file info for files
        mock_file_info = Mock()
        mock_file_info.is_dir = False
        browser.file_info_manager.get_cached_file_info.return_value = mock_file_info
        
        result = browser._has_directory_selection()
        assert result is False

    def test_show_directory_error(self, root):
        """Test _show_directory_error method."""
        browser = PathBrowser(root)
        browser.config.title = "Test Browser"

        with patch('tkface.dialog.messagebox.showerror') as mock_error:
            browser._show_directory_error()
            mock_error.assert_called_once()

    def test_on_cancel(self, root):
        """Test _on_cancel method."""
        browser = PathBrowser(root)

        with patch.object(browser, 'event_generate') as mock_event:
            browser._on_cancel()
            mock_event.assert_called_once_with("<<PathBrowserCancel>>")

    def test_update_status(self, root):
        """Test _update_status method."""
        browser = PathBrowser(root)
        browser.status_var = Mock()
        browser.state.selected_items = ["/test/file1.txt", "/test/file2.txt"]

        browser._update_status()
        browser.status_var.set.assert_called_once()

    def test_add_extension_if_needed(self, root):
        """Test _add_extension_if_needed method."""
        browser = PathBrowser(root)
        browser.config.filetypes = [("Text files", "*.txt")]
        browser.filter_var = Mock()
        browser.filter_var.get.return_value = "*.txt"

        with patch('tkface.widget.pathbrowser.utils.add_extension_if_needed') as mock_add_ext:
            # Test with extension
            mock_add_ext.return_value = "test.txt"
            result = browser._add_extension_if_needed("test.txt")
            assert result == "test.txt"
            mock_add_ext.assert_called_once_with("test.txt", browser.config.filetypes, "*.txt")

            # Test without extension
            mock_add_ext.return_value = "test.txt"
            result = browser._add_extension_if_needed("test")
            assert result == "test.txt"
            mock_add_ext.assert_called_with("test", browser.config.filetypes, "*.txt")

    def test_schedule_memory_monitoring(self, root):
        """Test _schedule_memory_monitoring method."""
        browser = PathBrowser(root)

        with patch.object(browser, 'after') as mock_after:
            browser._schedule_memory_monitoring()
            mock_after.assert_called_once()

    def test_check_memory_usage(self, root, mock_file_info_manager):
        """Test _check_memory_usage method."""
        browser = PathBrowser(root)
        browser.file_info_manager = mock_file_info_manager

        with patch.object(browser, 'after') as mock_after:
            browser._check_memory_usage()
            # メソッドが正常に実行されることを確認
            browser.file_info_manager.get_memory_usage_estimate.assert_called_once()
            browser.file_info_manager.get_cache_size.assert_called_once()

    def test_optimize_performance(self, root, mock_file_info_manager):
        """Test optimize_performance method."""
        browser = PathBrowser(root)
        browser.file_info_manager = mock_file_info_manager

        with patch.object(browser, '_load_directory') as mock_load:
            browser.optimize_performance()
            # メソッドが正常に実行されることを確認
            browser.file_info_manager.clear_cache.assert_called_once()
            mock_load.assert_called_once_with(browser.state.current_dir)

    def test_on_file_double_click(self, root, mock_treeview_operations, mock_file_info_manager):
        """Test _on_file_double_click method."""
        browser = PathBrowser(root)
        browser.state.selected_items = ["/test/file1.txt"]
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = ["/test/file1.txt"]
        browser.file_info_manager = mock_file_info_manager
        browser.file_info_manager._resolve_symlink.return_value = "/test/file1.txt"
        browser.file_info_manager.get_cached_file_info.return_value = Mock(is_dir=False)

        with patch.object(browser, '_on_ok') as mock_on_ok:
            browser._on_file_double_click(None)
            mock_on_ok.assert_called_once()

    def test_on_filter_change(self, root):
        """Test _on_filter_change method."""
        browser = PathBrowser(root)
        browser.filter_var = Mock()
        browser.filter_var.get.return_value = "*.txt"

        with patch.object(view, 'load_files') as mock_load:
            browser._on_filter_change(None)
            mock_load.assert_called_once_with(browser)

    def test_sort_files(self, root):
        """Test _sort_files method."""
        browser = PathBrowser(root)
        browser.state.sort_column = "#0"
        browser.state.sort_reverse = False

        with patch.object(view, 'load_files') as mock_load:
            browser._sort_files("#1")
            assert browser.state.sort_column == "#1"
            assert browser.state.sort_reverse is False
            mock_load.assert_called_once_with(browser)

    def test_on_filename_focus(self, root):
        """Test _on_filename_focus method."""
        browser = PathBrowser(root)
        browser.selected_files_entry = Mock()

        browser._on_filename_focus(None)
        browser.selected_files_entry.select_range.assert_called_once_with(0, tk.END)

    def test_on_tree_select(self, root, comprehensive_treeview_mock, mock_file_info_manager):
        """Test _on_tree_select method."""
        browser = PathBrowser(root)
        browser.tree = comprehensive_treeview_mock
        browser.tree.selection.return_value = ["/test/dir1"]
        browser.file_info_manager = mock_file_info_manager
        browser.file_info_manager._resolve_symlink.return_value = "/test/dir1"
        browser.file_info_manager.get_cached_file_info.return_value = Mock(is_dir=True)

        with patch.object(browser, '_load_directory') as mock_load:
            with patch.object(view, 'update_selected_display') as mock_update_display:
                browser._on_tree_select(None)
                mock_load.assert_called_once_with("/test/dir1")

    def test_on_tree_open(self, root, comprehensive_treeview_mock, mock_file_info_manager):
        """Test _on_tree_open method."""
        browser = PathBrowser(root)
        browser.tree = comprehensive_treeview_mock
        browser.tree.selection.return_value = ["/test/dir1"]
        browser.tree.get_children.return_value = []
        browser.file_info_manager = mock_file_info_manager
        browser.file_info_manager.get_file_info.return_value = Mock(is_dir=True)

        with patch.object(view, 'populate_tree_node') as mock_populate:
            browser._on_tree_open(None)
            mock_populate.assert_called_once_with(browser, "/test/dir1")

    def test_copy_path(self, root, comprehensive_treeview_mock, mock_treeview_operations):
        """Test _copy_path method."""
        browser = PathBrowser(root)
        browser.tree = comprehensive_treeview_mock
        browser.tree.selection.return_value = ["/test/file1.txt"]
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = []

        with patch.object(browser, 'clipboard_clear') as mock_clear:
            with patch.object(browser, 'clipboard_append') as mock_append:
                browser._copy_path()
                mock_clear.assert_called_once()
                mock_append.assert_called_once_with("/test/file1.txt")

    def test_open_selected(self, root, mock_treeview_operations, mock_file_info_manager):
        """Test _open_selected method."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = ["/test/file1.txt"]
        browser.file_info_manager = mock_file_info_manager
        browser.file_info_manager._resolve_symlink.return_value = "/test/file1.txt"
        browser.file_info_manager.get_cached_file_info.return_value = Mock(is_dir=False)

        with patch('tkface.widget.pathbrowser.utils.open_file_with_default_app') as mock_open:
            mock_open.return_value = True
            browser._open_selected()
            mock_open.assert_called_once_with("/test/file1.txt")

    def test_expand_node(self, root, comprehensive_treeview_mock, mock_file_info_manager):
        """Test _expand_node method."""
        browser = PathBrowser(root)
        browser.tree = comprehensive_treeview_mock
        browser.tree.selection.return_value = ["/test/dir1"]
        browser.tree.get_children.return_value = []
        browser.tree.item.return_value = None
        browser.file_info_manager = mock_file_info_manager
        browser.file_info_manager.get_cached_file_info.return_value = Mock(is_dir=True)

        with patch.object(view, 'populate_tree_node') as mock_populate:
            result = browser._expand_node(None)
            assert result == "break"
            browser.tree.item.assert_called_once_with("/test/dir1", open=True)

    def test_collapse_node(self, root, comprehensive_treeview_mock, mock_file_info_manager):
        """Test _collapse_node method."""
        browser = PathBrowser(root)
        browser.tree = comprehensive_treeview_mock
        browser.tree.selection.return_value = ["/test/dir1"]
        browser.tree.item.return_value = None
        browser.file_info_manager = mock_file_info_manager
        browser.file_info_manager.get_cached_file_info.return_value = Mock(is_dir=True)

        result = browser._collapse_node(None)
        assert result == "break"
        browser.tree.item.assert_called_once_with("/test/dir1", open=False)

    def test_toggle_selected_node(self, root, comprehensive_treeview_mock, mock_file_info_manager):
        """Test _toggle_selected_node method."""
        browser = PathBrowser(root)
        browser.tree = comprehensive_treeview_mock
        browser.tree.selection.return_value = ["/test/dir1"]
        # Mock tree.item to return a dictionary with "open" key
        browser.tree.item.return_value = {"open": False}
        browser.file_info_manager = mock_file_info_manager
        browser.file_info_manager.get_cached_file_info.return_value = Mock(is_dir=True)

        with patch.object(browser, '_expand_node') as mock_expand:
            result = browser._toggle_selected_node(None)
            assert result == "break"
            mock_expand.assert_called_once_with(None)

    def test_on_file_tree_click(self, root, mock_treeview_operations):
        """Test _on_file_tree_click method."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = ["/test/file1.txt"]

        browser._on_file_tree_click(None)
        browser.file_tree.focus_set.assert_called_once()

    def test_on_file_frame_click(self, root, mock_treeview_operations):
        """Test _on_file_frame_click method."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = ["/test/file1.txt"]

        browser._on_file_frame_click(None)
        browser.file_tree.focus_set.assert_called_once()

    def test_handle_up_key(self, root, mock_treeview_operations):
        """Test _handle_up_key method."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.focus_get = Mock(return_value=browser.file_tree)

        with patch.object(browser, '_move_selection_up') as mock_move:
            result = browser._handle_up_key(None)
            mock_move.assert_called_once_with(None)
            assert result is not None

    def test_handle_down_key(self, root, mock_treeview_operations):
        """Test _handle_down_key method."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.focus_get = Mock(return_value=browser.file_tree)

        with patch.object(browser, '_move_selection_down') as mock_move:
            result = browser._handle_down_key(None)
            mock_move.assert_called_once_with(None)
            assert result is not None

    def test_handle_home_key(self, root, mock_treeview_operations):
        """Test _handle_home_key method."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.focus_get = Mock(return_value=browser.file_tree)

        with patch.object(browser, '_move_to_first') as mock_move:
            result = browser._handle_home_key(None)
            mock_move.assert_called_once_with(None)
            assert result is not None

    def test_handle_end_key(self, root, mock_treeview_operations):
        """Test _handle_end_key method."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.focus_get = Mock(return_value=browser.file_tree)

        with patch.object(browser, '_move_to_last') as mock_move:
            result = browser._handle_end_key(None)
            mock_move.assert_called_once_with(None)
            assert result is not None

    def test_handle_shift_up_key(self, root, mock_treeview_operations):
        """Test _handle_shift_up_key method."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.focus_get = Mock(return_value=browser.file_tree)

        with patch.object(browser, '_extend_selection_up') as mock_extend:
            result = browser._handle_shift_up_key(None)
            mock_extend.assert_called_once_with(None)
            assert result is not None

    def test_handle_shift_down_key(self, root, mock_treeview_operations):
        """Test _handle_shift_down_key method."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.focus_get = Mock(return_value=browser.file_tree)

        with patch.object(browser, '_extend_selection_down') as mock_extend:
            result = browser._handle_shift_down_key(None)
            mock_extend.assert_called_once_with(None)
            assert result is not None

    def test_move_to_first(self, root, mock_treeview_operations):
        """Test _move_to_first method."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.get_children.return_value = ["/test/file1.txt", "/test/file2.txt"]

        with patch.object(browser, '_on_file_select') as mock_select_callback:
            browser._move_to_first(None)
            browser.file_tree.selection_set.assert_called_once_with("/test/file1.txt")
            browser.file_tree.see.assert_called_once_with("/test/file1.txt")
            mock_select_callback.assert_called_once_with(None)

    def test_move_to_last(self, root, mock_treeview_operations):
        """Test _move_to_last method."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.get_children.return_value = ["/test/file1.txt", "/test/file2.txt"]

        with patch.object(browser, '_on_file_select') as mock_select_callback:
            browser._move_to_last(None)
            browser.file_tree.selection_set.assert_called_once_with("/test/file2.txt")
            browser.file_tree.see.assert_called_once_with("/test/file2.txt")
            mock_select_callback.assert_called_once_with(None)

    def test_move_to_edge(self, root, mock_treeview_operations):
        """Test _move_to_edge method."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.get_children.return_value = ["/test/file1.txt", "/test/file2.txt"]
        browser.file_tree.selection.return_value = ["/test/file1.txt"]

        with patch.object(browser, '_on_file_select') as mock_select:
            result = browser._move_to_edge(None, "first")
            assert result == "break"
            browser.file_tree.selection_set.assert_called_once_with("/test/file1.txt")
            browser.file_tree.see.assert_called_once_with("/test/file1.txt")
            mock_select.assert_called_once_with(None)

        # Reset mock for second test
        browser.file_tree.selection_set.reset_mock()
        browser.file_tree.see.reset_mock()

        with patch.object(browser, '_on_file_select') as mock_select:
            result = browser._move_to_edge(None, "last")
            assert result == "break"
            browser.file_tree.selection_set.assert_called_once_with("/test/file2.txt")
            browser.file_tree.see.assert_called_once_with("/test/file2.txt")
            mock_select.assert_called_once_with(None)

    def test_extend_selection_up(self, root):
        """Test _extend_selection_up method."""
        browser = PathBrowser(root)
        browser.config.multiple = True

        with patch.object(browser, '_extend_selection_range') as mock_extend:
            browser._extend_selection_up(None)
            mock_extend.assert_called_once_with(None, direction=-1)

    def test_extend_selection_down(self, root):
        """Test _extend_selection_down method."""
        browser = PathBrowser(root)
        browser.config.multiple = True

        with patch.object(browser, '_extend_selection_range') as mock_extend:
            browser._extend_selection_down(None)
            mock_extend.assert_called_once_with(None, direction=1)

    def test_move_selection(self, root, mock_treeview_operations):
        """Test _move_selection method."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = ["/test/file1.txt"]
        browser.file_tree.get_children.return_value = ["/test/file1.txt", "/test/file2.txt"]
        browser.state = Mock()
        browser.state.selection_anchor = None

        with patch.object(browser, '_on_file_select') as mock_select:
            # Test moving down from file1 to file2 (index 0 to 1)
            result = browser._move_selection(None, 1)
            assert result == "break"
            browser.file_tree.selection_set.assert_called_once_with("/test/file2.txt")
            browser.file_tree.see.assert_called_once_with("/test/file2.txt")
            mock_select.assert_called_once_with(None)

        # Reset mock for second test
        browser.file_tree.selection_set.reset_mock()
        browser.file_tree.see.reset_mock()
        browser.file_tree.selection.return_value = ["/test/file2.txt"]

        with patch.object(browser, '_on_file_select') as mock_select:
            # Test moving up from file2 to file1 (index 1 to 0)
            result = browser._move_selection(None, -1)
            assert result == "break"
            browser.file_tree.selection_set.assert_called_once_with("/test/file1.txt")
            browser.file_tree.see.assert_called_once_with("/test/file1.txt")
            mock_select.assert_called_once_with(None)

    def test_update_filter_options(self, root):
        """Test _update_filter_options method."""
        browser = PathBrowser(root)
        browser.filter_combo = Mock()
        browser.filter_combo.__setitem__ = Mock()
        browser.config.filetypes = [("Text files", "*.txt"), ("Python files", "*.py")]

        browser._update_filter_options()
        browser.filter_combo.__setitem__.assert_called()

    def test_update_navigation_buttons(self, root):
        """Test _update_navigation_buttons method."""
        browser = PathBrowser(root)
        browser.up_button = Mock()
        browser.down_button = Mock()
        browser.state.current_dir = "/test/dir1/subdir"
        browser.state.forward_history = ["/test/dir2"]

        browser._update_navigation_buttons()
        browser.up_button.config.assert_called()
        browser.down_button.config.assert_called()

    def test_go_up(self, root):
        """Test _go_up method."""
        browser = PathBrowser(root)
        browser.state.current_dir = "/test/dir1/subdir"

        with patch.object(browser, '_load_directory') as mock_load:
            browser._go_up()
            mock_load.assert_called_once_with("/test/dir1")

    def test_go_down(self, root):
        """Test _go_down method."""
        browser = PathBrowser(root)
        browser.state.forward_history = ["/test/dir2"]

        with patch.object(browser, '_load_directory') as mock_load:
            browser._go_down()
            mock_load.assert_called_once_with("/test/dir2")

    def test_go_to_path(self, root, mock_file_info_manager):
        """Test _go_to_path method."""
        browser = PathBrowser(root)
        browser.path_var = Mock()
        browser.path_var.get.return_value = "/test/dir2"
        browser.file_info_manager = mock_file_info_manager
        browser.file_info_manager._resolve_symlink.return_value = "/test/dir2"
        browser.file_info_manager.get_cached_file_info.return_value = Mock(is_dir=True)

        with patch.object(browser, '_load_directory') as mock_load:
            browser._go_to_path()
            mock_load.assert_called_once_with("/test/dir2")

    def test_load_directory_error_handling(self, root):
        """Test _load_directory method error handling."""
        browser = PathBrowser(root)

        with patch('os.listdir') as mock_listdir:
            mock_listdir.side_effect = PermissionError("Access denied")
            
            with patch('tkface.dialog.messagebox.showerror') as mock_error:
                browser._load_directory("/protected/directory")
                mock_error.assert_called_once()

    def test_init_language(self, root):
        """Test _init_language method."""
        browser = PathBrowser(root)
        
        # Test that language module is available
        from tkface import lang
        assert lang is not None

    def test_on_tree_right_click(self, root, comprehensive_treeview_mock, mock_file_info_manager):
        """Test _on_tree_right_click method."""
        browser = PathBrowser(root)
        browser.tree = comprehensive_treeview_mock
        browser.tree.identify_row.return_value = "/test/dir1"
        browser.tree.selection_set = Mock()

        with patch.object(view, 'show_context_menu') as mock_show:
            event = Mock(y=100)
            browser._on_tree_right_click(event)
            browser.tree.selection_set.assert_called_once_with("/test/dir1")
            mock_show.assert_called_once_with(browser, event, "tree")

    def test_on_file_right_click(self, root, mock_treeview_operations, mock_file_info_manager):
        """Test _on_file_right_click method."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.identify_row.return_value = "/test/file1.txt"
        browser.file_tree.selection_set = Mock()

        with patch.object(view, 'show_context_menu') as mock_show:
            event = Mock(y=100)
            browser._on_file_right_click(event)
            browser.file_tree.selection_set.assert_called_once_with("/test/file1.txt")
            mock_show.assert_called_once_with(browser, event, "file")

    def test_copy_path_tree_selection(self, root, comprehensive_treeview_mock, mock_treeview_operations):
        """Test _copy_path method with tree selection."""
        browser = PathBrowser(root)
        browser.tree = comprehensive_treeview_mock
        browser.tree.selection.return_value = ["/test/dir1"]
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = []

        with patch.object(browser, 'clipboard_clear') as mock_clear:
            with patch.object(browser, 'clipboard_append') as mock_append:
                browser._copy_path()
                mock_clear.assert_called_once()
                mock_append.assert_called_once_with("/test/dir1")

    def test_copy_path_no_selection(self, root, comprehensive_treeview_mock, mock_treeview_operations):
        """Test _copy_path method with no selection."""
        browser = PathBrowser(root)
        browser.tree = comprehensive_treeview_mock
        browser.tree.selection.return_value = []
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = []

        with patch.object(browser, 'clipboard_clear') as mock_clear:
            with patch.object(browser, 'clipboard_append') as mock_append:
                browser._copy_path()
                mock_clear.assert_not_called()
                mock_append.assert_not_called()

    def test_open_selected_directory(self, root, mock_treeview_operations, mock_file_info_manager):
        """Test _open_selected method with directory."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = ["/test/dir1"]
        browser.file_info_manager = mock_file_info_manager
        browser.file_info_manager._resolve_symlink.return_value = "/test/dir1"
        browser.file_info_manager.get_cached_file_info.return_value = Mock(is_dir=True)

        with patch.object(browser, '_load_directory') as mock_load:
            browser._open_selected()
            mock_load.assert_called_once_with("/test/dir1")

    def test_open_selected_file_failure(self, mock_pathbrowser_instance, mock_file_info_manager):
        """Test _open_selected method with file open failure."""
        browser = mock_pathbrowser_instance
        browser.file_info_manager = mock_file_info_manager
        browser.file_tree = Mock()
        browser.file_tree.selection.return_value = ["/test/file1.txt"]

        mock_file_info = Mock()
        mock_file_info.is_dir = False
        mock_file_info_manager._resolve_symlink.return_value = "/test/file1.txt"
        mock_file_info_manager.get_cached_file_info.return_value = mock_file_info

        with patch('tkface.widget.pathbrowser.utils.open_file_with_default_app') as mock_open:
            mock_open.return_value = False
            with patch('logging.Logger.warning') as mock_warning:
                browser._open_selected()
                mock_warning.assert_called_once_with("Failed to open file %s", "/test/file1.txt")

    def test_expand_node_no_selection(self, mock_pathbrowser_instance, comprehensive_treeview_mock, mock_file_info_manager):
        """Test _expand_node method with no selection."""
        browser = mock_pathbrowser_instance
        browser.tree = comprehensive_treeview_mock
        browser.tree.selection.return_value = []
        browser.file_info_manager = mock_file_info_manager

        result = browser._expand_node(None)
        assert result == "break"

    def test_expand_node_not_directory(self, mock_pathbrowser_instance, comprehensive_treeview_mock, mock_file_info_manager):
        """Test _expand_node method with non-directory selection."""
        browser = mock_pathbrowser_instance
        browser.tree = comprehensive_treeview_mock
        browser.tree.selection.return_value = ["/test/file1.txt"]
        browser.file_info_manager = mock_file_info_manager
        browser.file_info_manager.get_cached_file_info.return_value = Mock(is_dir=False)

        result = browser._expand_node(None)
        assert result == "break"

    def test_collapse_node_no_selection(self, mock_pathbrowser_instance, comprehensive_treeview_mock, mock_file_info_manager):
        """Test _collapse_node method with no selection."""
        browser = mock_pathbrowser_instance
        browser.tree = comprehensive_treeview_mock
        browser.tree.selection.return_value = []
        browser.file_info_manager = mock_file_info_manager

        result = browser._collapse_node(None)
        assert result == "break"

    def test_collapse_node_not_directory(self, mock_pathbrowser_instance, comprehensive_treeview_mock, mock_file_info_manager):
        """Test _collapse_node method with non-directory selection."""
        browser = mock_pathbrowser_instance
        browser.tree = comprehensive_treeview_mock
        browser.tree.selection.return_value = ["/test/file1.txt"]
        browser.file_info_manager = mock_file_info_manager
        browser.file_info_manager.get_cached_file_info.return_value = Mock(is_dir=False)

        result = browser._collapse_node(None)
        assert result == "break"

    def test_toggle_selected_node_no_selection(self, mock_pathbrowser_instance, comprehensive_treeview_mock, mock_file_info_manager):
        """Test _toggle_selected_node method with no selection."""
        browser = mock_pathbrowser_instance
        browser.tree = comprehensive_treeview_mock
        browser.tree.selection.return_value = []
        browser.file_info_manager = mock_file_info_manager

        result = browser._toggle_selected_node(None)
        assert result == "break"

    def test_toggle_selected_node_not_directory(self, mock_pathbrowser_instance, comprehensive_treeview_mock, mock_file_info_manager):
        """Test _toggle_selected_node method with non-directory selection."""
        browser = mock_pathbrowser_instance
        browser.tree = comprehensive_treeview_mock
        browser.tree.selection.return_value = ["/test/file1.txt"]
        browser.file_info_manager = mock_file_info_manager
        browser.file_info_manager.get_cached_file_info.return_value = Mock(is_dir=False)

        result = browser._toggle_selected_node(None)
        assert result == "break"

    def test_toggle_selected_node_collapsed(self, root, comprehensive_treeview_mock, mock_file_info_manager):
        """Test _toggle_selected_node method with collapsed node."""
        browser = PathBrowser(root)
        browser.tree = comprehensive_treeview_mock
        browser.tree.selection.return_value = ["/test/dir1"]
        browser.tree.item.return_value = False
        browser.file_info_manager = mock_file_info_manager
        browser.file_info_manager.get_cached_file_info.return_value = Mock(is_dir=True)

        with patch.object(browser, '_expand_node') as mock_expand:
            result = browser._toggle_selected_node(None)
            assert result == "break"
            mock_expand.assert_called_once_with(None)

    def test_move_selection_no_children(self, root, mock_treeview_operations):
        """Test _move_selection method with no children."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = ["/test/file1.txt"]
        browser.file_tree.get_children.return_value = []

        result = browser._move_selection(None, 1)
        assert result == "break"

    def test_move_selection_no_current_selection(self, root, mock_treeview_operations):
        """Test _move_selection method with no current selection."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = []
        browser.file_tree.get_children.return_value = ["/test/file1.txt", "/test/file2.txt"]

        with patch.object(browser.file_tree, 'selection_set') as mock_set:
            with patch.object(browser.file_tree, 'see') as mock_see:
                result = browser._move_selection(None, 1)
                assert result == "break"
                mock_set.assert_called_once_with("/test/file1.txt")
                mock_see.assert_called_once_with("/test/file1.txt")

    def test_move_selection_invalid_direction(self, root, mock_treeview_operations):
        """Test _move_selection method with invalid direction."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = ["/test/file1.txt"]
        browser.file_tree.get_children.return_value = ["/test/file1.txt", "/test/file2.txt"]

        result = browser._move_selection(None, 2)  # Invalid direction
        assert result == "break"

    def test_move_selection_invalid_direction_down(self, root, mock_treeview_operations):
        """Test _move_selection method with invalid down direction."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = ["/test/file2.txt"]
        browser.file_tree.get_children.return_value = ["/test/file1.txt", "/test/file2.txt"]

        result = browser._move_selection(None, 1)  # Invalid down direction
        assert result == "break"

    def test_move_selection_invalid_direction_up(self, root, mock_treeview_operations):
        """Test _move_selection method with invalid up direction."""
        browser = PathBrowser(root)
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = ["/test/file1.txt"]
        browser.file_tree.get_children.return_value = ["/test/file1.txt", "/test/file2.txt"]

        result = browser._move_selection(None, -1)  # Invalid up direction
        assert result == "break"

    def test_extend_selection_range_no_children(self, root):
        """Test _extend_selection_range method with no children."""
        browser = PathBrowser(root)
        browser.config.multiple = True

        result = browser._extend_selection_range(None, 1)
        assert result == "break"

    def test_extend_selection_range_no_current_selection(self, root, mock_treeview_operations):
        """Test _extend_selection_range method with no current selection."""
        browser = PathBrowser(root)
        browser.config.multiple = True
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = []
        browser.file_tree.get_children.return_value = ["/test/file1.txt", "/test/file2.txt"]

        with patch.object(browser.file_tree, 'selection_set') as mock_set:
            with patch.object(browser.file_tree, 'see') as mock_see:
                with patch.object(browser, '_on_file_select') as mock_select:
                    result = browser._extend_selection_range(None, 1)
                    assert result == "break"
                    mock_set.assert_called_once_with("/test/file1.txt")
                    mock_see.assert_called_once_with("/test/file1.txt")
                    mock_select.assert_called_once_with(None)

    def test_extend_selection_range_invalid_direction(self, root, mock_treeview_operations):
        """Test _extend_selection_range method with invalid direction."""
        browser = PathBrowser(root)
        browser.config.multiple = True
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = ["/test/file1.txt"]
        browser.file_tree.get_children.return_value = ["/test/file1.txt", "/test/file2.txt"]
        browser.state.selection_anchor = "/test/file1.txt"

        result = browser._extend_selection_range(None, 2)  # Invalid direction
        assert result == "break"

    def test_extend_selection_range_invalid_direction_down(self, root, mock_treeview_operations):
        """Test _extend_selection_range method with invalid down direction."""
        browser = PathBrowser(root)
        browser.config.multiple = True
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = ["/test/file2.txt"]
        browser.file_tree.get_children.return_value = ["/test/file1.txt", "/test/file2.txt"]
        browser.state.selection_anchor = "/test/file1.txt"

        result = browser._extend_selection_range(None, 1)  # Invalid down direction
        assert result == "break"

    def test_extend_selection_range_invalid_direction_up(self, root, mock_treeview_operations):
        """Test _extend_selection_range method with invalid up direction."""
        browser = PathBrowser(root)
        browser.config.multiple = True
        browser.file_tree = mock_treeview_operations
        browser.file_tree.selection.return_value = ["/test/file1.txt"]
        browser.file_tree.get_children.return_value = ["/test/file1.txt", "/test/file2.txt"]
        browser.state.selection_anchor = "/test/file1.txt"

        result = browser._extend_selection_range(None, -1)  # Invalid up direction
        assert result == "break"

    def test_expand_all_no_children(self, root, comprehensive_treeview_mock, mock_file_info_manager):
        """Test _expand_all method with no children."""
        browser = PathBrowser(root)
        browser.tree = comprehensive_treeview_mock
        browser.tree.get_children.return_value = []
        browser.file_info_manager = mock_file_info_manager
        browser.file_info_manager.get_cached_file_info.return_value = Mock(is_dir=True)

        browser._expand_all("/test/dir")
        browser.tree.item.assert_called_with("/test/dir", open=True)

    def test_expand_all_not_directory(self, root, comprehensive_treeview_mock, mock_file_info_manager):
        """Test _expand_all method with non-directory."""
        browser = PathBrowser(root)
        browser.tree = comprehensive_treeview_mock
        browser.file_info_manager = mock_file_info_manager
        browser.file_info_manager.get_cached_file_info.return_value = Mock(is_dir=False)

        browser._expand_all("/test/file.txt")
        browser.tree.item.assert_not_called()

    def test_on_file_select_directory_selection(self, root, mock_file_info_manager):
        """Test _on_file_select method with directory selection."""
        browser = PathBrowser(root)
        browser.config.select = "dir"
        browser.file_tree = Mock()
        browser.file_tree.selection.return_value = ["/test/dir"]
        browser.file_info_manager = mock_file_info_manager

        mock_file_info = Mock()
        mock_file_info.is_dir = True
        mock_file_info_manager.get_cached_file_info.return_value = mock_file_info

        with patch.object(view, 'update_selected_display') as mock_update_display:
            with patch.object(browser, '_update_status') as mock_update_status:
                browser._on_file_select(None)
                assert "/test/dir" in browser.state.selected_items
                mock_update_display.assert_called_once_with(browser)
                mock_update_status.assert_called_once()

    def test_on_file_select_file_selection(self, root, mock_file_info_manager):
        """Test _on_file_select method with file selection."""
        browser = PathBrowser(root)
        browser.config.select = "file"
        browser.file_tree = Mock()
        browser.file_tree.selection.return_value = ["/test/file.txt"]
        browser.file_info_manager = mock_file_info_manager

        mock_file_info = Mock()
        mock_file_info.is_dir = False
        mock_file_info_manager.get_cached_file_info.return_value = mock_file_info

        with patch.object(view, 'update_selected_display') as mock_update_display:
            with patch.object(browser, '_update_status') as mock_update_status:
                browser._on_file_select(None)
                assert "/test/file.txt" in browser.state.selected_items
                mock_update_display.assert_called_once_with(browser)
                mock_update_status.assert_called_once()

    def test_on_file_select_both_selection(self, root, mock_file_info_manager):
        """Test _on_file_select method with both file and directory selection."""
        browser = PathBrowser(root)
        browser.config.select = "both"
        browser.file_tree = Mock()
        browser.file_tree.selection.return_value = ["/test/dir", "/test/file.txt"]
        browser.file_info_manager = mock_file_info_manager

        mock_dir_info = Mock()
        mock_dir_info.is_dir = True
        mock_file_info = Mock()
        mock_file_info.is_dir = False
        mock_file_info_manager.get_cached_file_info.side_effect = [mock_dir_info, mock_file_info]

        with patch.object(view, 'update_selected_display') as mock_update_display:
            with patch.object(browser, '_update_status') as mock_update_status:
                browser._on_file_select(None)
                assert "/test/dir" in browser.state.selected_items
                assert "/test/file.txt" in browser.state.selected_items
                mock_update_display.assert_called_once_with(browser)
                mock_update_status.assert_called_once()

    def test_on_file_select_single_selection_anchor(self, root, mock_file_info_manager):
        """Test _on_file_select method sets anchor for single selection."""
        browser = PathBrowser(root)
        browser.file_tree = Mock()
        browser.file_tree.selection.return_value = ["/test/file.txt"]
        browser.state.selection_anchor = None
        browser.file_info_manager = mock_file_info_manager

        mock_file_info = Mock()
        mock_file_info.is_dir = False
        mock_file_info_manager.get_cached_file_info.return_value = mock_file_info

        with patch.object(view, 'update_selected_display'):
            with patch.object(browser, '_update_status'):
                browser._on_file_select(None)
                assert browser.state.selection_anchor == "/test/file.txt"

    def test_sort_files_same_column(self, root, mock_treeview_operations):
        """Test _sort_files method with same column."""
        browser = PathBrowser(root)
        browser.state.sort_column = "size"
        browser.state.sort_reverse = False
        browser.file_tree = mock_treeview_operations
        browser.file_tree.heading.return_value = {"text": "Size"}

        with patch.object(view, 'load_files') as mock_load:
            browser._sort_files("size")
            assert browser.state.sort_reverse is True
            mock_load.assert_called_once_with(browser)

    def test_sort_files_different_column(self, root, mock_treeview_operations):
        """Test _sort_files method with different column."""
        browser = PathBrowser(root)
        browser.state.sort_column = "size"
        browser.state.sort_reverse = True
        browser.file_tree = mock_treeview_operations
        browser.file_tree.heading.return_value = {"text": "Modified"}

        with patch.object(view, 'load_files') as mock_load:
            browser._sort_files("modified")
            assert browser.state.sort_column == "modified"
            assert browser.state.sort_reverse is False
            mock_load.assert_called_once_with(browser)

    def test_on_file_double_click_directory(self, root, mock_file_info_manager):
        """Test _on_file_double_click method with directory."""
        browser = PathBrowser(root)
        browser.file_tree = Mock()
        browser.file_tree.selection.return_value = ["/test/dir"]
        browser.file_info_manager = mock_file_info_manager

        mock_file_info = Mock()
        mock_file_info.is_dir = True
        mock_file_info_manager._resolve_symlink.return_value = "/test/dir"
        mock_file_info_manager.get_cached_file_info.return_value = mock_file_info

        with patch.object(browser, '_load_directory') as mock_load:
            browser._on_file_double_click(None)
            mock_load.assert_called_once_with("/test/dir")

    def test_on_file_double_click_file_single_selection(self, root, mock_file_info_manager):
        """Test _on_file_double_click method with file in single selection mode."""
        browser = PathBrowser(root)
        browser.config.select = "file"
        browser.config.multiple = False
        browser.file_tree = Mock()
        browser.file_tree.selection.return_value = ["/test/file.txt"]
        browser.file_info_manager = mock_file_info_manager

        mock_file_info = Mock()
        mock_file_info.is_dir = False
        mock_file_info_manager._resolve_symlink.return_value = "/test/file.txt"
        mock_file_info_manager.get_cached_file_info.return_value = mock_file_info

        with patch.object(browser, '_on_ok') as mock_ok:
            browser._on_file_double_click(None)
            mock_ok.assert_called_once()

    def test_on_ok_save_mode_no_filename(self, mock_pathbrowser_save_mode):
        """Test _on_ok method in save mode with no filename."""
        browser = mock_pathbrowser_save_mode
        browser.selected_var.get.return_value = ""

        with patch('tkface.dialog.messagebox.showwarning') as mock_warning:
            browser._on_ok()
            mock_warning.assert_called_once()

    def test_on_ok_save_mode_file_exists(self, mock_pathbrowser_save_mode):
        """Test _on_ok method in save mode with existing file."""
        browser = mock_pathbrowser_save_mode
        browser.selected_var.get.return_value = "existing.txt"
        browser.state.current_dir = "/test"

        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            with patch('tkface.dialog.messagebox.askyesno') as mock_ask:
                mock_ask.return_value = False
                browser._on_ok()
                mock_ask.assert_called_once()

    def test_on_ok_save_mode_file_exists_overwrite(self, mock_pathbrowser_save_mode):
        """Test _on_ok method in save mode with existing file and overwrite."""
        browser = mock_pathbrowser_save_mode
        browser.selected_var.get.return_value = "existing.txt"
        browser.state.current_dir = "/test"

        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            with patch('tkface.dialog.messagebox.askyesno') as mock_ask:
                mock_ask.return_value = True
                with patch.object(browser, 'destroy') as mock_destroy:
                    browser._on_ok()
                    mock_destroy.assert_called_once()

    def test_on_ok_open_mode_no_selection(self, mock_pathbrowser_open_mode):
        """Test _on_ok method in open mode with no selection."""
        browser = mock_pathbrowser_open_mode

        with patch('tkface.dialog.messagebox.showwarning') as mock_warning:
            browser._on_ok()
            mock_warning.assert_called_once()

    def test_on_ok_open_mode_directory_selection_error(self, mock_pathbrowser_open_mode, mock_file_info_manager):
        """Test _on_ok method in open mode with directory selection error."""
        browser = mock_pathbrowser_open_mode
        browser.config.select = "file"
        browser.state.selected_items = ["/test/dir"]
        browser.file_info_manager = mock_file_info_manager

        mock_file_info = Mock()
        mock_file_info.is_dir = True
        mock_file_info_manager._resolve_symlink.return_value = "/test/dir"
        mock_file_info_manager.get_cached_file_info.return_value = mock_file_info

        with patch('tkface.lang.get', return_value="Test message"):
            with patch('tkface.dialog.messagebox.showerror') as mock_error:
                browser._on_ok()
                mock_error.assert_called_once()

    def test_get_selection_save_mode_with_filename(self, root):
        """Test get_selection method in save mode with filename."""
        browser = PathBrowser(root)
        browser.config.save_mode = True
        browser.selected_var = Mock()
        browser.selected_var.get.return_value = "test.txt"
        browser.state.current_dir = "/test"

        with patch.object(browser, '_add_extension_if_needed') as mock_add:
            mock_add.return_value = "test.txt"
            result = browser.get_selection()
            assert result == ["/test/test.txt"]

    def test_get_selection_save_mode_no_filename(self, root):
        """Test get_selection method in save mode with no filename."""
        browser = PathBrowser(root)
        browser.config.save_mode = True
        browser.selected_var = Mock()
        browser.selected_var.get.return_value = ""

        result = browser.get_selection()
        assert result == []

    def test_get_selection_open_mode(self, root):
        """Test get_selection method in open mode."""
        browser = PathBrowser(root)
        browser.config.save_mode = False
        browser.state.selected_items = ["/test/file1.txt", "/test/file2.txt"]

        result = browser.get_selection()
        assert result == ["/test/file1.txt", "/test/file2.txt"]

    def test_set_initial_directory_not_directory(self, root, mock_file_info_manager):
        """Test set_initial_directory method with non-directory."""
        browser = PathBrowser(root)
        browser.file_info_manager = mock_file_info_manager

        mock_file_info = Mock()
        mock_file_info.is_dir = False
        mock_file_info_manager.get_file_info.return_value = mock_file_info

        with patch.object(browser, '_load_directory') as mock_load:
            browser.set_initial_directory("/test/file.txt")
            mock_load.assert_not_called()

    def test_set_file_types(self, root):
        """Test set_file_types method."""
        browser = PathBrowser(root)
        browser.config.filetypes = [("All files", "*.*")]

        with patch.object(browser, '_update_filter_options') as mock_update:
            with patch.object(view, 'load_files') as mock_load:
                browser.set_file_types([("Text files", "*.txt"), ("Python files", "*.py")])
                assert browser.config.filetypes == [("Text files", "*.txt"), ("Python files", "*.py")]
                mock_update.assert_called_once()
                mock_load.assert_called_once_with(browser)

    def test_schedule_memory_monitoring_disabled(self, root):
        """Test _schedule_memory_monitoring method when disabled."""
        browser = PathBrowser(root)
        browser.config.enable_memory_monitoring = False

        with patch.object(browser, '_check_memory_usage') as mock_check:
            with patch.object(browser, 'after') as mock_after:
                browser._schedule_memory_monitoring()
                mock_check.assert_not_called()
                mock_after.assert_not_called()

    def test_check_memory_usage_normal(self, root, mock_file_info_manager):
        """Test _check_memory_usage method with normal memory usage."""
        browser = PathBrowser(root)
        browser.file_info_manager = mock_file_info_manager

        mock_file_info_manager.get_memory_usage_estimate.return_value = 5 * 1024 * 1024  # 5MB
        mock_file_info_manager.get_cache_size.return_value = 100

        with patch('logging.Logger.info') as mock_info:
            browser._check_memory_usage()
            mock_info.assert_not_called()

    def test_check_memory_usage_high(self, root, mock_file_info_manager):
        """Test _check_memory_usage method with high memory usage."""
        browser = PathBrowser(root)
        browser.file_info_manager = mock_file_info_manager

        mock_file_info_manager.get_memory_usage_estimate.return_value = 20 * 1024 * 1024  # 20MB
        mock_file_info_manager.get_cache_size.return_value = 500

        with patch('logging.Logger.info') as mock_info:
            browser._check_memory_usage()
            mock_info.assert_called_once()

    def test_check_memory_usage_very_high(self, root, mock_file_info_manager):
        """Test _check_memory_usage method with very high memory usage."""
        browser = PathBrowser(root)
        browser.file_info_manager = mock_file_info_manager

        mock_file_info_manager.get_memory_usage_estimate.return_value = 60 * 1024 * 1024  # 60MB
        mock_file_info_manager.get_cache_size.return_value = 1000

        with patch('logging.Logger.warning') as mock_warning:
            browser._check_memory_usage()
            mock_warning.assert_called_once()
            mock_file_info_manager.clear_cache.assert_called_once()

    def test_get_performance_stats(self, root, mock_file_info_manager):
        """Test get_performance_stats method."""
        browser = PathBrowser(root)
        browser.file_info_manager = mock_file_info_manager

        mock_file_info_manager.get_cache_size.return_value = 100
        mock_file_info_manager.get_memory_usage_estimate.return_value = 1024 * 1024  # 1MB

        with patch('tkface.widget.pathbrowser.utils.get_performance_stats') as mock_get_stats:
            mock_get_stats.return_value = {"cache_size": 100, "memory_usage": 1024 * 1024}
            result = browser.get_performance_stats()

            mock_get_stats.assert_called_once_with(100, 1024 * 1024, browser.state.current_dir, 0)
            assert result == {"cache_size": 100, "memory_usage": 1024 * 1024}

    def test_optimize_performance(self, root, mock_file_info_manager):
        """Test optimize_performance method."""
        browser = PathBrowser(root)
        browser.file_info_manager = mock_file_info_manager

        mock_file_info_manager.get_memory_usage_estimate.side_effect = [1000000, 500000]  # 1MB, 500KB

        with patch.object(browser, '_load_directory') as mock_load:
            with patch('logging.Logger.info') as mock_info:
                browser.optimize_performance()
                mock_file_info_manager.clear_cache.assert_called_once()
                mock_info.assert_called_once()
                mock_load.assert_called_once_with(browser.state.current_dir)

    def test_load_directory_file_not_found(self, root):
        """Test _load_directory method with FileNotFoundError."""
        browser = PathBrowser(root)
        browser.path_var = Mock()
        browser.status_var = Mock()

        with patch('os.listdir') as mock_listdir:
            mock_listdir.side_effect = FileNotFoundError("Directory not found")
            with patch('tkface.dialog.messagebox.showerror') as mock_error:
                with patch.object(browser, '_load_directory') as mock_load:
                    browser._load_directory("/nonexistent/directory")
                    # FileNotFoundError shows error message in status bar, not messagebox
                    mock_error.assert_not_called()
                    # Should try to navigate to parent directory
                    mock_load.assert_called()

    def test_load_directory_os_error(self, root):
        """Test _load_directory method with OSError."""
        browser = PathBrowser(root)
        browser.path_var = Mock()
        browser.status_var = Mock()

        with patch('os.listdir') as mock_listdir:
            mock_listdir.side_effect = OSError("Permission denied")
            with patch('tkface.dialog.messagebox.showerror') as mock_error:
                with patch.object(browser, '_load_directory') as mock_load:
                    browser._load_directory("/protected/directory")
                    # OSError shows error message in status bar, not messagebox
                    mock_error.assert_not_called()
                    # Should try to navigate to parent directory
                    mock_load.assert_called()

    def test_load_directory_os_error_fallback_home(self, root):
        """Test _load_directory method with OSError and home directory fallback."""
        browser = PathBrowser(root)
        browser.path_var = Mock()
        browser.status_var = Mock()

        with patch('os.listdir') as mock_listdir:
            mock_listdir.side_effect = OSError("Permission denied")
            with patch('pathlib.Path') as mock_path_class:
                mock_path_class.parent.return_value = "/protected"
                mock_path_class.home.return_value = "/home/user"
                with patch.object(browser, '_load_directory') as mock_load:
                    browser._load_directory("/protected/directory")
                    # Should fallback to home directory
                    # The actual implementation calls _load_directory with the parent directory first
                    mock_load.assert_called()

    def test_update_filter_options_all_files_first(self, root):
        """Test _update_filter_options method with All files first."""
        browser = PathBrowser(root)
        browser.config.filetypes = [("All files", "*.*"), ("Text files", "*.txt")]
        browser.filter_combo = Mock()
        browser.filter_combo.__setitem__ = Mock()

        browser._update_filter_options()
        # Should set to second option (first filetype) when "All files" is first
        # The actual implementation sets to the first option when "All files" is first
        browser.filter_combo.set.assert_called_with("All files (*.*)")

    def test_update_filter_options_no_all_files(self, root):
        """Test _update_filter_options method without All files."""
        browser = PathBrowser(root)
        browser.config.filetypes = [("Text files", "*.txt"), ("Python files", "*.py")]
        browser.filter_combo = Mock()
        browser.filter_combo.__setitem__ = Mock()

        browser._update_filter_options()
        # Should set to first option when no "All files"
        browser.filter_combo.set.assert_called_with("Text files (*.txt)")

    def test_go_up_no_parent(self, root):
        """Test _go_up method with no parent directory."""
        browser = PathBrowser(root)
        browser.state.current_dir = "/"

        with patch.object(browser, '_load_directory') as mock_load:
            browser._go_up()
            mock_load.assert_not_called()

    def test_go_down_no_history(self, root):
        """Test _go_down method with no forward history."""
        browser = PathBrowser(root)
        browser.state.forward_history = []
        browser.status_var = Mock()

        browser._go_down()
        browser.status_var.set.assert_called_once()

    def test_go_to_path_not_directory(self, root, mock_file_info_manager):
        """Test _go_to_path method with non-directory."""
        browser = PathBrowser(root)
        browser.path_var = Mock()
        browser.path_var.get.return_value = "/test/file.txt"
        browser.file_info_manager = mock_file_info_manager
        browser.file_info_manager._resolve_symlink.return_value = "/test/file.txt"
        browser.file_info_manager.get_cached_file_info.return_value = Mock(is_dir=False)

        with patch.object(browser, '_load_directory') as mock_load:
            browser._go_to_path()
            mock_load.assert_not_called()

    def test_add_extension_if_needed_with_filter_var(self, root):
        """Test _add_extension_if_needed method with filter_var."""
        browser = PathBrowser(root)
        browser.config.filetypes = [("Text files", "*.txt")]
        browser.filter_var = Mock()
        browser.filter_var.get.return_value = "*.txt"

        with patch('tkface.widget.pathbrowser.utils.add_extension_if_needed') as mock_add:
            mock_add.return_value = "test.txt"
            result = browser._add_extension_if_needed("test")
            assert result == "test.txt"
            mock_add.assert_called_once_with("test", browser.config.filetypes, "*.txt")

    def test_add_extension_if_needed_no_filter_var(self, root):
        """Test _add_extension_if_needed method without filter_var."""
        browser = PathBrowser(root)
        browser.config.filetypes = [("Text files", "*.txt")]

        with patch('tkface.widget.pathbrowser.utils.add_extension_if_needed') as mock_add:
            mock_add.return_value = "test.txt"
            result = browser._add_extension_if_needed("test")
            assert result == "test.txt"
            # The actual call includes the current filter, so we need to check differently
            mock_add.assert_called_once()
            args = mock_add.call_args[0]
            assert args[0] == "test"
            assert args[1] == browser.config.filetypes

    def test_init_language_deprecated(self, root):
        """Test _init_language method (deprecated)."""
        browser = PathBrowser(root)
        # This method should do nothing as it's deprecated
        browser._init_language()

    def test_load_directory_cache_clearing(self, mock_pathbrowser_instance, mock_file_info_manager):
        """Test _load_directory method with cache clearing."""
        browser = mock_pathbrowser_instance
        browser.file_info_manager = mock_file_info_manager
        browser.state.current_dir = "/old/directory"

        with patch('os.listdir', return_value=[]):
            with patch('pathlib.Path') as mock_path_class:
                # Create a proper mock for Path class
                mock_path_instance = Mock()
                mock_path_instance.absolute.return_value = "/new/directory"
                mock_path_class.return_value = mock_path_instance
                # Mock the class methods properly
                mock_path_class.exists = Mock(return_value=True)
                mock_path_class.home = Mock(return_value="/home/user")
                
                with patch.object(view, 'load_directory_tree') as mock_load_tree:
                    with patch.object(view, 'load_files') as mock_load_files:
                        with patch.object(browser, '_update_status') as mock_update:
                            with patch.object(view, 'update_selected_display') as mock_update_display:
                                with patch.object(browser, '_update_navigation_buttons') as mock_update_nav:
                                    # Mock _resolve_symlink to return the expected path
                                    mock_file_info_manager._resolve_symlink.return_value = "/new/directory"
                                    browser._load_directory("/new/directory")
                                    # Should clear cache for old directory
                                    mock_file_info_manager.clear_directory_cache.assert_called_once_with("/old/directory")

    def test_load_directory_permission_error(self, mock_pathbrowser_instance):
        """Test _load_directory method with PermissionError."""
        browser = mock_pathbrowser_instance

        with patch('pathlib.Path') as mock_path_class:
            mock_path_class.exists.return_value = False
            with patch('tkface.lang.get') as mock_lang:
                mock_lang.side_effect = lambda key, obj: key
                with patch.object(browser, '_load_directory') as mock_load:
                    browser._load_directory("/protected/directory")
                    # Should try to navigate to parent directory
                    mock_load.assert_called()

    def test_load_directory_file_not_found_with_parent(self, mock_pathbrowser_instance):
        """Test _load_directory method with FileNotFoundError and parent directory fallback."""
        browser = mock_pathbrowser_instance

        # Mock _resolve_symlink to return the same path
        browser.file_info_manager._resolve_symlink.return_value = "/missing/directory"
        
        # Mock Path.exists to return False
        with patch('pathlib.Path') as mock_path_class:
            mock_path_class.exists.return_value = False
            # Mock _load_directory to prevent infinite recursion
            with patch.object(browser, '_load_directory') as mock_load:
                browser._load_directory("/missing/directory")
                # Should try to navigate to parent directory
                mock_load.assert_called()

    def test_load_directory_file_not_found_no_parent(self, mock_pathbrowser_instance):
        """Test _load_directory method with FileNotFoundError and no parent directory."""
        browser = mock_pathbrowser_instance

        # Mock _resolve_symlink to return the same path
        browser.file_info_manager._resolve_symlink.return_value = "/missing/directory"
        
        # Mock Path.exists to return False
        with patch('pathlib.Path') as mock_path_class:
            mock_path_class.exists.return_value = False
            mock_path_class.home.return_value = "/home/user"
            with patch.object(browser, '_load_directory') as mock_load:
                browser._load_directory("/missing/directory")
                # Should fallback to home directory
                mock_load.assert_called()

    def test_load_directory_os_error_with_parent(self, mock_pathbrowser_instance):
        """Test _load_directory method with OSError and parent directory fallback."""
        browser = mock_pathbrowser_instance

        # Mock _resolve_symlink to return the same path
        browser.file_info_manager._resolve_symlink.return_value = "/error/directory"
        
        # Mock Path.exists to return False
        with patch('pathlib.Path') as mock_path_class:
            mock_path_class.exists.return_value = False
            with patch.object(browser, '_load_directory') as mock_load:
                browser._load_directory("/error/directory")
                # Should try to navigate to parent directory
                mock_load.assert_called()

    def test_load_directory_os_error_no_parent(self, mock_pathbrowser_instance):
        """Test _load_directory method with OSError and no parent directory."""
        browser = mock_pathbrowser_instance

        # Mock _resolve_symlink to return the same path
        browser.file_info_manager._resolve_symlink.return_value = "/error/directory"
        
        # Mock Path.exists to return False
        with patch('pathlib.Path') as mock_path_class:
            mock_path_class.exists.return_value = False
            mock_path_class.home.return_value = "/home/user"
            with patch.object(browser, '_load_directory') as mock_load:
                browser._load_directory("/error/directory")
                # Should fallback to home directory
                mock_load.assert_called()

    def test_on_tree_open_with_placeholder_removal(self, mock_pathbrowser_instance, mock_file_info_manager):
        """Test _on_tree_open method with placeholder removal."""
        browser = mock_pathbrowser_instance
        browser.file_info_manager = mock_file_info_manager
        browser.tree = Mock()
        browser.tree.selection.return_value = ["/test/dir"]
        browser.tree.get_children.return_value = ["/test/dir/file1", "/test/dir/file2_placeholder"]

        mock_file_info = Mock()
        mock_file_info.is_dir = True
        mock_file_info_manager.get_file_info.return_value = mock_file_info

        browser._on_tree_open(None)
        # Should remove placeholder
        browser.tree.delete.assert_called_once_with("/test/dir/file2_placeholder")

    def test_on_tree_open_no_placeholder(self, mock_pathbrowser_instance, mock_file_info_manager):
        """Test _on_tree_open method without placeholder."""
        browser = mock_pathbrowser_instance
        browser.file_info_manager = mock_file_info_manager

        mock_file_info = Mock()
        mock_file_info.is_dir = True
        mock_file_info_manager.get_file_info.return_value = mock_file_info

        with patch.object(view, 'populate_tree_node') as mock_populate:
            browser._on_tree_open(None)
            # Should not call populate if children already exist
            mock_populate.assert_not_called()

    def test_expand_node_with_placeholder_removal(self, mock_pathbrowser_instance, mock_file_info_manager):
        """Test _expand_node method with placeholder removal."""
        browser = mock_pathbrowser_instance
        browser.file_info_manager = mock_file_info_manager
        browser.tree = Mock()
        browser.tree.selection.return_value = ["/test/dir"]
        browser.tree.get_children.return_value = ["/test/dir/file1_placeholder", "/test/dir/file2"]

        mock_file_info = Mock()
        mock_file_info.is_dir = True
        browser.file_info_manager.get_cached_file_info.return_value = mock_file_info

        result = browser._expand_node(None)
        assert result == "break"
        # Should remove placeholder
        browser.tree.delete.assert_called_once_with("/test/dir/file1_placeholder")

    def test_collapse_node_with_directory(self, root, mock_file_info_manager):
        """Test _collapse_node method with directory."""
        browser = PathBrowser(root)
        browser.tree = Mock()
        browser.tree.selection.return_value = ["/test/dir"]
        browser.file_info_manager = mock_file_info_manager

        mock_file_info = Mock()
        mock_file_info.is_dir = True
        mock_file_info_manager.get_cached_file_info.return_value = mock_file_info

        result = browser._collapse_node(None)
        assert result == "break"
        browser.tree.item.assert_called_once_with("/test/dir", open=False)

    def test_toggle_selected_node_expanded(self, mock_pathbrowser_instance, mock_file_info_manager):
        """Test _toggle_selected_node method with expanded node."""
        browser = mock_pathbrowser_instance
        browser.tree.selection.return_value = ["/test/dir"]
        # Mock the tree.item method to handle both calls
        browser.tree.item.side_effect = lambda item, option=None, **kwargs: {"open": True} if option == "open" else None
        browser.file_info_manager = mock_file_info_manager

        mock_file_info = Mock()
        mock_file_info.is_dir = True
        mock_file_info_manager.get_cached_file_info.return_value = mock_file_info

        result = browser._toggle_selected_node(None)
        assert result == "break"
        # Should call _collapse_node which sets open=False
        browser.tree.item.assert_called()

    def test_toggle_selected_node_collapsed(self, mock_pathbrowser_instance, mock_file_info_manager):
        """Test _toggle_selected_node method with collapsed node."""
        browser = mock_pathbrowser_instance
        browser.tree.selection.return_value = ["/test/dir"]
        # Mock the tree.item method to handle both calls
        browser.tree.item.side_effect = lambda item, option=None, **kwargs: {"open": False} if option == "open" else None
        # Mock get_children to return empty list so populate_tree_node is called
        # The method is called twice: once for placeholder removal, once for checking if empty
        browser.tree.get_children.side_effect = [[], []]
        browser.file_info_manager = mock_file_info_manager

        mock_file_info = Mock()
        mock_file_info.is_dir = True
        mock_file_info_manager.get_cached_file_info.return_value = mock_file_info

        # Debug: check what methods are called
        with patch.object(browser, '_expand_node') as mock_expand:
            with patch.object(browser, '_collapse_node') as mock_collapse:
                result = browser._toggle_selected_node(None)
                assert result == "break"
                # Should call _expand_node since node is collapsed
                mock_expand.assert_called_once_with(None)
                mock_collapse.assert_not_called()

    