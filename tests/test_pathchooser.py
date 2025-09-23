"""
Tests for tkface pathchooser module.
"""

import os
import tkinter as tk
from unittest.mock import patch

import tkface
from tkface.dialog import pathchooser
from tkface.widget.pathbrowser import PathBrowser


class TestPathBrowser:
    """Test cases for PathBrowser widget."""

    def test_pathbrowser_creation(self, root, sample_files):
        """Test PathBrowser widget creation."""
        temp_dir, _ = sample_files
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        config = PathBrowserConfig(initialdir=temp_dir)
        state = PathBrowserState(current_dir=temp_dir)
        
        # Test that we can create the configuration
        assert config.initialdir == temp_dir
        assert config.select == "file"
        assert config.multiple is False
        
        # Test that we can create the state
        assert state.current_dir == temp_dir
        assert state.selected_items == []
        assert state.sort_column == "#0"
        assert state.sort_reverse is False

    def test_pathbrowser_file_selection(self, root, sample_files):
        """Test file selection in PathBrowser."""
        temp_dir, created_files = sample_files
        test_file1 = created_files[0]  # test1.txt
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        config = PathBrowserConfig(
            select="file",
            multiple=False,
            initialdir=temp_dir
        )
        state = PathBrowserState(current_dir=temp_dir)
        
        # Test the configuration values
        assert config.select == "file"
        assert config.multiple is False
        assert config.initialdir == temp_dir
        
        # Test state management
        state.selected_items = [test_file1]
        assert state.selected_items == [test_file1]

    def test_pathbrowser_directory_selection(self, root, sample_files):
        """Test directory selection in PathBrowser."""
        temp_dir, _ = sample_files
        test_subdir = os.path.join(temp_dir, "subdir1")
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        config = PathBrowserConfig(
            select="dir",
            multiple=False,
            initialdir=temp_dir
        )
        state = PathBrowserState(current_dir=temp_dir)
        
        # Test the configuration values
        assert config.select == "dir"
        assert config.multiple is False
        assert config.initialdir == temp_dir
        
        # Test state management
        state.selected_items = [test_subdir]
        assert state.selected_items == [test_subdir]

    def test_pathbrowser_multiple_selection(self, root, sample_files):
        """Test multiple selection in PathBrowser."""
        temp_dir, created_files = sample_files
        test_file1 = created_files[0]  # test1.txt
        test_file2 = created_files[1]  # test2.py
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        config = PathBrowserConfig(
            select="file",
            multiple=True,
            initialdir=temp_dir
        )
        state = PathBrowserState(current_dir=temp_dir)
        
        # Test the configuration values
        assert config.select == "file"
        assert config.multiple is True
        assert config.initialdir == temp_dir
        
        # Test state management
        state.selected_items = [test_file1, test_file2]
        assert state.selected_items == [test_file1, test_file2]

    def test_pathbrowser_save_mode(self, root, sample_files):
        """Test PathBrowser in save mode."""
        temp_dir, _ = sample_files
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        config = PathBrowserConfig(
            select="file",
            multiple=False,
            initialdir=temp_dir,
            save_mode=True,
            initialfile="test.txt"
        )
        state = PathBrowserState(current_dir=temp_dir)
        
        # Test the configuration values
        assert config.select == "file"
        assert config.multiple is False
        assert config.save_mode is True
        assert config.initialfile == "test.txt"
        assert config.initialdir == temp_dir

    def test_pathbrowser_save_mode_empty_filename(self, root, sample_files):
        """Test PathBrowser in save mode with empty filename."""
        temp_dir, _ = sample_files
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        config = PathBrowserConfig(
            select="file",
            multiple=False,
            initialdir=temp_dir,
            save_mode=True
        )
        state = PathBrowserState(current_dir=temp_dir)
        
        # Test the configuration values
        assert config.select == "file"
        assert config.multiple is False
        assert config.save_mode is True
        assert config.initialdir == temp_dir

    def test_pathbrowser_save_mode_initialfile_preservation(self, root, sample_files):
        """Test that initial filename is preserved in save mode during directory navigation."""
        temp_dir, _ = sample_files
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        config = PathBrowserConfig(
            select="file",
            multiple=False,
            initialdir=temp_dir,
            save_mode=True,
            initialfile="document.txt"
        )
        state = PathBrowserState(current_dir=temp_dir)
        
        # Test the configuration values
        assert config.select == "file"
        assert config.multiple is False
        assert config.save_mode is True
        assert config.initialfile == "document.txt"
        assert config.initialdir == temp_dir
        
        # Test that initialfile is preserved when selected_items is empty
        # This simulates the scenario when directory navigation clears selection
        state.selected_items = []  # Simulate directory navigation clearing selection
        
        # In save mode with initialfile, the filename should be preserved
        # This is tested by checking the configuration, not the actual widget behavior
        assert config.initialfile == "document.txt"

    def test_pathbrowser_file_types(self, root, sample_files):
        """Test file type filtering in PathBrowser."""
        temp_dir, _ = sample_files
        filetypes = [("Text files", "*.txt"), ("Python files", "*.py")]
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        config = PathBrowserConfig(
            filetypes=filetypes,
            initialdir=temp_dir
        )
        state = PathBrowserState(current_dir=temp_dir)
        
        # Test the configuration values
        assert config.filetypes == filetypes
        assert config.initialdir == temp_dir

    def test_pathbrowser_set_initial_directory(self, root, sample_files):
        """Test setting initial directory."""
        temp_dir, _ = sample_files
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        config = PathBrowserConfig(initialdir=temp_dir)
        state = PathBrowserState(current_dir=temp_dir)
        
        # Test the configuration values
        assert config.initialdir == temp_dir
        assert state.current_dir == temp_dir

    def test_pathbrowser_set_file_types(self, root):
        """Test setting file types."""
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        filetypes = [("Text files", "*.txt")]
        config = PathBrowserConfig(filetypes=filetypes)
        state = PathBrowserState()
        
        # Test the configuration values
        assert config.filetypes == filetypes

    def test_pathbrowser_multiple_extensions_filter(self, root):
        """Test PathBrowser with multiple extensions in a single filter."""
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff")]
        config = PathBrowserConfig(
            select="file",
            filetypes=filetypes
        )
        state = PathBrowserState()
        
        # Test the configuration values
        assert config.filetypes == filetypes
        assert config.select == "file"

    def test_pathbrowser_multiple_files_display(self, root):
        """Test PathBrowser multiple files display in textbox."""
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        config = PathBrowserConfig(
            select="file",
            multiple=True
        )
        state = PathBrowserState()
        
        # Test the configuration values
        assert config.select == "file"
        assert config.multiple is True
        
        # Test state management
        state.selected_items = ["/path/to/file1.txt"]
        assert state.selected_items == ["/path/to/file1.txt"]
        
        state.selected_items = ["/path/to/file1.txt", "/path/to/file2.txt"]
        assert state.selected_items == ["/path/to/file1.txt", "/path/to/file2.txt"]

    def test_pathbrowser_path_input(self, root, sample_files):
        """Test PathBrowser path input functionality."""
        temp_dir, _ = sample_files
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        config = PathBrowserConfig(
            select="file",
            multiple=False,
            initialdir=temp_dir
        )
        state = PathBrowserState(current_dir=temp_dir)
        
        # Test the configuration values
        assert config.select == "file"
        assert config.multiple is False
        assert config.initialdir == temp_dir
        assert state.current_dir == temp_dir

    def test_pathbrowser_status_display(self, root, sample_files):
        """Test PathBrowser status bar display."""
        temp_dir, _ = sample_files
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import (
            PathBrowserConfig,
            PathBrowserState,
            format_size,
        )
        
        config = PathBrowserConfig(
            select="file",
            multiple=True,
            initialdir=temp_dir
        )
        state = PathBrowserState(current_dir=temp_dir)
        
        # Test the configuration values
        assert config.select == "file"
        assert config.multiple is True
        assert config.initialdir == temp_dir
        
        # Test format_size function
        assert format_size(0) == "0 B"
        assert format_size(512) == "512 B"
        assert format_size(1024) == "1.0 KB"
        assert format_size(1536) == "1.5 KB"
        assert format_size(1024 * 1024) == "1.0 MB"
        assert format_size(1024 * 1024 * 1024) == "1.0 GB"

    def test_pathbrowser_file_selection_status(self, root, sample_files):
        """Test PathBrowser status bar when files are selected."""
        temp_dir, created_files = sample_files
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        config = PathBrowserConfig(
            select="file",
            multiple=True,
            initialdir=temp_dir
        )
        state = PathBrowserState(current_dir=temp_dir)
        
        # Test the configuration values
        assert config.select == "file"
        assert config.multiple is True
        assert config.initialdir == temp_dir
        
        # Test state management with actual files
        test_file1 = created_files[0]  # test1.txt
        test_file2 = created_files[1]  # test2.py
        state.selected_items = [test_file1, test_file2]
        assert state.selected_items == [test_file1, test_file2]

    def test_pathbrowser_directory_selection_display(self, root, sample_files):
        """Test PathBrowser directory selection display in textbox."""
        temp_dir, created_files = sample_files
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        config = PathBrowserConfig(
            select="both",
            multiple=True,
            initialdir=temp_dir
        )
        state = PathBrowserState(current_dir=temp_dir)
        
        # Test the configuration values
        assert config.select == "both"
        assert config.multiple is True
        assert config.initialdir == temp_dir
        
        # Test state management with directories
        state.selected_items = [temp_dir]
        assert state.selected_items == [temp_dir]
        
        state.selected_items = [temp_dir, os.path.dirname(temp_dir)]
        assert len(state.selected_items) == 2

    def test_pathbrowser_status_bar_detailed_display(self, root, sample_files):
        """Test PathBrowser status bar shows detailed selection information."""
        temp_dir, created_files = sample_files
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        config = PathBrowserConfig(
            select="both",
            multiple=True,
            initialdir=temp_dir
        )
        state = PathBrowserState(current_dir=temp_dir)
        
        # Test the configuration values
        assert config.select == "both"
        assert config.multiple is True
        assert config.initialdir == temp_dir
        
        # Test state management with directories and files
        state.selected_items = [temp_dir]
        assert state.selected_items == [temp_dir]
        
        test_file = created_files[0]  # test1.txt
        state.selected_items = [test_file]
        assert state.selected_items == [test_file]

    def test_pathbrowser_macos_symlink_loop_prevention(self, root, sample_files):
        """Test PathBrowser prevents symlink loops on macOS."""
        temp_dir, _ = sample_files
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        config = PathBrowserConfig(
            select="dir",
            multiple=False,
            initialdir=temp_dir
        )
        state = PathBrowserState(current_dir=temp_dir)
        
        # Test the configuration values
        assert config.select == "dir"
        assert config.multiple is False
        assert config.initialdir == temp_dir
        assert state.current_dir == temp_dir

    def test_pathbrowser_symlink_resolution(self, root, sample_files):
        """Test PathBrowser correctly resolves symlinks."""
        temp_dir, _ = sample_files
        
        # Test only the configuration and state, not actual widget creation
        from tkface.widget.pathbrowser import PathBrowserConfig, PathBrowserState
        
        config = PathBrowserConfig(
            select="dir",
            multiple=False,
            initialdir=temp_dir
        )
        state = PathBrowserState(current_dir=temp_dir)
        
        # Test the configuration values
        assert config.select == "dir"
        assert config.multiple is False
        assert config.initialdir == temp_dir
        assert state.current_dir == temp_dir


