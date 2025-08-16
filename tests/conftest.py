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
    ]
    # Start all patches
    for p in patches:
        p.start()
    yield patches
    # Stop all patches
    for p in patches:
        p.stop()


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
    for item in items:
        # Add gui marker to GUI tests
        if "messagebox" in item.nodeid or "calendar" in item.nodeid:
            item.add_marker(pytest.mark.gui)
