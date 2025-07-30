import pytest
import sys
from unittest.mock import patch, MagicMock
from tkface import win

def test_dpi_function_exists():
    """Test that dpi function exists."""
    assert hasattr(win, 'dpi')
    assert callable(win.dpi)

def test_unround_function_exists():
    """Test that unround function exists."""
    assert hasattr(win, 'unround')
    assert callable(win.unround)

def test_bell_function_exists():
    """Test that bell function exists."""
    assert hasattr(win, 'bell')
    assert callable(win.bell)

def test_dpi_function_no_error():
    """Test that dpi function doesn't raise errors."""
    try:
        win.dpi()
    except Exception as e:
        pytest.fail(f"win.dpi() raised {e} unexpectedly!")

def test_unround_function_no_error(root):
    """Test that unround function doesn't raise errors."""
    try:
        win.unround(root)
    except Exception as e:
        pytest.fail(f"win.unround() raised {e} unexpectedly!")

def test_bell_function_no_error():
    """Test that bell function doesn't raise errors."""
    try:
        win.bell()
    except Exception as e:
        pytest.fail(f"win.bell() raised {e} unexpectedly!")

@pytest.mark.parametrize("sound_type", ["error", "warning", "info", "question", "default"])
def test_bell_with_different_sound_types(sound_type):
    """Test bell function with different sound types."""
    try:
        result = win.bell(sound_type)
        # Should return boolean or None
        assert result is None or isinstance(result, bool)
    except Exception as e:
        pytest.fail(f"win.bell('{sound_type}') raised {e} unexpectedly!")

def test_bell_with_invalid_sound_type():
    """Test bell function with invalid sound type."""
    try:
        result = win.bell("invalid_sound")
        # Should handle invalid sound types gracefully
        assert result is None or isinstance(result, bool)
    except Exception as e:
        pytest.fail(f"win.bell('invalid_sound') raised {e} unexpectedly!")

@pytest.mark.skipif(sys.platform != 'win32', reason="Windows-specific test")
def test_dpi_on_windows():
    """Test DPI function on Windows platform."""
    # This test only runs on Windows
    win.dpi()
    # Should not raise any errors on Windows

@patch('sys.platform', 'darwin')
def test_dpi_on_non_windows():
    """Test DPI function on non-Windows platform."""
    # Should not raise any errors on non-Windows
    try:
        win.dpi()
    except Exception as e:
        pytest.fail(f"win.dpi() raised {e} on non-Windows platform!")

def test_get_scaling_factor_function_exists():
    """Test that get_scaling_factor function exists."""
    assert hasattr(win, 'get_scaling_factor')
    assert callable(win.get_scaling_factor)

def test_get_scaling_factor_returns_float(root):
    """Test that get_scaling_factor returns a float."""
    try:
        result = win.get_scaling_factor(root)
        assert isinstance(result, float)
        assert result > 0
    except Exception as e:
        pytest.fail(f"win.get_scaling_factor() raised {e} unexpectedly!")

def test_calculate_dpi_sizes_function_exists():
    """Test that calculate_dpi_sizes function exists."""
    assert hasattr(win, 'calculate_dpi_sizes')
    assert callable(win.calculate_dpi_sizes)

def test_calculate_dpi_sizes_returns_dict(root):
    """Test that calculate_dpi_sizes returns a dictionary."""
    base_sizes = {"width": 100, "height": 200}
    try:
        result = win.calculate_dpi_sizes(base_sizes, root)
        assert isinstance(result, dict)
        assert "width" in result
        assert "height" in result
    except Exception as e:
        pytest.fail(f"win.calculate_dpi_sizes() raised {e} unexpectedly!")

def test_scale_icon_function_exists():
    """Test that scale_icon function exists."""
    assert hasattr(win, 'scale_icon')
    assert callable(win.scale_icon)

def test_scale_icon_returns_string(root):
    """Test that scale_icon returns a string."""
    try:
        result = win.scale_icon("error", root)
        assert isinstance(result, str)
    except Exception as e:
        pytest.fail(f"win.scale_icon() raised {e} unexpectedly!") 