# pylint: disable=protected-access,too-many-lines
"""Unit tests for tkface.widget.timespinner module."""

import datetime
import tkinter as tk
from unittest.mock import Mock, patch

import pytest

from tkface.dialog.timepicker import TimePickerConfig, _TimePickerBase
from tkface.widget.timespinner import CustomAMPMSpinbox, CustomSpinbox, TimeSpinner


# ---------------------------------------------------------------------------
# Shared helpers (ported from the former test_timepicker coverage)
# ---------------------------------------------------------------------------

def create_test_config():
    def dummy_callback(time_obj):  # pylint: disable=unused-argument
        return None

    return TimePickerConfig(
        time_format="%H:%M:%S",
        hour_format="24",
        show_seconds=True,
        theme="light",
        language="en",
        time_callback=dummy_callback,
    )


def _test_widget_creation(widget_class, root, use_config=True, **kwargs):
    if use_config:
        config = create_test_config()
        widget = widget_class(root, config=config, **kwargs)
        expected = config.time_callback
    else:
        widget = widget_class(
            root,
            time_format="%H:%M:%S",
            hour_format="24",
            show_seconds=True,
            theme="light",
            language="en",
            **kwargs,
        )
        expected = None

    assert widget.time_format == "%H:%M:%S"
    assert widget.hour_format == "24"
    assert widget.show_seconds is True
    if hasattr(widget, "time_callback"):
        assert widget.time_callback == expected
    return widget


def _test_dpi_scaling_error_handling(widget_class, root):
    with patch("tkface.dialog.timepicker.get_scaling_factor") as mocked:
        mocked.side_effect = ImportError("boom")
        widget = widget_class(root)
        assert widget.dpi_scaling_factor == 1.0
        return widget


def create_mock_popup_window():
    popup = Mock()
    popup.winfo_exists.return_value = True
    popup.winfo_rootx.return_value = 100
    popup.winfo_rooty.return_value = 100
    popup.winfo_width.return_value = 200
    popup.winfo_height.return_value = 200
    popup.winfo_pointerxy.return_value = (150, 150)
    popup.after = Mock()
    return popup


def create_mock_time_picker():
    time_picker = Mock()
    time_picker.get_selected_time.return_value = datetime.time(14, 30, 0)
    time_picker.focus_set = Mock()
    time_picker.focus_force = Mock()
    return time_picker


@pytest.fixture(name="timespinner_root", scope="module")
def fixture_timespinner_root():
    master = tk.Tk()
    master.withdraw()
    yield master
    master.destroy()


