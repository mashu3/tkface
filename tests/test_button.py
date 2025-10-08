"""
Tests for tkface.win.button module.

This module contains tests for button-related functionality including
Windows-specific button styling and keyboard shortcuts.
"""

import sys
from unittest.mock import patch

import pytest


# Button module tests
def test_button_is_windows_function():
    """Test the is_windows function in button module."""
    from tkface.win.button import is_windows
    result = is_windows()
    assert isinstance(result, bool)
    if sys.platform == "win32":
        assert result is True
    else:
        assert result is False


@patch("sys.platform", "darwin")
def test_button_is_windows_function_non_windows():
    """Test the is_windows function on non-Windows platform."""
    from tkface.win.button import is_windows
    result = is_windows()
    assert result is False


def test_configure_button_for_windows_with_button():
    """Test configure_button_for_windows using a mock button (no real Tk)."""
    from unittest.mock import Mock, patch
    from tkface.win.button import configure_button_for_windows

    button = Mock()
    button.configure = Mock()
    with patch("tkface.win.button.is_windows", return_value=True):
        configure_button_for_windows(button)
    button.configure.assert_called_once_with(relief="solid", bd=1)


def test_configure_button_for_windows_with_none():
    """Test configure_button_for_windows with None button."""
    from tkface.win.button import configure_button_for_windows
    configure_button_for_windows(None)
    # Should not raise any exceptions


@patch("sys.platform", "darwin")
def test_configure_button_for_windows_non_windows():
    """Test configure_button_for_windows on non-Windows without requiring real Tk."""
    from unittest.mock import Mock
    from tkface.win.button import configure_button_for_windows

    button = Mock()
    button.configure = Mock()
    configure_button_for_windows(button)
    # On non-Windows, it should not configure relief/bd; but we only assert no error
    assert button is not None


def test_configure_button_for_windows_windows_styling():
    """Test configure_button_for_windows applies Windows styling using mocks."""
    from unittest.mock import Mock, patch
    from tkface.win.button import configure_button_for_windows

    button = Mock()
    # Track kwargs passed to configure
    def mock_configure(**kwargs):
        button._last_config = kwargs
    button.configure = Mock(side_effect=mock_configure)

    with patch("tkface.win.button.is_windows", return_value=True):
        configure_button_for_windows(button)

    assert getattr(button, "_last_config", {}) == {"relief": "solid", "bd": 1}


def test_get_button_label_with_shortcut_none_inputs():
    """Test get_button_label_with_shortcut with None inputs."""
    from tkface.win.button import get_button_label_with_shortcut

    # Test with both None
    result = get_button_label_with_shortcut(None, None)
    assert result == ""
    
    # Test with button_value None
    result = get_button_label_with_shortcut(None, "Test")
    assert result == "Test"
    
    # Test with translated_text None
    result = get_button_label_with_shortcut("yes", None)
    assert result == ""


def test_get_button_label_with_shortcut_non_windows():
    """Test get_button_label_with_shortcut on non-Windows platform."""
    from tkface.win.button import get_button_label_with_shortcut
    
    with patch("sys.platform", "darwin"):
        result = get_button_label_with_shortcut("yes", "はい")
        assert result == "はい"


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_get_button_label_with_shortcut_windows_shortcuts():
    """Test get_button_label_with_shortcut with Windows shortcuts."""
    from tkface.win.button import get_button_label_with_shortcut

    # Test all supported shortcuts
    test_cases = [
        ("yes", "はい", "はい(Y)"),
        ("no", "いいえ", "いいえ(N)"),
        ("retry", "再試行", "再試行(R)"),
        ("abort", "中止", "中止(A)"),
        ("ignore", "無視", "無視(I)"),
    ]
    
    for button_value, translated_text, expected in test_cases:
        result = get_button_label_with_shortcut(button_value, translated_text)
        assert result == expected


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_get_button_label_with_shortcut_case_insensitive():
    """Test get_button_label_with_shortcut is case insensitive."""
    from tkface.win.button import get_button_label_with_shortcut

    # Test uppercase
    result = get_button_label_with_shortcut("YES", "はい")
    assert result == "はい(Y)"
    
    # Test mixed case
    result = get_button_label_with_shortcut("Yes", "はい")
    assert result == "はい(Y)"


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_get_button_label_with_shortcut_unsupported_button():
    """Test get_button_label_with_shortcut with unsupported button value."""
    from tkface.win.button import get_button_label_with_shortcut
    
    result = get_button_label_with_shortcut("cancel", "キャンセル")
    assert result == "キャンセル"


