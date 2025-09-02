import gc
import logging
import os
import threading
import time
import tkinter as tk
from unittest.mock import patch, Mock, MagicMock

import pytest

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
                except (tk.TclError, AttributeError):
                    pass
            # Destroy the main window
            _TK_ROOT.destroy()
        except tk.TclError:
            pass
        except Exception:  # pylint: disable=W0718
            pass
        finally:
            _TK_ROOT = None
            _TK_INITIALIZED = False
    # Force garbage collection
    gc.collect()
    # Short wait for resource cleanup
    time.sleep(0.1)


@pytest.fixture(scope="session")
def root():
    """Create a root window for the tests with session scope
    for better parallel execution."""
    global _TK_ROOT, _TK_INITIALIZED  # pylint: disable=global-statement
    with _TK_LOCK:
        try:
            # Set environment variables
            os.environ["TK_SILENCE_DEPRECATION"] = "1"
            os.environ["PYTHONUNBUFFERED"] = "1"
            # Clean up existing instance
            if _TK_INITIALIZED:
                _cleanup_tkinter()
            # Create new root window
            _TK_ROOT = tk.Tk()
            _TK_ROOT.withdraw()  # Hide the main window
            # Force window updates
            _TK_ROOT.update()
            _TK_ROOT.update_idletasks()
            _TK_INITIALIZED = True
            yield _TK_ROOT
            # Clean up after session
            _cleanup_tkinter()
        except tk.TclError as e:
            error_str = str(e)
            if any(
                pattern in error_str
                for pattern in [
                    "Can't find a usable tk.tcl",
                    "invalid command name",
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
            _cleanup_tkinter()
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
        yield temp_root
        # Cleanup
        try:
            temp_root.destroy()
        except tk.TclError:
            pass
    except tk.TclError as e:
        error_str = str(e)
        if any(
            pattern in error_str
            for pattern in [
                "Can't find a usable tk.tcl",
                "invalid command name",
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
    import tempfile  # pylint: disable=import-outside-toplevel
    import shutil  # pylint: disable=import-outside-toplevel

    temp_dir_path = tempfile.mkdtemp()  # pylint: disable=redefined-outer-name
    yield temp_dir_path
    # Cleanup
    try:
        shutil.rmtree(temp_dir_path, ignore_errors=True)
    except Exception:  # pylint: disable=W0718
        pass


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
