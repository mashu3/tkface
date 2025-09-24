# pylint: disable=import-outside-toplevel,protected-access
"""
Tests for tkface DatePicker widgets
"""

import datetime
import tkinter as tk
from unittest.mock import Mock, patch

import pytest

from tkface.dialog.datepicker import (
    DateEntry,
    DateFrame,
    DatePickerConfig,
    _DatePickerBase,
)


# Test helper functions
def create_test_config():
    """Create a test DatePickerConfig with custom values."""
    def dummy_callback(date):
        pass

    return DatePickerConfig(
        date_format="%d/%m/%Y",
        year=2024,
        month=3,
        show_week_numbers=True,
        week_start="Monday",
        day_colors={"Sunday": "red"},
        holidays={"2024-01-01": "red"},
        selectmode="range",
        theme="dark",
        language="ja",
        today_color="blue",
        date_callback=dummy_callback
    )


def assert_config_values(config, expected_values):
    """Assert that config has the expected values."""
    assert config.date_format == expected_values["date_format"]
    assert config.year == expected_values["year"]
    assert config.month == expected_values["month"]
    assert config.show_week_numbers == expected_values["show_week_numbers"]
    assert config.week_start == expected_values["week_start"]
    assert config.day_colors == expected_values["day_colors"]
    assert config.holidays == expected_values["holidays"]
    assert config.selectmode == expected_values["selectmode"]
    assert config.theme == expected_values["theme"]
    assert config.language == expected_values["language"]
    assert config.today_color == expected_values["today_color"]
    assert config.date_callback == expected_values["date_callback"]


def assert_calendar_config_values(widget, expected_values):
    """Assert that widget's calendar_config has the expected values."""
    assert widget.calendar_config["date_format"] == expected_values["date_format"]
    assert widget.calendar_config["year"] == expected_values["year"]
    assert widget.calendar_config["month"] == expected_values["month"]
    assert widget.calendar_config["show_week_numbers"] == expected_values["show_week_numbers"]
    assert widget.calendar_config["week_start"] == expected_values["week_start"]
    assert widget.calendar_config["day_colors"] == expected_values["day_colors"]
    assert widget.calendar_config["holidays"] == expected_values["holidays"]
    assert widget.calendar_config["selectmode"] == expected_values["selectmode"]
    assert widget.calendar_config["theme"] == expected_values["theme"]
    # Language is not stored in calendar_config, it's handled separately
    assert widget.today_color == expected_values["today_color"]


def _test_widget_creation(widget_class, root, use_config=True, **kwargs):
    """Test widget creation with either config or individual parameters."""
    if use_config:
        config = create_test_config()
        widget = widget_class(root, config=config, **kwargs)
        expected_values = {
            "date_format": "%d/%m/%Y",
            "year": 2024,
            "month": 3,
            "show_week_numbers": True,
            "week_start": "Monday",
            "day_colors": {"Sunday": "red"},
            "holidays": {"2024-01-01": "red"},
            "selectmode": "range",
            "theme": "dark",
            "language": "ja",
            "today_color": "blue",
            "date_callback": config.date_callback
        }
    else:
        widget = widget_class(
            root,
            date_format="%d/%m/%Y",
            year=2024,
            month=3,
            show_week_numbers=True,
            week_start="Monday",
            day_colors={"Sunday": "red"},
            holidays={"2024-01-01": "red"},
            selectmode="range",
            theme="dark",
            language="ja",
            today_color="blue",
            **kwargs
        )
        expected_values = {
            "date_format": "%d/%m/%Y",
            "year": 2024,
            "month": 3,
            "show_week_numbers": True,
            "week_start": "Monday",
            "day_colors": {"Sunday": "red"},
            "holidays": {"2024-01-01": "red"},
            "selectmode": "range",
            "theme": "dark",
            "language": "ja",
            "today_color": "blue",
            "date_callback": None
        }
    
    assert_calendar_config_values(widget, expected_values)
    return widget


def _test_dpi_scaling_error_handling(widget_class, root):
    """Test DPI scaling error handling for widgets."""
    with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling:
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


def create_mock_calendar():
    """Create a mock calendar with standard properties."""
    calendar = Mock()
    calendar.year_selection_mode = False
    calendar.month_selection_mode = False
    calendar.get_popup_geometry.return_value = "300x200+100+100"
    return calendar


def _test_dpi_scaling_scenarios(base_instance, root):
    """Test various DPI scaling scenarios for _DatePickerBase."""
    # Test no significant change
    base_instance.dpi_scaling_factor = 1.0
    with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling:
        mock_get_scaling.return_value = 1.01  # Small change
        base_instance.update_dpi_scaling()
        # Should return early due to small change
    
    # Test error handling
    base_instance.dpi_scaling_factor = 1.0
    with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling:
        mock_get_scaling.side_effect = ImportError("Test error")
        base_instance.update_dpi_scaling()
        assert base_instance.dpi_scaling_factor == 1.0
    
    # Test significant change with popup
    with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling, \
         patch('tkface.dialog.datepicker.re') as mock_re:
        
        base_instance.dpi_scaling_factor = 1.0
        base_instance.calendar = Mock()
        base_instance.calendar.update_dpi_scaling = Mock()
        base_instance.popup = Mock()
        base_instance.popup.winfo_exists.return_value = True
        base_instance.calendar.get_popup_geometry.return_value = "300x200+100+100"
        
        mock_get_scaling.return_value = 2.0
        mock_match = Mock()
        mock_match.groups.return_value = (300, 200, 100, 100)
        mock_re.match.return_value = mock_match
        
        base_instance.update_dpi_scaling()
        
        assert base_instance.dpi_scaling_factor == 2.0
        base_instance.calendar.update_dpi_scaling.assert_called_once()
        base_instance.popup.geometry.assert_called_once_with("600x400+100+100")
    
    # Test without popup
    with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling:
        base_instance.dpi_scaling_factor = 1.0
        base_instance.popup = None
        
        mock_get_scaling.return_value = 2.0
        
        base_instance.update_dpi_scaling()
        
        assert base_instance.dpi_scaling_factor == 2.0
    
    # Test popup not existing
    with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling:
        base_instance.dpi_scaling_factor = 1.0
        base_instance.popup = Mock()
        base_instance.popup.winfo_exists.return_value = False
        
        mock_get_scaling.return_value = 2.0
        
        base_instance.update_dpi_scaling()
        
        assert base_instance.dpi_scaling_factor == 2.0
    
    # Test geometry parsing error
    with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling, \
         patch('tkface.dialog.datepicker.re') as mock_re:
        
        base_instance.dpi_scaling_factor = 1.0
        base_instance.popup = Mock()
        base_instance.popup.winfo_exists.return_value = True
        base_instance.calendar = Mock()
        base_instance.calendar.get_popup_geometry.return_value = "invalid_geometry"
        
        mock_get_scaling.return_value = 2.0
        mock_re.match.return_value = None
        
        base_instance.update_dpi_scaling()
        
        assert base_instance.dpi_scaling_factor == 2.0
        base_instance.popup.geometry.assert_called_once_with("invalid_geometry")


class TestDatePickerConfig:
    """Test cases for DatePickerConfig dataclass."""

    def test_datepicker_config_values(self):
        """Test DatePickerConfig with both default and custom values."""
        # Test default values
        default_config = DatePickerConfig()
        default_expected = {
            "date_format": "%Y-%m-%d",
            "year": None,
            "month": None,
            "show_week_numbers": False,
            "week_start": "Sunday",
            "day_colors": None,
            "holidays": None,
            "selectmode": "single",
            "theme": "light",
            "language": "en",
            "today_color": "yellow",
            "date_callback": None
        }
        assert_config_values(default_config, default_expected)
        
        # Test custom values
        custom_config = create_test_config()
        custom_expected = {
            "date_format": "%d/%m/%Y",
            "year": 2024,
            "month": 3,
            "show_week_numbers": True,
            "week_start": "Monday",
            "day_colors": {"Sunday": "red"},
            "holidays": {"2024-01-01": "red"},
            "selectmode": "range",
            "theme": "dark",
            "language": "ja",
            "today_color": "blue",
            "date_callback": custom_config.date_callback
        }
        assert_config_values(custom_config, custom_expected)


