"""Tests for tkface TimePicker widget components."""

import datetime
import tkinter as tk
from unittest.mock import patch, MagicMock
import pytest

from tkface.widget.timespinner import TimeSpinner, CanvasSpinbox, CanvasAMPMSpinbox, _load_theme, _get_default_theme


@pytest.fixture(scope="function")
def root_function():
    """Create a temporary root window for individual function tests."""
    try:
        # Set environment variables
        import os
        os.environ["TK_SILENCE_DEPRECATION"] = "1"
        # Create new root window
        temp_root = tk.Tk()
        temp_root.withdraw()  # Hide the main window
        temp_root.update()
        yield temp_root
        # Cleanup
        try:
            temp_root.destroy()
        except tk.TclError as e:
            # Window may already be destroyed
            import logging
            logging.debug(f"Failed to destroy temporary root window: {e}")
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
                "auto.tcl",
                "No error",
                "fonts.tcl",
                "icons.tcl",
                "tk.tcl",
                "no display name and no $DISPLAY environment variable",
                "no display name",
                "$DISPLAY environment variable",
                "application has been destroyed",
            ]
        ):
            pytest.skip(
                f"Tkinter not properly installed or display not available: "
                f"{error_str}"
            )
        else:
            raise


class TestTimeSpinner:
    """Test TimeSpinner widget."""
    
    def test_timespinner_creation_default(self, root_function, timepicker_complete_mock):
        """Test TimeSpinner creation with default parameters."""
        spinner = TimeSpinner(root_function)
        assert spinner.hour_format == "24"
        assert spinner.show_seconds is True
        assert spinner.theme == "light"
        assert spinner.selected_time is not None
        assert isinstance(spinner.selected_time, datetime.time)
    
    def test_timespinner_creation_custom(self, root_function, timepicker_complete_mock):
        """Test TimeSpinner creation with custom parameters."""
        test_time = datetime.time(14, 30, 45)
        spinner = TimeSpinner(
            root_function,
            hour_format="12",
            show_seconds=False,
            theme="dark",
            initial_time=test_time
        )
        assert spinner.hour_format == "12"
        assert spinner.show_seconds is False
        assert spinner.theme == "dark"
        assert spinner.selected_time == test_time
    
    def test_timespinner_get_selected_time(self, root_function, timepicker_complete_mock):
        """Test get_selected_time method."""
        test_time = datetime.time(14, 30, 45)
        spinner = TimeSpinner(root_function, initial_time=test_time)
        assert spinner.get_selected_time() == test_time
    
    def test_timespinner_set_selected_time(self, root_function, timepicker_complete_mock):
        """Test set_selected_time method."""
        spinner = TimeSpinner(root_function)
        test_time = datetime.time(14, 30, 45)
        spinner.set_selected_time(test_time)
        assert spinner.selected_time == test_time
    
    def test_timespinner_set_hour_format(self, root_function, timepicker_complete_mock):
        """Test set_hour_format method."""
        spinner = TimeSpinner(root_function)
        spinner.set_hour_format("12")
        assert spinner.hour_format == "12"
        
        spinner.set_hour_format("24")
        assert spinner.hour_format == "24"
    
    def test_timespinner_set_show_seconds(self, root_function, timepicker_complete_mock):
        """Test set_show_seconds method."""
        spinner = TimeSpinner(root_function)
        spinner.set_show_seconds(False)
        assert spinner.show_seconds is False
        
        spinner.set_show_seconds(True)
        assert spinner.show_seconds is True
    
    def test_timespinner_set_theme(self, root_function, timepicker_complete_mock):
        """Test set_theme method."""
        spinner = TimeSpinner(root_function)
        spinner.set_theme("dark")
        assert spinner.theme == "dark"
        assert spinner.bg_color is not None
    
    def test_timespinner_time_change_12h(self, root_function, timepicker_complete_mock):
        """Test time change handling in 12-hour format."""
        spinner = TimeSpinner(root_function, hour_format="12")
        # Simulate time change
        spinner._on_time_change()
        assert spinner.selected_time is not None
    
    def test_timespinner_time_change_24h(self, root_function, timepicker_complete_mock):
        """Test time change handling in 24-hour format."""
        spinner = TimeSpinner(root_function, hour_format="24")
        # Simulate time change
        spinner._on_time_change()
        assert spinner.selected_time is not None
    
    def test_timespinner_ok_callback(self, root_function, timepicker_complete_mock):
        """Test OK button callback."""
        callback_called = []
        def test_callback(time_obj):
            callback_called.append(time_obj)
        
        spinner = TimeSpinner(root_function, time_callback=test_callback)
        spinner._on_ok()
        assert len(callback_called) == 1
        assert callback_called[0] is not None
    
    def test_timespinner_cancel_callback(self, root_function, timepicker_complete_mock):
        """Test Cancel button callback."""
        callback_called = []
        def test_callback(time_obj):
            callback_called.append(time_obj)
        
        spinner = TimeSpinner(root_function, time_callback=test_callback)
        spinner._on_cancel()
        assert len(callback_called) == 1
        assert callback_called[0] is None

    def test_timespinner_toggle_format(self, root_function, timepicker_complete_mock):
        """Test format toggle functionality."""
        spinner = TimeSpinner(root_function, hour_format="24")
        assert spinner.hour_format == "24"
        
        spinner._toggle_format()
        assert spinner.hour_format == "12"
        
        spinner._toggle_format()
        assert spinner.hour_format == "24"
    
    def test_timespinner_mouse_wheel(self, root_function, timepicker_complete_mock):
        """Test mouse wheel handling."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        spinbox = CanvasSpinbox(
            canvas, 10, 10, 50, 50,
            from_=0, to=59, value=30
        )
        
        # Test mouse wheel up
        event = MagicMock()
        event.delta = 120  # Positive delta for up
        spinbox._on_mouse_wheel(event)
        assert spinbox.get() == 31
        
        # Test mouse wheel down
        event.delta = -120  # Negative delta for down
        spinbox._on_mouse_wheel(event)
        assert spinbox.get() == 30
    
    def test_timespinner_hover_effects(self, root_function, timepicker_complete_mock):
        """Test hover effects on spinbox."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        spinbox = CanvasSpinbox(
            canvas, 10, 10, 50, 50,
            from_=0, to=59, value=30
        )
        
        # Test hover on up button
        spinbox._on_hover_up(True)
        # Should not raise exception
        
        spinbox._on_hover_up(False)
        # Should not raise exception
        
        # Test hover on down button
        spinbox._on_hover_down(True)
        # Should not raise exception
        
        spinbox._on_hover_down(False)
        # Should not raise exception
    
    def test_timespinner_ampm_hover_effects(self, root_function, timepicker_complete_mock):
        """Test hover effects on AM/PM spinbox."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        spinbox = CanvasAMPMSpinbox(
            canvas, 10, 10, 50, 50,
            value="AM"
        )
        
        # Test hover on up button
        spinbox._on_hover_up(True)
        # Should not raise exception
        
        spinbox._on_hover_up(False)
        # Should not raise exception
        
        # Test hover on down button
        spinbox._on_hover_down(True)
        # Should not raise exception
        
        spinbox._on_hover_down(False)
        # Should not raise exception

    def test_timespinner_time_change_invalid_time(self, root_function, timepicker_complete_mock):
        """Test time change with invalid time."""
        spinner = TimeSpinner(root_function)
        spinner.hour_spinbox = MagicMock()
        spinner.hour_spinbox.get.return_value = 25  # Invalid hour
        spinner.minute_spinbox = MagicMock()
        spinner.minute_spinbox.get.return_value = 30
        spinner.second_spinbox = MagicMock()
        spinner.second_spinbox.get.return_value = 45
        
        # Should not raise exception
        spinner._on_time_change()
    
    def test_timespinner_time_change_missing_spinboxes(self, root_function, timepicker_complete_mock):
        """Test time change with missing spinboxes."""
        spinner = TimeSpinner(root_function)
        spinner.hour_spinbox = None
        spinner.minute_spinbox = None
        spinner.second_spinbox = None
        
        # Should not raise exception
        spinner._on_time_change()
    
    def test_timespinner_time_change_12h_with_am_pm(self, root_function, timepicker_complete_mock):
        """Test time change in 12h format with AM/PM."""
        spinner = TimeSpinner(root_function, hour_format="12")
        spinner.hour_spinbox = MagicMock()
        spinner.hour_spinbox.get.return_value = 2
        spinner.minute_spinbox = MagicMock()
        spinner.minute_spinbox.get.return_value = 30
        spinner.second_spinbox = MagicMock()
        spinner.second_spinbox.get.return_value = 45
        spinner.am_pm_spinbox = MagicMock()
        spinner.am_pm_spinbox.get.return_value = "PM"
        
        spinner._on_time_change()
        assert spinner.selected_time.hour == 14  # 2 PM = 14:00
    
    def test_timespinner_time_change_12h_am_midnight(self, root_function, timepicker_complete_mock):
        """Test time change in 12h format with AM midnight."""
        spinner = TimeSpinner(root_function, hour_format="12")
        spinner.hour_spinbox = MagicMock()
        spinner.hour_spinbox.get.return_value = 12
        spinner.minute_spinbox = MagicMock()
        spinner.minute_spinbox.get.return_value = 0
        spinner.second_spinbox = MagicMock()
        spinner.second_spinbox.get.return_value = 0
        spinner.am_pm_spinbox = MagicMock()
        spinner.am_pm_spinbox.get.return_value = "AM"
        
        spinner._on_time_change()
        assert spinner.selected_time.hour == 0  # 12 AM = 00:00
    
    def test_timespinner_time_change_12h_pm_noon(self, root_function, timepicker_complete_mock):
        """Test time change in 12h format with PM noon."""
        spinner = TimeSpinner(root_function, hour_format="12")
        spinner.hour_spinbox = MagicMock()
        spinner.hour_spinbox.get.return_value = 12
        spinner.minute_spinbox = MagicMock()
        spinner.minute_spinbox.get.return_value = 0
        spinner.second_spinbox = MagicMock()
        spinner.second_spinbox.get.return_value = 0
        spinner.am_pm_spinbox = MagicMock()
        spinner.am_pm_spinbox.get.return_value = "PM"
        
        spinner._on_time_change()
        assert spinner.selected_time.hour == 12  # 12 PM = 12:00


class TestCanvasSpinbox:
    """Test CanvasSpinbox widget."""
    
    def test_canvas_spinbox_creation(self, root_function, timepicker_complete_mock):
        """Test CanvasSpinbox creation."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        spinbox = CanvasSpinbox(
            canvas, 10, 10, 50, 50,
            from_=0, to=59, value=30,
            format_str="%02d"
        )
        assert spinbox.value == 30
        assert spinbox.from_ == 0
        assert spinbox.to == 59
        assert spinbox.format_str == "%02d"
    
    def test_canvas_spinbox_get_set(self, root_function, timepicker_complete_mock):
        """Test CanvasSpinbox get and set methods."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        spinbox = CanvasSpinbox(
            canvas, 10, 10, 50, 50,
            from_=0, to=59, value=30
        )
        assert spinbox.get() == 30
        
        spinbox.set(45)
        assert spinbox.get() == 45
    
    def test_canvas_spinbox_increment(self, root_function, timepicker_complete_mock):
        """Test CanvasSpinbox increment."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        spinbox = CanvasSpinbox(
            canvas, 10, 10, 50, 50,
            from_=0, to=59, value=58
        )
        spinbox._increment()
        assert spinbox.get() == 59
        
        # Test wraparound
        spinbox._increment()
        assert spinbox.get() == 0
    
    def test_canvas_spinbox_decrement(self, root_function, timepicker_complete_mock):
        """Test CanvasSpinbox decrement."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        spinbox = CanvasSpinbox(
            canvas, 10, 10, 50, 50,
            from_=0, to=59, value=1
        )
        spinbox._decrement()
        assert spinbox.get() == 0
        
        # Test wraparound
        spinbox._decrement()
        assert spinbox.get() == 59
    
    def test_canvas_spinbox_callback(self, root_function, timepicker_complete_mock):
        """Test CanvasSpinbox callback."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        callback_called = []
        def test_callback():
            callback_called.append(True)
        
        spinbox = CanvasSpinbox(
            canvas, 10, 10, 50, 50,
            from_=0, to=59, value=30,
            callback=test_callback
        )
        spinbox._increment()
        assert len(callback_called) == 1
    
    def test_canvas_spinbox_destroy(self, root_function, timepicker_complete_mock):
        """Test CanvasSpinbox destroy method."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        spinbox = CanvasSpinbox(
            canvas, 10, 10, 50, 50,
            from_=0, to=59, value=30
        )
        # Should not raise exception
        spinbox.destroy()

    def test_canvas_spinbox_set_invalid_value(self, root_function, timepicker_complete_mock):
        """Test set with invalid value."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        spinbox = CanvasSpinbox(
            canvas, 10, 10, 50, 50,
            from_=0, to=59, value=30
        )
        
        # Set invalid value (should not change)
        original_value = spinbox.get()
        spinbox.set(100)  # Invalid value
        assert spinbox.get() == original_value
    
    def test_canvas_spinbox_set_valid_value(self, root_function, timepicker_complete_mock):
        """Test set with valid value."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        spinbox = CanvasSpinbox(
            canvas, 10, 10, 50, 50,
            from_=0, to=59, value=30
        )
        
        spinbox.set(45)  # Valid value
        assert spinbox.get() == 45


class TestCanvasAMPMSpinbox:
    """Test CanvasAMPMSpinbox widget."""
    
    def test_canvas_ampm_spinbox_creation(self, root_function, timepicker_complete_mock):
        """Test CanvasAMPMSpinbox creation."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        spinbox = CanvasAMPMSpinbox(
            canvas, 10, 10, 50, 50,
            value="AM"
        )
        assert spinbox.get() == "AM"
        assert spinbox.values == ["AM", "PM"]
    
    def test_canvas_ampm_spinbox_get_set(self, root_function, timepicker_complete_mock):
        """Test CanvasAMPMSpinbox get and set methods."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        spinbox = CanvasAMPMSpinbox(
            canvas, 10, 10, 50, 50,
            value="AM"
        )
        assert spinbox.get() == "AM"
        
        spinbox.set("PM")
        assert spinbox.get() == "PM"
    
    def test_canvas_ampm_spinbox_toggle(self, root_function, timepicker_complete_mock):
        """Test CanvasAMPMSpinbox toggle."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        spinbox = CanvasAMPMSpinbox(
            canvas, 10, 10, 50, 50,
            value="AM"
        )
        assert spinbox.get() == "AM"
        
        spinbox._toggle()
        assert spinbox.get() == "PM"
        
        spinbox._toggle()
        assert spinbox.get() == "AM"
    
    def test_canvas_ampm_spinbox_callback(self, root_function, timepicker_complete_mock):
        """Test CanvasAMPMSpinbox callback."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        callback_called = []
        def test_callback():
            callback_called.append(True)
        
        spinbox = CanvasAMPMSpinbox(
            canvas, 10, 10, 50, 50,
            value="AM",
            callback=test_callback
        )
        spinbox._toggle()
        assert len(callback_called) == 1
    
    def test_canvas_ampm_spinbox_destroy(self, root_function, timepicker_complete_mock):
        """Test CanvasAMPMSpinbox destroy method."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        spinbox = CanvasAMPMSpinbox(
            canvas, 10, 10, 50, 50,
            value="AM"
        )
        # Should not raise exception
        spinbox.destroy()

    def test_canvas_ampm_spinbox_set_invalid_value(self, root_function, timepicker_complete_mock):
        """Test AM/PM spinbox set with invalid value."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        spinbox = CanvasAMPMSpinbox(
            canvas, 10, 10, 50, 50,
            value="AM"
        )
        
        # Set invalid value (should not change)
        original_value = spinbox.get()
        spinbox.set("INVALID")  # Invalid value
        assert spinbox.get() == original_value
    
    def test_canvas_ampm_spinbox_set_valid_value(self, root_function, timepicker_complete_mock):
        """Test AM/PM spinbox set with valid value."""
        canvas = tk.Canvas(root_function, width=100, height=100)
        spinbox = CanvasAMPMSpinbox(
            canvas, 10, 10, 50, 50,
            value="AM"
        )
        
        spinbox.set("PM")  # Valid value
        assert spinbox.get() == "PM"


class TestLoadTheme:
    """Test _load_theme function."""
    
    def test_load_light_theme(self):
        """Test loading light theme."""
        colors = _load_theme("light")
        assert isinstance(colors, dict)
        assert 'time_background' in colors
        assert 'time_foreground' in colors
        assert 'time_spinbox_bg' in colors
    
    def test_load_dark_theme(self):
        """Test loading dark theme."""
        colors = _load_theme("dark")
        assert isinstance(colors, dict)
        assert 'time_background' in colors
        assert 'time_foreground' in colors
        assert 'time_spinbox_bg' in colors
    
    def test_load_nonexistent_theme(self):
        """Test loading nonexistent theme returns default."""
        colors = _load_theme("nonexistent")
        assert isinstance(colors, dict)
        assert 'time_background' in colors
        assert colors['time_background'] == 'white'  # Default value
    
    @patch('tkface.widget.timespinner.Path')
    def test_load_theme_file_error(self, mock_path):
        """Test theme loading with file error."""
        mock_path.side_effect = Exception("File error")
        colors = _load_theme("light")
        assert isinstance(colors, dict)
        assert 'time_background' in colors
        assert colors['time_background'] == 'white'  # Default fallback


class TestGetDefaultTheme:
    """Test _get_default_theme function."""
    
    def test_get_default_theme(self):
        """Test getting default theme colors."""
        colors = _get_default_theme()
        assert isinstance(colors, dict)
        assert 'time_background' in colors
        assert 'time_foreground' in colors
        assert 'time_spinbox_bg' in colors
        assert colors['time_background'] == 'white'
        assert colors['time_foreground'] == '#333333'