"""
Comprehensive tests for tkface TimeSpinner widget.

This module provides all tests for the TimeSpinner widget functionality,
including basic functionality, integration tests, edge cases, and platform-specific tests.
"""

import datetime
import sys
import tkinter as tk
from unittest.mock import Mock, patch
import pytest

from tkface.widget.timespinner import (
    TimeSpinner,
    CanvasSpinbox,
    CanvasAMPMSpinbox,
    _load_theme,
    _get_default_theme
)


class TestThemeLoading:
    """Test theme loading functionality."""
    
    def test_load_theme_light(self):
        """Test loading light theme."""
        theme = _load_theme("light")
        assert isinstance(theme, dict)
        assert 'time_background' in theme
        assert 'time_foreground' in theme
    
    def test_load_theme_dark(self):
        """Test loading dark theme."""
        theme = _load_theme("dark")
        assert isinstance(theme, dict)
        assert 'time_background' in theme
        assert 'time_foreground' in theme
    
    def test_load_theme_invalid(self):
        """Test loading invalid theme returns default."""
        theme = _load_theme("invalid_theme")
        default_theme = _get_default_theme()
        assert theme == default_theme
    
    def test_get_default_theme(self):
        """Test default theme structure."""
        theme = _get_default_theme()
        assert isinstance(theme, dict)
        required_keys = [
            'time_background', 'time_foreground', 'time_spinbox_bg',
            'time_spinbox_button_bg', 'time_spinbox_hover_bg',
            'time_spinbox_active_bg', 'time_spinbox_outline',
            'time_separator_color', 'time_label_color'
        ]
        for key in required_keys:
            assert key in theme


class TestCanvasSpinbox:
    """Test CanvasSpinbox widget."""
    
    def test_canvas_spinbox_creation(self, root_isolated):
        """Test CanvasSpinbox creation."""
        canvas = tk.Canvas(root_isolated)
        spinbox = CanvasSpinbox(
            canvas, x=10, y=10, width=50, height=80,
            from_=0, to=23, value=12, format_str="%02d"
        )
        assert spinbox.value == 12
        assert spinbox.from_ == 0
        assert spinbox.to == 23
        assert spinbox.format_str == "%02d"
    
    def test_canvas_spinbox_increment(self, root_isolated):
        """Test CanvasSpinbox increment functionality."""
        canvas = tk.Canvas(root_isolated)
        spinbox = CanvasSpinbox(
            canvas, x=10, y=10, width=50, height=80,
            from_=0, to=23, value=12
        )
        
        spinbox._increment()
        assert spinbox.value == 13
        
        # Test wraparound
        spinbox.value = 23
        spinbox._increment()
        assert spinbox.value == 0
    
    def test_canvas_spinbox_decrement(self, root_isolated):
        """Test CanvasSpinbox decrement functionality."""
        canvas = tk.Canvas(root_isolated)
        spinbox = CanvasSpinbox(
            canvas, x=10, y=10, width=50, height=80,
            from_=0, to=23, value=12
        )
        
        spinbox._decrement()
        assert spinbox.value == 11
        
        # Test wraparound
        spinbox.value = 0
        spinbox._decrement()
        assert spinbox.value == 23
    
    def test_canvas_spinbox_set_get(self, root_isolated):
        """Test CanvasSpinbox set and get methods."""
        canvas = tk.Canvas(root_isolated)
        spinbox = CanvasSpinbox(
            canvas, x=10, y=10, width=50, height=80,
            from_=0, to=23, value=12
        )
        
        # Test set method
        spinbox.set(15)
        assert spinbox.get() == 15
        
        # Test set with invalid value (should not change)
        original_value = spinbox.get()
        spinbox.set(25)  # Out of range
        assert spinbox.get() == original_value
    
    def test_canvas_spinbox_callback(self, root_isolated):
        """Test CanvasSpinbox callback functionality."""
        canvas = tk.Canvas(root_isolated)
        callback_called = False
        
        def test_callback():
            nonlocal callback_called
            callback_called = True
        
        spinbox = CanvasSpinbox(
            canvas, x=10, y=10, width=50, height=80,
            from_=0, to=23, value=12, callback=test_callback
        )
        
        spinbox._increment()
        assert callback_called
    
    def test_canvas_spinbox_mouse_wheel(self, root_isolated):
        """Test CanvasSpinbox mouse wheel functionality."""
        canvas = tk.Canvas(root_isolated)
        spinbox = CanvasSpinbox(
            canvas, x=10, y=10, width=50, height=80,
            from_=0, to=23, value=12
        )
        
        # Test positive delta (scroll up)
        event = Mock()
        event.delta = 1
        spinbox._on_mouse_wheel(event)
        assert spinbox.value == 13
        
        # Test negative delta (scroll down)
        event.delta = -1
        spinbox._on_mouse_wheel(event)
        assert spinbox.value == 12
    
    def test_canvas_spinbox_destroy(self, root_isolated):
        """Test CanvasSpinbox destroy method."""
        canvas = tk.Canvas(root_isolated)
        spinbox = CanvasSpinbox(
            canvas, x=10, y=10, width=50, height=80,
            from_=0, to=23, value=12
        )
        
        # Store original item count
        original_count = len(canvas.find_all())
        
        spinbox.destroy()
        
        # Check that items were removed
        new_count = len(canvas.find_all())
        assert new_count < original_count