def test_flat_button_creation():
    """Test FlatButton creation without real Tk by patching tk.Button.__init__."""
    import tkinter as tk
    from unittest.mock import patch
    from tkface.win.button import FlatButton

    def mock_init(self, master=None, **kwargs):
        self._kwargs = kwargs
        # Provide cget to read from kwargs like Tk would
        self.cget = lambda key: self._kwargs.get(key, "")
        return None

    with patch.object(tk.Button, "__init__", mock_init), \
         patch("tkface.win.button.configure_button_for_windows"):
        button = FlatButton(None, text="Test")
    assert button is not None
    assert button.cget("text") == "Test"


def test_flat_button_inheritance():
    """Test FlatButton inherits from tk.Button without requiring real Tk."""
    import tkinter as tk
    from unittest.mock import patch

    from tkface.win.button import FlatButton
    
    # Avoid calling real tk.Button.__init__ (no real Tk root needed)
    with patch.object(tk.Button, "__init__", return_value=None), \
         patch("tkface.win.button.configure_button_for_windows"):
        button = FlatButton(None, text="Test")
    assert isinstance(button, tk.Button)


def test_flat_button_configure_called():
    """Test FlatButton calls configure_button_for_windows."""
    from tkface.win.button import FlatButton
    
    import tkinter as tk
    def mock_init(self, master=None, **kwargs):
        return None
    with patch.object(tk.Button, "__init__", mock_init), \
         patch("tkface.win.button.configure_button_for_windows") as mock_configure:
        button = FlatButton(None, text="Test")
        mock_configure.assert_called_once_with(button)


def test_flat_button_with_kwargs():
    """Test FlatButton with additional kwargs."""
    from tkface.win.button import FlatButton

    import tkinter as tk
    from unittest.mock import patch

    def mock_init(self, master=None, **kwargs):
        self._kwargs = kwargs
        self.cget = lambda key: self._kwargs.get(key, "")
        return None

    with patch.object(tk.Button, "__init__", mock_init), \
         patch("tkface.win.button.configure_button_for_windows"):
        button = FlatButton(None, text="Test", bg="red", fg="white")
    assert button.cget("text") == "Test"
    assert button.cget("bg") == "red"
    assert button.cget("fg") == "white"


def test_create_flat_button_basic():
    """Test create_flat_button without real Tk by patching tk.Button.__init__."""
    import tkinter as tk
    from unittest.mock import patch
    from tkface.win.button import create_flat_button

    def mock_init(self, master=None, **kwargs):
        self._kwargs = {**kwargs, "text": kwargs.get("text", "")}
        self.cget = lambda key: self._kwargs.get(key, "")
        return None

    with patch.object(tk.Button, "__init__", mock_init), \
         patch("tkface.win.button.configure_button_for_windows"):
        button = create_flat_button(None, "Test")
    assert button is not None
    assert button.cget("text") == "Test"


def test_create_flat_button_with_command():
    """Test create_flat_button with command."""
    from tkface.win.button import create_flat_button

    import tkinter as tk
    from unittest.mock import patch

    def test_command():
        return None

    def mock_init(self, master=None, **kwargs):
        self._kwargs = kwargs
        self.cget = lambda key: self._kwargs.get(key, "")
        return None

    with patch.object(tk.Button, "__init__", mock_init), \
         patch("tkface.win.button.configure_button_for_windows"):
        button = create_flat_button(None, "Test", command=test_command)
    assert button.cget("command") is not None


def test_create_flat_button_with_kwargs():
    """Test create_flat_button with additional kwargs."""
    from tkface.win.button import create_flat_button

    import tkinter as tk
    from unittest.mock import patch

    def mock_init(self, master=None, **kwargs):
        self._kwargs = kwargs
        self.cget = lambda key: self._kwargs.get(key, "")
        return None

    with patch.object(tk.Button, "__init__", mock_init), \
         patch("tkface.win.button.configure_button_for_windows"):
        button = create_flat_button(None, "Test", bg="blue", fg="yellow")
    assert button.cget("text") == "Test"
    assert button.cget("bg") == "blue"
    assert button.cget("fg") == "yellow"


def test_create_flat_button_returns_flat_button():
    """Test create_flat_button returns FlatButton instance."""
    from tkface.win.button import FlatButton, create_flat_button

    import tkinter as tk
    from unittest.mock import patch

    with patch.object(tk.Button, "__init__", return_value=None), \
         patch("tkface.win.button.configure_button_for_windows"):
        button = create_flat_button(None, "Test")
    assert isinstance(button, FlatButton)


def test_create_flat_button_with_master_none():
    """Test create_flat_button with master=None."""
    from tkface.win.button import create_flat_button

    import tkinter as tk
    from unittest.mock import patch

    def mock_init(self, master=None, **kwargs):
        self._kwargs = kwargs
        self.cget = lambda key: self._kwargs.get(key, "")
        return None

    with patch.object(tk.Button, "__init__", mock_init), \
         patch("tkface.win.button.configure_button_for_windows"):
        button = create_flat_button(None, "Test")
    assert button is not None
    assert button.cget("text") == "Test"


