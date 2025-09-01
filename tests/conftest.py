import gc
import logging
import os
import threading
import time
import tkinter as tk
from unittest.mock import patch

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
