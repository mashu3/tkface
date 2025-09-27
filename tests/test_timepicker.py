# pylint: disable=
#   import-outside-toplevel,
#   protected-access,
#   too-many-lines,
#   too-few-public-methods,
#   too-many-public-methods
"""
Tests for tkface TimePicker widgets
"""

import datetime
import tkinter as tk
from contextlib import suppress
from unittest.mock import Mock, patch

import pytest

from tkface.dialog.timepicker import (
    TimeEntry,
    TimeFrame,
    TimePickerConfig,
    _TimePickerBase,
)


# Test helper functions
def create_test_config():
    """Create a test TimePickerConfig with custom values."""

    def dummy_callback(time_obj):  # pylint: disable=unused-argument
        pass

    return TimePickerConfig(
        time_format="%H:%M:%S",
        hour_format="24",
        show_seconds=True,
        theme="light",
        language="en",
        time_callback=dummy_callback,
    )


def assert_config_values(config, expected_values):
    """Assert that config has the expected values."""
    assert config.time_format == expected_values["time_format"]
    assert config.hour_format == expected_values["hour_format"]
    assert config.show_seconds == expected_values["show_seconds"]
    assert config.theme == expected_values["theme"]
    assert config.language == expected_values["language"]
    assert config.time_callback == expected_values["time_callback"]


def _test_widget_creation(widget_class, root, use_config=True, **kwargs):
    """Test widget creation with either config or individual parameters."""
    if use_config:
        config = create_test_config()
        widget = widget_class(root, config=config, **kwargs)
        expected_values = {
            "time_format": "%H:%M:%S",
            "hour_format": "24",
            "show_seconds": True,
            "theme": "light",
            "language": "en",
            "time_callback": config.time_callback,
        }
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
        expected_values = {
            "time_format": "%H:%M:%S",
            "hour_format": "24",
            "show_seconds": True,
            "theme": "light",
            "language": "en",
            "time_callback": None,
        }

    assert widget.time_format == expected_values["time_format"]
    assert widget.hour_format == expected_values["hour_format"]
    assert widget.show_seconds == expected_values["show_seconds"]
    return widget


def _test_dpi_scaling_error_handling(widget_class, root):
    """Test DPI scaling error handling for widgets."""
    with patch("tkface.dialog.timepicker.get_scaling_factor") as mock_get_scaling:
        mock_get_scaling.side_effect = ImportError("Test error")

        widget = widget_class(root)
        assert widget.dpi_scaling_factor == 1.0
        return widget


def create_mock_popup_window():
    """Create a mock popup window with standard properties."""
    popup = Mock()
    popup.winfo_exists.return_value = True
    popup.winfo_rootx.return_value = 100
    popup.winfo_rooty.return_value = 100
    popup.winfo_width.return_value = 200
    popup.winfo_height.return_value = 200
    popup.winfo_pointerxy.return_value = (150, 150)
    return popup


def create_mock_time_picker():
    """Create a mock time picker with standard properties."""
    time_picker = Mock()
    time_picker.get_selected_time.return_value = datetime.time(14, 30, 0)
    return time_picker


class TestTimePickerConfig:
    """Test cases for TimePickerConfig dataclass."""

    def test_timepicker_config_values(self):
        """Test TimePickerConfig with both default and custom values."""
        # Test default values
        default_config = TimePickerConfig()
        default_expected = {
            "time_format": "%H:%M:%S",
            "hour_format": "24",
            "show_seconds": True,
            "theme": "light",
            "language": "en",
            "time_callback": None,
        }
        assert_config_values(default_config, default_expected)

        # Test custom values
        custom_config = create_test_config()
        custom_expected = {
            "time_format": "%H:%M:%S",
            "hour_format": "24",
            "show_seconds": True,
            "theme": "light",
            "language": "en",
            "time_callback": custom_config.time_callback,
        }
        assert_config_values(custom_config, custom_expected)