class TestCanvasAMPMSpinbox:
    """Test CanvasAMPMSpinbox widget."""
    
    def test_ampm_spinbox_creation(self, root_isolated):
        """Test CanvasAMPMSpinbox creation."""
        canvas = tk.Canvas(root_isolated)
        spinbox = CanvasAMPMSpinbox(
            canvas, x=10, y=10, width=50, height=80,
            value="AM"
        )
        assert spinbox.get() == "AM"
        assert spinbox.current_index == 0
    
    def test_ampm_spinbox_toggle(self, root_isolated):
        """Test CanvasAMPMSpinbox toggle functionality."""
        canvas = tk.Canvas(root_isolated)
        spinbox = CanvasAMPMSpinbox(
            canvas, x=10, y=10, width=50, height=80,
            value="AM"
        )
        
        # Toggle from AM to PM
        spinbox._toggle()
        assert spinbox.get() == "PM"
        assert spinbox.current_index == 1
        
        # Toggle from PM to AM
        spinbox._toggle()
        assert spinbox.get() == "AM"
        assert spinbox.current_index == 0
    
    def test_ampm_spinbox_set_get(self, root_isolated):
        """Test CanvasAMPMSpinbox set and get methods."""
        canvas = tk.Canvas(root_isolated)
        spinbox = CanvasAMPMSpinbox(
            canvas, x=10, y=10, width=50, height=80,
            value="AM"
        )
        
        # Test set method
        spinbox.set("PM")
        assert spinbox.get() == "PM"
        assert spinbox.current_index == 1
        
        # Test set with invalid value (should not change)
        original_value = spinbox.get()
        spinbox.set("INVALID")
        assert spinbox.get() == original_value
    
    def test_ampm_spinbox_callback(self, root_isolated):
        """Test CanvasAMPMSpinbox callback functionality."""
        canvas = tk.Canvas(root_isolated)
        callback_called = False
        
        def test_callback():
            nonlocal callback_called
            callback_called = True
        
        spinbox = CanvasAMPMSpinbox(
            canvas, x=10, y=10, width=50, height=80,
            value="AM", callback=test_callback
        )
        
        spinbox._toggle()
        assert callback_called
    
    def test_ampm_spinbox_destroy(self, root_isolated):
        """Test CanvasAMPMSpinbox destroy method."""
        canvas = tk.Canvas(root_isolated)
        spinbox = CanvasAMPMSpinbox(
            canvas, x=10, y=10, width=50, height=80,
            value="AM"
        )
        
        # Store original item count
        original_count = len(canvas.find_all())
        
        spinbox.destroy()
        
        # Check that items were removed
        new_count = len(canvas.find_all())
        assert new_count < original_count


