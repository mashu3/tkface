import pytest
import tkinter as tk

@pytest.fixture(scope="function")
def root():
    """Create a root window for the tests."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    yield root
    root.destroy() 