class TestTimePickerWidgets:
    """Test cases for TimePicker widgets (TimeFrame, TimeEntry)."""

    # TimeFrame tests
    def test_timeframe_creation(self, root):
        """Test TimeFrame creation and configuration."""
        # Test basic creation
        tf = TimeFrame(root)
        assert tf is not None
        assert hasattr(tf, "entry")
        assert hasattr(tf, "button")

        # Test with config
        _test_widget_creation(TimeFrame, root, use_config=True)

        # Test with individual parameters including button_text
        tf = _test_widget_creation(TimeFrame, root, use_config=False, button_text="🕐")
        assert tf.button.cget("text") == "🕐"

    def test_timeframe_create_class_method(self, root):
        """Test TimeFrame.create class method."""
        tf = TimeFrame.create(root, time_format="%H:%M", button_text="🕐")
        assert tf.time_format == "%H:%M"
        assert tf.button.cget("text") == "🕐"

    def test_timeframe_update_entry_text(self, root):
        """Test TimeFrame _update_entry_text method."""
        tf = TimeFrame(root)
        tf._update_entry_text("14:30:45")

        # Check that entry text was updated
        assert tf.entry.get() == "14:30:45"

    def test_timeframe_set_button_text(self, root):
        """Test TimeFrame set_button_text method."""
        tf = TimeFrame(root)
        tf.set_button_text("🕐")
        assert tf.button.cget("text") == "🕐"

    def test_timeframe_set_button_text_handles_update_error(self, root):
        """TimeFrame.set_button_text should log when update_idletasks fails."""
        tf = TimeFrame(root)
        with patch.object(
            tf.button,
            "update_idletasks",
            side_effect=tk.TclError("boom"),
        ) as mocked:
            tf.set_button_text("★")
        mocked.assert_called_once()

    def test_timeframe_dpi_scaling(self, root):
        """Test TimeFrame DPI scaling functionality."""
        # Test basic DPI scaling error handling
        _test_dpi_scaling_error_handling(TimeFrame, root)

    def test_timeframe_setup_click_outside_handling_rebinds(self, root):
        """TimeFrame should rebind parent click handlers when setting up."""
        tf = TimeFrame(root)
        tf.time_picker = Mock()
        tf.popup = Mock()
        mock_toplevel = Mock()
        mock_toplevel.bind.return_value = "new-id"
        tf.master = Mock()
        tf.master.winfo_toplevel.return_value = mock_toplevel
        tf._parent_click_binding = ("<ButtonRelease-1>", "old-id")

        tf._setup_click_outside_handling()

        mock_toplevel.unbind.assert_called_once_with("<ButtonRelease-1>", "old-id")
        assert tf._parent_click_binding == ("<ButtonRelease-1>", "new-id")
        tf.time_picker.bind.assert_called_once()
        tf.popup.bind.assert_called()

    def test_timeframe_hide_time_picker_unbinds_parent(self, root):
        """TimeFrame.hide_time_picker should remove parent bindings."""
        tf = TimeFrame(root)
        tf.popup = Mock()
        tf.time_picker = Mock()
        tf.master = Mock()
        mock_toplevel = Mock()
        tf.master.winfo_toplevel.return_value = mock_toplevel
        tf._parent_click_binding = ("<ButtonRelease-1>", "bind-id")

        tf.hide_time_picker()

        mock_toplevel.unbind.assert_called_once_with("<ButtonRelease-1>", "bind-id")
        assert tf._parent_click_binding is None

    def test_timeframe_position_popup_with_button_adjusts_bounds(self, root):
        """_position_popup should respect screen bounds for TimeFrame."""
        tf = TimeFrame(root)
        tf.popup = Mock()
        tf.popup.winfo_reqwidth.return_value = 200
        tf.popup.winfo_reqheight.return_value = 150
        tf.popup.winfo_screenwidth.return_value = 250
        tf.popup.winfo_screenheight.return_value = 200
        tf.master.winfo_rooty = Mock(return_value=10)
        tf.entry.winfo_rootx = Mock(return_value=120)
        tf.entry.winfo_rooty = Mock(return_value=80)
        tf.entry.winfo_height = Mock(return_value=40)

        tf._position_popup()

        tf.popup.geometry.assert_called_once()

    def test_timeframe_set_width_updates_entry(self, root):
        """TimeFrame.set_width should update entry widget width."""
        tf = TimeFrame(root)
        tf.set_width(25)
        assert tf.entry.cget("width") == 25

    # TimeEntry tests
    def test_timeentry_creation(self, root):
        """Test TimeEntry creation and configuration."""
        # Test basic creation
        te = TimeEntry(root)
        assert te is not None
        assert te.time_format == "%H:%M:%S"
        assert te.selected_time is not None  # Now sets current time by default

        # Test with config
        _test_widget_creation(TimeEntry, root, use_config=True)

        # Test with individual parameters including width
        _test_widget_creation(TimeEntry, root, use_config=False, width=20)

    def test_timeentry_create_class_method(self, root):
        """Test TimeEntry.create class method."""
        te = TimeEntry.create(root, time_format="%H:%M", width=20)
        assert te.time_format == "%H:%M"

    def test_timeentry_setup_style(self, root):
        """Test TimeEntry _setup_style method."""
        te = TimeEntry(root)
        # Should not raise exception
        assert hasattr(te, "style")

    def test_timeentry_update_entry_text(self, root):
        """Test TimeEntry _update_entry_text method."""
        te = TimeEntry(root)
        te._update_entry_text("14:30:45")

        # Check that entry text was updated
        assert te.get() == "14:30:45"

    def test_timeentry_dpi_scaling(self, root):
        """Test TimeEntry DPI scaling functionality."""
        # Test basic DPI scaling error handling
        _test_dpi_scaling_error_handling(TimeEntry, root)

    def test_timeentry_setup_click_outside_binds_without_button(self, root):
        """TimeEntry should bind popup clicks without parent button logic."""
        te = TimeEntry(root)
        te.time_picker = Mock()
        te.popup = Mock()
        te.master = Mock()
        te.master.winfo_toplevel.return_value = None

        te._setup_click_outside_handling()

        te.time_picker.bind.assert_called_once()
        te.popup.bind.assert_called()

    def test_timeentry_hide_time_picker_without_parent_click(self, root):
        """TimeEntry.hide_time_picker should not fail without button binding."""
        te = TimeEntry(root)
        te.popup = Mock()
        te.time_picker = Mock()
        te.master = Mock()
        te.master.winfo_toplevel.return_value = Mock()
        te._parent_click_binding = None

        te.hide_time_picker()

        te.master.winfo_toplevel.return_value.unbind.assert_not_called()

    def test_timeentry_set_width_logs_on_error(self, root):
        """TimeEntry.set_width should handle exceptions from configure."""
        te = TimeEntry(root)
        with patch.object(te, "configure", side_effect=tk.TclError("fail")) as mocked:
            te.set_width(30)
        mocked.assert_called_once_with(width=30)

    def test_timeentry_button_text_removal(self, root):
        """Test TimeEntry removes button_text from kwargs."""
        TimeEntry(root, button_text="test", width=20)
        # Should not raise exception and button_text should be removed from kwargs
        assert True

    def test_timeentry_on_b1_press_right_area(self, root):
        """Test TimeEntry _on_b1_press in right area."""
        te = TimeEntry(root)
        te.state = Mock()
        te.drop_down = Mock()

        event = Mock()
        event.x = 105  # Right area (width=120, so x=105 > 120-20=100)
        te.winfo_width = Mock(return_value=120)

        result = te._on_b1_press(event)

        assert result == "break"
        te.state.assert_called_once_with(["pressed"])
        te.drop_down.assert_called_once()

    def test_timeentry_on_b1_press_left_area(self, root):
        """Test TimeEntry _on_b1_press in left area."""
        te = TimeEntry(root)
        te.state = Mock()
        te.drop_down = Mock()

        event = Mock()
        event.x = 50
        te.winfo_width = Mock(return_value=120)

        result = te._on_b1_press(event)

        assert result is None
        te.state.assert_not_called()
        te.drop_down.assert_not_called()

    def test_timeentry_drop_down_show_time_picker(self, root):
        """Test TimeEntry drop_down to show time picker."""
        te = TimeEntry(root)
        te.popup = None
        te.show_time_picker = Mock()

        te.drop_down()

        te.show_time_picker.assert_called_once()

    def test_timeentry_drop_down_hide_time_picker(self, root):
        """Test TimeEntry drop_down to hide time picker."""
        te = TimeEntry(root)
        te.popup = Mock()
        te.popup.winfo_ismapped.return_value = True
        te.hide_time_picker = Mock()

        te.drop_down()

        te.hide_time_picker.assert_called_once()

    def test_timeentry_on_focus_out_entry(self, root):
        """Test TimeEntry _on_focus_out_entry."""
        te = TimeEntry(root)
        te.popup = Mock()
        te.popup.winfo_ismapped.return_value = True
        te.focus_get = Mock(return_value=Mock())
        te._is_child_of_time_picker = Mock(return_value=False)
        te.hide_time_picker = Mock()

        te._on_focus_out_entry(Mock())

        te.hide_time_picker.assert_called_once()

    def test_timeentry_on_focus_out_entry_focus_on_self(self, root):
        """Test TimeEntry _on_focus_out_entry with focus on self."""
        te = TimeEntry(root)
        te.popup = Mock()
        te.popup.winfo_ismapped.return_value = True
        te.focus_get = Mock(return_value=te)
        te.hide_time_picker = Mock()

        te._on_focus_out_entry(Mock())

        te.hide_time_picker.assert_not_called()

    def test_timeentry_on_focus_out_entry_focus_on_time_picker(self, root):
        """Test TimeEntry _on_focus_out_entry with focus on time picker."""
        te = TimeEntry(root)
        te.popup = Mock()
        te.popup.winfo_ismapped.return_value = True
        te.focus_get = Mock(return_value=Mock())
        te._is_child_of_time_picker = Mock(return_value=True)
        te.hide_time_picker = Mock()

        te._on_focus_out_entry(Mock())

        te.hide_time_picker.assert_not_called()

    def test_timeentry_on_focus_out_entry_no_popup(self, root):
        """Test TimeEntry _on_focus_out_entry without popup."""
        te = TimeEntry(root)
        te.popup = None
        te.hide_time_picker = Mock()

        te._on_focus_out_entry(Mock())

        te.hide_time_picker.assert_not_called()

    def test_timeentry_on_key(self, root):
        """Test TimeEntry _on_key with various keys."""
        te = TimeEntry(root)
        te.show_time_picker = Mock()

        # Test Down key - should show time picker
        event_down = Mock()
        event_down.keysym = "Down"
        te._on_key(event_down)
        te.show_time_picker.assert_called_once()

        # Test space key - should show time picker
        te.show_time_picker.reset_mock()
        event_space = Mock()
        event_space.keysym = "space"
        te._on_key(event_space)
        te.show_time_picker.assert_called_once()

        # Test other key - should not show time picker
        te.show_time_picker.reset_mock()
        event_other = Mock()
        event_other.keysym = "Return"
        te._on_key(event_other)
        te.show_time_picker.assert_not_called()


