import pytest
import tkinter as tk

@pytest.fixture(scope="session")
def root():
    """Create a root window for the tests."""
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        yield root
        root.destroy()
    except tk.TclError as e:
        if ("Can't find a usable tk.tcl" in str(e) or 
            "invalid command name" in str(e) or 
            "Can't find a usable init.tcl" in str(e)):
            pytest.skip("Tkinter not properly installed or Tcl/Tk files missing")
        else:
            raise 