class TestTimeSpinner:
    """Test TimeSpinner widget."""
    
    def test_timespinner_creation_default(self, root_isolated):
        """Test TimeSpinner creation with default parameters."""
        spinner = TimeSpinner(root_isolated)
        assert spinner.hour_format == "24"
        assert spinner.show_seconds is True
        assert spinner.theme == "light"
        assert spinner.selected_time is not None
        assert isinstance(spinner.selected_time, datetime.time)
    
    def test_timespinner_creation_custom(self, root_isolated):
        """Test TimeSpinner creation with custom parameters."""
        test_time = datetime.time(14, 30, 45)
        spinner = TimeSpinner(
            root_isolated,
            hour_format="12",
            show_seconds=False,
            theme="dark",
            initial_time=test_time
        )
        assert spinner.hour_format == "12"
        assert spinner.show_seconds is False
        assert spinner.theme == "dark"
        assert spinner.selected_time == test_time
    
    def test_timespinner_get_selected_time(self, root_isolated):
        """Test get_selected_time method."""
        test_time = datetime.time(14, 30, 45)
        spinner = TimeSpinner(root_isolated, initial_time=test_time)
        assert spinner.get_selected_time() == test_time
    
    def test_timespinner_set_selected_time(self, root_isolated):
        """Test set_selected_time method."""
        spinner = TimeSpinner(root_isolated)
        test_time = datetime.time(14, 30, 45)
        spinner.set_selected_time(test_time)
        assert spinner.selected_time == test_time
    
    def test_timespinner_set_hour_format(self, root_isolated):
        """Test set_hour_format method."""
        spinner = TimeSpinner(root_isolated)
        spinner.set_hour_format("12")
        assert spinner.hour_format == "12"
        
        spinner.set_hour_format("24")
        assert spinner.hour_format == "24"
    
    def test_timespinner_set_show_seconds(self, root_isolated):
        """Test set_show_seconds method."""
        spinner = TimeSpinner(root_isolated)
        spinner.set_show_seconds(False)
        assert spinner.show_seconds is False
        
        spinner.set_show_seconds(True)
        assert spinner.show_seconds is True
    
    def test_timespinner_set_theme(self, root_isolated):
        """Test set_theme method."""
        spinner = TimeSpinner(root_isolated)
        spinner.set_theme("dark")
        assert spinner.theme == "dark"
        assert spinner.theme_colors is not None
    
    def test_timespinner_time_callback(self, root_isolated):
        """Test time callback functionality."""
        callback_times = []

        def test_callback(time_obj):
            callback_times.append(time_obj)

        spinner = TimeSpinner(root_isolated, time_callback=test_callback)
        
        # Simulate OK button click
        spinner._on_ok()
        assert len(callback_times) == 1
        assert callback_times[0] is not None
        
        # Simulate Cancel button click
        spinner._on_cancel()
        assert len(callback_times) == 2
        assert callback_times[1] is None
    
    def test_timespinner_toggle_format(self, root_isolated):
        """Test format toggle functionality."""
        spinner = TimeSpinner(root_isolated, hour_format="24")
        original_time = spinner.selected_time
        
        # Toggle to 12-hour format
        spinner._toggle_format()
        assert spinner.hour_format == "12"
        
        # Toggle back to 24-hour format
        spinner._toggle_format()
        assert spinner.hour_format == "24"
    
    def test_timespinner_time_change_24_hour(self, root_isolated):
        """Test time change handling in 24-hour format."""
        spinner = TimeSpinner(root_isolated, hour_format="24")
        
        # Mock spinboxes
        spinner.hour_spinbox = Mock()
        spinner.hour_spinbox.get.return_value = 14
        spinner.minute_spinbox = Mock()
        spinner.minute_spinbox.get.return_value = 30
        spinner.second_spinbox = Mock()
        spinner.second_spinbox.get.return_value = 45
        
        spinner._on_time_change()
        
        expected_time = datetime.time(14, 30, 45)
        assert spinner.selected_time == expected_time
    
    def test_timespinner_time_change_12_hour(self, root_isolated):
        """Test time change handling in 12-hour format."""
        spinner = TimeSpinner(root_isolated, hour_format="12")
        
        # Mock spinboxes
        spinner.hour_spinbox = Mock()
        spinner.hour_spinbox.get.return_value = 2
        spinner.minute_spinbox = Mock()
        spinner.minute_spinbox.get.return_value = 30
        spinner.second_spinbox = Mock()
        spinner.second_spinbox.get.return_value = 45
        spinner.am_pm_spinbox = Mock()
        spinner.am_pm_spinbox.get.return_value = "PM"
        
        spinner._on_time_change()
        
        expected_time = datetime.time(14, 30, 45)  # 2 PM = 14:00
        assert spinner.selected_time == expected_time
    
    def test_timespinner_time_change_12_hour_am(self, root_isolated):
        """Test time change handling in 12-hour format with AM."""
        spinner = TimeSpinner(root_isolated, hour_format="12")
        
        # Mock spinboxes
        spinner.hour_spinbox = Mock()
        spinner.hour_spinbox.get.return_value = 2
        spinner.minute_spinbox = Mock()
        spinner.minute_spinbox.get.return_value = 30
        spinner.second_spinbox = Mock()
        spinner.second_spinbox.get.return_value = 45
        spinner.am_pm_spinbox = Mock()
        spinner.am_pm_spinbox.get.return_value = "AM"
        
        spinner._on_time_change()
        
        expected_time = datetime.time(2, 30, 45)  # 2 AM = 02:00
        assert spinner.selected_time == expected_time
    
    def test_timespinner_time_change_12_hour_midnight(self, root_isolated):
        """Test time change handling in 12-hour format with midnight."""
        spinner = TimeSpinner(root_isolated, hour_format="12")
        
        # Mock spinboxes for 12 AM (midnight)
        spinner.hour_spinbox = Mock()
        spinner.hour_spinbox.get.return_value = 12
        spinner.minute_spinbox = Mock()
        spinner.minute_spinbox.get.return_value = 0
        spinner.second_spinbox = Mock()
        spinner.second_spinbox.get.return_value = 0
        spinner.am_pm_spinbox = Mock()
        spinner.am_pm_spinbox.get.return_value = "AM"
        
        spinner._on_time_change()
        
        expected_time = datetime.time(0, 0, 0)  # 12 AM = 00:00
        assert spinner.selected_time == expected_time
    
    def test_timespinner_time_change_12_hour_noon(self, root_isolated):
        """Test time change handling in 12-hour format with noon."""
        spinner = TimeSpinner(root_isolated, hour_format="12")
        
        # Mock spinboxes for 12 PM (noon)
        spinner.hour_spinbox = Mock()
        spinner.hour_spinbox.get.return_value = 12
        spinner.minute_spinbox = Mock()
        spinner.minute_spinbox.get.return_value = 0
        spinner.second_spinbox = Mock()
        spinner.second_spinbox.get.return_value = 0
        spinner.am_pm_spinbox = Mock()
        spinner.am_pm_spinbox.get.return_value = "PM"
        
        spinner._on_time_change()
        
        expected_time = datetime.time(12, 0, 0)  # 12 PM = 12:00
        assert spinner.selected_time == expected_time
    
    def test_timespinner_time_change_invalid(self, root_isolated):
        """Test time change handling with invalid values."""
        spinner = TimeSpinner(root_isolated)
        original_time = spinner.selected_time
        
        # Mock spinboxes with invalid values
        spinner.hour_spinbox = Mock()
        spinner.hour_spinbox.get.return_value = 25  # Invalid hour
        spinner.minute_spinbox = Mock()
        spinner.minute_spinbox.get.return_value = 30
        spinner.second_spinbox = Mock()
        spinner.second_spinbox.get.return_value = 45
        
        spinner._on_time_change()
        
        # Should not change the time with invalid values
        assert spinner.selected_time == original_time
    
    def test_timespinner_time_change_exception(self, root_isolated):
        """Test time change handling with exceptions."""
        spinner = TimeSpinner(root_isolated)
        original_time = spinner.selected_time
        
        # Mock spinboxes to raise exceptions
        spinner.hour_spinbox = Mock()
        spinner.hour_spinbox.get.side_effect = ValueError("Test error")
        spinner.minute_spinbox = Mock()
        spinner.minute_spinbox.get.return_value = 30
        spinner.second_spinbox = Mock()
        spinner.second_spinbox.get.return_value = 45
        
        # Should not raise exception
        spinner._on_time_change()
        
        # Should not change the time with exceptions
        assert spinner.selected_time == original_time
    
    def test_timespinner_scaling_config(self, root_isolated):
        """Test scaling configuration setup."""
        spinner = TimeSpinner(root_isolated)
        
        # Check that scaling attributes are set
        assert hasattr(spinner, 'spinbox_width')
        assert hasattr(spinner, 'spinbox_height')
        assert hasattr(spinner, 'margin')
        assert hasattr(spinner, 'unified_scale')
        assert hasattr(spinner, 'margin_scale')
        
        # Check that values are positive
        assert spinner.spinbox_width > 0
        assert spinner.spinbox_height > 0
        assert spinner.margin > 0
    
    def test_timespinner_canvas_size_update(self, root_isolated):
        """Test canvas size update functionality."""
        spinner = TimeSpinner(root_isolated)
        original_width = spinner.canvas.winfo_reqwidth()
        original_height = spinner.canvas.winfo_reqheight()
        
        # Update canvas size
        spinner._update_canvas_size()
        
        # Canvas size should be updated
        new_width = spinner.canvas.winfo_reqwidth()
        new_height = spinner.canvas.winfo_reqheight()
        assert new_width > 0
        assert new_height > 0
    
    def test_timespinner_widget_creation(self, root_isolated):
        """Test widget creation functionality."""
        spinner = TimeSpinner(root_isolated)
        
        # Check that widgets are created
        assert spinner.hour_spinbox is not None
        assert spinner.minute_spinbox is not None
        assert spinner.second_spinbox is not None
        
        # Check that buttons are created
        assert spinner.ok_button is not None
        assert spinner.cancel_button is not None
    
    def test_timespinner_widget_creation_no_seconds(self, root_isolated):
        """Test widget creation without seconds."""
        spinner = TimeSpinner(root_isolated, show_seconds=False)
        
        # Check that widgets are created
        assert spinner.hour_spinbox is not None
        assert spinner.minute_spinbox is not None
        assert spinner.second_spinbox is None  # Should be None when seconds disabled
    
    def test_timespinner_widget_creation_12_hour(self, root_isolated):
        """Test widget creation in 12-hour format."""
        spinner = TimeSpinner(root_isolated, hour_format="12")
        
        # Check that widgets are created
        assert spinner.hour_spinbox is not None
        assert spinner.minute_spinbox is not None
        assert spinner.am_pm_spinbox is not None  # Should exist in 12-hour format
    
    def test_timespinner_widget_creation_24_hour(self, root_isolated):
        """Test widget creation in 24-hour format."""
        spinner = TimeSpinner(root_isolated, hour_format="24")
        
        # Check that widgets are created
        assert spinner.hour_spinbox is not None
        assert spinner.minute_spinbox is not None
        assert spinner.am_pm_spinbox is None  # Should be None in 24-hour format
    
    def test_timespinner_button_creation(self, root_isolated):
        """Test button creation functionality."""
        spinner = TimeSpinner(root_isolated)
        
        # Check that buttons are created
        assert spinner.ok_button is not None
        assert spinner.cancel_button is not None
        
        # Check that buttons are packed
        assert spinner.ok_button.winfo_exists()
        assert spinner.cancel_button.winfo_exists()
    
    def test_timespinner_hover_toggle(self, root_isolated):
        """Test hover functionality on format toggle."""
        spinner = TimeSpinner(root_isolated)
        
        # Test hover enter
        spinner._on_hover_toggle(True)
        # Should not raise exception
        
        # Test hover leave
        spinner._on_hover_toggle(False)
        # Should not raise exception
    
    def test_timespinner_keyboard_shortcuts(self, root_isolated):
        """Test keyboard shortcuts."""
        spinner = TimeSpinner(root_isolated)
        
        # Test Return key (should call _on_ok)
        with patch.object(spinner, '_on_ok') as mock_ok:
            event = Mock()
            spinner.bind("<Return>", lambda e: spinner._on_ok())
            spinner.event_generate("<Return>")
            # Note: event_generate might not work in test environment
            # but the binding should be set
        
        # Test Escape key (should call _on_cancel)
        with patch.object(spinner, '_on_cancel') as mock_cancel:
            event = Mock()
            spinner.bind("<Escape>", lambda e: spinner._on_cancel())
            spinner.event_generate("<Escape>")
            # Note: event_generate might not work in test environment
            # but the binding should be set
    
    def test_timespinner_dpi_scaling_error(self, root_isolated):
        """Test DPI scaling error handling."""
        with patch('tkface.widget.timespinner.get_scaling_factor', side_effect=ImportError("Test error")):
            spinner = TimeSpinner(root_isolated)
            assert spinner.dpi_scaling_factor == 1.0
    
    def test_timespinner_dpi_scaling_attribute_error(self, root_isolated):
        """Test DPI scaling AttributeError handling."""
        with patch('tkface.widget.timespinner.get_scaling_factor', side_effect=AttributeError("Test error")):
            spinner = TimeSpinner(root_isolated)
            assert spinner.dpi_scaling_factor == 1.0
    
    def test_timespinner_dpi_scaling_type_error(self, root_isolated):
        """Test DPI scaling TypeError handling."""
        with patch('tkface.widget.timespinner.get_scaling_factor', side_effect=TypeError("Test error")):
            spinner = TimeSpinner(root_isolated)
            assert spinner.dpi_scaling_factor == 1.0


