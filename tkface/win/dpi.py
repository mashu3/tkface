import sys

def dpi():
    """
    Enable DPI awareness on Windows.
    Does nothing on other OSes.
    """
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)  # SYSTEM_AWARE
        except Exception:
            pass 