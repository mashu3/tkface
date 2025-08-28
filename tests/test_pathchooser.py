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
        browser = PathBrowser(root, initialdir=temp_dir)
        assert isinstance(browser, tk.Frame)
        # On macOS, paths may be resolved to their real paths
        expected_path = os.path.realpath(temp_dir)
        actual_path = os.path.realpath(browser.state.current_dir)
        assert actual_path == expected_path

    def test_pathbrowser_file_selection(self, root, sample_files):
        """Test file selection in PathBrowser."""
        temp_dir, created_files = sample_files
        test_file1 = created_files[0]  # test1.txt

        browser = PathBrowser(
            root,
            select="file",
            multiple=False,
            initialdir=temp_dir
        )

        # Simulate file selection
        browser.state.selected_items = [test_file1]
        result = browser.get_selection()

        assert result == [test_file1]

    def test_pathbrowser_directory_selection(self, root, sample_files):
        """Test directory selection in PathBrowser."""
        temp_dir, _ = sample_files
        test_subdir = os.path.join(temp_dir, "subdir1")

        browser = PathBrowser(
            root,
            select="dir",
            multiple=False,
            initialdir=temp_dir
        )

        # Simulate directory selection
        browser.state.selected_items = [test_subdir]
        result = browser.get_selection()

        assert result == [test_subdir]

    def test_pathbrowser_multiple_selection(self, root, sample_files):
        """Test multiple selection in PathBrowser."""
        temp_dir, created_files = sample_files
        test_file1 = created_files[0]  # test1.txt
        test_file2 = created_files[1]  # test2.py

        browser = PathBrowser(
            root,
            select="file",
            multiple=True,
            initialdir=temp_dir
        )

        # Simulate multiple file selection
        browser.state.selected_items = [test_file1, test_file2]
        result = browser.get_selection()

        assert result == [test_file1, test_file2]

    def test_pathbrowser_save_mode(self, root, sample_files):
        """Test PathBrowser in save mode."""
        temp_dir, _ = sample_files
        browser = PathBrowser(
            root,
            select="file",
            multiple=False,
            initialdir=temp_dir,
            save_mode=True,
            initialfile="test.txt"
        )

        # In save mode, get_selection should return the filename from entry field
        browser.selected_var.set("newfile.txt")  # pylint: disable=no-member
        result = browser.get_selection()

        expected_path = os.path.join(temp_dir, "newfile.txt")
        # On macOS, paths may be resolved to their real paths
        expected_path = os.path.realpath(expected_path)
        actual_path = os.path.realpath(result[0])
        assert actual_path == expected_path

    def test_pathbrowser_save_mode_empty_filename(self, root, sample_files):
        """Test PathBrowser in save mode with empty filename."""
        temp_dir, _ = sample_files
        browser = PathBrowser(
            root,
            select="file",
            multiple=False,
            initialdir=temp_dir,
            save_mode=True
        )

        # In save mode with empty filename, should return empty list
        browser.selected_var.set("")  # pylint: disable=no-member
        result = browser.get_selection()

        assert result == []

    def test_pathbrowser_file_types(self, root, sample_files):
        """Test file type filtering in PathBrowser."""
        temp_dir, _ = sample_files
        filetypes = [("Text files", "*.txt"), ("Python files", "*.py")]
        browser = PathBrowser(
            root,
            filetypes=filetypes,
            initialdir=temp_dir
        )

        assert browser.config.filetypes == filetypes

    def test_pathbrowser_set_initial_directory(self, root, sample_files):
        """Test setting initial directory."""
        temp_dir, _ = sample_files
        browser = PathBrowser(root)
        browser.set_initial_directory(temp_dir)

        # On macOS, paths may be resolved to their real paths
        expected_path = os.path.realpath(temp_dir)
        actual_path = os.path.realpath(browser.state.current_dir)
        assert actual_path == expected_path

    def test_pathbrowser_set_file_types(self, root):
        """Test setting file types."""
        browser = PathBrowser(root)
        filetypes = [("Text files", "*.txt")]
        browser.set_file_types(filetypes)

        assert browser.config.filetypes == filetypes

    def test_pathbrowser_multiple_extensions_filter(self, root):
        """Test PathBrowser with multiple extensions in a single filter."""
        browser = PathBrowser(
            root,
            select="file",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff")]
        )

        # Test that the filter is set correctly
        assert browser.config.filetypes == [
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff")]

        # Set the filter to the specific pattern we want to test
        filter_text = "Image files (*.png *.jpg *.jpeg *.gif *.bmp *.tiff)"
        browser.filter_var.set(filter_text)  # pylint: disable=no-member

        # Test that multiple extensions are handled correctly
        # pylint: disable=import-outside-toplevel
        from tkface.widget.pathbrowser.view import matches_filter
        assert matches_filter(browser, "test.png")
        assert matches_filter(browser, "test.jpg")
        assert matches_filter(browser, "test.jpeg")
        assert matches_filter(browser, "test.gif")
        assert matches_filter(browser, "test.bmp")
        assert matches_filter(browser, "test.tiff")

        assert not matches_filter(browser, "test.txt")
        assert not matches_filter(browser, "test.doc")

    def test_pathbrowser_multiple_files_display(self, root):
        """Test PathBrowser multiple files display in textbox."""
        browser = PathBrowser(
            root,
            select="file",
            multiple=True
        )

        # Test single file selection
        browser.state.selected_items = ["/path/to/file1.txt"]
        # pylint: disable=import-outside-toplevel
        from tkface.widget.pathbrowser.view import (
            update_selected_display as update_display)
        update_display(browser)
        assert browser.selected_var.get() == "file1.txt"  # pylint: disable=no-member

        # Test two files selection
        browser.state.selected_items = [
            "/path/to/file1.txt", "/path/to/file2.txt"]
        update_display(browser)
        assert (browser.selected_var.get() ==  # pylint: disable=no-member
                "file1.txt, file2.txt")

        # Test three files selection
        browser.state.selected_items = [
            "/path/to/file1.txt",
            "/path/to/file2.txt",
            "/path/to/file3.txt"]
        update_display(browser)
        assert (browser.selected_var.get() ==  # pylint: disable=no-member
                "file1.txt, file2.txt, file3.txt")

        # Test more than three files selection
        browser.state.selected_items = [
            "/path/to/file1.txt",
            "/path/to/file2.txt",
            "/path/to/file3.txt",
            "/path/to/file4.txt"]
        update_display(browser)
        assert (browser.selected_var.get() ==  # pylint: disable=no-member
                "file1.txt (+3 more)")

        # Test no selection
        browser.state.selected_items = []
        update_display(browser)
        assert (browser.selected_var.get() ==  # pylint: disable=no-member
                "")

    def test_pathbrowser_path_input(self, root, sample_files):
        """Test PathBrowser path input functionality."""
        temp_dir, _ = sample_files
        browser = PathBrowser(
            root,
            select="file",
            multiple=False
        )

        # Test that path entry is editable
        assert (str(browser.path_entry.cget("state")) ==  # pylint: disable=no-member
                "normal")

        # Test path navigation via Go button
        test_path = os.path.dirname(temp_dir)
        browser.path_var.set(test_path)  # pylint: disable=no-member
        browser._go_to_path()  # pylint: disable=protected-access
        # On macOS, paths may be resolved to their real paths
        expected_path = os.path.realpath(test_path)
        actual_path = os.path.realpath(browser.state.current_dir)
        assert actual_path == expected_path

    def test_pathbrowser_status_display(self, root, sample_files):
        """Test PathBrowser status bar display."""
        temp_dir, _ = sample_files
        browser = PathBrowser(
            root,
            select="file",
            multiple=True
        )

        # Test format_size function
        # pylint: disable=import-outside-toplevel
        from tkface.widget.pathbrowser import format_size
        assert format_size(0) == "0 B"
        assert format_size(512) == "512 B"
        assert format_size(1024) == "1.0 KB"
        assert format_size(1536) == "1.5 KB"
        assert format_size(1024 * 1024) == "1.0 MB"
        assert (format_size(1024 * 1024 * 1024) ==
                "1.0 GB")

        # Test status update when no selection
        # pylint: disable=import-outside-toplevel
        from tkface.widget.pathbrowser.view import update_status
        update_status(browser)
        status = browser.status_var.get()  # pylint: disable=no-member
        # Status should contain information about files and folders
        assert isinstance(status, str)
        assert len(status) > 0

        # Test status update when files are selected
        browser.state.selected_items = [
            "/path/to/file1.txt", "/path/to/file2.txt"]
        update_status(browser)
        sel_status = browser.status_var.get()  # pylint: disable=no-member
        # Check for translated "Selected:" text
        from tkface import lang  # pylint: disable=import-outside-toplevel
        selected_text = lang.get("Selected:", browser)
        files_text = lang.get("files", browser)
        assert selected_text in sel_status
        assert f"2 {files_text}" in sel_status

        # Test status update when folders are selected
        # Use actual existing directories for testing
        browser.state.selected_items = [
            temp_dir, os.path.dirname(temp_dir)]
        update_status(browser)
        folder_status = browser.status_var.get()  # pylint: disable=no-member
        # Check for translated text
        from tkface import lang  # pylint: disable=import-outside-toplevel,reimported
        selected_text = lang.get("Selected:", browser)
        folder_text = lang.get("folder", browser)
        assert selected_text in folder_status
        assert folder_text in folder_status

    def test_pathbrowser_file_selection_status(self, root, sample_files):
        """Test PathBrowser status bar when files are selected."""
        temp_dir, created_files = sample_files  # pylint: disable=unused-variable
        browser = PathBrowser(
            root,
            select="file",
            multiple=True
        )

        # Use existing test files from sample_files fixture
        test_file1 = created_files[0]  # test1.txt
        test_file2 = created_files[1]  # test2.py

        # Test file selection status
        browser.state.selected_items = [test_file1, test_file2]
        # pylint: disable=import-outside-toplevel
        from tkface.widget.pathbrowser.view import update_status
        update_status(browser)
        status = browser.status_var.get()  # pylint: disable=no-member

        # Should show translated text for selected files
        from tkface import lang  # pylint: disable=import-outside-toplevel,reimported
        selected_text = lang.get("Selected:", browser)
        files_text = lang.get("files", browser)
        folder_text = lang.get("folder", browser)
        assert selected_text in status
        assert f"2 {files_text}" in status
        assert folder_text not in status

    def test_pathbrowser_directory_selection_display(self, root, sample_files):
        """Test PathBrowser directory selection display in textbox."""
        temp_dir, created_files = sample_files
        browser = PathBrowser(
            root,
            select="both",
            multiple=True
        )

        # Test single directory selection - filename entry should be empty
        browser.state.selected_items = [temp_dir]
        # pylint: disable=import-outside-toplevel
        from tkface.widget.pathbrowser.view import (
            update_selected_display as update_display)
        update_display(browser)
        assert browser.selected_var.get() == ""  # pylint: disable=no-member

        # Test multiple directories selection - filename entry should be empty
        browser.state.selected_items = [
            temp_dir, os.path.dirname(temp_dir)]
        update_display(browser)
        assert (browser.selected_var.get() ==  # pylint: disable=no-member
                "")

        # Test mixed selection (files and directories) - only show files
        test_file = created_files[0]  # test1.txt

        browser.state.selected_items = [temp_dir, test_file]
        update_display(browser)
        assert (browser.selected_var.get() ==  # pylint: disable=no-member
                "test1.txt")

        # Test multiple files with directories - show file names
        test_file2 = created_files[1]  # test2.py

        browser.state.selected_items = [
            temp_dir, test_file, test_file2]
        update_display(browser)
        assert (browser.selected_var.get() ==  # pylint: disable=no-member
                "test1.txt, test2.py")

    def test_pathbrowser_status_bar_detailed_display(self, root, sample_files):
        """Test PathBrowser status bar shows detailed selection information."""
        temp_dir, created_files = sample_files
        browser = PathBrowser(
            root,
            select="both",
            multiple=True
        )

        # Test single directory selection status
        browser.state.selected_items = [temp_dir]
        # pylint: disable=import-outside-toplevel
        from tkface.widget.pathbrowser.view import (
            update_status)
        update_status(browser)
        status = browser.status_var.get()  # pylint: disable=no-member
        assert f"📁 {os.path.basename(temp_dir)}" in status

        # Test single file selection status
        test_file = created_files[0]  # test1.txt

        browser.state.selected_items = [test_file]
        update_status(browser)
        status = browser.status_var.get()  # pylint: disable=no-member
        assert "test1.txt" in status

        # Test mixed selection status
        browser.state.selected_items = [temp_dir, test_file]
        update_status(browser)
        status = browser.status_var.get()  # pylint: disable=no-member
        assert f"📁 {os.path.basename(temp_dir)}" in status
        assert "test1.txt" in status

    def test_pathbrowser_macos_symlink_loop_prevention(self, root, sample_files):
        """Test PathBrowser prevents symlink loops on macOS."""
        temp_dir, _ = sample_files  # pylint: disable=unused-variable
        browser = PathBrowser(
            root,
            select="dir",
            multiple=False,
            initialdir=temp_dir
        )

        # Test that symlink resolution works correctly
        import sys  # pylint: disable=import-outside-toplevel
        if sys.platform == "darwin":
            # Test with a path that would create a loop
            test_path = "/Volumes/Macintosh HD/Volumes"
            try:
                # This should resolve to "/Volumes" and not create a loop
                browser._load_directory(test_path)  # pylint: disable=protected-access
                # The current directory should be resolved to the real path
                assert browser.state.current_dir == "/Volumes"
            except (OSError, PermissionError):
                # It's okay if we can't access the path
                pass

            # Test that the tree doesn't show duplicate entries
            # pylint: disable=import-outside-toplevel
            from tkface.widget.pathbrowser.view import (
                load_directory_tree as load_tree)
            load_tree(browser)
            tree_items = browser.tree.get_children()  # pylint: disable=no-member
            # Should not have duplicate root entries
            root_entries = [item for item in tree_items if item == "/"]
            assert len(root_entries) <= 1

    def test_pathbrowser_symlink_resolution(self, root, sample_files):
        """Test PathBrowser correctly resolves symlinks."""
        temp_dir, _ = sample_files
        browser = PathBrowser(
            root,
            select="dir",
            multiple=False,
            initialdir=temp_dir
        )

        # Test symlink resolution in path navigation
        test_path = os.path.join(temp_dir, "test_symlink")
        target_path = os.path.join(temp_dir, "target_dir")

        try:
            # Create a target directory
            os.makedirs(target_path, exist_ok=True)

            # Create a symlink (only on Unix-like systems)
            if hasattr(os, 'symlink'):
                os.symlink(target_path, test_path)

                # Test that navigating to the symlink resolves to the target
                browser.path_var.set(test_path)  # pylint: disable=no-member
                browser._go_to_path()  # pylint: disable=protected-access

                # The current directory should be the resolved path
                # On macOS, /var is a symlink to /private/var, so we need to compare
                # real paths
                expected_path = os.path.realpath(target_path)
                actual_path = os.path.realpath(browser.state.current_dir)
                assert actual_path == expected_path

                # Clean up
                os.unlink(test_path)
                os.rmdir(target_path)
        except (OSError, PermissionError):
            # Skip test if symlinks are not supported or permission denied
            pass


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