class TestCustomSpinbox:
    def test_increment_wraps(self, timespinner_root):
        widget = CustomSpinbox(
            timespinner_root,
            from_=0,
            to=1,
            textvariable=tk.StringVar(value="00"),
        )
        widget._increment()
        assert widget.get() == 1
        widget._increment()
        assert widget.get() == 0

    def test_decrement_wraps(self, timespinner_root):
        widget = CustomSpinbox(
            timespinner_root,
            from_=0,
            to=1,
            textvariable=tk.StringVar(value="00"),
        )
        widget._decrement()
        assert widget.get() == 1

    def test_validate_accepts_valid(self, timespinner_root):
        var = tk.StringVar(value="00")
        widget = CustomSpinbox(timespinner_root, from_=0, to=5, textvariable=var)
        widget.entry.config(state="normal")
        widget.entry.delete(0, tk.END)
        widget.entry.insert(0, "03")
        widget._validate_and_set()
        assert widget.get() == 3

    def test_validate_rejects_invalid(self, timespinner_root):
        var = tk.StringVar(value="00")
        widget = CustomSpinbox(timespinner_root, from_=0, to=5, textvariable=var)
        widget.entry.config(state="normal")
        widget.entry.delete(0, tk.END)
        widget.entry.insert(0, "invalid")
        widget._validate_and_set()
        assert widget.get() == 0

    def test_set_within_range(self, timespinner_root):
        widget = CustomSpinbox(timespinner_root, from_=0, to=5)
        widget.set(4)
        assert widget.get() == 4

    def test_set_out_of_range_ignored(self, timespinner_root):
        widget = CustomSpinbox(timespinner_root, from_=0, to=5)
        widget.set(9)
        assert widget.get() == 0

    def test_on_key_press_branches(self, timespinner_root):
        widget = CustomSpinbox(
            timespinner_root,
            from_=0,
            to=1,
            textvariable=tk.StringVar(value="00"),
        )
        widget._on_key_press(Mock(keysym="Up"))
        assert widget.get() == 1
        widget._on_key_press(Mock(keysym="Down"))
        assert widget.get() == 0
        widget.entry.config(state="normal")
        widget.entry.delete(0, tk.END)
        widget.entry.insert(0, "01")
        widget._on_key_press(Mock(keysym="Return"))
        assert widget.get() == 1

    def test_on_mouse_wheel(self, timespinner_root):
        widget = CustomSpinbox(
            timespinner_root,
            from_=0,
            to=1,
            textvariable=tk.StringVar(value="00"),
        )
        widget._on_mouse_wheel(Mock(delta=120))
        assert widget.get() == 1
        widget._on_mouse_wheel(Mock(delta=-120))
        assert widget.get() == 0

    def test_update_display_without_textvariable(self, timespinner_root):
        widget = CustomSpinbox(timespinner_root, from_=0, to=5, textvariable=None)
        widget.value = 3
        widget._update_display()
        assert widget.entry.get() == "03"

    def test_on_entry_click_enables_editing(self, timespinner_root):
        widget = CustomSpinbox(
            timespinner_root,
            from_=0,
            to=5,
            textvariable=tk.StringVar(value="02"),
        )
        widget._on_entry_click(Mock())
        assert widget.entry.cget("state") == "normal"
        # Note: selection_present() may not work in test environment
        # Just verify state is normal

    def test_on_key_press_return_validates(self, timespinner_root):
        """Test _on_key_press with Return key validation."""
        widget = CustomSpinbox(
            timespinner_root,
            from_=0,
            to=5,
            textvariable=tk.StringVar(value="02"),
        )
        widget.entry.config(state="normal")
        widget.entry.delete(0, tk.END)
        widget.entry.insert(0, "04")
        widget._on_key_press(Mock(keysym="Return"))
        assert widget.get() == 4

    def test_on_key_press_up_down_keys(self, timespinner_root):
        """Test _on_key_press with Up/Down keys."""
        widget = CustomSpinbox(
            timespinner_root,
            from_=0,
            to=5,
            textvariable=tk.StringVar(value="02"),
        )
        widget._on_key_press(Mock(keysym="Up"))
        assert widget.get() == 3
        widget._on_key_press(Mock(keysym="Down"))
        assert widget.get() == 2

    def test_validate_out_of_range_restores_value(self, timespinner_root):
        var = tk.StringVar(value="01")
        widget = CustomSpinbox(timespinner_root, from_=0, to=5, textvariable=var)
        widget.entry.config(state="normal")
        widget.entry.delete(0, tk.END)
        widget.entry.insert(0, "99")
        widget._validate_and_set()
        assert widget.get() == 1

    def test_increment_triggers_callback(self, timespinner_root):
        callback = Mock()
        widget = CustomSpinbox(
            timespinner_root,
            from_=0,
            to=1,
            textvariable=tk.StringVar(value="00"),
            callback=callback,
        )
        widget._increment()
        callback.assert_called_once()

    def test_decrement_triggers_callback(self, timespinner_root):
        callback = Mock()
        widget = CustomSpinbox(
            timespinner_root,
            from_=0,
            to=1,
            textvariable=tk.StringVar(value="01"),
            callback=callback,
        )
        widget._decrement()
        callback.assert_called_once()

    def test_validate_and_set_triggers_callback(self, timespinner_root):
        callback = Mock()
        var = tk.StringVar(value="01")
        widget = CustomSpinbox(timespinner_root, from_=0, to=5, textvariable=var, callback=callback)
        widget.entry.config(state="normal")
        widget.entry.delete(0, tk.END)
        widget.entry.insert(0, "03")
        widget._validate_and_set()
        callback.assert_called_once()


