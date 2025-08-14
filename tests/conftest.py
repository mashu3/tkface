import gc
import logging
import os
import threading
import time
import tkinter as tk
import pytest
from unittest.mock import patch

# Global Tkinter instance management
_tk_root = None
_tk_lock = threading.Lock()
_tk_initialized = False


def _cleanup_tkinter():
    """Clean up Tkinter resources safely."""
    global _tk_root, _tk_initialized
    if _tk_root is not None:
        try:
            # Destroy all child windows
            for widget in _tk_root.winfo_children():
                try:
                    widget.destroy()
                except (tk.TclError, AttributeError):
                    pass
            # Destroy the main window
            _tk_root.destroy()
        except tk.TclError:
            pass
        except Exception:
            pass
        finally:
            _tk_root = None
            _tk_initialized = False
    # Force garbage collection
    gc.collect()
    # Short wait for resource cleanup
    time.sleep(0.1)


@pytest.fixture(scope="session")
def root():
    """Create a root window for the tests with session scope for better parallel execution."""
    global _tk_root, _tk_initialized
    with _tk_lock:
        try:
            # Set environment variables
            os.environ["TK_SILENCE_DEPRECATION"] = "1"
            os.environ["PYTHONUNBUFFERED"] = "1"
            # Clean up existing instance
            if _tk_initialized:
                _cleanup_tkinter()
            # Create new root window
            _tk_root = tk.Tk()
            _tk_root.withdraw()  # Hide the main window
            # Force window updates
            _tk_root.update()
            _tk_root.update_idletasks()
            _tk_initialized = True
            yield _tk_root
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
                ]
            ):
                pytest.skip(
                    f"Tkinter not properly installed or Tcl/Tk files missing: {error_str}"
                )
            else:
                raise
        except Exception:
            # Try cleanup for unexpected errors
            _cleanup_tkinter()
            raise


@pytest.fixture(scope="session", autouse=True)
def cleanup_session():
    """Clean up Tkinter resources after all tests complete."""
    yield
    with _tk_lock:
        _cleanup_tkinter()


@pytest.fixture(scope="function")
def root_function():
    """Create a temporary root window for individual function tests."""
    try:
        # Set environment variables
        os.environ["TK_SILENCE_DEPRECATION"] = "1"
        # Create new root window
        temp_root = tk.Tk()
        temp_root.withdraw()
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
            ]
        ):
            pytest.skip(
                f"Tkinter not properly installed or Tcl/Tk files missing: {error_str}"
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
    ]
    # Start all patches
    for p in patches:
        p.start()
    yield patches
    # Stop all patches
    for p in patches:
        p.stop()


# Configuration for parallel testing


def pytest_configure(config):
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


def pytest_collection_modifyitems(config, items):
    """Modify test collection for better parallel execution."""
    for item in items:
        # Add gui marker to GUI tests
        if "messagebox" in item.nodeid or "calendar" in item.nodeid:
            item.add_marker(pytest.mark.gui)