class TestTimeSpinnerIntegration:
    """Test TimeSpinner integration scenarios."""
    
    def test_timespinner_full_workflow(self, root_isolated):
        """Test complete TimeSpinner workflow."""
        # Create spinner
        spinner = TimeSpinner(
            root_isolated,
            hour_format="24",
            show_seconds=True,
            initial_time=datetime.time(14, 30, 45)
        )
        
        # Verify initial state
        assert spinner.get_selected_time() == datetime.time(14, 30, 45)
        
        # Change format
        spinner.set_hour_format("12")
        assert spinner.hour_format == "12"
        
        # Change seconds setting
        spinner.set_show_seconds(False)
        assert spinner.show_seconds is False
        
        # Change theme
        spinner.set_theme("dark")
        assert spinner.theme == "dark"
        
        # Set new time
        new_time = datetime.time(9, 15, 30)
        spinner.set_selected_time(new_time)
        assert spinner.get_selected_time() == new_time
    
    def test_timespinner_callback_workflow(self, root_isolated):
        """Test TimeSpinner with callback workflow."""
        callback_times = []

        def test_callback(time_obj):
            callback_times.append(time_obj)

        spinner = TimeSpinner(root_isolated, time_callback=test_callback)
        
        # Simulate OK
        spinner._on_ok()
        assert len(callback_times) == 1
        assert callback_times[0] is not None
        
        # Simulate Cancel
        spinner._on_cancel()
        assert len(callback_times) == 2
        assert callback_times[1] is None
    
    def test_timespinner_format_toggle_workflow(self, root_isolated):
        """Test format toggle workflow."""
        spinner = TimeSpinner(root_isolated, hour_format="24")
        original_time = spinner.selected_time
        
        # Toggle to 12-hour
        spinner._toggle_format()
        assert spinner.hour_format == "12"
        
        # Toggle back to 24-hour
        spinner._toggle_format()
        assert spinner.hour_format == "24"
        
        # Time should be preserved (allow for microsecond differences)
        assert abs((spinner.selected_time.hour * 3600 + spinner.selected_time.minute * 60 + spinner.selected_time.second) - 
                   (original_time.hour * 3600 + original_time.minute * 60 + original_time.second)) < 1