class TestCustomAMPMSpinbox:
    def test_increment_decrement_toggle(self, timespinner_root):
        var = tk.StringVar(value="AM")
        widget = CustomAMPMSpinbox(timespinner_root, textvariable=var)
        widget._increment()
        assert widget.get() == "PM"
        widget._decrement()
        assert widget.get() == "AM"

    def test_validate_accepts(self, timespinner_root):
        var = tk.StringVar(value="AM")
        widget = CustomAMPMSpinbox(timespinner_root, textvariable=var)
        widget.entry.config(state="normal")
        widget.entry.delete(0, tk.END)
        widget.entry.insert(0, "pm")
        widget._validate_and_set()
        assert widget.get() == "PM"

    def test_validate_rejects(self, timespinner_root):
        var = tk.StringVar(value="AM")
        widget = CustomAMPMSpinbox(timespinner_root, textvariable=var)
        widget.entry.config(state="normal")
        widget.entry.delete(0, tk.END)
        widget.entry.insert(0, "xx")
        widget._validate_and_set()
        assert widget.get() == "AM"

    def test_set_ignores_invalid(self, timespinner_root):
        widget = CustomAMPMSpinbox(timespinner_root)
        widget.set("XX")
        assert widget.get() == "AM"

    def test_on_key_press(self, timespinner_root):
        var = tk.StringVar(value="AM")
        widget = CustomAMPMSpinbox(timespinner_root, textvariable=var)
        widget._on_key_press(Mock(keysym="Up"))
        assert widget.get() == "PM"
        widget._on_key_press(Mock(keysym="Down"))
        assert widget.get() == "AM"
        widget.entry.config(state="normal")
        widget.entry.delete(0, tk.END)
        widget.entry.insert(0, "pm")
        widget._on_key_press(Mock(keysym="Return"))
        assert widget.get() == "PM"

    def test_on_mouse_wheel(self, timespinner_root):
        var = tk.StringVar(value="AM")
        widget = CustomAMPMSpinbox(timespinner_root, textvariable=var)
        widget._on_mouse_wheel(Mock(delta=120))
        assert widget.get() == "PM"
        widget._on_mouse_wheel(Mock(delta=-120))
        assert widget.get() == "AM"

    def test_update_button_visibility(self, timespinner_root):
        var = tk.StringVar(value="AM")
        widget = CustomAMPMSpinbox(timespinner_root, textvariable=var)
        assert widget.up_button.cget("state") == "disabled"
        assert widget.down_button.cget("state") == "normal"
        widget.set("PM")
        assert widget.up_button.cget("state") == "normal"
        assert widget.down_button.cget("state") == "disabled"

    def test_increment_triggers_callback(self, timespinner_root):
        callback = Mock()
        var = tk.StringVar(value="AM")
        widget = CustomAMPMSpinbox(timespinner_root, textvariable=var, callback=callback)
        widget._increment()
        callback.assert_called_once()

    def test_decrement_triggers_callback(self, timespinner_root):
        callback = Mock()
        var = tk.StringVar(value="PM")
        widget = CustomAMPMSpinbox(timespinner_root, textvariable=var, callback=callback)
        widget._decrement()
        callback.assert_called_once()

    def test_validate_and_set_triggers_callback(self, timespinner_root):
        callback = Mock()
        var = tk.StringVar(value="AM")
        widget = CustomAMPMSpinbox(timespinner_root, textvariable=var, callback=callback)
        widget.entry.config(state="normal")
        widget.entry.delete(0, tk.END)
        widget.entry.insert(0, "pm")
        widget._validate_and_set()
        callback.assert_called_once()

    def test_on_entry_click_enables_editing(self, timespinner_root):
        var = tk.StringVar(value="AM")
        widget = CustomAMPMSpinbox(timespinner_root, textvariable=var)
        widget._on_entry_click(Mock())
        assert widget.entry.cget("state") == "normal"

    def test_validate_and_set_exception_handling(self, timespinner_root):
        var = tk.StringVar(value="AM")
        widget = CustomAMPMSpinbox(timespinner_root, textvariable=var)
        widget.entry.config(state="normal")
        widget.entry.delete(0, tk.END)
        widget.entry.insert(0, "invalid")
        # Should not raise exception
        widget._validate_and_set()
        assert widget.get() == "AM"  # Should remain unchanged

    def test_validate_and_set_value_error_handling(self, timespinner_root):
        """Test _validate_and_set with ValueError exception."""
        var = tk.StringVar(value="AM")
        widget = CustomAMPMSpinbox(timespinner_root, textvariable=var)
        widget.entry.config(state="normal")
        widget.entry.delete(0, tk.END)
        widget.entry.insert(0, "invalid")
        # Mock entry.get to raise ValueError
        widget.entry.get = Mock(side_effect=ValueError("Test error"))
        widget._validate_and_set()
        # Should handle exception gracefully and not change value
        assert widget.get() == "AM"

    def test_on_key_press_return_validates_ampm(self, timespinner_root):
        """Test _on_key_press with Return key validation for AM/PM."""
        var = tk.StringVar(value="AM")
        widget = CustomAMPMSpinbox(timespinner_root, textvariable=var)
        widget.entry.config(state="normal")
        widget.entry.delete(0, tk.END)
        widget.entry.insert(0, "pm")
        widget._on_key_press(Mock(keysym="Return"))
        assert widget.get() == "PM"

    def test_on_key_press_up_down_keys_ampm(self, timespinner_root):
        """Test _on_key_press with Up/Down keys for AM/PM."""
        var = tk.StringVar(value="AM")
        widget = CustomAMPMSpinbox(timespinner_root, textvariable=var)
        widget._on_key_press(Mock(keysym="Up"))
        assert widget.get() == "PM"
        widget._on_key_press(Mock(keysym="Down"))
        assert widget.get() == "AM"


