"""Additional tests to increase coverage for tkface.win.bell."""

import sys
from unittest.mock import patch

import pytest


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
    from tkface.win.bell import bell, MB_OK

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