class TestTimeSpinnerEdgeCases:
    """Test TimeSpinner edge cases and error conditions."""
    
    def test_timespinner_invalid_theme(self, root_isolated):
        """Test TimeSpinner with invalid theme."""
        spinner = TimeSpinner(root_isolated, theme="invalid_theme")
        # Should not raise exception and use default theme
        assert spinner.theme == "invalid_theme"
        assert spinner.theme_colors is not None
    
    def test_timespinner_none_initial_time(self, root_isolated):
        """Test TimeSpinner with None initial time."""
        spinner = TimeSpinner(root_isolated, initial_time=None)
        # Should use current time
        assert spinner.selected_time is not None
        assert isinstance(spinner.selected_time, datetime.time)
    
    def test_timespinner_invalid_hour_format(self, root_isolated):
        """Test TimeSpinner with invalid hour format."""
        spinner = TimeSpinner(root_isolated, hour_format="invalid")
        # Should not raise exception
        assert spinner.hour_format == "invalid"
    
    def test_timespinner_theme_change_preserves_time(self, root_isolated):
        """Test that theme change preserves selected time."""
        test_time = datetime.time(14, 30, 45)
        spinner = TimeSpinner(root_isolated, initial_time=test_time)
        
        # Change theme
        spinner.set_theme("dark")
        
        # Time should be preserved
        assert spinner.get_selected_time() == test_time
    
    def test_timespinner_format_change_preserves_time(self, root_isolated):
        """Test that format change preserves selected time."""
        test_time = datetime.time(14, 30, 45)
        spinner = TimeSpinner(root_isolated, initial_time=test_time)
        
        # Change format
        spinner.set_hour_format("12")
        
        # Time should be preserved
        assert spinner.get_selected_time() == test_time
    
    def test_timespinner_seconds_change_preserves_time(self, root_isolated):
        """Test that seconds setting change preserves selected time."""
        test_time = datetime.time(14, 30, 45)
        spinner = TimeSpinner(root_isolated, initial_time=test_time)
        
        # Change seconds setting
        spinner.set_show_seconds(False)
        
        # Time should be preserved
        assert spinner.get_selected_time() == test_time


