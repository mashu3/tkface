"""
Tests for tkface.win.bell module.

This module contains tests for Windows-specific bell functionality including
system sound playback and error handling.
"""

import sys
from unittest.mock import patch

import pytest

from tkface import win


def test_bell_function_exists():
    """Test that bell function exists."""
    assert hasattr(win, "bell")
    assert callable(win.bell)


def test_bell_function_no_error():
    """Test that bell function doesn't raise errors."""
    try:
        win.bell()
    except (AttributeError, TypeError, ValueError) as e:
        pytest.fail(f"win.bell() raised {e} unexpectedly!")


@pytest.mark.parametrize(
    "sound_type", ["error", "warning", "info", "question", "default"]
)
def test_bell_with_different_sound_types(sound_type):
    """Test bell function with different sound types."""
    try:
        result = win.bell(sound_type)
        # Should return boolean or None
        assert result is None or isinstance(result, bool)
    except (AttributeError, TypeError, ValueError) as e:
        pytest.fail(f"win.bell('{sound_type}') raised {e} unexpectedly!")


def test_bell_with_invalid_sound_type():
    """Test bell function with invalid sound type."""
    try:
        result = win.bell("invalid_sound")
        # Should handle invalid sound types gracefully
        assert result is None or isinstance(result, bool)
    except (AttributeError, TypeError, ValueError) as e:
        pytest.fail(f"win.bell('invalid_sound') raised {e} unexpectedly!")


# Additional tests for better coverage


def test_bell_sound_constants():
    """Test that bell sound constants are defined correctly."""
    from tkface.win.bell import (
        MB_ICONASTERISK,
        MB_ICONEXCLAMATION,
        MB_ICONHAND,
        MB_ICONQUESTION,
        MB_OK,
    )
    assert MB_ICONASTERISK == 0x00000040
    assert MB_ICONEXCLAMATION == 0x00000030
    assert MB_ICONHAND == 0x00000010
    assert MB_ICONQUESTION == 0x00000020
    assert MB_OK == 0x00000000




@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
@patch("ctypes.windll.user32.MessageBeep")
def test_bell_messagebeep_success(mock_messagebeep):
    """Test bell function when MessageBeep succeeds."""
    mock_messagebeep.return_value = 1
    from tkface.win.bell import bell
    result = bell("error")
    assert result is True
    mock_messagebeep.assert_called_once()


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
@patch("ctypes.windll.user32.MessageBeep")
def test_bell_messagebeep_failure(mock_messagebeep):
    """Test bell function when MessageBeep fails."""
    mock_messagebeep.return_value = 0
    from tkface.win.bell import bell
    result = bell("error")
    assert result is False
    mock_messagebeep.assert_called_once()


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
@patch("ctypes.windll.user32.MessageBeep", side_effect=OSError("API Error"))
def test_bell_messagebeep_exception_fallback(mock_messagebeep):
    """Test bell function fallback when MessageBeep raises exception."""
    from tkface.win.bell import bell
    result = bell("error")
    # Should return False when both attempts fail
    assert result is False
    # Should be called twice: once for the specific sound, once for fallback
    assert mock_messagebeep.call_count == 2


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
@patch("ctypes.windll.user32.MessageBeep", side_effect=AttributeError("No windll"))
def test_bell_no_windll(mock_messagebeep):
    """Test bell function when windll is not available."""
    from tkface.win.bell import bell
    result = bell("error")
    assert result is False


def test_bell_sound_type_mapping():
    """Test that all sound types are mapped correctly."""
    from tkface.win.bell import bell
    sound_types = ["error", "warning", "info", "question", "default"]
    for sound_type in sound_types:
        # Should not raise any exceptions
        try:
            bell(sound_type)
        except Exception as e:
            pytest.fail(f"bell('{sound_type}') raised {e} unexpectedly!")


def test_bell_case_insensitive():
    """Test that bell function handles case insensitive sound types."""
    from tkface.win.bell import bell

    # Should not raise any exceptions for uppercase
    try:
        bell("ERROR")
        bell("WARNING")
        bell("INFO")
        bell("QUESTION")
        bell("DEFAULT")
    except Exception as e:
        pytest.fail(f"bell with uppercase sound type raised {e} unexpectedly!")


# Additional tests to increase coverage for tkface.win.bell
def test_is_windows_type_and_behavior():
    """is_windows returns bool and reflects platform correctly."""
    from tkface.win.bell import is_windows

    result = is_windows()
    assert isinstance(result, bool)
    if sys.platform == "win32":
        assert result is True
    else:
        assert result is False


@patch("sys.platform", "darwin")
def test_bell_non_windows_returns_false():
    """bell should return False on non-Windows without calling MessageBeep."""
    from tkface.win.bell import bell

    assert bell("error") is False


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_bell_invalid_type_maps_to_default():
    """Invalid sound types should fall back to MB_OK (default)."""
    from tkface.win.bell import MB_OK, bell

    with patch("ctypes.windll.user32.MessageBeep") as mock_beep:
        mock_beep.return_value = 1
        assert bell("not-a-type") is True
        # The called arg should be MB_OK
        called_arg = mock_beep.call_args[0][0]
        assert called_arg == MB_OK


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_bell_case_insensitive_types():
    """Upper/mixed case types should be handled via .lower()."""
    from tkface.win.bell import bell

    with patch("ctypes.windll.user32.MessageBeep") as mock_beep:
        mock_beep.return_value = 1
        assert bell("ERROR") is True
        assert bell("WarNing") is True
        assert bell("INFO") is True
        assert bell("QuestIoN") is True
        assert bell("DEFAULT") is True


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_bell_messagebeep_raises_then_fallback_fails():
    """When MessageBeep raises, fallback attempt also fails -> False."""
    from tkface.win.bell import bell

    with patch("ctypes.windll.user32.MessageBeep", side_effect=OSError("boom")) as mock_beep:
        # First call (mapped sound) raises; second call (fallback MB_OK) raises too
        assert bell("error") is False
        # Called twice due to fallback
        assert mock_beep.call_count == 2


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_bell_messagebeep_attribute_error_then_fallback_attribute_error():
    """Both primary and fallback attempts raising AttributeError -> False."""
    from tkface.win.bell import bell

    with patch("ctypes.windll.user32.MessageBeep", side_effect=AttributeError("no api")) as mock_beep:
        assert bell("warning") is False
        assert mock_beep.call_count == 2