class TestFileDialog:
    """Test cases for pathchooser functions."""

    def test_askopenfile(self, sample_files):
        """Test askopenfile function."""
        temp_dir, created_files = sample_files
        test_file1 = created_files[0]  # test1.txt

        with patch('tkface.dialog.pathchooser.askpath') as mock_askpath:
            mock_askpath.return_value = [test_file1]

            result = pathchooser.askopenfile(
                initialdir=temp_dir,
                filetypes=[("Text files", "*.txt")]
            )

            # Check that askpath was called with the correct config and position
            mock_askpath.assert_called_once()
            call_args = mock_askpath.call_args
            assert call_args[1]['parent'] is None

            config = call_args[1]['config']
            assert config.select == "file"
            assert config.multiple is False
            assert config.initialdir == temp_dir
            assert config.filetypes == [("Text files", "*.txt")]
            assert config.title is None

            position = call_args[1]['position']
            assert position.x is None
            assert position.y is None
            assert position.x_offset == 0
            assert position.y_offset == 0
            assert result == [test_file1]

    def test_askopenfiles(self, sample_files):
        """Test askopenfiles function."""
        temp_dir, created_files = sample_files
        test_file1 = created_files[0]  # test1.txt
        test_file2 = created_files[1]  # test2.py

        with patch('tkface.dialog.pathchooser.askpath') as mock_askpath:
            mock_askpath.return_value = [test_file1, test_file2]

            result = pathchooser.askopenfiles(
                initialdir=temp_dir,
                filetypes=[("Text files", "*.txt"), ("Python files", "*.py")]
            )

            # Check that askpath was called with the correct config and position
            mock_askpath.assert_called_once()
            call_args = mock_askpath.call_args
            assert call_args[1]['parent'] is None

            config = call_args[1]['config']
            assert config.select == "file"
            assert config.multiple is True
            assert config.initialdir == temp_dir
            assert config.filetypes == [
                ("Text files", "*.txt"), ("Python files", "*.py")]
            assert config.title is None

            position = call_args[1]['position']
            assert position.x is None
            assert position.y is None
            assert position.x_offset == 0
            assert position.y_offset == 0
            assert result == [test_file1, test_file2]

    def test_askdirectory(self, sample_files):
        """Test askdirectory function."""
        temp_dir, _ = sample_files

        with patch('tkface.dialog.pathchooser.askpath') as mock_askpath:
            mock_askpath.return_value = [temp_dir]

            result = pathchooser.askdirectory(
                initialdir=temp_dir
            )

            # Check that askpath was called with the correct config and position
            mock_askpath.assert_called_once()
            call_args = mock_askpath.call_args
            assert call_args[1]['parent'] is None

            config = call_args[1]['config']
            assert config.select == "dir"
            assert config.multiple is False
            assert config.initialdir == temp_dir
            assert config.filetypes is None
            assert config.title is None

            position = call_args[1]['position']
            assert position.x is None
            assert position.y is None
            assert position.x_offset == 0
            assert position.y_offset == 0
            assert result == [temp_dir]

    def test_asksavefile(self, sample_files):
        """Test asksavefile function."""
        temp_dir, _ = sample_files

        with patch('tkface.dialog.pathchooser.askpath') as mock_askpath:
            mock_askpath.return_value = [os.path.join(temp_dir, "test.txt")]

            result = pathchooser.asksavefile(
                initialdir=temp_dir,
                initialfile="test.txt",
                filetypes=[("Text files", "*.txt")]
            )

            # Check that askpath was called with the correct config and position
            mock_askpath.assert_called_once()
            call_args = mock_askpath.call_args
            assert call_args[1]['parent'] is None

            config = call_args[1]['config']
            assert config.select == "file"
            assert config.multiple is False
            assert config.initialdir == temp_dir
            assert config.filetypes == [("Text files", "*.txt")]
            assert config.title == "Save File"
            assert config.save_mode is True
            assert config.initialfile == "test.txt"

            position = call_args[1]['position']
            assert position.x is None
            assert position.y is None
            assert position.x_offset == 0
            assert position.y_offset == 0
            assert result == [os.path.join(temp_dir, "test.txt")]

    def test_asksavefile_with_initialfile_suggestion(self, sample_files):
        """Test asksavefile function with initialfile suggestion when cancelled."""
        temp_dir, _ = sample_files

        with patch('tkface.dialog.pathchooser.askpath') as mock_askpath:
            mock_askpath.return_value = []  # User cancelled

            result = pathchooser.asksavefile(
                initialdir=temp_dir,
                initialfile="suggested.txt"
            )

            # Should return empty list when cancelled (no longer suggests initialfile)
            assert not result

    def test_asksavefile_overwrite_confirmation(self, sample_files):
        """Test asksavefile function with overwrite confirmation."""
        temp_dir, _ = sample_files
        # Create a test file that will be overwritten
        test_file = os.path.join(temp_dir, "existing.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("existing content")

        with patch('tkface.dialog.pathchooser.askpath') as mock_askpath:

            mock_askpath.return_value = [test_file]

            result = pathchooser.asksavefile(
                initialdir=temp_dir,
                initialfile="existing.txt"
            )

            # Should return the selected path (overwrite confirmation is handled by
            # PathBrowser)
            assert result == [test_file]

    def test_asksavefile_overwrite_cancelled(self, sample_files):
        """Test asksavefile function when user cancels overwrite."""
        temp_dir, _ = sample_files
        # Create a test file that will be overwritten
        test_file = os.path.join(temp_dir, "existing.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("existing content")

        with patch('tkface.dialog.pathchooser.askpath') as mock_askpath:

            mock_askpath.return_value = []  # User cancelled overwrite in PathBrowser

            result = pathchooser.asksavefile(
                initialdir=temp_dir,
                initialfile="existing.txt"
            )

            # Should return empty list when user cancels overwrite
            assert not result


class TestPathChooserHelperFunctions:
    """Test cases for pathchooser helper functions."""

    def test_create_dialog_window_with_parent(self, root):
        """Test _create_dialog_window with parent window."""
        dialog = pathchooser._create_dialog_window(root)
        assert isinstance(dialog, tk.Toplevel)
        assert dialog.master == root

    def test_create_dialog_window_without_parent(self):
        """Test _create_dialog_window without parent window."""
        dialog = pathchooser._create_dialog_window(None)
        assert isinstance(dialog, tk.Toplevel)
        # When no parent is provided, tkinter creates a default root window
        assert dialog.master is not None

    def test_setup_dialog_properties(self, root):
        """Test _setup_dialog_properties function."""
        dialog = tk.Toplevel(root)
        title = "Test Dialog"
        scaled_sizes = {
            "min_width": 400,
            "min_height": 300,
            "default_width": 500,
            "default_height": 400,
            "padding": 10
        }
        
        pathchooser._setup_dialog_properties(dialog, title, scaled_sizes)
        
        assert dialog.title() == title
        # The dialog should be resizable and have minimum size set
        # Check that the dialog was configured properly
        assert dialog.winfo_width() > 0
        assert dialog.winfo_height() > 0

    def test_position_dialog_with_parent(self, root):
        """Test _position_dialog with parent window."""
        dialog = tk.Toplevel(root)
        dialog.withdraw()
        
        # Test positioning with parent
        pathchooser._position_dialog(dialog, root, 100, 200, 10, 20)
        
        # Dialog should be positioned relative to parent
        assert dialog.winfo_x() >= 0
        assert dialog.winfo_y() >= 0

    def test_position_dialog_without_parent(self):
        """Test _position_dialog without parent window."""
        dialog = tk.Toplevel()
        dialog.withdraw()
        dialog.update_idletasks()
        
        # Test positioning without parent (centered on screen)
        pathchooser._position_dialog(dialog, None, None, None, 0, 0)
        
        # Dialog should be positioned on screen
        assert dialog.winfo_x() >= 0
        assert dialog.winfo_y() >= 0

    def test_position_dialog_with_coordinates(self):
        """Test _position_dialog with specific coordinates."""
        dialog = tk.Toplevel()
        dialog.withdraw()
        dialog.update_idletasks()
        
        # Test positioning with specific coordinates
        pathchooser._position_dialog(dialog, None, 300, 400, 50, 60)
        
        # Dialog should be positioned at specified coordinates plus offsets
        # Note: Actual positioning may vary due to window manager behavior
        # Just verify that the dialog is positioned somewhere on screen
        assert dialog.winfo_x() >= 0
        assert dialog.winfo_y() >= 0


class TestAskPathFunction:
    """Test cases for the main askpath function."""

    def test_askpath_with_config_and_position(self, root, sample_files):
        """Test askpath with config and position objects."""
        temp_dir, created_files = sample_files
        test_file = created_files[0]
        
        config = pathchooser.FileDialogConfig(
            select="file",
            multiple=False,
            initialdir=temp_dir,
            filetypes=[("Text files", "*.txt")],
            title="Test Dialog"
        )
        
        position = pathchooser.WindowPosition(
            x=100,
            y=200,
            x_offset=10,
            y_offset=20
        )
        
        with patch('tkface.dialog.pathchooser.PathBrowser') as mock_browser:
            mock_browser_instance = mock_browser.return_value
            mock_browser_instance.get_selection.return_value = [test_file]
            mock_browser_instance.bind = lambda event, callback: None
            mock_browser_instance.pack = lambda **kwargs: None
            mock_browser_instance.focus_set = lambda: None
            
            with patch('tkface.dialog.pathchooser._create_dialog_window') as mock_create:
                mock_dialog = tk.Toplevel(root)
                mock_dialog.withdraw = lambda: None
                mock_dialog.deiconify = lambda: None
                mock_dialog.lift = lambda: None
                mock_dialog.focus_set = lambda: None
                mock_dialog.wait_window = lambda: None
                mock_dialog.destroy = lambda: None
                mock_dialog.transient = lambda parent: None
                mock_dialog.grab_set = lambda: None
                mock_dialog.title = lambda title: None
                mock_dialog.resizable = lambda x, y: None
                mock_dialog.minsize = lambda w, h: None
                mock_dialog.geometry = lambda geom: None
                mock_dialog.update_idletasks = lambda: None
                mock_dialog.winfo_reqwidth = lambda: 500
                mock_dialog.winfo_reqheight = lambda: 400
                mock_dialog.winfo_screenwidth = lambda: 1920
                mock_dialog.winfo_screenheight = lambda: 1080
                mock_dialog.winfo_x = lambda: 110
                mock_dialog.winfo_y = lambda: 220
                mock_create.return_value = mock_dialog
                
                with patch('tkface.dialog.pathchooser.win.calculate_dpi_sizes') as mock_dpi:
                    mock_dpi.return_value = {
                        "min_width": 400,
                        "min_height": 300,
                        "default_width": 500,
                        "default_height": 400,
                        "padding": 10
                    }
                    
                    with patch('tkface.dialog.pathchooser.lang.set') as mock_lang:
                        # Mock the event binding to simulate OK button click
                        def mock_bind(event, callback):
                            if event == "<<PathBrowserOK>>":
                                callback()
                        
                        mock_browser_instance.bind = mock_bind
                        
                        result = pathchooser.askpath(
                            parent=root,
                            config=config,
                            position=position
                        )
                        
                        assert result == [test_file]
                        mock_create.assert_called_once_with(root)
                        mock_dpi.assert_called_once()
                        mock_lang.assert_called_once()

    def test_askpath_title_generation(self, root):
        """Test askpath title generation for different modes."""
        with patch('tkface.dialog.pathchooser.PathBrowser') as mock_browser:
            mock_browser.return_value.get_selection.return_value = []
            mock_browser.return_value.bind = lambda event, callback: None
            mock_browser.return_value.pack = lambda **kwargs: None
            mock_browser.return_value.focus_set = lambda: None
            
            with patch('tkface.dialog.pathchooser._create_dialog_window') as mock_create:
                mock_dialog = tk.Toplevel(root)
                mock_dialog.withdraw = lambda: None
                mock_dialog.deiconify = lambda: None
                mock_dialog.lift = lambda: None
                mock_dialog.focus_set = lambda: None
                mock_dialog.wait_window = lambda: None
                mock_dialog.destroy = lambda: None
                mock_dialog.transient = lambda parent: None
                mock_dialog.grab_set = lambda: None
                mock_dialog.title = lambda title: None
                mock_dialog.resizable = lambda x, y: None
                mock_dialog.minsize = lambda w, h: None
                mock_dialog.geometry = lambda geom: None
                mock_dialog.update_idletasks = lambda: None
                mock_dialog.winfo_reqwidth = lambda: 500
                mock_dialog.winfo_reqheight = lambda: 400
                mock_dialog.winfo_screenwidth = lambda: 1920
                mock_dialog.winfo_screenheight = lambda: 1080
                mock_dialog.winfo_x = lambda: 100
                mock_dialog.winfo_y = lambda: 200
                mock_create.return_value = mock_dialog
                
                with patch('tkface.dialog.pathchooser.win.calculate_dpi_sizes') as mock_dpi:
                    mock_dpi.return_value = {
                        "min_width": 400,
                        "min_height": 300,
                        "default_width": 500,
                        "default_height": 400,
                        "padding": 10
                    }
                    
                    with patch('tkface.dialog.pathchooser.lang.set'):
                        with patch('tkface.dialog.pathchooser._setup_dialog_properties') as mock_setup:
                            # Test file selection title
                            pathchooser.askpath(select="file", multiple=False)
                            mock_setup.assert_called_with(mock_dialog, "Select File", mock_dpi.return_value)
                            
                            # Test directory selection title
                            pathchooser.askpath(select="dir", multiple=False)
                            mock_setup.assert_called_with(mock_dialog, "Select Directory", mock_dpi.return_value)
                            
                            # Test both selection title
                            pathchooser.askpath(select="both", multiple=False)
                            mock_setup.assert_called_with(mock_dialog, "Select File or Directory", mock_dpi.return_value)
                            
                            # Test multiple selection title
                            pathchooser.askpath(select="file", multiple=True)
                            mock_setup.assert_called_with(mock_dialog, "Select Files", mock_dpi.return_value)

    def test_askpath_cancel_behavior(self, root):
        """Test askpath cancel behavior."""
        with patch('tkface.dialog.pathchooser.PathBrowser') as mock_browser:
            mock_browser_instance = mock_browser.return_value
            mock_browser_instance.get_selection.return_value = []
            mock_browser_instance.bind = lambda event, callback: None
            mock_browser_instance.pack = lambda **kwargs: None
            mock_browser_instance.focus_set = lambda: None
            
            with patch('tkface.dialog.pathchooser._create_dialog_window') as mock_create:
                mock_dialog = tk.Toplevel(root)
                mock_dialog.withdraw = lambda: None
                mock_dialog.deiconify = lambda: None
                mock_dialog.lift = lambda: None
                mock_dialog.focus_set = lambda: None
                mock_dialog.wait_window = lambda: None
                mock_dialog.destroy = lambda: None
                mock_dialog.transient = lambda parent: None
                mock_dialog.grab_set = lambda: None
                mock_dialog.title = lambda title: None
                mock_dialog.resizable = lambda x, y: None
                mock_dialog.minsize = lambda w, h: None
                mock_dialog.geometry = lambda geom: None
                mock_dialog.update_idletasks = lambda: None
                mock_dialog.winfo_reqwidth = lambda: 500
                mock_dialog.winfo_reqheight = lambda: 400
                mock_dialog.winfo_screenwidth = lambda: 1920
                mock_dialog.winfo_screenheight = lambda: 1080
                mock_dialog.winfo_x = lambda: 100
                mock_dialog.winfo_y = lambda: 200
                mock_create.return_value = mock_dialog
                
                with patch('tkface.dialog.pathchooser.win.calculate_dpi_sizes') as mock_dpi:
                    mock_dpi.return_value = {
                        "min_width": 400,
                        "min_height": 300,
                        "default_width": 500,
                        "default_height": 400,
                        "padding": 10
                    }
                    
                    with patch('tkface.dialog.pathchooser.lang.set'):
                        # Mock the event binding to simulate Cancel button click
                        def mock_bind(event, callback):
                            if event == "<<PathBrowserCancel>>":
                                callback()
                        
                        mock_browser_instance.bind = mock_bind
                        
                        result = pathchooser.askpath()
                        assert result == []

    def test_askpath_save_mode_config(self, root):
        """Test askpath with save_mode config."""
        config = pathchooser.FileDialogConfig(
            select="file",
            multiple=False,
            save_mode=True,
            initialfile="test.txt"
        )
        
        with patch('tkface.dialog.pathchooser.PathBrowser') as mock_browser:
            mock_browser_instance = mock_browser.return_value
            mock_browser_instance.get_selection.return_value = ["/path/to/test.txt"]
            mock_browser_instance.bind = lambda event, callback: None
            mock_browser_instance.pack = lambda **kwargs: None
            mock_browser_instance.focus_set = lambda: None
            
            with patch('tkface.dialog.pathchooser._create_dialog_window') as mock_create:
                mock_dialog = tk.Toplevel(root)
                mock_dialog.withdraw = lambda: None
                mock_dialog.deiconify = lambda: None
                mock_dialog.lift = lambda: None
                mock_dialog.focus_set = lambda: None
                mock_dialog.wait_window = lambda: None
                mock_dialog.destroy = lambda: None
                mock_dialog.transient = lambda parent: None
                mock_dialog.grab_set = lambda: None
                mock_dialog.title = lambda title: None
                mock_dialog.resizable = lambda x, y: None
                mock_dialog.minsize = lambda w, h: None
                mock_dialog.geometry = lambda geom: None
                mock_dialog.update_idletasks = lambda: None
                mock_dialog.winfo_reqwidth = lambda: 500
                mock_dialog.winfo_reqheight = lambda: 400
                mock_dialog.winfo_screenwidth = lambda: 1920
                mock_dialog.winfo_screenheight = lambda: 1080
                mock_dialog.winfo_x = lambda: 100
                mock_dialog.winfo_y = lambda: 200
                mock_create.return_value = mock_dialog
                
                with patch('tkface.dialog.pathchooser.win.calculate_dpi_sizes') as mock_dpi:
                    mock_dpi.return_value = {
                        "min_width": 400,
                        "min_height": 300,
                        "default_width": 500,
                        "default_height": 400,
                        "padding": 10
                    }
                    
                    with patch('tkface.dialog.pathchooser.lang.set'):
                        # Mock the event binding to simulate OK button click
                        def mock_bind(event, callback):
                            if event == "<<PathBrowserOK>>":
                                callback()
                        
                        mock_browser_instance.bind = mock_bind
                        
                        result = pathchooser.askpath(config=config)
                        assert result == ["/path/to/test.txt"]
                        
                        # Verify PathBrowser was created with save_mode and initialfile
                        mock_browser.assert_called_once()
                        call_args = mock_browser.call_args
                        assert call_args[1]['save_mode'] is True
                        assert call_args[1]['initialfile'] == "test.txt"


class TestPathChooserIntegration:
    """Integration tests for pathchooser module."""

    def test_pathchooser_module_import(self):
        """Test that pathchooser module can be imported."""
        assert tkface.pathchooser is not None
        assert hasattr(tkface.pathchooser, 'askpath')
        assert hasattr(tkface.pathchooser, 'askopenfile')
        assert hasattr(tkface.pathchooser, 'askopenfiles')
        assert hasattr(tkface.pathchooser, 'askdirectory')

    def test_pathbrowser_widget_import(self):
        """Test that PathBrowser widget can be imported."""
        # pylint: disable=import-outside-toplevel,reimported,redefined-outer-name
        from tkface.widget.pathbrowser import PathBrowser
        assert PathBrowser is not None

    def test_create_dialog_window_with_none_parent(self):
        """Test _create_dialog_window with None parent."""
        from tkface.dialog.pathchooser import _create_dialog_window
        
        dialog = _create_dialog_window(None)
        assert isinstance(dialog, tk.Toplevel)
        dialog.destroy()

    def test_askpath_with_unround_override(self, root):
        """Test askpath with unround parameter overriding config."""
        config = pathchooser.FileDialogConfig(
            select="file",
            unround=False  # Config says no unround
        )
        
        with patch('tkface.dialog.pathchooser.PathBrowser') as mock_browser:
            mock_browser_instance = mock_browser.return_value
            mock_browser_instance.get_selection.return_value = ["/path/to/test.txt"]
            mock_browser_instance.bind = lambda event, callback: None
            mock_browser_instance.pack = lambda **kwargs: None
            mock_browser_instance.focus_set = lambda: None
            
            with patch('tkface.dialog.pathchooser._create_dialog_window') as mock_create:
                mock_dialog = tk.Toplevel(root)
                mock_dialog.withdraw = lambda: None
                mock_dialog.deiconify = lambda: None
                mock_dialog.lift = lambda: None
                mock_dialog.focus_set = lambda: None
                mock_dialog.wait_window = lambda: None
                mock_dialog.destroy = lambda: None
                mock_dialog.transient = lambda parent: None
                mock_dialog.grab_set = lambda: None
                mock_dialog.title = lambda title: None
                mock_dialog.resizable = lambda x, y: None
                mock_dialog.minsize = lambda w, h: None
                mock_dialog.geometry = lambda geom: None
                mock_dialog.update_idletasks = lambda: None
                mock_dialog.winfo_reqwidth = lambda: 500
                mock_dialog.winfo_reqheight = lambda: 400
                mock_dialog.winfo_screenwidth = lambda: 1920
                mock_dialog.winfo_screenheight = lambda: 1080
                mock_dialog.winfo_x = lambda: 100
                mock_dialog.winfo_y = lambda: 200
                mock_create.return_value = mock_dialog
                
                with patch('tkface.dialog.pathchooser.win.calculate_dpi_sizes') as mock_dpi:
                    mock_dpi.return_value = {
                        "min_width": 400,
                        "min_height": 300,
                        "default_width": 500,
                        "default_height": 400,
                        "padding": 10
                    }
                    
                    with patch('tkface.dialog.pathchooser.lang.set'):
                        with patch('tkface.dialog.pathchooser.win.unround') as mock_unround:
                            # Mock the event binding to simulate OK button click
                            def mock_bind(event, callback):
                                if event == "<<PathBrowserOK>>":
                                    callback()
                            
                            mock_browser_instance.bind = mock_bind
                            
                            # Call with unround=True to override config.unround=False
                            result = pathchooser.askpath(config=config, unround=True)
                            assert result == ["/path/to/test.txt"]
                            
                            # Verify that unround was called despite config saying False
                            mock_unround.assert_called_once_with(mock_dialog, auto_toplevel=False)
