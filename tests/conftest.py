import gc
import logging
import os
import threading
import time
import tkinter as tk
from unittest.mock import MagicMock, Mock, patch

import pytest

# Import tkface modules for fixtures
import tkface.lang.lang

# Global Tkinter instance management
_TK_ROOT = None
_TK_LOCK = threading.Lock()
_TK_INITIALIZED = False


def _cleanup_tkinter():
    """Clean up Tkinter resources safely."""
    global _TK_ROOT, _TK_INITIALIZED  # pylint: disable=global-statement
    if _TK_ROOT is not None:
        try:
            # Destroy all child windows
            for widget in _TK_ROOT.winfo_children():
                try:
                    widget.destroy()
                except (tk.TclError, AttributeError) as e:
                    # Widget may already be destroyed or invalid
                    logging.debug(f"Failed to destroy widget: {e}")
            # Destroy the main window
            _TK_ROOT.destroy()
        except tk.TclError as e:
            # Main window may already be destroyed
            logging.debug(f"Failed to destroy main window: {e}")
        except Exception as e:  # pylint: disable=W0718
            # Log unexpected errors but continue cleanup
            logging.warning(f"Unexpected error during Tkinter cleanup: {e}")
        finally:
            _TK_ROOT = None
            _TK_INITIALIZED = False
    # Force garbage collection
    gc.collect()
    # Short wait for resource cleanup
    time.sleep(0.1)


@pytest.fixture(scope="function")
def root():
    """Create a root window for each test function to avoid conflicts."""
    try:
        # Set environment variables
        os.environ["TK_SILENCE_DEPRECATION"] = "1"
        os.environ["PYTHONUNBUFFERED"] = "1"
        
        # Create new root window for each test
        temp_root = tk.Tk()
        temp_root.withdraw()  # Hide the main window
        # Force window updates
        temp_root.update()
        temp_root.update_idletasks()
        
        # Load msgcat package for language support
        try:
            temp_root.tk.call("package", "require", "msgcat")
        except tk.TclError as e:
            logging.warning(f"Failed to load msgcat package: {e}")
        
        yield temp_root
        
        # Clean up after each test
        try:
            # Destroy all child windows first
            for child in temp_root.winfo_children():
                try:
                    child.destroy()
                except tk.TclError:
                    pass
            temp_root.destroy()
        except tk.TclError as e:
            # Window may already be destroyed
            logging.debug(f"Failed to destroy root window: {e}")
        # Force garbage collection
        gc.collect()
        time.sleep(0.01)  # Brief pause for cleanup
        
    except tk.TclError as e:
        error_str = str(e)
        if any(
            pattern in error_str
            for pattern in [
                "Can't find a usable tk.tcl",
                "Can't find a usable init.tcl",
                "vistaTheme.tcl",
                "init.tcl",
                "No error",
                "fonts.tcl",
                "icons.tcl",
                "tk.tcl",
                "no display name and no $DISPLAY environment variable",
                "no display name",
                "$DISPLAY environment variable",
                "application has been destroyed",
                "invalid command name \"tcl_findLibrary\"",
            ]
        ):
            pytest.skip(
                f"Tkinter not properly installed or display not available: "
                f"{error_str}"
            )
        else:
            raise
    except Exception:  # pylint: disable=W0718
        # Try cleanup for unexpected errors
        try:
            temp_root.destroy()
        except:
            pass
        raise


@pytest.fixture(scope="session", autouse=True)
def cleanup_session():
    """Clean up Tkinter resources after all tests complete."""
    yield
    with _TK_LOCK:
        _cleanup_tkinter()


@pytest.fixture(scope="function")
def root_function():
    """Create a temporary root window for individual function tests."""
    try:
        # Set environment variables
        os.environ["TK_SILENCE_DEPRECATION"] = "1"
        # Create new root window
        temp_root = tk.Tk()
        temp_root.withdraw()  # Hide the main window
        temp_root.update()
        # Load msgcat package for language support
        try:
            temp_root.tk.call("package", "require", "msgcat")
        except tk.TclError as e:
            logging.warning(f"Failed to load msgcat package: {e}")
        yield temp_root
        # Cleanup
        try:
            temp_root.destroy()
        except tk.TclError as e:
            # Window may already be destroyed
            logging.debug(f"Failed to destroy temporary root window: {e}")
    except tk.TclError as e:
        error_str = str(e)
        if any(
            pattern in error_str
            for pattern in [
                "Can't find a usable tk.tcl",
                "Can't find a usable init.tcl",
                "vistaTheme.tcl",
                "init.tcl",
                "No error",
                "fonts.tcl",
                "icons.tcl",
                "tk.tcl",
                "no display name and no $DISPLAY environment variable",
                "no display name",
                "$DISPLAY environment variable",
                "application has been destroyed",
                "invalid command name \"tcl_findLibrary\"",
            ]
        ):
            pytest.skip(
                f"Tkinter not properly installed or display not available: "
                f"{error_str}"
            )
        else:
            raise


@pytest.fixture(scope="function")
def root_isolated():
    """Create an isolated root window for tests that need complete isolation."""
    try:
        # Set environment variables
        os.environ["TK_SILENCE_DEPRECATION"] = "1"
        # Create new root window
        temp_root = tk.Tk()
        temp_root.withdraw()  # Hide the main window
        temp_root.update()
        temp_root.update_idletasks()
        # Load msgcat package for language support
        try:
            temp_root.tk.call("package", "require", "msgcat")
        except tk.TclError as e:
            logging.warning(f"Failed to load msgcat package: {e}")
        yield temp_root
        # Cleanup
        try:
            # Destroy all children first
            for child in temp_root.winfo_children():
                try:
                    child.destroy()
                except tk.TclError:
                    pass
            temp_root.destroy()
        except tk.TclError as e:
            # Window may already be destroyed
            logging.debug(f"Failed to destroy isolated root window: {e}")
        # Force garbage collection
        gc.collect()
        time.sleep(0.01)  # Brief pause for cleanup
    except tk.TclError as e:
        error_str = str(e)
        if any(
            pattern in error_str
            for pattern in [
                "Can't find a usable tk.tcl",
                "Can't find a usable init.tcl",
                "vistaTheme.tcl",
                "init.tcl",
                "No error",
                "fonts.tcl",
                "icons.tcl",
                "tk.tcl",
                "no display name and no $DISPLAY environment variable",
                "no display name",
                "$DISPLAY environment variable",
                "application has been destroyed",
                "invalid command name \"tcl_findLibrary\"",
            ]
        ):
            pytest.skip(
                f"Tkinter not properly installed or display not available: "
                f"{error_str}"
            )
        else:
            raise


@pytest.fixture
def calendar_mock_patches():
    """Provide comprehensive mock patches for Calendar class tests."""
    patches = [
        patch("tkinter.Frame.__init__", return_value=None),
        patch("tkinter.Frame.configure"),
        patch("tkinter.Frame.pack"),
        patch("tkinter.Frame.grid"),
        patch("tkinter.Frame.place"),
        patch("tkinter.Frame.columnconfigure"),
        patch("tkinter.Frame.rowconfigure"),
        patch("tkinter.Frame.grid_columnconfigure"),
        patch("tkinter.Frame.grid_rowconfigure"),
        patch("tkinter.Label"),
        patch("tkinter.Button"),
        patch("tkinter.Label.configure"),
        patch("tkinter.Button.configure"),
        patch("tkinter.Label.pack"),
        patch("tkinter.Button.pack"),
        patch("tkinter.Label.grid"),
        patch("tkinter.Button.grid"),
        patch("tkinter.Label.place"),
        patch("tkinter.Button.place"),
        patch("tkinter.Label.cget"),
        patch("tkinter.Button.cget"),
        patch("tkinter.Label.winfo_width"),
        patch("tkinter.Button.winfo_width"),
        patch("tkinter.Label.winfo_height"),
        patch("tkinter.Button.winfo_height"),
        patch("tkinter.Label.winfo_children"),
        patch("tkinter.Button.winfo_children"),
        patch("tkinter.Frame.winfo_children"),
        patch("tkinter.Frame.winfo_width"),
        patch("tkinter.Frame.winfo_height"),
        patch("tkinter.Frame.cget"),
        patch("tkinter.Frame.bind"),
        patch("tkinter.Label.bind"),
        patch("tkinter.Button.bind"),
        # Additional patches to prevent window creation
        patch("tkinter.Tk"),
        patch("tkinter.Toplevel"),
        patch("tkinter.Tk.__init__", return_value=None),
        patch("tkinter.Toplevel.__init__", return_value=None),
    ]
    # Start all patches
    for p in patches:
        p.start()
    yield patches
    # Stop all patches
    for p in patches:
        p.stop()


@pytest.fixture
def calendar_theme_colors():
    """Provide complete theme_colors for Calendar tests."""
    return {
        "background": "white",
        "month_header_bg": "white",
        "month_header_fg": "black",
        "navigation_bg": "white",
        "navigation_fg": "black",
        "navigation_font": ("Arial", 10),
        "navigation_hover_bg": "lightgray",
        "navigation_hover_fg": "black",
        "day_header_bg": "white",
        "day_header_fg": "black",
        "day_header_font": ("Arial", 10),
        "week_number_bg": "white",
        "week_number_fg": "black",
        "week_number_font": ("Arial", 8),
        "day_bg": "white",
        "day_fg": "black",
        "day_font": ("Arial", 10),
        "selected_bg": "blue",
        "selected_fg": "white",
        "hover_bg": "lightgray",
        "hover_fg": "black",
        "adjacent_day_bg": "lightgray",
        "adjacent_day_fg": "gray",
        "weekend_bg": "lightgray",
        "weekend_fg": "black"
    }


@pytest.fixture
def calendar_mock_widgets():
    """Provide mock widgets for Calendar tests."""
    from unittest.mock import Mock

    # Create mock widgets
    mock_label = Mock()
    mock_label.config = Mock()
    mock_label.cget = Mock(return_value="white")
    mock_label.winfo_children = Mock(return_value=[])
    
    mock_frame = Mock()
    mock_frame.winfo_children = Mock(return_value=[])
    mock_frame.config = Mock()
    mock_frame._last_child_ids = {}
    mock_frame.tk = Mock()
    mock_frame._w = "."
    mock_frame.children = {}
    
    return {
        "label": mock_label,
        "frame": mock_frame
    }