class TestTimeSpinner:
    def test_bind_events(self, timespinner_root):
        widget = TimeSpinner(timespinner_root, show_seconds=False, hour_format="24")
        widget.hour_spinbox.entry = Mock()
        widget.minute_spinbox.entry = Mock()
        widget._bind_events()
        widget.hour_spinbox.entry.bind.assert_called_once_with(
            "<KeyRelease>",
            widget._on_time_change,
        )
        widget.minute_spinbox.entry.bind.assert_called_once_with(
            "<KeyRelease>",
            widget._on_time_change,
        )

    def test_on_time_change_invalid_string(self, timespinner_root):
        widget = TimeSpinner(timespinner_root)
        original = widget.selected_time
        widget.hour_var.set("XX")
        widget.minute_var.set("30")
        widget.second_var.set("45")
        widget._on_time_change()
        assert widget.selected_time == original

    def test_on_time_change_out_of_range(self, timespinner_root):
        widget = TimeSpinner(timespinner_root)
        original = widget.selected_time
        widget.hour_var.set("99")
        widget.minute_var.set("30")
        widget.second_var.set("45")
        widget._on_time_change()
        assert widget.selected_time == original

    def test_creation_defaults(self, timespinner_root):
        widget = TimeSpinner(timespinner_root)
        assert widget.hour_format == "24"
        assert widget.show_seconds is True
        assert widget.selected_time is not None

    def test_creation_12_hour(self, timespinner_root):
        widget = TimeSpinner(timespinner_root, hour_format="12")
        assert widget.hour_format == "12"

    def test_creation_no_seconds(self, timespinner_root):
        widget = TimeSpinner(timespinner_root, show_seconds=False)
        assert widget.show_seconds is False

    def test_set_selected_time_24_hour(self, timespinner_root):
        widget = TimeSpinner(timespinner_root, hour_format="24")
        test_time = datetime.time(14, 30, 45)
        widget.set_selected_time(test_time)
        assert widget.selected_time == test_time
        assert widget.hour_var.get() == "14"
        assert widget.minute_var.get() == "30"
        assert widget.second_var.get() == "45"

    def test_set_selected_time_12_hour(self, timespinner_root):
        widget = TimeSpinner(timespinner_root, hour_format="12")
        test_time = datetime.time(14, 30, 45)
        widget.set_selected_time(test_time)
        assert widget.selected_time == test_time
        assert widget.hour_var.get() == "02"
        assert widget.minute_var.get() == "30"
        assert widget.second_var.get() == "45"
        assert widget.am_pm_var.get() == "PM"

    def test_set_selected_time_12_hour_midnight(self, timespinner_root):
        widget = TimeSpinner(timespinner_root, hour_format="12")
        test_time = datetime.time(0, 30, 45)
        widget.set_selected_time(test_time)
        assert widget.hour_var.get() == "12"
        assert widget.am_pm_var.get() == "AM"

    def test_set_selected_time_12_hour_noon(self, timespinner_root):
        widget = TimeSpinner(timespinner_root, hour_format="12")
        test_time = datetime.time(12, 30, 45)
        widget.set_selected_time(test_time)
        assert widget.hour_var.get() == "12"
        assert widget.am_pm_var.get() == "PM"

    def test_get_selected_time(self, timespinner_root):
        widget = TimeSpinner(timespinner_root)
        test_time = datetime.time(14, 30, 45)
        widget.selected_time = test_time
        assert widget.get_selected_time() == test_time

    def test_on_time_change_valid(self, timespinner_root):
        widget = TimeSpinner(timespinner_root, hour_format="24")
        widget.hour_var.set("14")
        widget.minute_var.set("30")
        widget.second_var.set("45")
        widget._on_time_change()
        assert widget.selected_time == datetime.time(14, 30, 45)

    def test_on_time_change_12_hour(self, timespinner_root):
        widget = TimeSpinner(timespinner_root, hour_format="12")
        widget.hour_var.set("02")
        widget.minute_var.set("30")
        widget.second_var.set("45")
        widget.am_pm_var.set("PM")
        widget._on_time_change()
        assert widget.selected_time == datetime.time(14, 30, 45)

    def test_on_time_change_invalid(self, timespinner_root):
        widget = TimeSpinner(timespinner_root)
        widget.hour_var.set("invalid")
        widget.minute_var.set("30")
        widget.second_var.set("45")
        widget._on_time_change()
        assert widget.selected_time is not None

    def test_initial_time_24_hour(self, timespinner_root):
        initial = datetime.time(9, 5, 30)
        widget = TimeSpinner(
            timespinner_root,
            hour_format="24",
            show_seconds=False,
            initial_time=initial,
        )
        assert widget.selected_time == initial
        assert widget.hour_var.get() == "09"
        assert widget.minute_var.get() == "05"

    def test_initial_time_12_hour(self, timespinner_root):
        initial = datetime.time(19, 45, 15)
        widget = TimeSpinner(
            timespinner_root,
            hour_format="12",
            show_seconds=True,
            initial_time=initial,
        )
        assert widget.selected_time == initial
        assert widget.hour_var.get() == "07"
        assert widget.minute_var.get() == "45"
        assert widget.second_var.get() == "15"
        assert widget.am_pm_var.get() == "PM"

    def test_on_time_change_without_seconds_sets_zero(self, timespinner_root):
        widget = TimeSpinner(timespinner_root, show_seconds=False)
        widget.hour_var.set("08")
        widget.minute_var.set("10")
        widget._on_time_change()
        assert widget.selected_time == datetime.time(8, 10, 0)

    def test_bind_events_with_seconds_and_ampm(self, timespinner_root):
        widget = TimeSpinner(
            timespinner_root,
            show_seconds=True,
            hour_format="12",
        )
        widget.hour_spinbox.entry = Mock()
        widget.minute_spinbox.entry = Mock()
        widget.second_spinbox.entry = Mock()
        widget.am_pm_spinbox.entry = Mock()
        widget._bind_events()
        widget.second_spinbox.entry.bind.assert_called_once_with(
            "<KeyRelease>",
            widget._on_time_change,
        )
        widget.am_pm_spinbox.entry.bind.assert_called_once_with(
            "<KeyRelease>",
            widget._on_time_change,
        )

    def test_set_selected_time_without_seconds_retains_second_var(self, timespinner_root):
        widget = TimeSpinner(timespinner_root, show_seconds=False)
        widget.second_var.set("preset")
        widget.set_selected_time(datetime.time(6, 20, 45))
        assert widget.second_var.get() == "preset"

    def test_set_initial_values_12_hour_midnight(self, timespinner_root):
        """Test _set_initial_values with 12-hour format at midnight."""
        widget = TimeSpinner(timespinner_root, hour_format="12")
        midnight = datetime.time(0, 0, 0)
        widget._set_initial_values(midnight)
        assert widget.hour_var.get() == "12"
        assert widget.am_pm_var.get() == "AM"

    def test_set_initial_values_12_hour_noon(self, timespinner_root):
        """Test _set_initial_values with 12-hour format at noon."""
        widget = TimeSpinner(timespinner_root, hour_format="12")
        noon = datetime.time(12, 0, 0)
        widget._set_initial_values(noon)
        assert widget.hour_var.get() == "12"
        assert widget.am_pm_var.get() == "PM"

    def test_set_initial_values_12_hour_afternoon(self, timespinner_root):
        """Test _set_initial_values with 12-hour format in afternoon."""
        widget = TimeSpinner(timespinner_root, hour_format="12")
        afternoon = datetime.time(15, 30, 45)
        widget._set_initial_values(afternoon)
        assert widget.hour_var.get() == "03"
        assert widget.am_pm_var.get() == "PM"

    def test_on_time_change_12_hour_midnight_conversion(self, timespinner_root):
        """Test _on_time_change with 12-hour format midnight conversion."""
        widget = TimeSpinner(timespinner_root, hour_format="12")
        widget.hour_var.set("12")
        widget.minute_var.set("00")
        widget.second_var.set("00")
        widget.am_pm_var.set("AM")
        widget._on_time_change()
        assert widget.selected_time == datetime.time(0, 0, 0)

    def test_on_time_change_12_hour_noon_conversion(self, timespinner_root):
        """Test _on_time_change with 12-hour format noon conversion."""
        widget = TimeSpinner(timespinner_root, hour_format="12")
        widget.hour_var.set("12")
        widget.minute_var.set("00")
        widget.second_var.set("00")
        widget.am_pm_var.set("PM")
        widget._on_time_change()
        assert widget.selected_time == datetime.time(12, 0, 0)

    def test_set_selected_time_12_hour_midnight_conversion(self, timespinner_root):
        """Test set_selected_time with 12-hour format midnight conversion."""
        widget = TimeSpinner(timespinner_root, hour_format="12")
        midnight = datetime.time(0, 30, 45)
        widget.set_selected_time(midnight)
        assert widget.hour_var.get() == "12"
        assert widget.am_pm_var.get() == "AM"

    def test_set_selected_time_12_hour_noon_conversion(self, timespinner_root):
        """Test set_selected_time with 12-hour format noon conversion."""
        widget = TimeSpinner(timespinner_root, hour_format="12")
        noon = datetime.time(12, 30, 45)
        widget.set_selected_time(noon)
        assert widget.hour_var.get() == "12"
        assert widget.am_pm_var.get() == "PM"

    def test_set_initial_values_12_hour_morning_edge_case(self, timespinner_root):
        """Test _set_initial_values with 12-hour format morning edge case (hour < 12)."""
        widget = TimeSpinner(timespinner_root, hour_format="12")
        morning = datetime.time(8, 15, 30)
        widget._set_initial_values(morning)
        assert widget.hour_var.get() == "08"
        assert widget.am_pm_var.get() == "AM"

    def test_set_selected_time_12_hour_morning_edge_case(self, timespinner_root):
        """Test set_selected_time with 12-hour format morning edge case (hour < 12)."""
        widget = TimeSpinner(timespinner_root, hour_format="12")
        morning = datetime.time(8, 15, 30)
        widget.set_selected_time(morning)
        assert widget.hour_var.get() == "08"
        assert widget.am_pm_var.get() == "AM"

    def test_on_time_change_exception_handling(self, timespinner_root):
        """Test _on_time_change with exception handling."""
        widget = TimeSpinner(timespinner_root)
        original_time = widget.selected_time
        # Set invalid values that will cause ValueError
        widget.hour_var.set("invalid")
        widget.minute_var.set("invalid")
        widget.second_var.set("invalid")
        widget._on_time_change()
        # Should handle exception gracefully and keep original time
        assert widget.selected_time == original_time

    def test_on_time_change_type_error_handling(self, timespinner_root):
        """Test _on_time_change with TypeError handling."""
        widget = TimeSpinner(timespinner_root)
        original_time = widget.selected_time
        # Mock StringVar.get to raise TypeError
        widget.hour_var.get = Mock(side_effect=TypeError("Test error"))
        widget._on_time_change()
        # Should handle exception gracefully and keep original time
        assert widget.selected_time == original_time

    def test_on_ok(self, timespinner_root):
        callback_called = False
        callback_time = None

        def callback(time_obj):
            nonlocal callback_called, callback_time
            callback_called = True
            callback_time = time_obj

        widget = TimeSpinner(timespinner_root, time_callback=callback)
        widget.hour_var.set("14")
        widget.minute_var.set("30")
        widget.second_var.set("45")
        widget._on_time_change()
        widget._on_ok()
        assert callback_called
        assert callback_time == datetime.time(14, 30, 45)

    def test_on_cancel(self, timespinner_root):
        callback_called = False
        callback_time = None

        def callback(time_obj):
            nonlocal callback_called, callback_time
            callback_called = True
            callback_time = time_obj

        widget = TimeSpinner(timespinner_root, time_callback=callback)
        widget._on_cancel()
        assert callback_called
        assert callback_time is None

    def test_set_hour_format(self, timespinner_root):
        widget = TimeSpinner(timespinner_root, hour_format="24")
        widget.set_hour_format("12")
        assert widget.hour_format == "12"

    def test_set_show_seconds(self, timespinner_root):
        widget = TimeSpinner(timespinner_root, show_seconds=True)
        widget.set_show_seconds(False)
        assert widget.show_seconds is False