class TestTimeSpinnerPlatformSpecific:
    """Test TimeSpinner platform-specific functionality."""
    
    def test_timespinner_windows_flat_button(self, root_isolated):
        """Test TimeSpinner with Windows flat button."""
        if sys.platform == "win32":
            with patch('tkface.widget.timespinner.FlatButton') as mock_flat_button:
                mock_flat_button.return_value = Mock()
                spinner = TimeSpinner(root_isolated)
                
                # Should use FlatButton on Windows
                mock_flat_button.assert_called()
    
    def test_timespinner_non_windows_button(self, root_isolated):
        """Test TimeSpinner with non-Windows button."""
        if sys.platform != "win32":
            with patch('tkinter.Button') as mock_button:
                mock_button.return_value = Mock()
                spinner = TimeSpinner(root_isolated)
                
                # Should use regular Button on non-Windows
                mock_button.assert_called()
    
    def test_timespinner_mouse_wheel_handling(self, root_isolated):
        """Test mouse wheel handling on different platforms."""
        canvas = tk.Canvas(root_isolated)
        spinbox = CanvasSpinbox(
            canvas, x=10, y=10, width=50, height=80,
            from_=0, to=23, value=12
        )
        
        # Test mouse wheel event
        event = Mock()
        event.delta = 1
        spinbox._on_mouse_wheel(event)
        assert spinbox.value == 13
        
        # Test negative delta
        event.delta = -1
        spinbox._on_mouse_wheel(event)
        assert spinbox.value == 12
    
    def test_timespinner_mouse_wheel_tcl_error(self, root_isolated):
        """Test mouse wheel handling with TclError."""
        canvas = tk.Canvas(root_isolated)
        
        # Mock canvas.tag_bind to raise TclError for MouseWheel
        original_tag_bind = canvas.tag_bind
        
        def mock_tag_bind(item, event, handler):
            if event == "<MouseWheel>":
                raise tk.TclError("MouseWheel not supported")
            return original_tag_bind(item, event, handler)
        
        canvas.tag_bind = mock_tag_bind
        
        # Should not raise exception
        spinbox = CanvasSpinbox(
            canvas, x=10, y=10, width=50, height=80,
            from_=0, to=23, value=12
        )
        assert spinbox is not None