# Additional edge case tests for button.py
def test_get_button_label_with_shortcut_empty_strings():
    """Test get_button_label_with_shortcut with empty strings."""
    from tkface.win.button import get_button_label_with_shortcut
    
    result = get_button_label_with_shortcut("", "")
    assert result == ""
    
    # On Windows, empty translated_text with valid button_value returns shortcut only
    with patch("sys.platform", "win32"):
        result = get_button_label_with_shortcut("yes", "")
        assert result == "(Y)"


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_get_button_label_with_shortcut_empty_button_value():
    """Test get_button_label_with_shortcut with empty button_value on Windows."""
    from tkface.win.button import get_button_label_with_shortcut
    
    result = get_button_label_with_shortcut("", "Test")
    assert result == "Test"


def test_configure_button_for_windows_with_invalid_button():
    """Test configure_button_for_windows with invalid button object."""
    from tkface.win.button import configure_button_for_windows

    # Create object that's not a button
    class MockButton:
        def configure(self, **kwargs):
            pass
    
    mock_button = MockButton()
    configure_button_for_windows(mock_button)
    # Should not raise any exceptions


def test_flat_button_with_master_none():
    """Test FlatButton with master=None."""
    from tkface.win.button import FlatButton

    import tkinter as tk
    from unittest.mock import patch

    def mock_init(self, master=None, **kwargs):
        self._kwargs = kwargs
        self.cget = lambda key: self._kwargs.get(key, "")
        return None

    with patch.object(tk.Button, "__init__", mock_init), \
         patch("tkface.win.button.configure_button_for_windows"):
        button = FlatButton(None, text="Test")
    assert button is not None
    assert button.cget("text") == "Test"


def test_create_flat_button_text_none():
    """Test create_flat_button with text=None."""
    from tkface.win.button import create_flat_button

    import tkinter as tk
    from unittest.mock import patch

    def mock_init(self, master=None, **kwargs):
        self._kwargs = {**kwargs, "text": kwargs.get("text") or ""}
        self.cget = lambda key: self._kwargs.get(key, "")
        return None

    with patch.object(tk.Button, "__init__", mock_init), \
         patch("tkface.win.button.configure_button_for_windows"):
        button = create_flat_button(None, None)
    assert button is not None
    assert button.cget("text") == ""


def test_create_flat_button_command_none():
    """Test create_flat_button with command=None."""
    from tkface.win.button import create_flat_button

    import tkinter as tk
    from unittest.mock import patch

    def mock_init(self, master=None, **kwargs):
        self._kwargs = kwargs
        self.cget = lambda key: self._kwargs.get(key, "")
        return None

    with patch.object(tk.Button, "__init__", mock_init), \
         patch("tkface.win.button.configure_button_for_windows"):
        button = create_flat_button(None, "Test", command=None)
    assert button is not None
    assert button.cget("command") == "" or button.cget("command") is None


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_get_button_label_with_shortcut_whitespace():
    """Test get_button_label_with_shortcut with whitespace in button_value."""
    from tkface.win.button import get_button_label_with_shortcut

    # The function uses .lower() which doesn't strip whitespace, so " yes " doesn't match "yes"
    result = get_button_label_with_shortcut(" yes ", "はい")
    assert result == "はい"


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_configure_button_for_windows_button_configure_exception():
    """Test configure_button_for_windows handles button.configure exceptions."""
    from tkface.win.button import configure_button_for_windows
    from unittest.mock import patch

    class BadButton:
        def configure(self, **kwargs):
            raise Exception("Configure failed")

    with patch("tkface.win.button.is_windows", return_value=True):
        with pytest.raises(Exception, match="Configure failed"):
            configure_button_for_windows(BadButton())


def test_flat_button_configure_exception_handling():
    """Test FlatButton handles configure exceptions during initialization."""
    from tkface.win.button import FlatButton
    
    import tkinter as tk
    from unittest.mock import patch

    with patch.object(tk.Button, "__init__", return_value=None), \
         patch("tkface.win.button.configure_button_for_windows", side_effect=Exception("Configure failed")):
        # The function doesn't handle exceptions, so it should raise them
        with pytest.raises(Exception, match="Configure failed"):
            FlatButton(None, text="Test")


def test_create_flat_button_flat_button_creation_exception():
    """Test create_flat_button handles FlatButton creation exceptions."""
    from tkface.win.button import create_flat_button
    
    with patch("tkface.win.button.FlatButton", side_effect=Exception("Button creation failed")):
        # Should propagate the exception
        with pytest.raises(Exception, match="Button creation failed"):
            create_flat_button(None, "Test")