class TestTimePickerBase:
    """Focused tests for common _TimePickerBase behaviour."""

    def test_creation_and_config(self, timespinner_root):
        base = _TimePickerBase(timespinner_root)
        assert base.dpi_scaling_factor >= 1.0
        assert base.selected_time is None

        _test_widget_creation(_TimePickerBase, timespinner_root, use_config=True)
        _test_widget_creation(_TimePickerBase, timespinner_root, use_config=False)

    def test_dpi_scaling_error_handling(self, timespinner_root):
        _test_dpi_scaling_error_handling(_TimePickerBase, timespinner_root)

    def test_update_entry_text_not_implemented(self, timespinner_root):
        base = _TimePickerBase(timespinner_root)
        with pytest.raises(NotImplementedError):
            base._update_entry_text("text")

    def test_get_time_variants(self, timespinner_root):
        base = _TimePickerBase(timespinner_root)
        base.time_picker = None
        base.selected_time = datetime.time(10, 20, 30)
        assert base.get_time() == datetime.time(10, 20, 30)

        base.time_picker = Mock()
        expected = datetime.time(1, 2, 3)
        base.time_picker.get_selected_time.return_value = expected
        assert base.get_time() == expected

        base.get_time = Mock(return_value=None)
        assert base.get_time_string() == ""
        base.get_time = Mock(return_value=datetime.time(4, 5, 6))
        assert base.get_time_string() == "04:05:06"

    def test_setters_delegate(self, timespinner_root):
        base = _TimePickerBase(timespinner_root)
        base.time_picker = Mock()
        base.set_hour_format("12")
        assert base.hour_format == "12"
        base.time_picker.set_hour_format.assert_called_once_with("12")

        base.set_show_seconds(False)
        assert base.show_seconds is False
        base.time_picker.set_show_seconds.assert_called_once_with(False)

    def test_set_selected_time_with_and_without_picker(self, timespinner_root):
        base = _TimePickerBase(timespinner_root)
        base._update_entry_text = Mock()
        base.time_picker = None
        moment = datetime.time(12, 34, 56)
        base.set_selected_time(moment)
        base._update_entry_text.assert_called_once_with("12:34:56")

        base.time_picker = Mock()
        base._update_entry_text.reset_mock()
        base.set_selected_time(moment)
        base.time_picker.set_selected_time.assert_called_once_with(moment)
        base._update_entry_text.assert_called_once_with("12:34:56")

    def test_on_time_selected_variants(self, timespinner_root):
        recorded = {"called": False, "value": None}

        def callback(value):
            recorded["called"] = True
            recorded["value"] = value

        base = _TimePickerBase(timespinner_root, time_callback=callback)
        base._update_entry_text = Mock()
        base.hide_time_picker = Mock()

        moment = datetime.time(7, 8, 9)
        base._on_time_selected(moment)
        assert base.selected_time == moment
        assert recorded["called"] is True
        assert recorded["value"] == moment
        base._update_entry_text.assert_called_once_with("07:08:09")
        base.hide_time_picker.assert_called_once()

        recorded["called"] = False
        recorded["value"] = None
        base._update_entry_text.reset_mock()
        base.hide_time_picker.reset_mock()
        base._on_time_selected(None)
        # _on_time_selected keeps previous value when None
        assert base.selected_time == moment
        assert recorded["called"] is True
        assert recorded["value"] is None
        base._update_entry_text.assert_not_called()
        base.hide_time_picker.assert_called_once()

    def test_show_and_hide_time_picker_behaviour(self, timespinner_root):
        base = _TimePickerBase(timespinner_root)
        popup = Mock()
        base.popup = popup
        base.show_time_picker()
        assert base.popup is popup

        popup = Mock()
        base.popup = popup
        base.time_picker = Mock()
        base.hide_time_picker()
        popup.destroy.assert_called_once()
        assert base.popup is None
        assert base.time_picker is None

    def test_focus_and_click_handling(self, timespinner_root):
        base = _TimePickerBase(timespinner_root)
        base.popup = Mock()
        base.time_picker = Mock()

        base._setup_focus()
        base.popup.lift.assert_called_once()
        base.time_picker.focus_set.assert_called()

        base.popup.lift.side_effect = tk.TclError("boom")
        base._setup_focus()

        popup = create_mock_popup_window()
        hide_callback = Mock()
        event = Mock()
        event.widget = "string"
        base._on_main_window_click(event, popup, hide_callback)
        hide_callback.assert_not_called()

        event.widget = Mock()
        event.x = -100
        event.y = -100
        base.master = Mock()
        mock_toplevel = Mock()
        mock_toplevel.winfo_rootx.return_value = 0
        mock_toplevel.winfo_rooty.return_value = 0
        base.master.winfo_toplevel.return_value = mock_toplevel
        base._on_main_window_click(event, popup, hide_callback)
        hide_callback.assert_called()

        time_picker_widget = Mock()
        event.widget = "string"
        base._on_popup_click(event, popup, time_picker_widget, hide_callback)
        time_picker_widget.focus_set.assert_called()

        base._is_child_of_time_picker = Mock(return_value=True)
        event.widget = Mock()
        base._on_popup_click(event, popup, time_picker_widget, hide_callback)

        base._is_child_of_time_picker = Mock(side_effect=Exception("boom"))
        base._on_popup_click(event, popup, time_picker_widget, hide_callback)

        base.focus_get = Mock(return_value=Mock())
        base._is_child_of_time_picker = Mock(return_value=True)
        assert base._on_focus_out(Mock()) == "break"

        base.focus_get = Mock(return_value=base)
        assert base._on_focus_out(Mock()) == "break"

        base.focus_get = Mock(return_value=None)
        popup.winfo_pointerxy.return_value = (0, 0)
        base.hide_time_picker = Mock()
        base._on_focus_out(Mock())
        base.hide_time_picker.assert_called()

        base.time_picker = Mock()
        base.popup = Mock()
        base.master = Mock()
        base.master.winfo_toplevel.return_value = Mock()
        base.master.winfo_toplevel.return_value.winfo_rootx.return_value = 0
        base.master.winfo_toplevel.return_value.winfo_rooty.return_value = 0
        base._setup_click_outside_handling()
        base.time_picker.bind.assert_called_once()
        base.popup.bind.assert_called()

        base.hide_time_picker = Mock()
        target = Mock()
        base._schedule_focus_restore(target, generate_click=True)
        target.after_idle.assert_called()