@pytest.fixture
def pathbrowser_mock_widgets():
    """Provide mock widgets for PathBrowser tests."""
    from unittest.mock import Mock

    # Create mock widgets
    mock_frame = Mock()
    mock_frame.config = Mock()
    mock_frame.cget = Mock(return_value="white")
    mock_frame.winfo_children = Mock(return_value=[])
    mock_frame._last_child_ids = {}
    mock_frame.tk = Mock()
    mock_frame._w = "."
    mock_frame.children = {}
    
    mock_label = Mock()
    mock_label.config = Mock()
    mock_label.cget = Mock(return_value="white")
    mock_label.winfo_children = Mock(return_value=[])
    
    mock_button = Mock()
    mock_button.config = Mock()
    mock_button.cget = Mock(return_value="white")
    mock_button.winfo_children = Mock(return_value=[])
    
    mock_entry = Mock()
    mock_entry.config = Mock()
    mock_entry.cget = Mock(return_value="white")
    mock_entry.winfo_children = Mock(return_value=[])
    
    mock_treeview = Mock()
    mock_treeview.config = Mock()
    mock_treeview.cget = Mock(return_value="white")
    mock_treeview.winfo_children = Mock(return_value=[])
    mock_treeview.selection = Mock(return_value=[])
    mock_treeview.get_children = Mock(return_value=[])
    
    return {
        "frame": mock_frame,
        "label": mock_label,
        "button": mock_button,
        "entry": mock_entry,
        "treeview": mock_treeview
    }


@pytest.fixture
def pathbrowser_mock_patches():
    """Provide comprehensive mock patches for PathBrowser class tests."""
    patches = [
        patch("tkinter.Frame.__init__", return_value=None),
        patch("tkinter.Frame.configure"),
        patch("tkinter.Frame.pack"),
        patch("tkinter.Frame.grid"),
        patch("tkinter.Frame.place"),
        patch("tkinter.Frame.columnconfigure"),
        patch("tkinter.Frame.rowconfigure"),
        patch("tkinter.Frame.grid_columnconfigure"),
        patch("tkinter.Frame.grid_rowconfigure"),
        patch("tkinter.Label"),
        patch("tkinter.Button"),
        patch("tkinter.Entry"),
        patch("tkinter.Text"),
        patch("tkinter.Scrollbar"),
        patch("tkinter.ttk.Frame"),
        patch("tkinter.ttk.Label"),
        patch("tkinter.ttk.Button"),
        patch("tkinter.ttk.Entry"),
        patch("tkinter.ttk.Combobox"),
        patch("tkinter.ttk.Scrollbar"),
        patch("tkinter.ttk.Treeview"),
        patch("tkinter.ttk.LabelFrame"),
        patch("tkinter.StringVar"),
        patch("tkinter.BooleanVar"),
        patch("tkinter.IntVar"),
        patch("tkinter.DoubleVar"),
        patch("tkinter.Label.configure"),
        patch("tkinter.Button.configure"),
        patch("tkinter.Entry.configure"),
        patch("tkinter.Text.configure"),
        patch("tkinter.Scrollbar.configure"),
        patch("tkinter.ttk.Frame.configure"),
        patch("tkinter.ttk.Label.configure"),
        patch("tkinter.ttk.Button.configure"),
        patch("tkinter.ttk.Entry.configure"),
        patch("tkinter.ttk.Combobox.configure"),
        patch("tkinter.ttk.Scrollbar.configure"),
        patch("tkinter.ttk.Treeview.configure"),
        patch("tkinter.ttk.LabelFrame.configure"),
        patch("tkinter.Label.pack"),
        patch("tkinter.Button.pack"),
        patch("tkinter.Entry.pack"),
        patch("tkinter.Text.pack"),
        patch("tkinter.Scrollbar.pack"),
        patch("tkinter.ttk.Frame.pack"),
        patch("tkinter.ttk.Label.pack"),
        patch("tkinter.ttk.Button.pack"),
        patch("tkinter.ttk.Entry.pack"),
        patch("tkinter.ttk.Combobox.pack"),
        patch("tkinter.ttk.Scrollbar.pack"),
        patch("tkinter.ttk.Treeview.pack"),
        patch("tkinter.ttk.LabelFrame.pack"),
        patch("tkinter.Label.grid"),
        patch("tkinter.Button.grid"),
        patch("tkinter.Entry.grid"),
        patch("tkinter.Text.grid"),
        patch("tkinter.Scrollbar.grid"),
        patch("tkinter.ttk.Frame.grid"),
        patch("tkinter.ttk.Label.grid"),
        patch("tkinter.ttk.Button.grid"),
        patch("tkinter.ttk.Entry.grid"),
        patch("tkinter.ttk.Combobox.grid"),
        patch("tkinter.ttk.Scrollbar.grid"),
        patch("tkinter.ttk.Treeview.grid"),
        patch("tkinter.ttk.LabelFrame.grid"),
        patch("tkinter.Label.place"),
        patch("tkinter.Button.place"),
        patch("tkinter.Entry.place"),
        patch("tkinter.Text.place"),
        patch("tkinter.Scrollbar.place"),
        patch("tkinter.ttk.Frame.place"),
        patch("tkinter.ttk.Label.place"),
        patch("tkinter.ttk.Button.place"),
        patch("tkinter.ttk.Entry.place"),
        patch("tkinter.ttk.Combobox.place"),
        patch("tkinter.ttk.Scrollbar.place"),
        patch("tkinter.ttk.Treeview.place"),
        patch("tkinter.ttk.LabelFrame.place"),
        patch("tkinter.Label.cget"),
        patch("tkinter.Button.cget"),
        patch("tkinter.Entry.cget"),
        patch("tkinter.Text.cget"),
        patch("tkinter.Scrollbar.cget"),
        patch("tkinter.ttk.Frame.cget"),
        patch("tkinter.ttk.Label.cget"),
        patch("tkinter.ttk.Button.cget"),
        patch("tkinter.ttk.Entry.cget"),
        patch("tkinter.ttk.Combobox.cget"),
        patch("tkinter.ttk.Scrollbar.cget"),
        patch("tkinter.ttk.Treeview.cget"),
        patch("tkinter.ttk.LabelFrame.cget"),
        patch("tkinter.Label.winfo_width"),
        patch("tkinter.Button.winfo_width"),
        patch("tkinter.Entry.winfo_width"),
        patch("tkinter.Text.winfo_width"),
        patch("tkinter.Scrollbar.winfo_width"),
        patch("tkinter.ttk.Frame.winfo_width"),
        patch("tkinter.ttk.Label.winfo_width"),
        patch("tkinter.ttk.Button.winfo_width"),
        patch("tkinter.ttk.Entry.winfo_width"),
        patch("tkinter.ttk.Combobox.winfo_width"),
        patch("tkinter.ttk.Scrollbar.winfo_width"),
        patch("tkinter.ttk.Treeview.winfo_width"),
        patch("tkinter.ttk.LabelFrame.winfo_width"),
        patch("tkinter.Label.winfo_height"),
        patch("tkinter.Button.winfo_height"),
        patch("tkinter.Entry.winfo_height"),
        patch("tkinter.Text.winfo_height"),
        patch("tkinter.Scrollbar.winfo_height"),
        patch("tkinter.ttk.Frame.winfo_height"),
        patch("tkinter.ttk.Label.winfo_height"),
        patch("tkinter.ttk.Button.winfo_height"),
        patch("tkinter.ttk.Entry.winfo_height"),
        patch("tkinter.ttk.Combobox.winfo_height"),
        patch("tkinter.ttk.Scrollbar.winfo_height"),
        patch("tkinter.ttk.Treeview.winfo_height"),
        patch("tkinter.ttk.LabelFrame.winfo_height"),
        patch("tkinter.Label.winfo_children"),
        patch("tkinter.Button.winfo_children"),
        patch("tkinter.Entry.winfo_children"),
        patch("tkinter.Text.winfo_children"),
        patch("tkinter.Scrollbar.winfo_children"),
        patch("tkinter.ttk.Frame.winfo_children"),
        patch("tkinter.ttk.Label.winfo_children"),
        patch("tkinter.ttk.Button.winfo_children"),
        patch("tkinter.ttk.Entry.winfo_children"),
        patch("tkinter.ttk.Combobox.winfo_children"),
        patch("tkinter.ttk.Scrollbar.winfo_children"),
        patch("tkinter.ttk.Treeview.winfo_children"),
        patch("tkinter.ttk.LabelFrame.winfo_children"),
        patch("tkinter.Frame.winfo_children"),
        patch("tkinter.Frame.winfo_width"),
        patch("tkinter.Frame.winfo_height"),
        patch("tkinter.Frame.cget"),
        patch("tkinter.Frame.bind"),
        patch("tkinter.Label.bind"),
        patch("tkinter.Button.bind"),
        patch("tkinter.Entry.bind"),
        patch("tkinter.Text.bind"),
        patch("tkinter.Scrollbar.bind"),
        patch("tkinter.ttk.Frame.bind"),
        patch("tkinter.ttk.Label.bind"),
        patch("tkinter.ttk.Button.bind"),
        patch("tkinter.ttk.Entry.bind"),
        patch("tkinter.ttk.Combobox.bind"),
        patch("tkinter.ttk.Scrollbar.bind"),
        patch("tkinter.ttk.Treeview.bind"),
        patch("tkinter.ttk.LabelFrame.bind"),

        patch("tkinter.ttk.Treeview.selection"),
        patch("tkinter.ttk.Treeview.selection_set"),
        patch("tkinter.ttk.Treeview.selection_remove"),
        patch("tkinter.ttk.Treeview.selection_toggle"),
        patch("tkinter.ttk.Treeview.get_children"),
        patch("tkinter.ttk.Treeview.insert"),
        patch("tkinter.ttk.Treeview.delete"),
        patch("tkinter.ttk.Treeview.item"),
        patch("tkinter.ttk.Treeview.see"),
        patch("tkinter.ttk.Treeview.exists"),
        patch("tkinter.ttk.Treeview.identify_row"),
        patch("tkinter.ttk.Treeview.identify_column"),
        patch("tkinter.ttk.Treeview.identify_region"),
        patch("tkinter.ttk.Treeview.identify_element"),
        patch("tkinter.ttk.Combobox.set"),
        patch("tkinter.ttk.Combobox.get"),
        patch("tkinter.ttk.Combobox.configure"),
        patch("tkinter.StringVar.set"),
        patch("tkinter.StringVar.get"),
        patch("tkinter.BooleanVar.set"),
        patch("tkinter.BooleanVar.get"),
        patch("tkinter.IntVar.set"),
        patch("tkinter.IntVar.get"),
        patch("tkinter.DoubleVar.set"),
        patch("tkinter.DoubleVar.get"),
        patch("tkinter.Text.insert"),
        patch("tkinter.Text.delete"),
        patch("tkinter.Text.get"),
        patch("tkinter.Text.see"),
        patch("tkinter.Text.configure"),
        patch("tkinter.Entry.insert"),
        patch("tkinter.Entry.delete"),
        patch("tkinter.Entry.get"),
        patch("tkinter.Entry.configure"),
        patch("tkinter.ttk.Entry.insert"),
        patch("tkinter.ttk.Entry.delete"),
        patch("tkinter.ttk.Entry.get"),
        patch("tkinter.ttk.Entry.configure"),
        patch("tkinter.Toplevel"),
        patch("tkinter.Toplevel.configure"),
        patch("tkinter.Toplevel.geometry"),
        patch("tkinter.Toplevel.title"),
        patch("tkinter.Toplevel.transient"),
        patch("tkinter.Toplevel.grab_set"),
        patch("tkinter.Toplevel.deiconify"),
        patch("tkinter.Toplevel.lift"),
        patch("tkinter.Toplevel.focus_set"),
        patch("tkinter.Toplevel.wait_window"),
        patch("tkinter.Toplevel.destroy"),
        patch("tkinter.Toplevel.winfo_toplevel"),
        patch("tkinter.Toplevel.winfo_rootx"),
        patch("tkinter.Toplevel.winfo_rooty"),
        patch("tkinter.Toplevel.winfo_width"),
        patch("tkinter.Toplevel.winfo_height"),
        patch("tkinter.Toplevel.update_idletasks"),
        patch("tkinter.Toplevel.update"),
        patch("tkinter.Toplevel.after"),
        patch("tkinter.Toplevel.bind"),
        patch("tkinter.Toplevel.event_generate"),
        patch("tkinter.Toplevel.focus_set"),
        patch("tkinter.Toplevel.clipboard_clear"),
        patch("tkinter.Toplevel.clipboard_append"),
        # Language management patches
        patch("tkface.lang.lang.LanguageManager.get", return_value="Go"),
        patch("tkface.lang.get", return_value="Test message"),
    ]
    # Start all patches
    for p in patches:
        p.start()
    yield patches
    # Stop all patches
    for p in patches:
        p.stop()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    import shutil  # pylint: disable=import-outside-toplevel
    import tempfile  # pylint: disable=import-outside-toplevel

    temp_dir_path = tempfile.mkdtemp()  # pylint: disable=redefined-outer-name
    yield temp_dir_path
    # Cleanup
    try:
        shutil.rmtree(temp_dir_path, ignore_errors=True)
    except Exception as e:  # pylint: disable=W0718
        # Log cleanup errors but don't fail the test
        logging.warning(f"Failed to cleanup temporary directory {temp_dir_path}: {e}")