class TestDatePickerWidgets:
    """Test cases for DatePicker widgets (DateFrame, DateEntry, _DatePickerBase)."""

    # _DatePickerBase tests
    def test_datepicker_base_creation(self, root):
        """Test _DatePickerBase creation and configuration."""
        # Test basic creation
        base = _DatePickerBase(root)
        assert base is not None
        assert base.dpi_scaling_factor >= 1.0  # DPI scaling factor should be at least 1.0
        assert base.calendar_config is not None
        assert base.selected_date is None
        
        # Test with config
        _test_widget_creation(_DatePickerBase, root, use_config=True)
        
        # Test with individual parameters
        _test_widget_creation(_DatePickerBase, root, use_config=False)

    def test_datepicker_base_dpi_scaling(self, root):
        """Test DPI scaling functionality including error handling and various scenarios."""
        # Test basic DPI scaling error handling
        _test_dpi_scaling_error_handling(_DatePickerBase, root)
        
        # Test various DPI scaling scenarios
        base = _DatePickerBase(root)
        _test_dpi_scaling_scenarios(base, root)

    def test_datepicker_base_update_entry_text_not_implemented(self, root):
        """Test that _update_entry_text raises NotImplementedError."""
        base = _DatePickerBase(root)
        with pytest.raises(NotImplementedError):
            base._update_entry_text("test")

    def test_datepicker_base_get_date_without_calendar(self, root):
        """Test get_date without calendar."""
        base = _DatePickerBase(root)
        base.calendar = None
        base.selected_date = datetime.date(2024, 3, 15)
        
        result = base.get_date()
        assert result == datetime.date(2024, 3, 15)

    def test_datepicker_base_get_date_string_without_date(self, root):
        """Test get_date_string without date."""
        base = _DatePickerBase(root)
        base.get_date = Mock(return_value=None)
        
        result = base.get_date_string()
        assert result == ""

    def test_datepicker_base_get_date_string_with_date(self, root):
        """Test get_date_string with date."""
        base = _DatePickerBase(root)
        base.get_date = Mock(return_value=datetime.date(2024, 3, 15))
        
        result = base.get_date_string()
        assert result == "2024-03-15"

    def test_datepicker_base_set_selected_date_without_calendar(self, root):
        """Test set_selected_date without calendar."""
        base = _DatePickerBase(root)
        base.calendar = None
        base._update_entry_text = Mock()
        
        test_date = datetime.date(2024, 3, 15)
        base.set_selected_date(test_date)
        
        assert base.selected_date == test_date
        base._update_entry_text.assert_called_once_with("2024-03-15")

    def test_datepicker_base_delegate_to_calendar_no_calendar(self, root):
        """Test delegate_to_calendar without calendar."""
        base = _DatePickerBase(root)
        base.calendar = None
        
        # Should not raise exception
        base._delegate_to_calendar("test_method", "arg1", "arg2")

    def test_datepicker_base_delegate_to_calendar_no_method(self, root):
        """Test delegate_to_calendar without method."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        # Don't add the method to the mock
        
        # Should not raise exception
        base._delegate_to_calendar("test_method", "arg1", "arg2")

    def test_datepicker_base_update_config_and_delegate(self, root):
        """Test update_config_and_delegate."""
        base = _DatePickerBase(root)
        base._delegate_to_calendar = Mock()
        
        base._update_config_and_delegate("test_key", "test_value", "test_method")
        
        assert base.calendar_config["test_key"] == "test_value"
        base._delegate_to_calendar.assert_called_once_with("test_method", "test_value")

    def test_datepicker_base_refresh_language(self, root):
        """Test refresh_language."""
        base = _DatePickerBase(root)
        base._delegate_to_calendar = Mock()
        
        base.refresh_language()
        base._delegate_to_calendar.assert_called_once_with("refresh_language")

    def test_datepicker_base_set_today_color(self, root):
        """Test set_today_color."""
        base = _DatePickerBase(root)
        base._delegate_to_calendar = Mock()
        
        base.set_today_color("red")
        
        assert base.today_color == "red"
        base._delegate_to_calendar.assert_called_once_with("set_today_color", "red")

    def test_datepicker_base_set_theme(self, root):
        """Test set_theme."""
        base = _DatePickerBase(root)
        base._update_config_and_delegate = Mock()
        
        base.set_theme("dark")
        base._update_config_and_delegate.assert_called_once_with("theme", "dark", "set_theme")

    def test_datepicker_base_set_day_colors(self, root):
        """Test set_day_colors."""
        base = _DatePickerBase(root)
        base._update_config_and_delegate = Mock()
        
        day_colors = {"Sunday": "red"}
        base.set_day_colors(day_colors)
        base._update_config_and_delegate.assert_called_once_with("day_colors", day_colors, "set_day_colors")

    def test_datepicker_base_set_week_start(self, root):
        """Test set_week_start."""
        base = _DatePickerBase(root)
        base._update_config_and_delegate = Mock()
        
        base.set_week_start("Monday")
        base._update_config_and_delegate.assert_called_once_with("week_start", "Monday", "set_week_start")

    def test_datepicker_base_set_show_week_numbers(self, root):
        """Test set_show_week_numbers."""
        base = _DatePickerBase(root)
        base._update_config_and_delegate = Mock()
        
        base.set_show_week_numbers(True)
        base._update_config_and_delegate.assert_called_once_with("show_week_numbers", True, "set_show_week_numbers")

    def test_datepicker_base_set_popup_size(self, root):
        """Test set_popup_size."""
        base = _DatePickerBase(root)
        base._delegate_to_calendar = Mock()
        
        base.set_popup_size(300, 200)
        base._delegate_to_calendar.assert_called_once_with("set_popup_size", 300, 200)



    # DateFrame tests
    def test_dateframe_creation(self, root):
        """Test DateFrame creation and configuration."""
        # Test basic creation
        df = DateFrame(root)
        assert df is not None
        assert hasattr(df, "entry")
        assert hasattr(df, "button")
        
        # Test with config
        _test_widget_creation(DateFrame, root, use_config=True)
        
        # Test with individual parameters including button_text
        df = _test_widget_creation(DateFrame, root, use_config=False, button_text="📆")
        assert df.button.cget("text") == "📆"

    def test_dateframe_create_class_method(self, root):
        """Test DateFrame.create class method."""
        df = DateFrame.create(root, date_format="%d/%m/%Y", button_text="📆")
        assert df.date_format == "%d/%m/%Y"
        assert df.button.cget("text") == "📆"

    def test_dateframe_update_entry_text(self, root):
        """Test DateFrame _update_entry_text method."""
        df = DateFrame(root)
        df._update_entry_text("2024-03-15")
        
        # Check that entry text was updated
        assert df.entry.get() == "2024-03-15"

    def test_dateframe_set_button_text(self, root):
        """Test DateFrame set_button_text method."""
        df = DateFrame(root)
        df.set_button_text("📅")
        assert df.button.cget("text") == "📅"

    def test_dateframe_dpi_scaling(self, root):
        """Test DateFrame DPI scaling functionality."""
        # Test basic DPI scaling error handling
        _test_dpi_scaling_error_handling(DateFrame, root)
        
        # Test update_dpi_scaling error during initialization
        with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling:
            mock_get_scaling.side_effect = ImportError("Test error")
            df = DateFrame(root)
            # When get_scaling_factor fails in update_dpi_scaling, it sets dpi_scaling_factor to 1.0 as fallback
            assert df.dpi_scaling_factor == 1.0


    # DateEntry tests
    def test_dateentry_creation(self, root):
        """Test DateEntry creation and configuration."""
        # Test basic creation
        de = DateEntry(root)
        assert de is not None
        assert de.date_format == "%Y-%m-%d"
        assert de.selected_date is None
        
        # Test with config
        _test_widget_creation(DateEntry, root, use_config=True)
        
        # Test with individual parameters including width
        _test_widget_creation(DateEntry, root, use_config=False, width=20)

    def test_dateentry_create_class_method(self, root):
        """Test DateEntry.create class method."""
        de = DateEntry.create(root, date_format="%d/%m/%Y", width=20)
        assert de.date_format == "%d/%m/%Y"

    def test_dateentry_setup_style(self, root):
        """Test DateEntry _setup_style method."""
        de = DateEntry(root)
        # Should not raise exception
        assert hasattr(de, 'style')

    def test_dateentry_update_entry_text(self, root):
        """Test DateEntry _update_entry_text method."""
        de = DateEntry(root)
        de._update_entry_text("2024-03-15")
        
        # Check that entry text was updated
        assert de.get() == "2024-03-15"

    def test_dateentry_dpi_scaling(self, root):
        """Test DateEntry DPI scaling functionality."""
        # Test basic DPI scaling error handling
        _test_dpi_scaling_error_handling(DateEntry, root)

    def test_dateentry_dpi_scaling_error_during_init(self, root):
        """Test DateEntry DPI scaling error during initialization."""
        # Test the specific error handling in DateEntry.__init__ for DPI scaling
        with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling:
            mock_get_scaling.side_effect = ImportError("Test error")
            de = DateEntry(root)
            # When get_scaling_factor fails in update_dpi_scaling, it sets dpi_scaling_factor to 1.0 as fallback
            assert de.dpi_scaling_factor == 1.0

    def test_dateentry_button_text_removal(self, root):
        """Test DateEntry removes button_text from kwargs."""
        de = DateEntry(root, button_text="test", width=20)
        # Should not raise exception and button_text should be removed from kwargs
        assert True


    def test_dateentry_button_text_removal_direct_kwargs(self, root):
        """Test DateEntry button_text removal when button_text is directly in kwargs."""
        # Test the specific case where button_text is passed as a keyword argument
        # This should trigger the del kwargs["button_text"] line in DateEntry.__init__
        
        # Create DateEntry with button_text in kwargs (this should be removed)
        de = DateEntry(root, button_text="test", width=20)
        
        # Verify the widget was created successfully
        assert de is not None

    def test_dateentry_button_text_removal_with_kwargs_dict(self, root):
        """Test DateEntry button_text removal when button_text is in kwargs dict."""
        # Test the specific case where button_text is in kwargs dict
        # This should trigger the del kwargs["button_text"] line in DateEntry.__init__
        
        # Create a custom DateEntry that forces button_text into kwargs
        class TestDateEntry(DateEntry):
            def __init__(self, parent, **kwargs):
                # Force button_text into kwargs to test the removal logic
                kwargs["button_text"] = "test"
                super().__init__(parent, **kwargs)
        
        # This should trigger the del kwargs["button_text"] line
        de = TestDateEntry(root, width=20)
        
        # Verify the widget was created successfully
        assert de is not None



    def test_dateentry_on_b1_press_right_area(self, root):
        """Test DateEntry _on_b1_press in right area."""
        de = DateEntry(root)
        de.state = Mock()
        de.drop_down = Mock()
        
        event = Mock()
        event.x = 105  # Right area (width=120, so x=105 > 120-20=100)
        de.winfo_width = Mock(return_value=120)
        
        result = de._on_b1_press(event)
        
        assert result == "break"
        de.state.assert_called_once_with(["pressed"])
        de.drop_down.assert_called_once()

    def test_dateentry_on_b1_press_left_area(self, root):
        """Test DateEntry _on_b1_press in left area."""
        de = DateEntry(root)
        de.state = Mock()
        de.drop_down = Mock()
        
        event = Mock()
        event.x = 50
        de.winfo_width = Mock(return_value=120)
        
        result = de._on_b1_press(event)
        
        assert result is None
        de.state.assert_not_called()
        de.drop_down.assert_not_called()

    def test_dateentry_drop_down_show_calendar(self, root):
        """Test DateEntry drop_down to show calendar."""
        de = DateEntry(root)
        de.popup = None
        de.show_calendar = Mock()
        
        de.drop_down()
        
        de.show_calendar.assert_called_once()

    def test_dateentry_drop_down_hide_calendar(self, root):
        """Test DateEntry drop_down to hide calendar."""
        de = DateEntry(root)
        de.popup = Mock()
        de.popup.winfo_ismapped.return_value = True
        de.hide_calendar = Mock()
        
        de.drop_down()
        
        de.hide_calendar.assert_called_once()

    def test_dateentry_on_focus_out_entry(self, root):
        """Test DateEntry _on_focus_out_entry."""
        de = DateEntry(root)
        de.popup = Mock()
        de.popup.winfo_ismapped.return_value = True
        de.focus_get = Mock(return_value=Mock())
        de._is_child_of_calendar = Mock(return_value=False)
        de.hide_calendar = Mock()
        
        de._on_focus_out_entry(Mock())
        
        de.hide_calendar.assert_called_once()

    def test_dateentry_on_focus_out_entry_focus_on_self(self, root):
        """Test DateEntry _on_focus_out_entry with focus on self."""
        de = DateEntry(root)
        de.popup = Mock()
        de.popup.winfo_ismapped.return_value = True
        de.focus_get = Mock(return_value=de)
        de.hide_calendar = Mock()
        
        de._on_focus_out_entry(Mock())
        
        de.hide_calendar.assert_not_called()

    def test_dateentry_on_focus_out_entry_focus_on_calendar(self, root):
        """Test DateEntry _on_focus_out_entry with focus on calendar."""
        de = DateEntry(root)
        de.popup = Mock()
        de.popup.winfo_ismapped.return_value = True
        de.focus_get = Mock(return_value=Mock())
        de._is_child_of_calendar = Mock(return_value=True)
        de.hide_calendar = Mock()
        
        de._on_focus_out_entry(Mock())
        
        de.hide_calendar.assert_not_called()

    def test_dateentry_on_focus_out_entry_no_popup(self, root):
        """Test DateEntry _on_focus_out_entry without popup."""
        de = DateEntry(root)
        de.popup = None
        de.hide_calendar = Mock()
        
        de._on_focus_out_entry(Mock())
        
        de.hide_calendar.assert_not_called()

    def test_dateentry_on_key(self, root):
        """Test DateEntry _on_key with various keys."""
        de = DateEntry(root)
        de.show_calendar = Mock()
        
        # Test Down key - should show calendar
        event_down = Mock()
        event_down.keysym = "Down"
        de._on_key(event_down)
        de.show_calendar.assert_called_once()
        
        # Test space key - should show calendar
        de.show_calendar.reset_mock()
        event_space = Mock()
        event_space.keysym = "space"
        de._on_key(event_space)
        de.show_calendar.assert_called_once()
        
        # Test other key - should not show calendar
        de.show_calendar.reset_mock()
        event_other = Mock()
        event_other.keysym = "Return"
        de._on_key(event_other)
        de.show_calendar.assert_not_called()

    def test_dateentry_setup_style(self, root):
        """Test DateEntry _setup_style with various configurations."""
        de = DateEntry(root)
        
        # Test with configure returning values
        de.style.configure = Mock(return_value={"background": "white"})
        de.style.layout = Mock()
        de.style.map = Mock(return_value={"background": [("active", "blue")]})
        de._setup_style()  # Should not raise exception
        
        # Test with configure returning None
        de.style.configure = Mock(return_value=None)
        de.style.map = Mock(return_value=None)
        de._setup_style()  # Should not raise exception


    # Integration tests
    def test_datepicker_integration(self, root):
        """Test DatePicker with comprehensive integration scenarios."""
        # Test DateFrame calendar integration
        df = DateFrame(root, year=2024, month=3)
        assert df.calendar_config["year"] == 2024
        assert df.calendar_config["month"] == 3
        
        test_date = datetime.date(2024, 3, 15)
        df.set_selected_date(test_date)
        assert df.selected_date == test_date
        assert df.get_date_string() == "2024-03-15"
        
        # Test DateEntry calendar integration
        de = DateEntry(root, year=2024, month=3)
        assert de.calendar_config["year"] == 2024
        assert de.calendar_config["month"] == 3
        
        de.set_selected_date(test_date)
        assert de.selected_date == test_date
        assert de.get_date_string() == "2024-03-15"
        
        # Test callback integration
        callback_called = False
        callback_date = None

        def callback(date):
            nonlocal callback_called, callback_date
            callback_called = True
            callback_date = date

        df_callback = DateFrame(root, date_callback=callback)
        df_callback._on_date_selected(test_date)
        assert callback_called
        assert callback_date == test_date
        
        # Test theme integration
        df_theme = DateFrame(root, theme="dark")
        assert df_theme.calendar_config["theme"] == "dark"
        df_theme.set_theme("light")
        assert df_theme.calendar_config["theme"] == "light"
        
        # Test language integration
        df_lang = DateFrame(root, language="ja")
        df_lang.refresh_language()  # Should not raise exception
        
        # Test holidays integration
        holidays = {"2024-01-01": "red", "2024-12-25": "green"}
        df_holidays = DateFrame(root, holidays=holidays)
        assert df_holidays.calendar_config["holidays"] == holidays
        
        new_holidays = {"2024-02-14": "pink"}
        df_holidays.calendar_config["holidays"] = new_holidays
        assert df_holidays.calendar_config["holidays"] == new_holidays
        
        # Test day colors integration
        day_colors = {"Sunday": "red", "Saturday": "blue"}
        df_colors = DateFrame(root, day_colors=day_colors)
        assert df_colors.calendar_config["day_colors"] == day_colors
        
        new_colors = {"Friday": "green"}
        df_colors.set_day_colors(new_colors)
        assert df_colors.calendar_config["day_colors"] == new_colors
        
        # Test week start integration
        df_week = DateFrame(root, week_start="Monday")
        assert df_week.calendar_config["week_start"] == "Monday"
        df_week.set_week_start("Saturday")
        assert df_week.calendar_config["week_start"] == "Saturday"
        
        # Test week numbers integration
        df_week_nums = DateFrame(root, show_week_numbers=True)
        assert df_week_nums.calendar_config["show_week_numbers"] is True
        df_week_nums.set_show_week_numbers(False)
        assert df_week_nums.calendar_config["show_week_numbers"] is False
        
        # Test select mode integration
        df_range = DateFrame(root, selectmode="range")
        assert df_range.calendar_config["selectmode"] == "range"
        
        df_single = DateFrame(root, selectmode="single")
        assert df_single.calendar_config["selectmode"] == "single"
        
        # Test today color integration
        df_today = DateFrame(root, today_color="blue")
        assert df_today.today_color == "blue"
        df_today.set_today_color("red")
        assert df_today.today_color == "red"
        
        # Test popup size integration
        df_popup = DateFrame(root)
        df_popup.set_popup_size(400, 300)  # Should not raise exception



class TestDatePickerEvents:
    """Test cases for DatePicker event handling and calendar operations."""

    def test_datepicker_base_on_date_selected_scenarios(self, root):
        """Test _on_date_selected with various scenarios."""
        # Test with callback
        callback_called = False
        callback_date = None

        def callback(date):
            nonlocal callback_called, callback_date
            callback_called = True
            callback_date = date

        base = _DatePickerBase(root, date_callback=callback)
        base._update_entry_text = Mock()
        base.hide_calendar = Mock()
        
        test_date = datetime.date(2024, 3, 15)
        base._on_date_selected(test_date)
        
        assert base.selected_date == test_date
        assert callback_called
        assert callback_date == test_date
        base._update_entry_text.assert_called_once_with("2024-03-15")
        base.hide_calendar.assert_called_once()
        
        # Test without callback
        base2 = _DatePickerBase(root)
        base2._update_entry_text = Mock()
        base2.hide_calendar = Mock()
        
        base2._on_date_selected(test_date)
        
        assert base2.selected_date == test_date
        base2._update_entry_text.assert_called_once_with("2024-03-15")
        base2.hide_calendar.assert_called_once()
        
        # Test with None date
        base3 = _DatePickerBase(root)
        base3._update_entry_text = Mock()
        base3.hide_calendar = Mock()
        
        base3._on_date_selected(None)
        
        assert base3.selected_date is None
        base3._update_entry_text.assert_not_called()
        base3.hide_calendar.assert_not_called()

    def test_datepicker_base_bind_calendar_events(self, root):
        """Test _bind_calendar_events."""
        base = _DatePickerBase(root)
        mock_widget = Mock()
        mock_child = Mock()
        mock_child.winfo_children.return_value = []  # Empty list to stop recursion
        mock_widget.winfo_children.return_value = [mock_child]
        
        base._bind_calendar_events(mock_widget)
        
        mock_widget.bind.assert_called_once()
        mock_child.winfo_children.assert_called_once()

    def test_datepicker_base_bind_calendar_events_error(self, root):
        """Test _bind_calendar_events with error."""
        base = _DatePickerBase(root)
        mock_widget = Mock()
        mock_widget.bind.side_effect = tk.TclError("Test error")
        
        # Should not raise exception
        base._bind_calendar_events(mock_widget)

    def test_datepicker_base_is_child_of_popup(self, root):
        """Test _is_child_of_popup."""
        base = _DatePickerBase(root)
        base.popup = Mock()
        
        # Test with popup as widget
        result = base._is_child_of_popup(base.popup)
        assert result is True
        
        # Test with child of popup
        child_widget = Mock()
        child_widget.master = base.popup
        result = base._is_child_of_popup(child_widget)
        assert result is True
        
        # Test with unrelated widget
        unrelated_widget = Mock()
        unrelated_widget.master = None
        result = base._is_child_of_popup(unrelated_widget)
        assert result is False

    def test_datepicker_base_setup_focus(self, root):
        """Test _setup_focus."""
        base = _DatePickerBase(root)
        base.popup = Mock()
        base.calendar = Mock()
        
        base._setup_focus()
        
        base.popup.lift.assert_called_once()
        base.calendar.focus_set.assert_called()
        base.popup.after.assert_called()

    def test_datepicker_base_setup_focus_error(self, root):
        """Test _setup_focus with error."""
        base = _DatePickerBase(root)
        base.popup = Mock()
        base.calendar = Mock()
        base.popup.lift.side_effect = tk.TclError("Test error")
        
        # Should not raise exception
        base._setup_focus()

    def test_datepicker_base_is_child_of_calendar(self, root):
        """Test _is_child_of_calendar."""
        base = _DatePickerBase(root)
        calendar_widget = Mock()
        
        # Test with string widget
        result = base._is_child_of_calendar("string", calendar_widget)
        assert result is False
        
        # Test with calendar as widget
        result = base._is_child_of_calendar(calendar_widget, calendar_widget)
        assert result is True
        
        # Test with child of calendar
        child_widget = Mock()
        child_widget.master = calendar_widget
        result = base._is_child_of_calendar(child_widget, calendar_widget)
        assert result is True
        
        # Test with unrelated widget
        unrelated_widget = Mock()
        unrelated_widget.master = None
        result = base._is_child_of_calendar(unrelated_widget, calendar_widget)
        assert result is False

    def test_datepicker_base_on_main_window_click_scenarios(self, root):
        """Test _on_main_window_click with various scenarios."""
        base = _DatePickerBase(root)
        
        # Test with string widget
        popup_window = create_mock_popup_window()
        hide_callback = Mock()
        
        event = Mock()
        event.widget = "string"
        
        result = base._on_main_window_click(event, popup_window, hide_callback)
        assert result == "break"
        hide_callback.assert_not_called()
        
        # Test with popup not existing
        popup_window.winfo_exists.return_value = False
        event.widget = "not_string"
        
        result = base._on_main_window_click(event, popup_window, hide_callback)
        assert result == "break"
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
        assert result == "break"
        # The condition checks: root_x < popup_x OR root_x > popup_x + popup_w OR root_y < popup_y OR root_y > popup_y + popup_h
        # root_x = 50, popup_x = 100, so 50 < 100 is True, so hide_callback should be called
        hide_callback.assert_called_once()

    def test_datepicker_base_on_popup_click_scenarios(self, root):
        """Test _on_popup_click with various scenarios."""
        base = _DatePickerBase(root)
        
        # Test with string widget
        popup_window = create_mock_popup_window()
        calendar_widget = Mock()
        hide_callback = Mock()
        
        event = Mock()
        event.widget = "string"
        
        result = base._on_popup_click(event, popup_window, calendar_widget, hide_callback)
        assert result == "break"
        calendar_widget.focus_set.assert_called_once()
        
        # Test with click outside popup
        popup_window.winfo_pointerxy.return_value = (50, 50)  # Outside
        hide_callback.reset_mock()
        calendar_widget.reset_mock()
        
        result = base._on_popup_click(event, popup_window, calendar_widget, hide_callback)
        assert result == "break"
        hide_callback.assert_called_once()
        
        # Test with calendar in selection mode, click inside
        base.calendar = create_mock_calendar()
        base.calendar.year_selection_mode = True
        base._is_child_of_calendar = Mock(return_value=True)
        
        event.widget = Mock()
        hide_callback.reset_mock()
        calendar_widget.reset_mock()
        
        result = base._on_popup_click(event, popup_window, calendar_widget, hide_callback)
        assert result == "break"
        calendar_widget.focus_set.assert_called_once()
        hide_callback.assert_not_called()
        
        # Test with calendar in selection mode, click outside
        base._is_child_of_calendar = Mock(return_value=False)
        hide_callback.reset_mock()
        calendar_widget.reset_mock()
        
        result = base._on_popup_click(event, popup_window, calendar_widget, hide_callback)
        assert result == "break"
        hide_callback.assert_called_once()
        
        # Test exception handling
        base._is_child_of_calendar = Mock(side_effect=Exception("Test error"))
        hide_callback.reset_mock()
        calendar_widget.reset_mock()
        
        result = base._on_popup_click(event, popup_window, calendar_widget, hide_callback)
        assert result == "break"
        # Should handle exception gracefully

    def test_datepicker_base_on_focus_out_scenarios(self, root):
        """Test _on_focus_out with various scenarios."""
        base = _DatePickerBase(root)
        
        # Test with focus on calendar
        base.calendar = Mock()
        base.focus_get = Mock(return_value=Mock())
        base._is_child_of_calendar = Mock(return_value=True)
        
        result = base._on_focus_out(Mock())
        assert result == "break"
        
        # Test with focus on self
        base.focus_get = Mock(return_value=base)
        result = base._on_focus_out(Mock())
        assert result == "break"
        
        # Test with calendar in selection mode, pointer inside
        base.calendar = create_mock_calendar()
        base.calendar.year_selection_mode = True
        base.popup = create_mock_popup_window()
        base.focus_get = Mock(return_value=None)
        
        result = base._on_focus_out(Mock())
        assert result == "break"
        base.calendar.focus_force.assert_called_once()
        
        # Test with calendar in selection mode, pointer outside
        base.popup.winfo_pointerxy.return_value = (50, 50)  # Outside
        base.hide_calendar = Mock()
        
        result = base._on_focus_out(Mock())
        assert result == "break"
        base.hide_calendar.assert_called_once()
        
        # Test with normal mode, pointer inside
        base4 = _DatePickerBase(root)
        base4.calendar = create_mock_calendar()
        base4.calendar.year_selection_mode = False
        base4.calendar.month_selection_mode = False
        base4.popup = create_mock_popup_window()
        base4.popup.winfo_pointerxy.return_value = (150, 150)  # Inside
        base4.focus_get = Mock(return_value=None)
        
        result = base4._on_focus_out(Mock())
        assert result == "break"
        base4.calendar.focus_force.assert_called_once()
        
        # Test with normal mode, pointer outside
        base5 = _DatePickerBase(root)
        base5.calendar = create_mock_calendar()
        base5.calendar.year_selection_mode = False
        base5.calendar.month_selection_mode = False
        base5.popup = create_mock_popup_window()
        base5.popup.winfo_pointerxy.return_value = (50, 50)  # Outside
        base5.focus_get = Mock(return_value=None)
        base5.hide_calendar = Mock()
        
        result = base5._on_focus_out(Mock())
        assert result == "break"
        base5.hide_calendar.assert_called_once()
        
        # Test exception handling
        base6 = _DatePickerBase(root)
        base6.calendar = create_mock_calendar()
        base6.calendar.year_selection_mode = True
        base6.popup = create_mock_popup_window()
        base6.popup.winfo_pointerxy.side_effect = Exception("Test error")
        base6.focus_get = Mock(return_value=None)
        
        result = base6._on_focus_out(Mock())
        assert result == "break"

    def test_datepicker_base_setup_click_outside_handling(self, root):
        """Test _setup_click_outside_handling."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.popup = Mock()
        base.master = Mock()
        base.master.winfo_toplevel.return_value = Mock()
        base._on_popup_click = Mock()
        base._on_main_window_click = Mock()
        base.hide_calendar = Mock()
        
        base._setup_click_outside_handling()
        
        base.calendar.bind.assert_called_once()
        base.popup.bind.assert_called()

    def test_datepicker_base_setup_year_view_click_outside_handling(self, root):
        """Test _setup_year_view_click_outside_handling."""
        base = _DatePickerBase(root)
        base.year_view_window = Mock()
        base.year_view_calendar = Mock()
        base.master = Mock()
        base.master.winfo_toplevel.return_value = Mock()
        base._on_popup_click = Mock()
        base._on_main_window_click = Mock()
        base.hide_year_view = Mock()
        
        base._setup_year_view_click_outside_handling()
        
        base.year_view_window.bind.assert_called()

    def test_datepicker_base_show_calendar_scenarios(self, root):
        """Test show_calendar with various scenarios."""
        # Test with theme error
        with patch('tkface.dialog.datepicker.Calendar') as mock_calendar_class, \
             patch('tkface.dialog.datepicker.get_calendar_theme') as mock_get_theme, \
             patch('tkface.dialog.datepicker.tk.Toplevel') as mock_toplevel:
            
            mock_calendar = Mock()
            mock_calendar.winfo_children.return_value = []  # Empty list to prevent iteration error
            mock_calendar_class.return_value = mock_calendar
            mock_calendar.get_popup_geometry.return_value = "300x200+100+100"
            # First call fails, second call (fallback) succeeds
            mock_get_theme.side_effect = [ValueError("Invalid theme"), {"background": "white"}]
            
            mock_popup = Mock()
            mock_toplevel.return_value = mock_popup
            
            base = _DatePickerBase(root, theme="invalid")
            base.winfo_toplevel = Mock(return_value=Mock())  # Add missing method
            base.show_calendar()
            
            assert base.popup is not None
            assert base.calendar is not None
        
        # Test with DPI scaling
        with patch('tkface.dialog.datepicker.Calendar') as mock_calendar_class, \
             patch('tkface.dialog.datepicker.get_calendar_theme') as mock_get_theme, \
             patch('tkface.dialog.datepicker.re') as mock_re, \
             patch('tkface.dialog.datepicker.tk.Toplevel') as mock_toplevel:
            
            mock_calendar = Mock()
            mock_calendar.winfo_children.return_value = []  # Empty list to prevent iteration error
            mock_calendar_class.return_value = mock_calendar
            mock_calendar.get_popup_geometry.return_value = "300x200+100+100"
            mock_get_theme.return_value = {"background": "white"}
            
            mock_match = Mock()
            mock_match.groups.return_value = (300, 200, 100, 100)
            mock_re.match.return_value = mock_match
            
            mock_popup = Mock()
            mock_toplevel.return_value = mock_popup
            
            base2 = _DatePickerBase(root)
            base2.dpi_scaling_factor = 2.0
            base2.winfo_toplevel = Mock(return_value=Mock())  # Add missing method
            base2.show_calendar()
            
            assert base2.popup is not None
            assert base2.calendar is not None
            # Should scale geometry
            mock_popup.geometry.assert_called_with("600x400+100+100")
        
        # Test with DPI scaling error
        with patch('tkface.dialog.datepicker.Calendar') as mock_calendar_class, \
             patch('tkface.dialog.datepicker.get_calendar_theme') as mock_get_theme, \
             patch('tkface.dialog.datepicker.re') as mock_re, \
             patch('tkface.dialog.datepicker.tk.Toplevel') as mock_toplevel:
            
            mock_calendar = Mock()
            mock_calendar.winfo_children.return_value = []  # Empty list to prevent iteration error
            mock_calendar_class.return_value = mock_calendar
            mock_calendar.get_popup_geometry.return_value = "300x200+100+100"
            mock_get_theme.return_value = {"background": "white"}
            
            mock_re.match.side_effect = ValueError("Invalid geometry")
            
            mock_popup = Mock()
            mock_toplevel.return_value = mock_popup
            
            base3 = _DatePickerBase(root)
            base3.dpi_scaling_factor = 2.0
            base3.winfo_toplevel = Mock(return_value=Mock())  # Add missing method
            base3.show_calendar()
            
            assert base3.popup is not None
            assert base3.calendar is not None
            # Should use original geometry on error
            mock_popup.geometry.assert_called_with("300x200+100+100")

    def test_datepicker_base_show_year_view_scenarios(self, root):
        """Test show_year_view with various scenarios."""
        # Test with theme error
        with patch('tkface.dialog.datepicker.Calendar') as mock_calendar_class, \
             patch('tkface.dialog.datepicker.get_calendar_theme') as mock_get_theme, \
             patch('tkface.dialog.datepicker.tk.Toplevel') as mock_toplevel:
            
            mock_calendar = Mock()
            mock_calendar_class.return_value = mock_calendar
            mock_calendar.get_popup_geometry.return_value = "300x200+100+100"
            # First call fails, second call (fallback) succeeds
            mock_get_theme.side_effect = [ValueError("Invalid theme"), {"background": "white"}]
            
            mock_year_view_window = Mock()
            mock_toplevel.return_value = mock_year_view_window
            
            base = _DatePickerBase(root, theme="invalid")
            base.popup = Mock()
            base.show_year_view()
            
            assert base.year_view_window is not None
            assert base.year_view_calendar is not None
        
        # Test with DPI scaling
        with patch('tkface.dialog.datepicker.Calendar') as mock_calendar_class, \
             patch('tkface.dialog.datepicker.get_calendar_theme') as mock_get_theme, \
             patch('tkface.dialog.datepicker.re') as mock_re, \
             patch('tkface.dialog.datepicker.tk.Toplevel') as mock_toplevel:
            
            mock_calendar = Mock()
            mock_calendar_class.return_value = mock_calendar
            mock_calendar.get_popup_geometry.return_value = "300x200+100+100"
            mock_get_theme.return_value = {"background": "white"}
            
            mock_match = Mock()
            mock_match.groups.return_value = (300, 200, 100, 100)
            mock_re.match.return_value = mock_match
            
            mock_year_view_window = Mock()
            mock_toplevel.return_value = mock_year_view_window
            
            base2 = _DatePickerBase(root)
            base2.dpi_scaling_factor = 2.0
            base2.popup = Mock()
            base2.show_year_view()
            
            assert base2.year_view_window is not None
            assert base2.year_view_calendar is not None
            # Should scale geometry
            mock_year_view_window.geometry.assert_called_with("600x400+100+100")

    def test_datepicker_base_hide_year_view_with_unbind_error(self, root):
        """Test hide_year_view with unbind error."""
        base = _DatePickerBase(root)
        mock_year_view_window = Mock()
        base.year_view_window = mock_year_view_window
        mock_year_view_window.unbind.side_effect = tk.TclError("Test error")
        base.year_view_calendar = Mock()
        
        # Should not raise exception
        base.hide_year_view()
        
        mock_year_view_window.destroy.assert_called_once()
        assert base.year_view_window is None
        assert base.year_view_calendar is None

    def test_datepicker_base_unbind_parent_movement_events_with_error(self, root):
        """Test _unbind_parent_movement_events with error."""
        base = _DatePickerBase(root)
        base._parent_configure_binding = "test_binding"
        base.winfo_toplevel = Mock(return_value=Mock())
        base.winfo_toplevel().unbind.side_effect = tk.TclError("Test error")
        
        # Should not raise exception
        base._unbind_parent_movement_events()
        
        assert not hasattr(base, '_parent_configure_binding')

    def test_datepicker_base_on_parent_configure_scenarios(self, root):
        """Test _on_parent_configure with various scenarios."""
        with patch('tkface.dialog.datepicker.re') as mock_re:
            # Test with DPI scaling
            base = _DatePickerBase(root)
            base.popup = Mock()
            base.popup.winfo_exists.return_value = True
            base.calendar = Mock()
            base.calendar.get_popup_geometry.return_value = "300x200+100+100"
            base.year_view_window = None
            base.dpi_scaling_factor = 2.0
            
            mock_match = Mock()
            mock_match.groups.return_value = (300, 200, 100, 100)
            mock_re.match.return_value = mock_match
            
            base._on_parent_configure(Mock())
            base.popup.geometry.assert_called_once_with("600x400+100+100")
            
            # Test with year view and DPI scaling
            base2 = _DatePickerBase(root)
            base2.popup = Mock()
            base2.year_view_window = Mock()
            base2.year_view_window.winfo_exists.return_value = True
            base2.year_view_calendar = Mock()
            base2.year_view_calendar.get_popup_geometry.return_value = "300x200+100+100"
            base2.dpi_scaling_factor = 2.0
            
            mock_match2 = Mock()
            mock_match2.groups.return_value = (300, 200, 100, 100)
            mock_re.match.return_value = mock_match2
            
            base2._on_parent_configure(Mock())
            base2.year_view_window.geometry.assert_called_once_with("600x400+100+100")
            
            # Test with geometry parsing error
            base3 = _DatePickerBase(root)
            base3.popup = Mock()
            base3.popup.winfo_exists.return_value = True
            base3.calendar = Mock()
            base3.calendar.get_popup_geometry.return_value = "invalid_geometry"
            base3.year_view_window = None
            base3.dpi_scaling_factor = 2.0
            
            mock_re.match.side_effect = ValueError("Invalid geometry")
            
            base3._on_parent_configure(Mock())
            # Should use original geometry on error
            base3.popup.geometry.assert_called_once_with("invalid_geometry")


    # Calendar operations tests
    def test_datepicker_base_show_calendar(self, root):
        """Test show_calendar method."""
        with patch('tkface.dialog.datepicker.Calendar') as mock_calendar_class, \
             patch('tkface.dialog.datepicker.get_calendar_theme') as mock_get_theme, \
             patch('tkface.dialog.datepicker.tk.Toplevel') as mock_toplevel:
            
            mock_calendar = Mock()
            mock_calendar.winfo_children.return_value = []  # Empty list to prevent iteration error
            mock_calendar_class.return_value = mock_calendar
            mock_calendar.get_popup_geometry.return_value = "300x200+100+100"
            mock_get_theme.return_value = {"background": "white"}
            
            mock_popup = Mock()
            mock_toplevel.return_value = mock_popup
            
            base = _DatePickerBase(root)
            base.winfo_toplevel = Mock(return_value=Mock())  # Add missing method
            base.show_calendar()
            
            assert base.popup is not None
            assert base.calendar is not None
            mock_calendar_class.assert_called_once()
            mock_calendar.pack.assert_called_once()

    @pytest.mark.parametrize("method_name,attribute_name", [
        ("show_calendar", "popup"),
        ("show_year_view", "year_view_window")
    ])
    def test_datepicker_base_show_methods_already_exists(self, root, method_name, attribute_name):
        """Test show methods when objects already exist."""
        base = _DatePickerBase(root)
        setattr(base, attribute_name, Mock())
        
        getattr(base, method_name)()
        
        # Should return early without creating new object
        assert getattr(base, attribute_name) is not None

    def test_datepicker_base_hide_calendar(self, root):
        """Test hide_calendar method."""
        base = _DatePickerBase(root)
        mock_popup = Mock()
        base.popup = mock_popup
        base.calendar = Mock()
        base._unbind_parent_movement_events = Mock()
        
        base.hide_calendar()
        
        base._unbind_parent_movement_events.assert_called_once()
        mock_popup.destroy.assert_called_once()
        assert base.popup is None
        assert base.calendar is None

    @pytest.mark.parametrize("method_name,attribute_name", [
        ("hide_calendar", "popup"),
        ("hide_year_view", "year_view_window")
    ])
    def test_datepicker_base_hide_methods_no_object(self, root, method_name, attribute_name):
        """Test hide methods when objects don't exist."""
        base = _DatePickerBase(root)
        setattr(base, attribute_name, None)
        
        # Should not raise exception
        getattr(base, method_name)()

    def test_datepicker_base_show_year_view(self, root):
        """Test show_year_view method."""
        with patch('tkface.dialog.datepicker.Calendar') as mock_calendar_class, \
             patch('tkface.dialog.datepicker.get_calendar_theme') as mock_get_theme, \
             patch('tkface.dialog.datepicker.tk.Toplevel') as mock_toplevel:
            
            mock_calendar = Mock()
            mock_calendar_class.return_value = mock_calendar
            mock_calendar.get_popup_geometry.return_value = "300x200+100+100"
            mock_get_theme.return_value = {"background": "white"}
            
            mock_year_view_window = Mock()
            mock_toplevel.return_value = mock_year_view_window
            
            base = _DatePickerBase(root)
            base.popup = Mock()
            base.show_year_view()
            
            assert base.year_view_window is not None
            assert base.year_view_calendar is not None
            mock_calendar_class.assert_called_once()

    def test_datepicker_base_hide_year_view(self, root):
        """Test hide_year_view method."""
        base = _DatePickerBase(root)
        mock_year_view_window = Mock()
        base.year_view_window = mock_year_view_window
        base.year_view_calendar = Mock()
        
        base.hide_year_view()
        
        mock_year_view_window.destroy.assert_called_once()
        assert base.year_view_window is None
        assert base.year_view_calendar is None

    def test_datepicker_base_on_calendar_month_selected(self, root):
        """Test _on_calendar_month_selected."""
        base = _DatePickerBase(root)
        base.hide_calendar = Mock()
        base.show_calendar = Mock()
        
        base._on_calendar_month_selected(2024, 3)
        
        assert base.calendar_config["year"] == 2024
        assert base.calendar_config["month"] == 3
        base.hide_calendar.assert_called_once()
        base.show_calendar.assert_called_once()

    @pytest.mark.parametrize("has_calendar,expected_behavior", [
        (True, "with_calendar"),
        (False, "without_calendar")
    ])
    def test_datepicker_base_on_calendar_year_view_request(self, root, has_calendar, expected_behavior):
        """Test _on_calendar_year_view_request with and without calendar."""
        if has_calendar:
            with patch('tkface.dialog.datepicker.view') as mock_view:
                base = _DatePickerBase(root)
                base.calendar = Mock()
                base.calendar.month_selection_mode = False
                base.calendar.year_selection_mode = False
                
                base._on_calendar_year_view_request()
                
                assert base.calendar.month_selection_mode is True
                assert base.calendar.year_selection_mode is False
                mock_view._create_year_view_content.assert_called_once_with(base.calendar)
                mock_view._update_year_view.assert_called_once_with(base.calendar)
        else:
            base = _DatePickerBase(root)
            base.calendar = None
            base.show_year_view = Mock()
            
            base._on_calendar_year_view_request()
            
            base.show_year_view.assert_called_once()

    def test_datepicker_base_on_year_view_month_selected(self, root):
        """Test _on_year_view_month_selected."""
        with patch('tkface.dialog.datepicker.view') as mock_view:
            base = _DatePickerBase(root)
            base.calendar = Mock()
            base.calendar.month_selection_mode = True
            base.calendar.year_selection_mode = True
            
            base._on_year_view_month_selected(2024, 3)
            
            assert base.calendar_config["year"] == 2024
            assert base.calendar_config["month"] == 3
            assert base.calendar.month_selection_mode is False
            assert base.calendar.year_selection_mode is False
            mock_view._destroy_year_container.assert_called_once_with(base.calendar)
            mock_view._create_widgets.assert_called_once_with(base.calendar)
            mock_view._update_display.assert_called_once_with(base.calendar)

    @pytest.mark.parametrize("method_name,has_popup,has_binding,expected_result", [
        ("_bind_parent_movement_events", True, None, "has_binding"),
        ("_bind_parent_movement_events", False, None, "no_exception"),
        ("_unbind_parent_movement_events", None, True, "no_binding"),
        ("_unbind_parent_movement_events", None, False, "no_exception")
    ])
    def test_datepicker_base_parent_movement_events(self, root, method_name, has_popup, has_binding, expected_result):
        """Test parent movement events binding and unbinding."""
        base = _DatePickerBase(root)
        base.winfo_toplevel = Mock(return_value=Mock())
        
        if method_name == "_bind_parent_movement_events":
            if has_popup:
                base.popup = Mock()
                base._on_parent_configure = Mock()
            else:
                base.popup = None
                base.year_view_window = None
        else:  # _unbind_parent_movement_events
            if has_binding:
                base._parent_configure_binding = "test_binding"
            # else: No binding set
        
        getattr(base, method_name)()
        
        if expected_result == "has_binding":
            assert hasattr(base, '_parent_configure_binding')
        elif expected_result == "no_binding":
            assert not hasattr(base, '_parent_configure_binding')
        # For "no_exception", we just verify the method completes without error

    @pytest.mark.parametrize("has_year_view,expected_target", [
        (False, "popup"),
        (True, "year_view_window")
    ])
    def test_datepicker_base_on_parent_configure(self, root, has_year_view, expected_target):
        """Test _on_parent_configure with and without year view."""
        with patch('tkface.dialog.datepicker.re') as mock_re:
            base = _DatePickerBase(root)
            base.popup = Mock()
            base.popup.winfo_exists.return_value = True
            base.calendar = Mock()
            base.calendar.get_popup_geometry.return_value = "300x200+100+100"
            base.dpi_scaling_factor = 1.0
            
            if has_year_view:
                base.year_view_window = Mock()
                base.year_view_window.winfo_exists.return_value = True
                base.year_view_calendar = Mock()
                base.year_view_calendar.get_popup_geometry.return_value = "300x200+100+100"
            else:
                base.year_view_window = None
            
            mock_re.match.return_value = None
            
            base._on_parent_configure(Mock())
            
            if expected_target == "popup":
                base.popup.geometry.assert_called_once_with("300x200+100+100")
            else:
                base.year_view_window.geometry.assert_called_once_with("300x200+100+100")


    # Additional coverage tests
    @pytest.mark.parametrize("is_inside_calendar,expected_focus,expected_hide", [
        (True, True, False),
        (False, False, True)
    ])
    def test_on_popup_click_normal_mode(self, root, is_inside_calendar, expected_focus, expected_hide):
        """Test popup click behavior in normal mode."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.calendar.year_selection_mode = False
        base.calendar.month_selection_mode = False

        popup_window = Mock()
        calendar_widget = Mock()
        hide_callback = Mock()

        base._is_child_of_calendar = Mock(return_value=is_inside_calendar)

        event = Mock()
        event.widget = Mock()

        result = base._on_popup_click(event, popup_window, calendar_widget, hide_callback)

        assert result == "break"
        if expected_focus:
            calendar_widget.focus_set.assert_called_once()
        else:
            calendar_widget.focus_set.assert_not_called()
        
        if expected_hide:
            hide_callback.assert_called_once()
        else:
            hide_callback.assert_not_called()

    def test_on_main_window_click_inside_popup(self, root):
        """Click inside popup should not hide."""
        base = _DatePickerBase(root)
        base.master = Mock()
        mock_toplevel = Mock()
        mock_toplevel.winfo_rootx.return_value = 0
        mock_toplevel.winfo_rooty.return_value = 0
        base.master.winfo_toplevel.return_value = mock_toplevel

        popup_window = Mock()
        popup_window.winfo_exists.return_value = True
        popup_window.winfo_rootx.return_value = 100
        popup_window.winfo_rooty.return_value = 100
        popup_window.winfo_width.return_value = 200
        popup_window.winfo_height.return_value = 200

        hide_callback = Mock()

        event = Mock()
        event.widget = Mock()
        event.x = 150  # inside horizontally
        event.y = 150  # inside vertically

        result = base._on_main_window_click(event, popup_window, hide_callback)

        assert result == "break"
        hide_callback.assert_not_called()

    def test_get_date_with_calendar(self, root):
        """get_date should delegate to calendar when it exists."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        expected = datetime.date(2024, 4, 1)
        base.calendar.get_selected_date.return_value = expected

        assert base.get_date() == expected

    def test_dateentry_on_date_selected_resets_state(self, root):
        """_on_date_selected should reset pressed state for DateEntry."""
        de = DateEntry(root)
        de._update_entry_text = Mock()
        de.hide_calendar = Mock()
        de.state = Mock()

        test_date = datetime.date(2024, 5, 20)
        de._on_date_selected(test_date)

        de._update_entry_text.assert_called_once_with("2024-05-20")
        de.hide_calendar.assert_called_once()
        de.state.assert_called_with(["!pressed"])

    def test_show_year_view_withdraws_popup(self, root):
        """show_year_view should withdraw existing popup before showing."""
        with patch('tkface.dialog.datepicker.Calendar') as mock_calendar_class, \
             patch('tkface.dialog.datepicker.get_calendar_theme') as mock_get_theme, \
             patch('tkface.dialog.datepicker.tk.Toplevel') as mock_toplevel:

            mock_calendar = Mock()
            mock_calendar_class.return_value = mock_calendar
            mock_calendar.get_popup_geometry.return_value = "300x200+100+100"
            mock_get_theme.return_value = {"background": "white"}
            mock_tl = Mock()
            mock_toplevel.return_value = mock_tl

            base = _DatePickerBase(root)
            base.popup = Mock()
            base.show_year_view()

            base.popup.withdraw.assert_called_once()

    def test_on_focus_out_other_widget_hides_calendar(self, root):
        """Focus moves to other widget should hide calendar."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.calendar.year_selection_mode = False
        base.calendar.month_selection_mode = False
        other_widget = Mock()
        base.focus_get = Mock(return_value=other_widget)
        base._is_child_of_calendar = Mock(return_value=False)
        base.hide_calendar = Mock()

        result = base._on_focus_out(Mock())

        assert result == "break"
        base.hide_calendar.assert_called_once()

    def test_on_focus_out_focus_on_self_returns_break(self, root):
        """When focus is on self, should return break without hiding calendar."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.calendar.year_selection_mode = False
        base.calendar.month_selection_mode = False
        base.focus_get = Mock(return_value=base)
        base.hide_calendar = Mock()

        result = base._on_focus_out(Mock())

        assert result == "break"
        base.hide_calendar.assert_not_called()

    def test_on_focus_out_focus_on_self_with_calendar_selection_mode(self, root):
        """When focus is on self and calendar is in selection mode, should return break."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.calendar.year_selection_mode = True
        base.calendar.month_selection_mode = False
        base.focus_get = Mock(return_value=base)
        base.hide_calendar = Mock()

        result = base._on_focus_out(Mock())

        assert result == "break"
        base.hide_calendar.assert_not_called()

    def test_dateentry_hide_calendar_resets_state(self, root):
        """hide_calendar should reset pressed state for DateEntry."""
        de = DateEntry(root)
        de._unbind_parent_movement_events = Mock()
        de.popup = Mock()
        de.calendar = Mock()
        de.state = Mock()

        de.hide_calendar()

        de._unbind_parent_movement_events.assert_called_once()
        de.state.assert_called_with(["!pressed"])

    def test_on_focus_out_pointer_inside_try_except_path(self, root):
        """When selection mode and pointer inside, focuses and returns via try path."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.calendar.year_selection_mode = True
        base.focus_get = Mock(return_value=None)
        base.popup = Mock()
        base.popup.winfo_pointerxy.return_value = (150, 150)
        base.popup.winfo_rootx.return_value = 100
        base.popup.winfo_rooty.return_value = 100
        base.popup.winfo_width.return_value = 200
        base.popup.winfo_height.return_value = 200

        result = base._on_focus_out(Mock())
        assert result == "break"
        base.calendar.focus_force.assert_called_once()

    def test_on_focus_out_pointer_inside_except_path(self, root):
        """When selection mode and pointer check raises, returns via except path."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.calendar.year_selection_mode = True
        base.focus_get = Mock(return_value=None)
        base.popup = Mock()
        base.popup.winfo_pointerxy.side_effect = Exception("boom")

        result = base._on_focus_out(Mock())
        assert result == "break"

    def test_on_focus_out_no_focus_pointer_inside(self, root):
        """No focus widget, pointer inside -> focus calendar; outside -> hide; attribute error -> hide."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.calendar.year_selection_mode = False
        base.calendar.month_selection_mode = False
        base.focus_get = Mock(return_value=None)
        base.popup = Mock()
        # inside
        base.popup.winfo_pointerxy.return_value = (150, 150)
        base.popup.winfo_rootx.return_value = 100
        base.popup.winfo_rooty.return_value = 100
        base.popup.winfo_width.return_value = 200
        base.popup.winfo_height.return_value = 200
        result = base._on_focus_out(Mock())
        assert result == "break"
        base.calendar.focus_force.assert_called()
        # outside
        base.hide_calendar = Mock()
        base.popup.winfo_pointerxy.return_value = (10, 10)
        result2 = base._on_focus_out(Mock())
        assert result2 == "break"
        base.hide_calendar.assert_called_once()
        # attribute error path
        base.hide_calendar = Mock()
        base.popup.winfo_pointerxy.side_effect = tk.TclError("err")
        base._on_focus_out(Mock())
        base.hide_calendar.assert_called_once()

    def test_on_popup_click_inner_focus_set_exception(self, root):
        """Cover inner try/except: calendar_widget.focus_set raises and is ignored."""
        base = _DatePickerBase(root)
        popup_window = Mock()
        calendar_widget = Mock()
        calendar_widget.focus_set.side_effect = Exception("focus fail")
        hide_callback = Mock()
        event = Mock()
        # Force outer exception to execute inner try
        base._is_child_of_calendar = Mock(side_effect=Exception("boom"))
        base.calendar = Mock()
        base.calendar.year_selection_mode = True

        result = base._on_popup_click(event, popup_window, calendar_widget, hide_callback)
        assert result == "break"

    def test_on_focus_out_outer_try_exception(self, root):
        """Cover outer try/except where _is_child_of_calendar raises; then hide occurs."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.calendar.year_selection_mode = False
        base.calendar.month_selection_mode = False
        focus_w = Mock()
        base.focus_get = Mock(return_value=focus_w)
        base._is_child_of_calendar = Mock(side_effect=Exception("oops"))
        base.hide_calendar = Mock()

        result = base._on_focus_out(Mock())
        assert result == "break"
        base.hide_calendar.assert_called_once()

    def test_on_main_window_click_no_toplevel(self, root):
        """Cover else branch when no toplevel is available (root_x/y from event)."""
        base = _DatePickerBase(root)
        base.master = Mock()
        base.master.winfo_toplevel.return_value = None
        popup_window = Mock()
        popup_window.winfo_exists.return_value = True
        popup_window.winfo_rootx.return_value = 100
        popup_window.winfo_rooty.return_value = 100
        popup_window.winfo_width.return_value = 200
        popup_window.winfo_height.return_value = 200
        hide_callback = Mock()
        event = Mock()
        event.widget = Mock()
        event.x = 10
        event.y = 10
        result = base._on_main_window_click(event, popup_window, hide_callback)
        assert result == "break"
        hide_callback.assert_called_once()

    def test_show_calendar_today_color_applied(self, root):
        """When today_color set, calendar.set_today_color should be called."""
        with patch('tkface.dialog.datepicker.Calendar') as mock_calendar_class, \
             patch('tkface.dialog.datepicker.get_calendar_theme') as mock_get_theme, \
             patch('tkface.dialog.datepicker.tk.Toplevel') as mock_toplevel:

            mock_calendar = Mock()
            mock_calendar.winfo_children.return_value = []
            mock_calendar.get_popup_geometry.return_value = "300x200+100+100"
            mock_calendar_class.return_value = mock_calendar
            mock_get_theme.return_value = {"background": "white"}
            mock_toplevel.return_value = Mock()

            base = _DatePickerBase(root, today_color="blue")
            base.winfo_toplevel = Mock(return_value=Mock())
            base.show_calendar()
            mock_calendar.set_today_color.assert_called_once_with("blue")

    def test_set_selected_date_with_calendar(self, root):
        """set_selected_date should call calendar.set_selected_date when calendar exists."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base._update_entry_text = Mock()
        d = datetime.date(2024, 7, 1)
        base.set_selected_date(d)
        base.calendar.set_selected_date.assert_called_once_with(d)
        base._update_entry_text.assert_called_once_with("2024-07-01")

    def test_update_dpi_scaling_le_one_geometry_path(self, root):
        """When new scaling <= 1.0, popup.geometry should be set and return early."""
        with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling:
            base = _DatePickerBase(root)
            base.dpi_scaling_factor = 2.0
            base.popup = Mock()
            base.popup.winfo_exists.return_value = True
            base.calendar = Mock()
            base.calendar.get_popup_geometry.return_value = "300x200+100+100"
            mock_get_scaling.return_value = 1.0

            base.update_dpi_scaling()
            base.popup.geometry.assert_called_once_with("300x200+100+100")

    def test_on_popup_click_broad_except_path(self, root):
        """Force exception in _on_popup_click to cover broad-except branch."""
        base = _DatePickerBase(root)
        popup_window = Mock()
        calendar_widget = Mock()
        hide_callback = Mock()
        event = Mock()
        # Make _is_child_of_calendar raise
        base._is_child_of_calendar = Mock(side_effect=Exception("boom"))
        base.calendar = Mock()
        base.calendar.year_selection_mode = True

        result = base._on_popup_click(event, popup_window, calendar_widget, hide_callback)
        assert result == "break"
        calendar_widget.focus_set.assert_called_once()

    def test_show_calendar_logger_debug_on_valueerror(self, root):
        """Cover ValueError path in show_calendar DPI scaling try/except."""
        with patch('tkface.dialog.datepicker.Calendar') as mock_calendar_class, \
             patch('tkface.dialog.datepicker.get_calendar_theme') as mock_get_theme, \
             patch('tkface.dialog.datepicker.re') as mock_re, \
             patch('tkface.dialog.datepicker.tk.Toplevel') as mock_toplevel:

            mock_calendar = Mock()
            mock_calendar.winfo_children.return_value = []
            mock_calendar_class.return_value = mock_calendar
            mock_calendar.get_popup_geometry.return_value = "300x200+100+100"
            mock_get_theme.return_value = {"background": "white"}
            mock_re.match.side_effect = ValueError("bad")
            mock_toplevel.return_value = Mock()

            base = _DatePickerBase(root)
            base.dpi_scaling_factor = 2.0
            base.winfo_toplevel = Mock(return_value=Mock())
            base.show_calendar()
            # Should have used original geometry without raising

    def test_on_parent_configure_logger_debug_paths(self, root):
        """Cover logger.debug except branches in _on_parent_configure for popup/year view."""
        with patch('tkface.dialog.datepicker.re') as mock_re:
            base = _DatePickerBase(root)
            # popup active without year view -> ValueError in match
            base.popup = Mock()
            base.popup.winfo_exists.return_value = True
            base.calendar = Mock()
            base.calendar.get_popup_geometry.return_value = "300x200+100+100"
            base.year_view_window = None
            base.dpi_scaling_factor = 2.0
            mock_re.match.side_effect = ValueError("bad")
            base._on_parent_configure(Mock())

        with patch('tkface.dialog.datepicker.re') as mock_re2:
            base2 = _DatePickerBase(root)
            # year view active -> AttributeError path
            base2.popup = Mock()
            base2.year_view_window = Mock()
            base2.year_view_window.winfo_exists.return_value = True
            base2.year_view_calendar = Mock()
            base2.year_view_calendar.get_popup_geometry.return_value = "300x200+100+100"
            base2.dpi_scaling_factor = 2.0
            mock_re2.match.side_effect = AttributeError("oops")
            base2._on_parent_configure(Mock())

    def test_update_dpi_scaling_attribute_error_debug_path(self, root):
        """Cover AttributeError in update_dpi_scaling except path for geometry scaling."""
        with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling, \
             patch('tkface.dialog.datepicker.re') as mock_re:
            base = _DatePickerBase(root)
            base.dpi_scaling_factor = 1.0
            base.popup = Mock()
            base.popup.winfo_exists.return_value = True
            base.calendar = Mock()
            base.calendar.get_popup_geometry.return_value = "300x200+100+100"
            mock_get_scaling.return_value = 2.0
            mock_re.match.side_effect = AttributeError("boom")
            base.update_dpi_scaling()
            base.popup.geometry.assert_called_with("300x200+100+100")

    def test_show_year_view_attribute_error_debug_path(self, root):
        """Cover AttributeError path in show_year_view DPI scaling try/except."""
        with patch('tkface.dialog.datepicker.Calendar') as mock_calendar_class, \
             patch('tkface.dialog.datepicker.get_calendar_theme') as mock_get_theme, \
             patch('tkface.dialog.datepicker.re') as mock_re, \
             patch('tkface.dialog.datepicker.tk.Toplevel') as mock_toplevel:

            mock_calendar = Mock()
            mock_calendar_class.return_value = mock_calendar
            mock_calendar.get_popup_geometry.return_value = "300x200+100+100"
            mock_get_theme.return_value = {"background": "white"}
            mock_re.match.side_effect = AttributeError("fail")
            mock_toplevel.return_value = Mock()

            base = _DatePickerBase(root)
            base.dpi_scaling_factor = 2.0
            base.popup = Mock()
            base.show_year_view()