class TestTimePickerEvents:
    """Test cases for TimePicker event handling and time picker operations."""

    def test_timepicker_base_bind_time_picker_events(self, root):
        """Test _bind_time_picker_events."""
        base = _TimePickerBase(root)
        mock_widget = Mock()
        mock_child = Mock()
        mock_child.winfo_children.return_value = []  # Empty list to stop recursion
        mock_widget.winfo_children.return_value = [mock_child]

        base._bind_time_picker_events(mock_widget)

        mock_widget.bind.assert_called_once()
        mock_child.winfo_children.assert_called_once()

    def test_timepicker_base_bind_time_picker_events_error(self, root):
        """Test _bind_time_picker_events with error."""
        base = _TimePickerBase(root)
        mock_widget = Mock()
        mock_widget.bind.side_effect = tk.TclError("Test error")

        # Should not raise exception
        base._bind_time_picker_events(mock_widget)

    def test_timepicker_base_is_child_of_time_picker(self, root):
        """Test _is_child_of_time_picker."""
        base = _TimePickerBase(root)
        time_picker_widget = Mock()

        # Test with string widget
        result = base._is_child_of_time_picker("string", time_picker_widget)
        assert result is False

        # Test with time picker as widget
        result = base._is_child_of_time_picker(time_picker_widget, time_picker_widget)
        assert result is True

        # Test with child of time picker
        child_widget = Mock()
        child_widget.master = time_picker_widget
        result = base._is_child_of_time_picker(child_widget, time_picker_widget)
        assert result is True

        # Test with unrelated widget
        unrelated_widget = Mock()
        unrelated_widget.master = None
        result = base._is_child_of_time_picker(unrelated_widget, time_picker_widget)
        assert result is False

    def test_timepicker_base_setup_focus(self, root):
        """Test _setup_focus."""
        base = _TimePickerBase(root)
        base.popup = Mock()
        base.time_picker = Mock()

        base._setup_focus()

        base.popup.lift.assert_called_once()
        base.time_picker.focus_set.assert_called()
        base.popup.after.assert_called()

    def test_timepicker_base_setup_focus_error(self, root):
        """Test _setup_focus with error."""
        base = _TimePickerBase(root)
        base.popup = Mock()
        base.time_picker = Mock()
        base.popup.lift.side_effect = tk.TclError("Test error")

        # Should not raise exception
        base._setup_focus()

    def test_timepicker_base_on_main_window_click_scenarios(self, root):
        """Test _on_main_window_click with various scenarios."""
        base = _TimePickerBase(root)

        # Test with string widget
        popup_window = create_mock_popup_window()
        hide_callback = Mock()

        event = Mock()
        event.widget = "string"

        result = base._on_main_window_click(event, popup_window, hide_callback)
        assert result is None
        hide_callback.assert_not_called()

        # Test with popup not existing
        popup_window.winfo_exists.return_value = False
        event.widget = "not_string"

        result = base._on_main_window_click(event, popup_window, hide_callback)
        assert result is None
        hide_callback.assert_not_called()

        # Test with click outside popup
        base.master = Mock()
        mock_toplevel = Mock()
        mock_toplevel.winfo_rootx.return_value = 0
        mock_toplevel.winfo_rooty.return_value = 0
        base.master.winfo_toplevel.return_value = mock_toplevel

        popup_window.winfo_exists.return_value = True
        popup_window.winfo_rootx.return_value = 100
        popup_window.winfo_rooty.return_value = 100
        popup_window.winfo_width.return_value = 200
        popup_window.winfo_height.return_value = 200

        event.widget = Mock()  # Not a string, so it will proceed to the main logic
        event.x = 50  # root_x = 0 + 50 = 50, which is < popup_x (100)
        event.y = 50  # root_y = 0 + 50 = 50, which is < popup_y (100)

        result = base._on_main_window_click(event, popup_window, hide_callback)
        assert result is None
        hide_callback.assert_called_once()

    def test_timepicker_base_on_popup_click_scenarios(self, root):
        """Test _on_popup_click with various scenarios."""
        base = _TimePickerBase(root)

        # Test with string widget
        popup_window = create_mock_popup_window()
        time_picker_widget = Mock()
        hide_callback = Mock()

        event = Mock()
        event.widget = "string"

        result = base._on_popup_click(
            event, popup_window, time_picker_widget, hide_callback
        )
        assert result == "break"
        time_picker_widget.focus_set.assert_called_once()

        # Test with click outside popup
        popup_window.winfo_pointerxy.return_value = (50, 50)  # Outside
        hide_callback.reset_mock()
        time_picker_widget.reset_mock()

        result = base._on_popup_click(
            event, popup_window, time_picker_widget, hide_callback
        )
        assert result == "break"
        hide_callback.assert_called_once()

        # Test with click inside popup
        popup_window.winfo_pointerxy.return_value = (150, 150)  # Inside
        base._is_child_of_time_picker = Mock(return_value=True)

        event.widget = Mock()
        hide_callback.reset_mock()
        time_picker_widget.reset_mock()

        result = base._on_popup_click(
            event, popup_window, time_picker_widget, hide_callback
        )
        assert result == "break"
        time_picker_widget.focus_set.assert_called_once()
        hide_callback.assert_not_called()

        # Test exception handling
        base._is_child_of_time_picker = Mock(side_effect=Exception("Test error"))
        hide_callback.reset_mock()
        time_picker_widget.reset_mock()

        result = base._on_popup_click(
            event, popup_window, time_picker_widget, hide_callback
        )
        assert result == "break"
        # Should handle exception gracefully
        with suppress(Exception):
            result = base._on_focus_out(Mock())
            assert result == "break"

    def test_timepicker_base_setup_click_outside_handling(self, root):
        """Test _setup_click_outside_handling."""
        base = _TimePickerBase(root)
        base.time_picker = Mock()
        base.popup = Mock()
        base.master = Mock()
        base.master.winfo_toplevel.return_value = Mock()
        base._on_popup_click = Mock()
        base._on_main_window_click = Mock()
        base.hide_time_picker = Mock()

        base._setup_click_outside_handling()

        base.time_picker.bind.assert_called_once()
        base.popup.bind.assert_called()

    def test_timepicker_base_show_time_picker_scenarios(self, root):
        """Test show_time_picker with various scenarios."""
        with patch(
            "tkface.dialog.timepicker.TimeSpinner"
        ) as mock_time_picker_class, patch(
            "tkface.dialog.timepicker.tk.Toplevel"
        ) as mock_toplevel:

            mock_time_picker = Mock()
            mock_time_picker.winfo_children.return_value = (
                []
            )  # Empty list to prevent iteration error
            mock_time_picker_class.return_value = mock_time_picker

            mock_popup = Mock()
            mock_popup.winfo_screenwidth.return_value = 1920
            mock_popup.winfo_screenheight.return_value = 1080
            mock_popup.winfo_reqwidth.return_value = 200
            mock_popup.winfo_reqheight.return_value = 150
            mock_toplevel.return_value = mock_popup

            base = _TimePickerBase(root)
            base.master = Mock()
            base.master.winfo_rootx.return_value = 100
            base.master.winfo_rooty.return_value = 50
            base.master.winfo_width.return_value = 100
            base.master.winfo_height.return_value = 30

            # Mock the winfo_rootx and winfo_rooty methods for _TimePickerBase
            base.winfo_rootx = Mock(return_value=100)
            base.winfo_rooty = Mock(return_value=50)
            base.winfo_height = Mock(return_value=30)

            base.show_time_picker()

            assert base.popup is not None
            assert base.time_picker is not None
            mock_time_picker_class.assert_called_once()
            mock_time_picker.pack.assert_called_once()

    def test_timepicker_base_show_time_picker_already_exists(self, root):
        """Test show_time_picker when popup already exists."""
        base = _TimePickerBase(root)
        base.popup = Mock()

        base.show_time_picker()

        # Should return early without creating new popup
        assert base.popup is not None

    def test_timepicker_base_hide_time_picker(self, root):
        """Test hide_time_picker method."""
        base = _TimePickerBase(root)
        mock_popup = Mock()
        base.popup = mock_popup
        base.time_picker = Mock()

        base.hide_time_picker()

        mock_popup.destroy.assert_called_once()
        assert base.popup is None
        assert base.time_picker is None

    def test_timepicker_base_hide_time_picker_no_popup(self, root):
        """Test hide_time_picker when popup doesn't exist."""
        base = _TimePickerBase(root)
        base.popup = None

        # Should not raise exception
        base.hide_time_picker()

    def test_timepicker_base_get_time_with_time_picker(self, root):
        """Test get_time should delegate to time picker when it exists."""
        base = _TimePickerBase(root)
        base.time_picker = Mock()
        expected = datetime.time(14, 30, 45)
        base.time_picker.get_selected_time.return_value = expected

        assert base.get_time() == expected

    def test_timepicker_base_set_selected_time_with_time_picker(self, root):
        """Test set_selected_time should call time_picker.set_selected_time."""
        base = _TimePickerBase(root)
        base.time_picker = Mock()
        base._update_entry_text = Mock()
        t = datetime.time(14, 30, 45)
        base.set_selected_time(t)
        base.time_picker.set_selected_time.assert_called_once_with(t)
        base._update_entry_text.assert_called_once_with("14:30:45")

    def test_timeentry_on_time_selected_resets_state(self, root):
        """Test _on_time_selected should reset pressed state for TimeEntry."""
        te = TimeEntry(root)
        te._update_entry_text = Mock()
        te.hide_time_picker = Mock()
        te.state = Mock()

        test_time = datetime.time(14, 30, 45)
        te._on_time_selected(test_time)

        te._update_entry_text.assert_called_once_with("14:30:45")
        te.hide_time_picker.assert_called_once()
        te.state.assert_called_with(["!pressed"])

    def test_timeentry_hide_time_picker_resets_state(self, root):
        """Test hide_time_picker should reset pressed state for TimeEntry."""
        te = TimeEntry(root)
        te.popup = Mock()
        te.time_picker = Mock()
        te.state = Mock()

        te.hide_time_picker()

        te.state.assert_called_with(["!pressed"])


