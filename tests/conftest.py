import pytest
import tkinter as tk
import os

@pytest.fixture(scope="function")
def root():
    """Create a root window for the tests."""
    try:
        # テーマ関連のエラーを回避
        os.environ['TK_SILENCE_DEPRECATION'] = '1'
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        yield root
        root.destroy()
    except tk.TclError as e:
        error_str = str(e)
        if any(pattern in error_str for pattern in [
            "Can't find a usable tk.tcl",
            "invalid command name",
            "Can't find a usable init.tcl",
            "vistaTheme.tcl",
            "init.tcl",
            "No error",
            "fonts.tcl",
            "icons.tcl",
            "tk.tcl"
        ]):
            pytest.skip(f"Tkinter not properly installed or Tcl/Tk files missing: {error_str}")
        else:
            raise 