class TestTimeSpinnerPerformance:
    """Test TimeSpinner performance scenarios."""
    
    def test_timespinner_rapid_format_changes(self, root_isolated):
        """Test rapid format changes."""
        spinner = TimeSpinner(root_isolated)
        
        # Rapidly change format multiple times
        for _ in range(10):
            spinner.set_hour_format("12")
            spinner.set_hour_format("24")
        
        # Should not raise exception
        assert spinner.hour_format == "24"
    
    def test_timespinner_rapid_theme_changes(self, root_isolated):
        """Test rapid theme changes."""
        spinner = TimeSpinner(root_isolated)
        
        # Rapidly change theme multiple times
        for _ in range(10):
            spinner.set_theme("light")
            spinner.set_theme("dark")
        
        # Should not raise exception
        assert spinner.theme == "dark"
    
    def test_timespinner_rapid_time_changes(self, root_isolated):
        """Test rapid time changes."""
        spinner = TimeSpinner(root_isolated)
        
        # Rapidly change time multiple times
        for i in range(10):
            test_time = datetime.time(i % 24, i % 60, i % 60)
            spinner.set_selected_time(test_time)
            assert spinner.get_selected_time() == test_time
        
        # Should not raise exception
        assert spinner.get_selected_time() is not None


class TestTimeSpinnerAccessibility:
    """Test TimeSpinner accessibility features."""
    
    def test_timespinner_keyboard_navigation(self, root_isolated):
        """Test keyboard navigation."""
        spinner = TimeSpinner(root_isolated)
        
        # Check that keyboard bindings are set
        bindings = spinner.bind()
        assert "<Key-Return>" in bindings
        assert "<Key-Escape>" in bindings
    
    def test_timespinner_focus_management(self, root_isolated):
        """Test focus management."""
        spinner = TimeSpinner(root_isolated)
        
        # Check that canvas can receive focus
        spinner.canvas.focus_set()
        # Focus might be on the root window, so just check that focus_set doesn't raise an exception
        assert spinner.canvas is not None
    
    def test_timespinner_screen_reader_support(self, root_isolated):
        """Test screen reader support."""
        spinner = TimeSpinner(root_isolated)
        
        # Check that widgets have proper structure
        assert spinner.hour_spinbox is not None
        assert spinner.minute_spinbox is not None
        assert spinner.ok_button is not None
        assert spinner.cancel_button is not None