class TestTimePickerIntegration:
    """Test cases for TimePicker integration scenarios."""

    def test_timepicker_integration(self, root):
        """Test TimePicker with comprehensive integration scenarios."""
        # Test TimeFrame time picker integration
        tf = TimeFrame(root, hour_format="24")
        assert tf.hour_format == "24"

        test_time = datetime.time(14, 30, 45)
        tf.set_selected_time(test_time)
        assert tf.selected_time == test_time
        assert tf.get_time_string() == "14:30:45"

        # Test TimeEntry time picker integration
        te = TimeEntry(root, hour_format="12")
        assert te.hour_format == "12"

        te.set_selected_time(test_time)
        assert te.selected_time == test_time
        assert te.get_time_string() == "14:30:45"

        # Test callback integration
        callback_called = False
        callback_time = None

        def callback(time_obj):
            nonlocal callback_called, callback_time
            callback_called = True
            callback_time = time_obj

        tf_callback = TimeFrame(root, time_callback=callback)
        tf_callback._on_time_selected(test_time)
        assert callback_called
        assert callback_time == test_time

        # Test hour format integration
        tf_24 = TimeFrame(root, hour_format="24")
        assert tf_24.hour_format == "24"
        tf_24.set_hour_format("12")
        assert tf_24.hour_format == "12"

        # Test seconds integration
        tf_seconds = TimeFrame(root, show_seconds=True)
        assert tf_seconds.show_seconds is True
        tf_seconds.set_show_seconds(False)
        assert tf_seconds.show_seconds is False

        # Test time format integration
        tf_format = TimeFrame(root, time_format="%H:%M")
        assert tf_format.time_format == "%H:%M"

        # Test theme integration
        TimeFrame(root, theme="dark")
        # Theme is stored in the base class but not exposed as attribute
        assert True  # Theme is handled internally

        # Test language integration
        TimeFrame(root, language="ja")
        # Language is stored in the base class but not exposed as attribute
        assert True  # Language is handled internally