@pytest.fixture
def sample_files(temp_dir):  # pylint: disable=redefined-outer-name
    """Create sample files in temporary directory for testing."""

    # Create sample files
    files = {
        "test1.txt": "test content 1",
        "test2.py": "test content 2",
        "test3.log": "test content 3",
        "image1.png": "fake image data",
        "image2.jpg": "fake image data",
        "document.pdf": "fake pdf data",
    }

    created_files = []
    for filename, content in files.items():
        file_path = os.path.join(temp_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        created_files.append(file_path)

    # Create subdirectories
    subdirs = ["subdir1", "subdir2", "docs", "images"]
    for subdir in subdirs:
        subdir_path = os.path.join(temp_dir, subdir)
        os.makedirs(subdir_path, exist_ok=True)
        # Add some files to subdirectories
        for i in range(3):
            file_path = os.path.join(subdir_path, f"file{i}.txt")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"content in {subdir} file {i}")
            created_files.append(file_path)

    yield temp_dir, created_files


# Configuration for parallel testing


def pytest_configure(config):  # pylint: disable=unused-argument
    """Configure pytest for parallel execution."""
    # Suppress warnings during parallel execution
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    )
    config.addinivalue_line("markers", "gui: marks tests as GUI tests")
    # Configure logging for tests
    logging.basicConfig(
        level=logging.WARNING,  # Only show warnings and errors during tests
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def pytest_collection_modifyitems(config, items):  # pylint: disable=unused-argument
    """Modify test collection for better parallel execution."""
    for item in items:  # pylint: disable=redefined-outer-name
        # Add gui marker to GUI tests
        if any(
            pattern in item.nodeid for pattern in [
                "messagebox",
                "calendar",
                "pathbrowser",
                "pathchooser"]):
            item.add_marker(pytest.mark.gui)


# Common mock settings for PathBrowser
@pytest.fixture
def mock_file_info_manager():
    """Provide common FileInfoManager mock"""
    mock = Mock()
    # Arithmetic operation enabled mock
    mock.get_memory_usage_estimate.return_value = 1024 * 1024  # 1MB
    mock.get_cache_size.return_value = 100
    mock._resolve_symlink.return_value = "/test/dir"
    mock.get_cached_file_info.return_value = Mock(is_dir=True)
    mock.get_file_info.return_value = Mock(is_dir=True)
    return mock


@pytest.fixture
def mock_tree_widget():
    """Provide common Tree widget mock"""
    mock = Mock()
    mock.selection.return_value = ["/test/dir1"]
    mock.get_children.return_value = []
    mock.item.return_value = None
    return mock


@pytest.fixture
def mock_file_tree_widget():
    """Provide common FileTree widget mock"""
    mock = Mock()
    mock.selection.return_value = ["/test/file1.txt"]
    mock.get_children.return_value = ["/test/file1.txt", "/test/file2.txt"]
    mock.focus_set = Mock()
    return mock


@pytest.fixture
def arithmetic_mock():
    """Create arithmetic operation enabled mock"""
    mock = Mock()
    # Set special methods to enable arithmetic operations
    mock.__sub__ = lambda self, other: 1024 * 1024  # 1MB
    mock.__add__ = lambda self, other: 1024 * 1024  # 1MB
    mock.__gt__ = lambda self, other: True
    mock.__lt__ = lambda self, other: False
    return mock


@pytest.fixture
def dict_like_mock():
    """Mock that supports dictionary-like operations"""
    mock = Mock()
    mock.__setitem__ = Mock()
    mock.__getitem__ = Mock()
    mock.configure = Mock()
    return mock


@pytest.fixture
def mock_pathbrowser_config():
    """PathBrowser configuration mock"""
    mock = Mock()
    mock.save_mode = False
    mock.multiple = True
    mock.enable_memory_monitoring = True
    mock.filetypes = [("Text files", "*.txt"), ("Python files", "*.py")]
    mock.title = "Test Browser"
    return mock


@pytest.fixture
def mock_pathbrowser_state():
    """PathBrowser state mock"""
    mock = Mock()
    mock.current_dir = "/test/dir"
    mock.selected_items = ["/test/file1.txt"]
    mock.navigation_history = ["/test/dir1"]
    mock.forward_history = ["/test/dir2"]
    mock.sort_column = "#0"
    mock.sort_reverse = False
    mock.selection_anchor = "/test/file1.txt"
    return mock


@pytest.fixture
def mock_treeview_operations():
    """Provide Treeview operation methods mock"""
    mock = Mock()
    
    # Basic Treeview operations
    mock.selection.return_value = []
    mock.selection_set = Mock()
    mock.selection_remove = Mock()
    mock.selection_toggle = Mock()
    mock.selection_add = Mock()
    
    # Item operations
    mock.get_children.return_value = []
    mock.insert = Mock(return_value="item1")
    mock.delete = Mock()
    # Mock item method to handle both get and set operations
    mock.item = Mock()
    mock.item.side_effect = lambda item, option=None, **kwargs: {"open": False} if option == "open" else {}
    mock.exists = Mock(return_value=True)
    
    # Display and navigation
    mock.see = Mock()
    mock.identify_row = Mock(return_value="0")
    mock.identify_column = Mock(return_value="#0")
    mock.identify_region = Mock(return_value="cell")
    mock.identify_element = Mock(return_value="text")
    
    # Column operations
    mock.column = Mock()
    mock.heading = Mock()
    
    # Scrolling
    mock.yview = Mock()
    mock.yview_scroll = Mock()
    mock.yview_moveto = Mock()
    
    # Focus
    mock.focus = Mock(return_value="item1")
    mock.focus_set = Mock()
    
    # State
    mock.state = Mock(return_value=[])
    mock.set = Mock()
    
    return mock


@pytest.fixture
def mock_treeview_item():
    """Provide Treeview item mock"""
    mock = Mock()
    mock.values = ["item1", "size1", "date1"]
    mock.tags = ["tag1", "tag2"]
    mock.image = ""
    mock.text = "item1"
    return mock


@pytest.fixture
def mock_treeview_column():
    """Provide Treeview column mock"""
    mock = Mock()
    mock.width = 100
    mock.minwidth = 50
    mock.stretch = True
    mock.anchor = "w"
    return mock


@pytest.fixture
def mock_treeview_heading():
    """Provide Treeview heading mock"""
    mock = Mock()
    mock.text = "Name"
    mock.image = ""
    mock.anchor = "w"
    mock.command = None
    return mock


@pytest.fixture
def mock_treeview_scrollbar():
    """Provide Treeview scrollbar mock"""
    mock = Mock()
    mock.set = Mock()
    mock.get = Mock(return_value=(0.0, 1.0))
    mock.configure = Mock()
    return mock


@pytest.fixture
def mock_treeview_bindings():
    """Provide Treeview event binding mock"""
    mock = Mock()
    mock.bind = Mock()
    mock.unbind = Mock()
    mock.event_generate = Mock()
    return mock


@pytest.fixture
def mock_treeview_selection_manager():
    """Provide Treeview selection management mock"""
    mock = Mock()
    mock.get_selection = Mock(return_value=["item1", "item2"])
    mock.set_selection = Mock()
    mock.clear_selection = Mock()
    mock.add_to_selection = Mock()
    mock.remove_from_selection = Mock()
    mock.toggle_selection = Mock()
    mock.select_all = Mock()
    mock.select_none = Mock()
    mock.select_inverse = Mock()
    return mock


@pytest.fixture
def mock_treeview_navigation():
    """Provide Treeview navigation mock"""
    mock = Mock()
    mock.get_visible_items = Mock(return_value=["item1", "item2", "item3"])
    mock.scroll_to_item = Mock()
    mock.ensure_item_visible = Mock()
    mock.get_item_position = Mock(return_value=1)
    mock.get_item_at_position = Mock(return_value="item2")
    return mock


@pytest.fixture
def mock_treeview_sorting():
    """Provide Treeview sorting functionality mock"""
    mock = Mock()
    mock.sort_by_column = Mock()
    mock.get_sort_column = Mock(return_value="#0")
    mock.get_sort_reverse = Mock(return_value=False)
    mock.toggle_sort = Mock()
    mock.clear_sort = Mock()
    return mock


@pytest.fixture
def mock_treeview_filtering():
    """Provide Treeview filtering mock"""
    mock = Mock()
    mock.apply_filter = Mock()
    mock.clear_filter = Mock()
    mock.get_filter_text = Mock(return_value="")
    mock.get_filtered_items = Mock(return_value=["item1", "item2"])
    mock.is_filtered = Mock(return_value=False)
    return mock


@pytest.fixture
def mock_treeview_context_menu():
    """Provide Treeview context menu mock"""
    mock = Mock()
    mock.show = Mock()
    mock.hide = Mock()
    mock.add_command = Mock()
    mock.add_separator = Mock()
    mock.post = Mock()
    mock.unpost = Mock()
    return mock


@pytest.fixture
def mock_treeview_drag_drop():
    """Provide Treeview drag and drop mock"""
    mock = Mock()
    mock.start_drag = Mock()
    mock.handle_drop = Mock()
    mock.can_drop = Mock(return_value=True)
    mock.get_drag_data = Mock(return_value=["item1"])
    return mock


@pytest.fixture
def mock_treeview_keyboard():
    """Provide Treeview keyboard operation mock"""
    mock = Mock()
    mock.handle_key = Mock()
    mock.handle_arrow_keys = Mock()
    mock.handle_enter_key = Mock()
    mock.handle_space_key = Mock()
    mock.handle_delete_key = Mock()
    mock.handle_ctrl_a = Mock()
    mock.handle_ctrl_c = Mock()
    mock.handle_ctrl_v = Mock()
    mock.handle_ctrl_x = Mock()
    return mock


@pytest.fixture
def mock_treeview_mouse():
    """Provide Treeview mouse operation mock"""
    mock = Mock()
    mock.handle_click = Mock()
    mock.handle_double_click = Mock()
    mock.handle_right_click = Mock()
    mock.handle_drag_start = Mock()
    mock.handle_drag_motion = Mock()
    mock.handle_drag_release = Mock()
    return mock


@pytest.fixture
def mock_treeview_theme():
    """Provide Treeview theme mock"""
    mock = Mock()
    mock.get_style = Mock(return_value="default")
    mock.set_style = Mock()
    mock.get_colors = Mock(return_value={
        "background": "white",
        "foreground": "black",
        "select_background": "blue",
        "select_foreground": "white",
        "alternate_background": "lightgray"
    })
    mock.apply_theme = Mock()
    return mock


@pytest.fixture
def mock_treeview_accessibility():
    """Provide Treeview accessibility mock"""
    mock = Mock()
    mock.announce_selection = Mock()
    mock.announce_item = Mock()
    mock.get_item_description = Mock(return_value="File item")
    mock.speak_item_count = Mock()
    return mock


@pytest.fixture
def comprehensive_treeview_mock():
    """Provide comprehensive Treeview mock"""
    mock = Mock()
    
    # Basic operations
    mock.selection.return_value = []
    mock.selection_set = Mock()
    mock.selection_remove = Mock()
    mock.selection_toggle = Mock()
    mock.get_children.return_value = []
    mock.insert = Mock(return_value="item1")
    mock.delete = Mock()
    # Mock item method to handle both get and set operations
    mock.item = Mock()
    mock.item.side_effect = lambda item, option=None, **kwargs: {"open": False} if option == "open" else {}
    mock.exists = Mock(return_value=True)
    mock.see = Mock()
    
    # Columns and headings
    mock.column = Mock()
    mock.heading = Mock()
    
    # Scrolling
    mock.yview = Mock()
    mock.yview_scroll = Mock()
    mock.yview_moveto = Mock()
    
    # Focus
    mock.focus = Mock(return_value="item1")
    mock.focus_set = Mock()
    
    # State
    mock.state = Mock(return_value=[])
    mock.set = Mock()
    
    # Events
    mock.bind = Mock()
    mock.unbind = Mock()
    mock.event_generate = Mock()
    
    # Identification
    mock.identify_row = Mock(return_value="0")
    mock.identify_column = Mock(return_value="#0")
    mock.identify_region = Mock(return_value="cell")
    mock.identify_element = Mock(return_value="text")
    
    return mock


@pytest.fixture
def mock_pathbrowser_instance(root):
    """Provide a properly configured PathBrowser instance for testing."""
    from tkface.widget.pathbrowser.core import PathBrowser

    # Create PathBrowser instance with minimal initialization
    browser = PathBrowser.__new__(PathBrowser)
    
    # Mock essential attributes
    browser.config = Mock()
    browser.config.save_mode = False
    browser.config.select = "file"
    browser.config.multiple = False
    browser.config.filetypes = [("All files", "*.*")]
    browser.config.batch_size = 100
    
    browser.state = Mock()
    browser.state.current_dir = "/test/dir"
    browser.state.selected_items = []
    browser.state.forward_history = []
    browser.state.navigation_history = []
    browser.state.sort_column = "#0"
    browser.state.sort_reverse = False
    browser.state.selection_anchor = None

    
    browser.selected_var = Mock()
    browser.selected_var.get.return_value = ""
    browser.selected_var.set = Mock()
    
    browser.path_var = Mock()
    browser.path_var.get.return_value = "/test/dir"
    browser.path_var.set = Mock()
    
    browser.status_var = Mock()
    browser.status_var.set = Mock()
    
    browser.tree = Mock()
    browser.tree.selection.return_value = []
    browser.tree.get_children.return_value = []
    browser.tree.item = Mock()
    browser.tree.delete = Mock()
    browser.tree.insert = Mock()
    browser.tree.exists = Mock(return_value=True)
    browser.tree.see = Mock()
    browser.tree.focus_set = Mock()
    
    browser.file_tree = Mock()
    browser.file_tree.selection.return_value = []
    browser.file_tree.get_children.return_value = []
    browser.file_tree.delete = Mock()
    browser.file_tree.insert = Mock()
    browser.file_tree.focus_set = Mock()
    
    browser.up_button = Mock()
    browser.up_button.config = Mock()
    browser.up_button.bind = Mock()
    
    browser.down_button = Mock()
    browser.down_button.config = Mock()
    browser.down_button.bind = Mock()
    
    browser.filter_combo = Mock()
    browser.filter_combo.get = Mock(return_value="All files")
    browser.filter_combo.set = Mock()
    browser.filter_combo.bind = Mock()
    
    browser.selected_files_entry = Mock()
    browser.selected_files_entry.get = Mock(return_value="")
    browser.selected_files_entry.set = Mock()
    browser.selected_files_entry.bind = Mock()
    
    browser.winfo_toplevel = Mock(return_value=root)
    browser.after = Mock()
    browser.focus_get = Mock(return_value=browser.file_tree)
    browser.focus_set = Mock()
    browser.clipboard_clear = Mock()
    browser.clipboard_append = Mock()
    browser.event_generate = Mock()
    browser.destroy = Mock()
    browser.tk = Mock()
    browser._w = "."
    
    # Mock file_info_manager
    browser.file_info_manager = Mock()
    browser.file_info_manager._resolve_symlink.return_value = "/test/dir"
    browser.file_info_manager.get_cached_file_info.return_value = Mock(is_dir=True)
    browser.file_info_manager.get_file_info.return_value = Mock(is_dir=True)
    
    return browser


@pytest.fixture
def mock_pathbrowser_save_mode(mock_pathbrowser_instance):
    """Provide a PathBrowser instance configured for save mode."""
    browser = mock_pathbrowser_instance
    browser.config.save_mode = True
    browser.config.filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
    return browser


@pytest.fixture
def mock_pathbrowser_open_mode(mock_pathbrowser_instance):
    """Provide a PathBrowser instance configured for open mode."""
    browser = mock_pathbrowser_instance
    browser.config.save_mode = False
    browser.config.select = "file"
    browser.config.multiple = True
    return browser


@pytest.fixture
def mock_pathlib_path():
    """Provide a comprehensive mock for pathlib.Path to avoid AttributeError issues."""
    with patch('tkface.widget.pathbrowser.core.Path') as mock_path_class:
        # Create a proper mock for Path class
        mock_path_instance = Mock()
        mock_path_instance.absolute.return_value = "/test/directory"
        mock_path_instance.exists.return_value = True
        mock_path_instance.parent.return_value = "/test"
        mock_path_instance.name = "directory"
        
        # Mock the class methods properly
        mock_path_class.return_value = mock_path_instance
        mock_path_class.exists.return_value = True
        mock_path_class.home.return_value = "/home/user"
        mock_path_class.parent.return_value = "/test"
        mock_path_class.cwd = Mock(return_value="/test/directory")
        
        # Create a custom Path class that behaves like the real one
        class MockPath:
            def __init__(self, path):
                self._path = path
                self._mock_instance = mock_path_instance
            
            def absolute(self):
                return self._mock_instance.absolute()
            
            def exists(self):
                return mock_path_class.exists()
            
            def parent(self):
                return self._mock_instance.parent()
            
            @property
            def name(self):
                return self._mock_instance.name
        
        # Replace the Path class with our mock
        mock_path_class.side_effect = MockPath
        
        yield mock_path_class


@pytest.fixture
def mock_root():
    """Create a mock Tkinter root for language tests."""
    root = Mock()
    root.tk = Mock()
    # Mock tk.call to handle msgcat package loading
    def mock_call(*args):
        if args == ("package", "require", "msgcat"):
            return "1.0"  # Mock version number
        return None
    root.tk.call = Mock(side_effect=mock_call)
    root.tk.globalgetvar = Mock(return_value='/usr/lib/tk')
    return root


@pytest.fixture
def mock_root_with_locale():
    """Create a mock Tkinter root with locale support for language tests."""
    root = Mock()
    root.tk = Mock()
    # Mock tk.call to handle msgcat package loading and locale calls
    def mock_call(*args):
        if args == ("package", "require", "msgcat"):
            return "1.0"  # Mock version number
        elif args == ("msgcat::mclocale",):
            return "ja_JP"  # Mock locale for testing
        return None
    root.tk.call = Mock(side_effect=mock_call)
    root.tk.globalgetvar = Mock(return_value='/usr/lib/tk')
    return root


@pytest.fixture
def mock_root_tcl_error():
    """Create a mock Tkinter root that raises TclError for language tests."""
    root = Mock()
    root.tk = Mock()
    root.tk.call = Mock(side_effect=tk.TclError('Tcl error'))
    root.tk.globalgetvar = Mock(return_value='/usr/lib/tk')
    return root


@pytest.fixture
def mock_root_os_error():
    """Create a mock Tkinter root that raises OSError for language tests."""
    root = Mock()
    root.tk = Mock()
    root.tk.call = Mock(side_effect=OSError('File not found'))
    root.tk.globalgetvar = Mock(return_value='/usr/lib/tk')
    return root


@pytest.fixture
def lang_manager():
    """Create a LanguageManager instance for testing."""
    return tkface.lang.lang.LanguageManager()


@pytest.fixture
def sample_translations():
    """Sample translation dictionaries for testing."""
    return {
        'ja': {'hello': 'こんにちは', 'goodbye': 'さようなら'},
        'en': {'hello': 'Hello', 'goodbye': 'Goodbye'},
        'fr': {'hello': 'Bonjour', 'goodbye': 'Au revoir'}
    }


@pytest.fixture
def simpledialog_mock_patches():
    """Provide comprehensive mock patches for SimpleDialog tests."""
    patches = [
        patch("tkinter.Toplevel.wait_window"),
        patch("tkinter.Label"),
        patch("tkinter.Button"),
        patch("tkinter.Entry"),
        patch("tkinter.Frame"),
        patch("tkinter.Scrollbar"),
        patch("tkinter.Listbox"),
        patch("tkinter.StringVar"),
    ]
    # Start all patches
    for p in patches:
        p.start()
    yield patches
    # Stop all patches
    for p in patches:
        p.stop()


@pytest.fixture
def simpledialog_mock_widgets():
    """Provide mock widgets for SimpleDialog tests."""
    from unittest.mock import MagicMock, Mock

    # Create mock widgets
    mock_toplevel = Mock()
    mock_toplevel.wait_window = Mock()
    mock_toplevel.grab_set = Mock()
    mock_toplevel.lift = Mock()
    mock_toplevel.focus_set = Mock()
    mock_toplevel.bind = Mock()
    mock_toplevel.destroy = Mock()
    
    mock_label = Mock()
    mock_label.grid = Mock()
    mock_label.pack = Mock()
    
    mock_button = Mock()
    mock_button.pack = Mock()
    mock_button.bind = Mock()
    mock_button.focus_set = Mock()
    mock_button.invoke = Mock()
    mock_button.cget = Mock(return_value="Button Text")
    
    mock_entry = Mock()
    mock_entry.grid = Mock()
    mock_entry.bind = Mock()
    mock_entry.focus_set = Mock()
    
    mock_frame = Mock()
    mock_frame.pack = Mock()
    mock_frame.grid = Mock()
    
    mock_listbox = Mock()
    mock_listbox.pack = Mock()
    mock_listbox.bind = Mock()
    mock_listbox.insert = Mock()
    mock_listbox.selection_set = Mock()
    mock_listbox.curselection = Mock(return_value=[])
    mock_listbox.yview = Mock()
    
    mock_scrollbar = Mock()
    mock_scrollbar.pack = Mock()
    mock_scrollbar.config = Mock()
    
    mock_stringvar = Mock()
    mock_stringvar.get = Mock(return_value="")
    mock_stringvar.set = Mock()
    
    return {
        "toplevel": mock_toplevel,
        "label": mock_label,
        "button": mock_button,
        "entry": mock_entry,
        "frame": mock_frame,
        "listbox": mock_listbox,
        "scrollbar": mock_scrollbar,
        "stringvar": mock_stringvar,
    }


@pytest.fixture
def simpledialog_config():
    """Provide a basic SimpleDialogConfig for testing."""
    from tkface.dialog.simpledialog import SimpleDialogConfig
    
    return SimpleDialogConfig(
        title="Test Dialog",
        message="Test Message",
        initialvalue="test",
        show=None,
        ok_label="OK",
        cancel_label="Cancel",
        language="en",
        custom_translations=None,
        choices=None,
        multiple=False,
        initial_selection=None,
        validate_func=None,
    )


@pytest.fixture
def simpledialog_position():
    """Provide a basic WindowPosition for testing."""
    from tkface.dialog.simpledialog import WindowPosition
    
    return WindowPosition(
        x=None,
        y=None,
        x_offset=0,
        y_offset=0,
    )


@pytest.fixture
def simpledialog_complete_mock():
    """Provide complete mocking for SimpleDialog tests to prevent Toplevel creation."""
    with patch("tkinter.Toplevel") as mock_toplevel_class, \
         patch("tkinter.Label") as mock_label_class, \
         patch("tkinter.Button") as mock_button_class, \
         patch("tkinter.Entry") as mock_entry_class, \
         patch("tkinter.Frame") as mock_frame_class, \
         patch("tkinter.Scrollbar") as mock_scrollbar_class, \
         patch("tkinter.Listbox") as mock_listbox_class, \
         patch("tkinter.StringVar") as mock_stringvar_class, \
         patch("tkface.dialog.simpledialog._position_window") as mock_position_window, \
         patch("tkface.dialog.simpledialog._setup_dialog_base") as mock_setup_dialog_base:
        
        # Create mock instances
        mock_toplevel = Mock()
        mock_toplevel.wait_window = Mock()
        mock_toplevel.grab_set = Mock()
        mock_toplevel.lift = Mock()
        mock_toplevel.focus_set = Mock()
        mock_toplevel.bind = Mock()
        mock_toplevel.destroy = Mock()
        mock_toplevel.configure = Mock()
        mock_toplevel.geometry = Mock()
        mock_toplevel.title = Mock()
        mock_toplevel.transient = Mock()
        mock_toplevel.winfo_toplevel = Mock(return_value=mock_toplevel)
        mock_toplevel.winfo_rootx = Mock(return_value=100)
        mock_toplevel.winfo_rooty = Mock(return_value=100)
        mock_toplevel.winfo_width = Mock(return_value=300)
        mock_toplevel.winfo_height = Mock(return_value=200)
        mock_toplevel.winfo_reqwidth = Mock(return_value=300)
        mock_toplevel.winfo_reqheight = Mock(return_value=200)
        mock_toplevel.update_idletasks = Mock()
        mock_toplevel.update = Mock()
        mock_toplevel.after = Mock()
        mock_toplevel.event_generate = Mock()
        mock_toplevel.clipboard_clear = Mock()
        mock_toplevel.clipboard_append = Mock()
        
        mock_label = Mock()
        mock_label.grid = Mock()
        mock_label.pack = Mock()
        mock_label.configure = Mock()
        
        mock_button = Mock()
        mock_button.pack = Mock()
        mock_button.bind = Mock()
        mock_button.focus_set = Mock()
        mock_button.invoke = Mock()
        mock_button.cget = Mock(return_value="Button Text")
        mock_button.configure = Mock()
        
        mock_entry = Mock()
        mock_entry.grid = Mock()
        mock_entry.bind = Mock()
        mock_entry.focus_set = Mock()
        mock_entry.configure = Mock()
        mock_entry.get = Mock(return_value="test")
        mock_entry.insert = Mock()
        mock_entry.delete = Mock()
        
        mock_frame = Mock()
        mock_frame.pack = Mock()
        mock_frame.grid = Mock()
        mock_frame.configure = Mock()
        
        mock_listbox = Mock()
        mock_listbox.pack = Mock()
        mock_listbox.bind = Mock()
        mock_listbox.insert = Mock()
        mock_listbox.selection_set = Mock()
        mock_listbox.curselection = Mock(return_value=[])
        mock_listbox.yview = Mock()
        mock_listbox.configure = Mock()
        
        mock_scrollbar = Mock()
        mock_scrollbar.pack = Mock()
        mock_scrollbar.config = Mock()
        mock_scrollbar.configure = Mock()
        
        mock_stringvar = Mock()
        mock_stringvar.get = Mock(return_value="")
        mock_stringvar.set = Mock()
        
        # Set return values for constructors
        mock_toplevel_class.return_value = mock_toplevel
        mock_label_class.return_value = mock_label
        mock_button_class.return_value = mock_button
        mock_entry_class.return_value = mock_entry
        mock_frame_class.return_value = mock_frame
        mock_scrollbar_class.return_value = mock_scrollbar
        mock_listbox_class.return_value = mock_listbox
        mock_stringvar_class.return_value = mock_stringvar
        
        # Mock _position_window to do nothing
        mock_position_window.return_value = None
        
        # Mock _setup_dialog_base to return a mock root and language
        mock_setup_dialog_base.return_value = (Mock(), False, "en")
        
        yield {
            "toplevel": mock_toplevel,
            "label": mock_label,
            "button": mock_button,
            "entry": mock_entry,
            "frame": mock_frame,
            "listbox": mock_listbox,
            "scrollbar": mock_scrollbar,
            "stringvar": mock_stringvar,
        }


@pytest.fixture
def simpledialog_class_mock():
    """Provide a mock for CustomSimpleDialog class that can be instantiated."""
    with patch("tkface.dialog.simpledialog.CustomSimpleDialog") as mock_class:
        # Create a mock instance that behaves like CustomSimpleDialog
        mock_instance = Mock()
        
        # Set up basic attributes
        mock_instance.result = None
        mock_instance.window = Mock()
        mock_instance.window.destroy = Mock()
        mock_instance.listbox = None
        mock_instance.choices = None
        mock_instance.multiple = False
        mock_instance.initial_selection = []
        mock_instance.validate_func = None  # Will be set by config
        mock_instance.entry_var = Mock()
        mock_instance.entry_var.get.return_value = ""
        mock_instance.ok_btn = Mock()
        mock_instance.ok_btn.cget.return_value = "Custom OK"
        mock_instance.cancel_btn = Mock()
        mock_instance.cancel_btn.cget.return_value = "Custom Cancel"
        
        # Set up methods
        mock_instance.close = Mock()
        
        # Make _on_cancel actually set result to None and call close
        def _on_cancel():
            mock_instance.result = None
            mock_instance.close()
        mock_instance._on_cancel = _on_cancel
        
        # Make _on_ok actually set the result and call close
        def _on_ok():
            mock_instance.result = mock_instance._get_selection_result()
            mock_instance.close()
        mock_instance._on_ok = _on_ok
        
        mock_instance._get_selection_result = Mock(return_value=None)
        mock_instance._on_double_click = Mock()
        
        # Make set_result actually set the result attribute
        def set_result(value):
            mock_instance.result = value
        mock_instance.set_result = set_result
        
        mock_instance._create_content = Mock(return_value=None)
        mock_instance._create_buttons = Mock()
        mock_instance._set_window_position = Mock()
        
        # Make the class constructor return our mock instance and set up attributes
        def mock_constructor(master=None, config=None, position=None):
            # Set up attributes based on config
            if config:
                mock_instance.validate_func = config.validate_func
                mock_instance.choices = config.choices
                mock_instance.multiple = config.multiple
                mock_instance.initial_selection = config.initial_selection or []
            return mock_instance
        
        mock_class.side_effect = mock_constructor
        
        yield mock_class


@pytest.fixture
def simpledialog_real_instance():
    """Provide comprehensive mocking for CustomSimpleDialog to allow real instance creation."""
    with patch("tkinter.Toplevel") as mock_toplevel_class, \
         patch("tkinter.Label") as mock_label_class, \
         patch("tkinter.Button") as mock_button_class, \
         patch("tkinter.Entry") as mock_entry_class, \
         patch("tkinter.Frame") as mock_frame_class, \
         patch("tkinter.Scrollbar") as mock_scrollbar_class, \
         patch("tkinter.Listbox") as mock_listbox_class, \
         patch("tkinter.StringVar") as mock_stringvar_class, \
         patch("tkface.dialog.simpledialog._position_window"), \
         patch("tkface.dialog.simpledialog._setup_dialog_base") as mock_setup, \
         patch("tkface.dialog.simpledialog.lang.set"), \
         patch("tkface.dialog.simpledialog.lang.get") as mock_lang_get, \
         patch("tkface.dialog.simpledialog.lang.register"), \
         patch("tkface.dialog.simpledialog.logging.getLogger") as mock_logger, \
         patch("tkface.dialog.simpledialog.CustomSimpleDialog.__new__") as mock_new:
        
        # Configure lang.get to return the key as the value
        mock_lang_get.side_effect = lambda key, *args, **kwargs: key
        
        # Mock logger
        mock_logger_instance = Mock()
        mock_logger.return_value = mock_logger_instance
        
        # Mock CustomSimpleDialog.__new__ to return a proper instance
        def mock_custom_simpledialog_new(cls, *args, **kwargs):
            # Create a mock instance
            instance = Mock()
            instance.window = mock_toplevel
            instance.listbox = None
            instance.choices = None
            instance.multiple = False
            instance.initial_selection = []
            instance.validate_func = None
            instance.entry_var = mock_stringvar
            instance.ok_btn = mock_button
            instance.cancel_btn = mock_button
            instance.result = None
            instance.language = "en"
            instance.logger = mock_logger_instance
            
            # Set up methods with actual behavior
            def mock_close():
                instance.window.destroy()
            instance.close = mock_close
            
            def mock_on_cancel():
                instance.result = None
                instance.close()
            instance._on_cancel = mock_on_cancel
            
            def mock_on_ok():
                result = instance._get_selection_result()
                if instance.validate_func is not None:
                    if instance.validate_func(result):
                        instance.result = result
                        instance.close()
                    else:
                        # Show warning message
                        from tkface.dialog import messagebox
                        messagebox.showwarning("Validation Error", "Invalid input")
                else:
                    instance.result = result
                    instance.close()
            instance._on_ok = mock_on_ok
            
            def mock_get_selection_result():
                if hasattr(instance, 'listbox') and instance.listbox is not None:
                    # Check if listbox has selection
                    if hasattr(instance.listbox, 'curselection'):
                        selection = instance.listbox.curselection()
                        if selection:
                            # Return the selected item
                            return f"Option {selection[0] + 1}"
                        else:
                            return None
                    else:
                        return "Choice 1"
                else:
                    # Simulate entry value - return None if empty
                    entry_value = instance.entry_var.get()
                    return entry_value if entry_value else None
            instance._get_selection_result = mock_get_selection_result
            
            def mock_on_double_click(event):
                if hasattr(instance, 'listbox') and instance.listbox is not None:
                    selection = instance.listbox.curselection()
                    if selection:
                        result = f"Option {selection[0] + 1}"
                        instance.set_result(result)
            instance._on_double_click = mock_on_double_click
            
            def mock_set_result(value):
                instance.result = value
            instance.set_result = mock_set_result
            
            instance._create_content = Mock(return_value=None)
            instance._create_buttons = Mock()
            instance._set_window_position = Mock()
            
            # Call the actual __init__ method if it exists
            if hasattr(cls, '__init__') and cls.__init__ is not object.__init__:
                try:
                    cls.__init__(instance, *args, **kwargs)
                except Exception as e:
                    # If __init__ fails, continue with mock instance
                    logging.debug(f"Failed to initialize CustomSimpleDialog: {e}")
            
            return instance
        
        mock_new.side_effect = mock_custom_simpledialog_new
        
        # Create comprehensive mock instances
        mock_toplevel = Mock()
        mock_toplevel.wait_window = Mock()
        mock_toplevel.grab_set = Mock()
        mock_toplevel.lift = Mock()
        mock_toplevel.focus_set = Mock()
        mock_toplevel.bind = Mock()
        mock_toplevel.destroy = Mock()
        mock_toplevel.configure = Mock()
        mock_toplevel.geometry = Mock()
        mock_toplevel.title = Mock()
        mock_toplevel.transient = Mock()
        mock_toplevel.winfo_toplevel = Mock(return_value=mock_toplevel)
        mock_toplevel.winfo_rootx = Mock(return_value=100)
        mock_toplevel.winfo_rooty = Mock(return_value=100)
        mock_toplevel.winfo_width = Mock(return_value=300)
        mock_toplevel.winfo_height = Mock(return_value=200)
        mock_toplevel.winfo_reqwidth = Mock(return_value=300)
        mock_toplevel.winfo_reqheight = Mock(return_value=200)
        mock_toplevel.update_idletasks = Mock()
        mock_toplevel.update = Mock()
        mock_toplevel.after = Mock()
        mock_toplevel.event_generate = Mock()
        mock_toplevel.clipboard_clear = Mock()
        mock_toplevel.clipboard_append = Mock()
        
        mock_label = Mock()
        mock_label.grid = Mock()
        mock_label.pack = Mock()
        mock_label.configure = Mock()
        
        mock_button = Mock()
        mock_button.pack = Mock()
        mock_button.bind = Mock()
        mock_button.focus_set = Mock()
        mock_button.invoke = Mock()
        mock_button.cget = Mock(return_value="Button Text")
        mock_button.configure = Mock()
        
        mock_entry = Mock()
        mock_entry.grid = Mock()
        mock_entry.bind = Mock()
        mock_entry.focus_set = Mock()
        mock_entry.configure = Mock()
        mock_entry.get = Mock(return_value="test")
        mock_entry.insert = Mock()
        mock_entry.delete = Mock()
        
        mock_frame = Mock()
        mock_frame.pack = Mock()
        mock_frame.grid = Mock()
        mock_frame.configure = Mock()
        
        mock_listbox = Mock()
        mock_listbox.pack = Mock()
        mock_listbox.bind = Mock()
        mock_listbox.insert = Mock()
        mock_listbox.selection_set = Mock()
        mock_listbox.curselection = Mock(return_value=[])
        mock_listbox.yview = Mock()
        mock_listbox.configure = Mock()
        
        mock_scrollbar = Mock()
        mock_scrollbar.pack = Mock()
        mock_scrollbar.config = Mock()
        mock_scrollbar.configure = Mock()
        
        mock_stringvar = Mock()
        mock_stringvar.get = Mock(return_value="")
        mock_stringvar.set = Mock()
        
        # Set return values for constructors
        mock_toplevel_class.return_value = mock_toplevel
        mock_label_class.return_value = mock_label
        mock_button_class.return_value = mock_button
        mock_entry_class.return_value = mock_entry
        mock_frame_class.return_value = mock_frame
        mock_scrollbar_class.return_value = mock_scrollbar
        mock_listbox_class.return_value = mock_listbox
        mock_stringvar_class.return_value = mock_stringvar
        
        # Mock _setup_dialog_base to return a mock root and language
        mock_root = Mock()
        mock_root.tk = Mock()
        mock_setup.return_value = (mock_root, False, "en")
        
        yield {
            "toplevel": mock_toplevel,
            "label": mock_label,
            "button": mock_button,
            "entry": mock_entry,
            "frame": mock_frame,
            "listbox": mock_listbox,
            "scrollbar": mock_scrollbar,
            "stringvar": mock_stringvar,
            "logger": mock_logger_instance,
            "new": mock_new,
        }


# Calendar widget fixtures
@pytest.fixture
def calendar_widget(root):
    """Create a Calendar widget for testing."""
    from tkface import Calendar
    return Calendar(root, year=2024, month=1)


@pytest.fixture
def dateframe_widget(root):
    """Create a DateFrame widget for testing."""
    from tkface import DateFrame
    return DateFrame(root)


@pytest.fixture
def dateentry_widget(root):
    """Create a DateEntry widget for testing."""
    from tkface import DateEntry
    return DateEntry(root)


# Common test fixtures for calendar widget tests
@pytest.fixture
def common_test_date():
    """Common test date for calendar tests."""
    import datetime
    return datetime.date(2024, 3, 15)


@pytest.fixture
def common_day_colors():
    """Common day colors for testing."""
    return {"Friday": "green"}


@pytest.fixture
def common_week_start_values():
    """Common week start values for testing."""
    return ["Monday", "Saturday"]


@pytest.fixture
def common_show_week_numbers_values():
    """Common show week numbers values for testing."""
    return [True, False]


@pytest.fixture
def common_today_color():
    """Common today color for testing."""
    return "red"


@pytest.fixture
def common_theme():
    """Common theme for testing."""
    return "dark"


@pytest.fixture
def common_date_format():
    """Common date format for testing."""
    return "%d/%m/%Y"


@pytest.fixture
def common_callback_data():
    """Common callback data for testing."""
    return {
        "callback_called": False,
        "callback_date": None,
        "callback_value": None
    }


@pytest.fixture
def common_exception_handling_data():
    """Common exception handling data for testing."""
    return {
        "exception_raised": False,
        "exception_type": None,
        "exception_message": None
    }


# Common test helper functions
def test_set_date_common(widget, test_date, date_format=None):
    """Common test for setting date functionality."""
    if hasattr(widget, 'set_selected_date'):
        widget.set_selected_date(test_date)
        assert widget.selected_date == test_date
        if hasattr(widget, 'get_date_string'):
            if date_format:
                expected_string = test_date.strftime(date_format)
            else:
                expected_string = test_date.strftime("%Y-%m-%d")
            assert widget.get_date_string() == expected_string
    elif hasattr(widget, 'set_date'):
        widget.set_date(test_date.year, test_date.month)
        assert widget.year == test_date.year
        assert widget.month == test_date.month


def test_set_day_colors_common(widget, day_colors):
    """Common test for setting day colors functionality."""
    if hasattr(widget, 'set_day_colors'):
        widget.set_day_colors(day_colors)
        if hasattr(widget, 'day_colors'):
            assert widget.day_colors == day_colors
        elif hasattr(widget, 'calendar_config'):
            assert widget.calendar_config["day_colors"] == day_colors


def test_set_week_start_common(widget, week_start_values):
    """Common test for setting week start functionality."""
    if hasattr(widget, 'set_week_start'):
        for week_start in week_start_values:
            widget.set_week_start(week_start)
            if hasattr(widget, 'week_start'):
                assert widget.week_start == week_start
                if hasattr(widget, 'cal'):
                    expected_weekday = {"Monday": 0, "Saturday": 5}.get(week_start, 0)
                    assert widget.cal.getfirstweekday() == expected_weekday
            elif hasattr(widget, 'calendar_config'):
                assert widget.calendar_config["week_start"] == week_start


def test_set_show_week_numbers_common(widget, show_week_numbers_values):
    """Common test for setting show week numbers functionality."""
    if hasattr(widget, 'set_show_week_numbers'):
        for show_week_numbers in show_week_numbers_values:
            widget.set_show_week_numbers(show_week_numbers)
            if hasattr(widget, 'show_week_numbers'):
                assert widget.show_week_numbers == show_week_numbers
            elif hasattr(widget, 'calendar_config'):
                assert widget.calendar_config["show_week_numbers"] == show_week_numbers


def test_set_today_color_common(widget, today_color):
    """Common test for setting today color functionality."""
    if hasattr(widget, 'set_today_color'):
        widget.set_today_color(today_color)
        if hasattr(widget, 'today_color'):
            assert widget.today_color == today_color
        elif hasattr(widget, 'calendar_config'):
            assert widget.calendar_config["today_color"] == today_color


def test_set_theme_common(widget, theme):
    """Common test for setting theme functionality."""
    if hasattr(widget, 'set_theme'):
        widget.set_theme(theme)
        if hasattr(widget, 'theme'):
            assert widget.theme == theme
        elif hasattr(widget, 'calendar_config'):
            assert widget.calendar_config["theme"] == theme


def test_get_date_none_common(widget):
    """Common test for getting date when none is set."""
    if hasattr(widget, 'get_date'):
        result = widget.get_date()
        assert result is None
    elif hasattr(widget, 'selected_date'):
        assert widget.selected_date is None


def test_get_date_string_none_common(widget):
    """Common test for getting date string when none is set."""
    if hasattr(widget, 'get_date_string'):
        result = widget.get_date_string()
        assert result == ""


def test_date_callback_common(widget, callback_data, test_date):
    """Common test for date callback functionality."""
    def callback(date):
        callback_data["callback_called"] = True
        callback_data["callback_date"] = date
    
    if hasattr(widget, 'set_date_callback'):
        widget.set_date_callback(callback)
        widget.set_selected_date(test_date)
        assert callback_data["callback_called"] is True
        assert callback_data["callback_date"] == test_date


def test_refresh_language_common(widget):
    """Common test for refresh language functionality."""
    if hasattr(widget, 'refresh_language'):
        # Should not raise an exception
        widget.refresh_language()


def test_exception_handling_common(widget, method_name, exception_data, *args, **kwargs):
    """Common test for exception handling."""
    try:
        method = getattr(widget, method_name)
        method(*args, **kwargs)
    except Exception as e:
        exception_data["exception_raised"] = True
        exception_data["exception_type"] = type(e).__name__
        exception_data["exception_message"] = str(e)


# TimePicker related fixtures
@pytest.fixture
def timepicker_mock_patches():
    """Provide comprehensive mock patches for TimePicker tests."""
    patches = [
        patch("tkinter.Frame.__init__", return_value=None),
        patch("tkinter.Frame.configure"),
        patch("tkinter.Frame.pack"),
        patch("tkinter.Frame.grid"),
        patch("tkinter.Frame.place"),
        patch("tkinter.Frame.columnconfigure"),
        patch("tkinter.Frame.rowconfigure"),
        patch("tkinter.Frame.grid_columnconfigure"),
        patch("tkinter.Frame.grid_rowconfigure"),
        patch("tkinter.Label"),
        patch("tkinter.Button"),
        patch("tkinter.Entry"),
        patch("tkinter.Canvas"),
        patch("tkinter.Spinbox"),
        patch("tkinter.ttk.Frame"),
        patch("tkinter.ttk.Label"),
        patch("tkinter.ttk.Button"),
        patch("tkinter.ttk.Entry"),
        patch("tkinter.ttk.Combobox"),
        patch("tkinter.ttk.Spinbox"),
        patch("tkinter.Label.configure"),
        patch("tkinter.Button.configure"),
        patch("tkinter.Entry.configure"),
        patch("tkinter.Canvas.configure"),
        patch("tkinter.Spinbox.configure"),
        patch("tkinter.ttk.Frame.configure"),
        patch("tkinter.ttk.Label.configure"),
        patch("tkinter.ttk.Button.configure"),
        patch("tkinter.ttk.Entry.configure"),
        patch("tkinter.ttk.Combobox.configure"),
        patch("tkinter.ttk.Spinbox.configure"),
        patch("tkinter.Label.pack"),
        patch("tkinter.Button.pack"),
        patch("tkinter.Entry.pack"),
        patch("tkinter.Canvas.pack"),
        patch("tkinter.Spinbox.pack"),
        patch("tkinter.ttk.Frame.pack"),
        patch("tkinter.ttk.Label.pack"),
        patch("tkinter.ttk.Button.pack"),
        patch("tkinter.ttk.Entry.pack"),
        patch("tkinter.ttk.Combobox.pack"),
        patch("tkinter.ttk.Spinbox.pack"),
        patch("tkinter.Label.grid"),
        patch("tkinter.Button.grid"),
        patch("tkinter.Entry.grid"),
        patch("tkinter.Canvas.grid"),
        patch("tkinter.Spinbox.grid"),
        patch("tkinter.ttk.Frame.grid"),
        patch("tkinter.ttk.Label.grid"),
        patch("tkinter.ttk.Button.grid"),
        patch("tkinter.ttk.Entry.grid"),
        patch("tkinter.ttk.Combobox.grid"),
        patch("tkinter.ttk.Spinbox.grid"),
        patch("tkinter.Label.place"),
        patch("tkinter.Button.place"),
        patch("tkinter.Entry.place"),
        patch("tkinter.Canvas.place"),
        patch("tkinter.Spinbox.place"),
        patch("tkinter.ttk.Frame.place"),
        patch("tkinter.ttk.Label.place"),
        patch("tkinter.ttk.Button.place"),
        patch("tkinter.ttk.Entry.place"),
        patch("tkinter.ttk.Combobox.place"),
        patch("tkinter.ttk.Spinbox.place"),
        patch("tkinter.Label.cget"),
        patch("tkinter.Button.cget"),
        patch("tkinter.Entry.cget"),
        patch("tkinter.Canvas.cget"),
        patch("tkinter.Spinbox.cget"),
        patch("tkinter.ttk.Frame.cget"),
        patch("tkinter.ttk.Label.cget"),
        patch("tkinter.ttk.Button.cget"),
        patch("tkinter.ttk.Entry.cget"),
        patch("tkinter.ttk.Combobox.cget"),
        patch("tkinter.ttk.Spinbox.cget"),
        patch("tkinter.Label.winfo_width"),
        patch("tkinter.Button.winfo_width"),
        patch("tkinter.Entry.winfo_width"),
        patch("tkinter.Canvas.winfo_width"),
        patch("tkinter.Spinbox.winfo_width"),
        patch("tkinter.ttk.Frame.winfo_width"),
        patch("tkinter.ttk.Label.winfo_width"),
        patch("tkinter.ttk.Button.winfo_width"),
        patch("tkinter.ttk.Entry.winfo_width"),
        patch("tkinter.ttk.Combobox.winfo_width"),
        patch("tkinter.ttk.Spinbox.winfo_width"),
        patch("tkinter.Label.winfo_height"),
        patch("tkinter.Button.winfo_height"),
        patch("tkinter.Entry.winfo_height"),
        patch("tkinter.Canvas.winfo_height"),
        patch("tkinter.Spinbox.winfo_height"),
        patch("tkinter.ttk.Frame.winfo_height"),
        patch("tkinter.ttk.Label.winfo_height"),
        patch("tkinter.ttk.Button.winfo_height"),
        patch("tkinter.ttk.Entry.winfo_height"),
        patch("tkinter.ttk.Combobox.winfo_height"),
        patch("tkinter.ttk.Spinbox.winfo_height"),
        patch("tkinter.Label.winfo_children"),
        patch("tkinter.Button.winfo_children"),
        patch("tkinter.Entry.winfo_children"),
        patch("tkinter.Canvas.winfo_children"),
        patch("tkinter.Spinbox.winfo_children"),
        patch("tkinter.ttk.Frame.winfo_children"),
        patch("tkinter.ttk.Label.winfo_children"),
        patch("tkinter.ttk.Button.winfo_children"),
        patch("tkinter.ttk.Entry.winfo_children"),
        patch("tkinter.ttk.Combobox.winfo_children"),
        patch("tkinter.ttk.Spinbox.winfo_children"),
        patch("tkinter.Frame.winfo_children"),
        patch("tkinter.Frame.winfo_width"),
        patch("tkinter.Frame.winfo_height"),
        patch("tkinter.Frame.cget"),
        patch("tkinter.Frame.bind"),
        patch("tkinter.Label.bind"),
        patch("tkinter.Button.bind"),
        patch("tkinter.Entry.bind"),
        patch("tkinter.Canvas.bind"),
        patch("tkinter.Spinbox.bind"),
        patch("tkinter.ttk.Frame.bind"),
        patch("tkinter.ttk.Label.bind"),
        patch("tkinter.ttk.Button.bind"),
        patch("tkinter.ttk.Entry.bind"),
        patch("tkinter.ttk.Combobox.bind"),
        patch("tkinter.ttk.Spinbox.bind"),
        # Additional patches for TimePicker specific functionality
        patch("tkinter.Toplevel"),
        patch("tkinter.Toplevel.configure"),
        patch("tkinter.Toplevel.geometry"),
        patch("tkinter.Toplevel.title"),
        patch("tkinter.Toplevel.transient"),
        patch("tkinter.Toplevel.grab_set"),
        patch("tkinter.Toplevel.deiconify"),
        patch("tkinter.Toplevel.lift"),
        patch("tkinter.Toplevel.focus_set"),
        patch("tkinter.Toplevel.wait_window"),
        patch("tkinter.Toplevel.destroy"),
        patch("tkinter.Toplevel.winfo_toplevel"),
        patch("tkinter.Toplevel.winfo_rootx"),
        patch("tkinter.Toplevel.winfo_rooty"),
        patch("tkinter.Toplevel.winfo_width"),
        patch("tkinter.Toplevel.winfo_height"),
        patch("tkinter.Toplevel.update_idletasks"),
        patch("tkinter.Toplevel.update"),
        patch("tkinter.Toplevel.after"),
        patch("tkinter.Toplevel.bind"),
        patch("tkinter.Toplevel.event_generate"),
        patch("tkinter.Toplevel.focus_set"),
        patch("tkinter.Toplevel.clipboard_clear"),
        patch("tkinter.Toplevel.clipboard_append"),
        # DPI scaling patches
        # Note: DPI scaling is handled internally, no need to patch
        # Theme loading patches
        patch("tkface.dialog.timepicker._load_theme_colors", return_value={
            'time_background': 'white',
            'time_foreground': '#333333',
            'time_spinbox_bg': 'white'
        }),
        patch("tkface.widget.timespinner._load_theme", return_value={
            'time_background': 'white',
            'time_foreground': '#333333',
            'time_spinbox_bg': 'white'
        }),
        patch("tkface.widget.timespinner._get_default_theme", return_value={
            'time_background': 'white',
            'time_foreground': '#333333',
            'time_spinbox_bg': 'white'
        }),
    ]
    # Start all patches
    for p in patches:
        p.start()
    yield patches
    # Stop all patches
    for p in patches:
        p.stop()


@pytest.fixture
def timepicker_mock_widgets():
    """Provide mock widgets for TimePicker tests."""
    from unittest.mock import Mock

    # Create mock widgets
    mock_frame = Mock()
    mock_frame.config = Mock()
    mock_frame.cget = Mock(return_value="white")
    mock_frame.winfo_children = Mock(return_value=[])
    mock_frame._last_child_ids = {}
    mock_frame.tk = Mock()
    mock_frame._w = "."
    mock_frame.children = {}
    
    mock_label = Mock()
    mock_label.config = Mock()
    mock_label.cget = Mock(return_value="white")
    mock_label.winfo_children = Mock(return_value=[])
    
    mock_button = Mock()
    mock_button.config = Mock()
    mock_button.cget = Mock(return_value="white")
    mock_button.winfo_children = Mock(return_value=[])
    
    mock_entry = Mock()
    mock_entry.config = Mock()
    mock_entry.cget = Mock(return_value="white")
    mock_entry.winfo_children = Mock(return_value=[])
    mock_entry.get = Mock(return_value="")
    mock_entry.set = Mock()
    mock_entry.insert = Mock()
    mock_entry.delete = Mock()
    
    mock_canvas = Mock()
    mock_canvas.config = Mock()
    mock_canvas.cget = Mock(return_value="white")
    mock_canvas.winfo_children = Mock(return_value=[])
    mock_canvas.create_rectangle = Mock()
    mock_canvas.create_text = Mock()
    mock_canvas.create_line = Mock()
    mock_canvas.create_polygon = Mock()
    mock_canvas.delete = Mock()
    mock_canvas.coords = Mock()
    mock_canvas.itemconfig = Mock()
    mock_canvas.bind = Mock()
    mock_canvas.unbind = Mock()
    mock_canvas.focus_set = Mock()
    
    mock_spinbox = Mock()
    mock_spinbox.config = Mock()
    mock_spinbox.cget = Mock(return_value="white")
    mock_spinbox.winfo_children = Mock(return_value=[])
    mock_spinbox.get = Mock(return_value="0")
    mock_spinbox.set = Mock()
    mock_spinbox.bind = Mock()
    mock_spinbox.focus_set = Mock()
    
    return {
        "frame": mock_frame,
        "label": mock_label,
        "button": mock_button,
        "entry": mock_entry,
        "canvas": mock_canvas,
        "spinbox": mock_spinbox
    }


@pytest.fixture
def timepicker_theme_colors():
    """Provide theme colors for TimePicker tests."""
    return {
        'time_background': 'white',
        'time_foreground': '#333333',
        'time_spinbox_bg': 'white',
        'time_spinbox_fg': '#333333',
        'time_button_bg': '#f0f0f0',
        'time_button_fg': '#333333',
        'time_button_active_bg': '#e0e0e0',
        'time_button_active_fg': '#000000',
        'time_border': '#cccccc',
        'time_hover_bg': '#f5f5f5',
        'time_hover_fg': '#000000',
        'time_selected_bg': '#0078d4',
        'time_selected_fg': 'white'
    }


@pytest.fixture
def timepicker_mock_time():
    """Provide mock time objects for TimePicker tests."""
    import datetime
    return {
        'test_time': datetime.time(14, 30, 45),
        'test_time_12h': datetime.time(2, 30, 45),
        'test_time_midnight': datetime.time(0, 0, 0),
        'test_time_noon': datetime.time(12, 0, 0),
        'test_time_invalid': datetime.time(25, 70, 80)  # Invalid time for testing
    }


@pytest.fixture
def timepicker_mock_callbacks():
    """Provide mock callbacks for TimePicker tests."""
    callbacks = {
        'time_callback': Mock(),
        'ok_callback': Mock(),
        'cancel_callback': Mock(),
        'change_callback': Mock()
    }
    
    # Set up callback behavior
    def time_callback(time_obj):
        callbacks['time_callback'].call_count += 1
        callbacks['time_callback'].last_time = time_obj
    
    def ok_callback():
        callbacks['ok_callback'].call_count += 1
    
    def cancel_callback():
        callbacks['cancel_callback'].call_count += 1
    
    def change_callback():
        callbacks['change_callback'].call_count += 1
    
    callbacks['time_callback'].side_effect = time_callback
    callbacks['ok_callback'].side_effect = ok_callback
    callbacks['cancel_callback'].side_effect = cancel_callback
    callbacks['change_callback'].side_effect = change_callback
    
    return callbacks


@pytest.fixture
def timepicker_mock_events():
    """Provide mock events for TimePicker tests."""
    from unittest.mock import Mock
    
    def create_mock_event(event_type, **kwargs):
        event = Mock()
        event.type = event_type
        for key, value in kwargs.items():
            setattr(event, key, value)
        return event
    
    return {
        'mouse_click': create_mock_event('<Button-1>', x=50, y=50),
        'mouse_release': create_mock_event('<ButtonRelease-1>', x=50, y=50),
        'mouse_motion': create_mock_event('<Motion>', x=50, y=50),
        'mouse_wheel_up': create_mock_event('<MouseWheel>', delta=120, x=50, y=50),
        'mouse_wheel_down': create_mock_event('<MouseWheel>', delta=-120, x=50, y=50),
        'key_press': create_mock_event('<KeyPress>', keysym='Return', char='\r'),
        'key_release': create_mock_event('<KeyRelease>', keysym='Return', char='\r'),
        'focus_in': create_mock_event('<FocusIn>'),
        'focus_out': create_mock_event('<FocusOut>'),
        'enter': create_mock_event('<Enter>', x=50, y=50),
        'leave': create_mock_event('<Leave>', x=50, y=50)
    }


@pytest.fixture
def timepicker_complete_mock():
    """Provide complete mocking for TimePicker tests to prevent widget creation."""
    # Don't mock tkinter classes globally - this causes isinstance() issues
    # Instead, mock the specific methods that cause problems
    with patch("tkface.dialog.timepicker._load_theme_colors", return_value={
             'time_background': 'white',
             'time_foreground': '#333333',
             'time_spinbox_bg': 'white'
         }), \
         patch("tkface.widget.timespinner._load_theme", return_value={
             'time_background': 'white',
             'time_foreground': '#333333',
             'time_spinbox_bg': 'white'
         }), \
         patch("tkface.widget.timespinner._get_default_theme", return_value={
             'time_background': 'white',
             'time_foreground': '#333333',
             'time_spinbox_bg': 'white'
         }):
        # Just yield empty dict - let widgets be created normally
        # This avoids isinstance() issues with mocked classes
        yield {}

