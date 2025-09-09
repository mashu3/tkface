# pylint: disable=import-outside-toplevel,protected-access
"""
Tests for tkface DatePicker widgets
"""

import datetime
import tkinter as tk
from unittest.mock import Mock, patch

import pytest

from tkface.dialog.datepicker import DateEntry, DateFrame, DatePickerConfig, _DatePickerBase


class TestDatePickerConfig:
    """Test cases for DatePickerConfig dataclass."""

    def test_datepicker_config_defaults(self):
        """Test DatePickerConfig default values."""
        config = DatePickerConfig()
        assert config.date_format == "%Y-%m-%d"
        assert config.year is None
        assert config.month is None
        assert config.show_week_numbers is False
        assert config.week_start == "Sunday"
        assert config.day_colors is None
        assert config.holidays is None
        assert config.selectmode == "single"
        assert config.theme == "light"
        assert config.language == "en"
        assert config.today_color == "yellow"
        assert config.date_callback is None

    def test_datepicker_config_custom_values(self):
        """Test DatePickerConfig with custom values."""
        def dummy_callback(date):
            pass

        config = DatePickerConfig(
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
        
        assert config.date_format == "%d/%m/%Y"
        assert config.year == 2024
        assert config.month == 3
        assert config.show_week_numbers is True
        assert config.week_start == "Monday"
        assert config.day_colors == {"Sunday": "red"}
        assert config.holidays == {"2024-01-01": "red"}
        assert config.selectmode == "range"
        assert config.theme == "dark"
        assert config.language == "ja"
        assert config.today_color == "blue"
        assert config.date_callback == dummy_callback


class TestDatePickerBase:
    """Test cases for _DatePickerBase class."""

    def test_datepicker_base_creation(self, root):
        """Test _DatePickerBase creation."""
        base = _DatePickerBase(root)
        assert base is not None
        assert base.dpi_scaling_factor >= 1.0  # DPI scaling factor should be at least 1.0
        assert base.calendar_config is not None
        assert base.selected_date is None

    def test_datepicker_base_with_config(self, root):
        """Test _DatePickerBase with DatePickerConfig."""
        config = DatePickerConfig(
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
            today_color="blue"
        )
        
        base = _DatePickerBase(root, config=config)
        assert base.calendar_config["date_format"] == "%d/%m/%Y"
        assert base.calendar_config["year"] == 2024
        assert base.calendar_config["month"] == 3
        assert base.calendar_config["show_week_numbers"] is True
        assert base.calendar_config["week_start"] == "Monday"
        assert base.calendar_config["day_colors"] == {"Sunday": "red"}
        assert base.calendar_config["holidays"] == {"2024-01-01": "red"}
        assert base.calendar_config["selectmode"] == "range"
        assert base.calendar_config["theme"] == "dark"
        # Language is not stored in calendar_config, it's handled separately
        assert base.today_color == "blue"

    def test_datepicker_base_with_individual_params(self, root):
        """Test _DatePickerBase with individual parameters."""
        base = _DatePickerBase(
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
            today_color="blue"
        )
        
        assert base.calendar_config["date_format"] == "%d/%m/%Y"
        assert base.calendar_config["year"] == 2024
        assert base.calendar_config["month"] == 3
        assert base.calendar_config["show_week_numbers"] is True
        assert base.calendar_config["week_start"] == "Monday"
        assert base.calendar_config["day_colors"] == {"Sunday": "red"}
        assert base.calendar_config["holidays"] == {"2024-01-01": "red"}
        assert base.calendar_config["selectmode"] == "range"
        assert base.calendar_config["theme"] == "dark"
        # Language is not stored in calendar_config, it's handled separately
        assert base.today_color == "blue"

    def test_datepicker_base_dpi_scaling_error(self, root):
        """Test DPI scaling error handling."""
        with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling:
            mock_get_scaling.side_effect = ImportError("Test error")
            
            base = _DatePickerBase(root)
            assert base.dpi_scaling_factor == 1.0

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

    def test_datepicker_base_update_dpi_scaling_no_change(self, root):
        """Test update_dpi_scaling with no significant change."""
        base = _DatePickerBase(root)
        base.dpi_scaling_factor = 1.0
        
        with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling:
            mock_get_scaling.return_value = 1.01  # Small change
            
            base.update_dpi_scaling()
            # Should return early due to small change

    def test_datepicker_base_update_dpi_scaling_error(self, root):
        """Test update_dpi_scaling with error."""
        base = _DatePickerBase(root)
        base.dpi_scaling_factor = 1.0
        
        with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling:
            mock_get_scaling.side_effect = ImportError("Test error")
            
            base.update_dpi_scaling()
            assert base.dpi_scaling_factor == 1.0


class TestDateFrame:
    """Test cases for DateFrame widget."""

    def test_dateframe_creation(self, root):
        """Test DateFrame creation."""
        df = DateFrame(root)
        assert df is not None
        assert hasattr(df, "entry")
        assert hasattr(df, "button")

    def test_dateframe_with_config(self, root):
        """Test DateFrame with DatePickerConfig."""
        config = DatePickerConfig(
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
            today_color="blue"
        )
        
        df = DateFrame(root, config=config)
        assert df.calendar_config["date_format"] == "%d/%m/%Y"
        assert df.calendar_config["year"] == 2024
        assert df.calendar_config["month"] == 3
        assert df.calendar_config["show_week_numbers"] is True
        assert df.calendar_config["week_start"] == "Monday"
        assert df.calendar_config["day_colors"] == {"Sunday": "red"}
        assert df.calendar_config["holidays"] == {"2024-01-01": "red"}
        assert df.calendar_config["selectmode"] == "range"
        assert df.calendar_config["theme"] == "dark"
        # Language is not stored in calendar_config, it's handled separately
        assert df.today_color == "blue"

    def test_dateframe_with_individual_params(self, root):
        """Test DateFrame with individual parameters."""
        df = DateFrame(
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
            button_text="📆"
        )
        
        assert df.calendar_config["date_format"] == "%d/%m/%Y"
        assert df.calendar_config["year"] == 2024
        assert df.calendar_config["month"] == 3
        assert df.calendar_config["show_week_numbers"] is True
        assert df.calendar_config["week_start"] == "Monday"
        assert df.calendar_config["day_colors"] == {"Sunday": "red"}
        assert df.calendar_config["holidays"] == {"2024-01-01": "red"}
        assert df.calendar_config["selectmode"] == "range"
        assert df.calendar_config["theme"] == "dark"
        # Language is not stored in calendar_config, it's handled separately
        assert df.today_color == "blue"
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

    def test_dateframe_dpi_scaling_error(self, root):
        """Test DateFrame DPI scaling error handling."""
        with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling:
            mock_get_scaling.side_effect = ImportError("Test error")
            
            # Should not raise exception
            df = DateFrame(root)
            assert df.dpi_scaling_factor == 1.0


class TestDateEntry:
    """Test cases for DateEntry widget."""

    def test_dateentry_creation(self, root):
        """Test DateEntry creation."""
        de = DateEntry(root)
        assert de is not None
        assert de.date_format == "%Y-%m-%d"
        assert de.selected_date is None

    def test_dateentry_with_config(self, root):
        """Test DateEntry with DatePickerConfig."""
        config = DatePickerConfig(
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
            today_color="blue"
        )
        
        de = DateEntry(root, config=config)
        assert de.calendar_config["date_format"] == "%d/%m/%Y"
        assert de.calendar_config["year"] == 2024
        assert de.calendar_config["month"] == 3
        assert de.calendar_config["show_week_numbers"] is True
        assert de.calendar_config["week_start"] == "Monday"
        assert de.calendar_config["day_colors"] == {"Sunday": "red"}
        assert de.calendar_config["holidays"] == {"2024-01-01": "red"}
        assert de.calendar_config["selectmode"] == "range"
        assert de.calendar_config["theme"] == "dark"
        # Language is not stored in calendar_config, it's handled separately
        assert de.today_color == "blue"

    def test_dateentry_with_individual_params(self, root):
        """Test DateEntry with individual parameters."""
        de = DateEntry(
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
            width=20
        )
        
        assert de.calendar_config["date_format"] == "%d/%m/%Y"
        assert de.calendar_config["year"] == 2024
        assert de.calendar_config["month"] == 3
        assert de.calendar_config["show_week_numbers"] is True
        assert de.calendar_config["week_start"] == "Monday"
        assert de.calendar_config["day_colors"] == {"Sunday": "red"}
        assert de.calendar_config["holidays"] == {"2024-01-01": "red"}
        assert de.calendar_config["selectmode"] == "range"
        assert de.calendar_config["theme"] == "dark"
        # Language is not stored in calendar_config, it's handled separately
        assert de.today_color == "blue"

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

    def test_dateentry_dpi_scaling_error(self, root):
        """Test DateEntry DPI scaling error handling."""
        with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling:
            mock_get_scaling.side_effect = ImportError("Test error")
            
            # Should not raise exception
            de = DateEntry(root)
            assert de.dpi_scaling_factor == 1.0

    def test_dateentry_button_text_removal(self, root):
        """Test DateEntry removes button_text from kwargs."""
        de = DateEntry(root, button_text="test", width=20)
        # Should not raise exception and button_text should be removed from kwargs
        assert True


class TestDatePickerIntegration:
    """Integration tests for DatePicker widgets."""

    def test_dateframe_calendar_integration(self, root):
        """Test DateFrame with calendar integration."""
        df = DateFrame(root, year=2024, month=3)
        
        # Test basic functionality
        assert df.calendar_config["year"] == 2024
        assert df.calendar_config["month"] == 3
        
        # Test date setting
        test_date = datetime.date(2024, 3, 15)
        df.set_selected_date(test_date)
        assert df.selected_date == test_date
        assert df.get_date_string() == "2024-03-15"

    def test_dateentry_calendar_integration(self, root):
        """Test DateEntry with calendar integration."""
        de = DateEntry(root, year=2024, month=3)
        
        # Test basic functionality
        assert de.calendar_config["year"] == 2024
        assert de.calendar_config["month"] == 3
        
        # Test date setting
        test_date = datetime.date(2024, 3, 15)
        de.set_selected_date(test_date)
        assert de.selected_date == test_date
        assert de.get_date_string() == "2024-03-15"

    def test_datepicker_callback_integration(self, root):
        """Test DatePicker with callback integration."""
        callback_called = False
        callback_date = None

        def callback(date):
            nonlocal callback_called, callback_date
            callback_called = True
            callback_date = date

        df = DateFrame(root, date_callback=callback)
        test_date = datetime.date(2024, 3, 15)
        df._on_date_selected(test_date)
        
        assert callback_called
        assert callback_date == test_date

    def test_datepicker_theme_integration(self, root):
        """Test DatePicker with theme integration."""
        df = DateFrame(root, theme="dark")
        assert df.calendar_config["theme"] == "dark"
        
        df.set_theme("light")
        assert df.calendar_config["theme"] == "light"

    def test_datepicker_language_integration(self, root):
        """Test DatePicker with language integration."""
        df = DateFrame(root, language="ja")
        # Language is not stored in calendar_config, it's handled separately
        
        # Test language refresh
        df.refresh_language()
        # Should not raise exception

    def test_datepicker_holidays_integration(self, root):
        """Test DatePicker with holidays integration."""
        holidays = {"2024-01-01": "red", "2024-12-25": "green"}
        df = DateFrame(root, holidays=holidays)
        assert df.calendar_config["holidays"] == holidays
        
        # Test holidays setting through calendar config
        new_holidays = {"2024-02-14": "pink"}
        df.calendar_config["holidays"] = new_holidays
        assert df.calendar_config["holidays"] == new_holidays

    def test_datepicker_day_colors_integration(self, root):
        """Test DatePicker with day colors integration."""
        day_colors = {"Sunday": "red", "Saturday": "blue"}
        df = DateFrame(root, day_colors=day_colors)
        assert df.calendar_config["day_colors"] == day_colors
        
        new_colors = {"Friday": "green"}
        df.set_day_colors(new_colors)
        assert df.calendar_config["day_colors"] == new_colors

    def test_datepicker_week_start_integration(self, root):
        """Test DatePicker with week start integration."""
        df = DateFrame(root, week_start="Monday")
        assert df.calendar_config["week_start"] == "Monday"
        
        df.set_week_start("Saturday")
        assert df.calendar_config["week_start"] == "Saturday"

    def test_datepicker_week_numbers_integration(self, root):
        """Test DatePicker with week numbers integration."""
        df = DateFrame(root, show_week_numbers=True)
        assert df.calendar_config["show_week_numbers"] is True
        
        df.set_show_week_numbers(False)
        assert df.calendar_config["show_week_numbers"] is False

    def test_datepicker_selectmode_integration(self, root):
        """Test DatePicker with select mode integration."""
        df = DateFrame(root, selectmode="range")
        assert df.calendar_config["selectmode"] == "range"
        
        # Test single mode
        df = DateFrame(root, selectmode="single")
        assert df.calendar_config["selectmode"] == "single"

    def test_datepicker_today_color_integration(self, root):
        """Test DatePicker with today color integration."""
        df = DateFrame(root, today_color="blue")
        assert df.today_color == "blue"
        
        df.set_today_color("red")
        assert df.today_color == "red"

    def test_datepicker_popup_size_integration(self, root):
        """Test DatePicker with popup size integration."""
        df = DateFrame(root)
        
        # Test popup size setting
        df.set_popup_size(400, 300)
        # Should not raise exception

    def test_datepicker_dpi_scaling_integration(self, root):
        """Test DatePicker with DPI scaling integration."""
        df = DateFrame(root)
        
        # Test DPI scaling update
        df.update_dpi_scaling()
        # Should not raise exception


class TestDatePickerEventHandling:
    """Test cases for DatePicker event handling methods."""

    def test_datepicker_base_on_date_selected_with_callback(self, root):
        """Test _on_date_selected with callback."""
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

    def test_datepicker_base_on_date_selected_without_callback(self, root):
        """Test _on_date_selected without callback."""
        base = _DatePickerBase(root)
        base._update_entry_text = Mock()
        base.hide_calendar = Mock()
        
        test_date = datetime.date(2024, 3, 15)
        base._on_date_selected(test_date)
        
        assert base.selected_date == test_date
        base._update_entry_text.assert_called_once_with("2024-03-15")
        base.hide_calendar.assert_called_once()

    def test_datepicker_base_on_date_selected_none_date(self, root):
        """Test _on_date_selected with None date."""
        base = _DatePickerBase(root)
        base._update_entry_text = Mock()
        base.hide_calendar = Mock()
        
        base._on_date_selected(None)
        
        assert base.selected_date is None
        base._update_entry_text.assert_not_called()
        base.hide_calendar.assert_not_called()

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

    def test_datepicker_base_on_main_window_click(self, root):
        """Test _on_main_window_click."""
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
        
        # Test with click outside popup
        event = Mock()
        event.widget = Mock()  # Not a string, so it will proceed to the main logic
        event.x = 50  # root_x = 0 + 50 = 50, which is < popup_x (100)
        event.y = 50  # root_y = 0 + 50 = 50, which is < popup_y (100)
        
        result = base._on_main_window_click(event, popup_window, hide_callback)
        
        assert result == "break"
        # The condition checks: root_x < popup_x OR root_x > popup_x + popup_w OR root_y < popup_y OR root_y > popup_y + popup_h
        # root_x = 50, popup_x = 100, so 50 < 100 is True, so hide_callback should be called
        hide_callback.assert_called_once()

    def test_datepicker_base_on_main_window_click_string_widget(self, root):
        """Test _on_main_window_click with string widget."""
        base = _DatePickerBase(root)
        popup_window = Mock()
        hide_callback = Mock()
        
        event = Mock()
        event.widget = "string"
        
        result = base._on_main_window_click(event, popup_window, hide_callback)
        
        assert result == "break"
        hide_callback.assert_not_called()

    def test_datepicker_base_on_main_window_click_popup_not_exists(self, root):
        """Test _on_main_window_click with popup not existing."""
        base = _DatePickerBase(root)
        popup_window = Mock()
        popup_window.winfo_exists.return_value = False
        hide_callback = Mock()
        
        event = Mock()
        event.widget = "not_string"
        
        result = base._on_main_window_click(event, popup_window, hide_callback)
        
        assert result == "break"
        hide_callback.assert_not_called()


class TestDatePickerCalendarOperations:
    """Test cases for DatePicker calendar operations."""

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

    def test_datepicker_base_show_calendar_already_exists(self, root):
        """Test show_calendar when popup already exists."""
        base = _DatePickerBase(root)
        base.popup = Mock()
        
        base.show_calendar()
        
        # Should return early without creating new popup
        assert base.popup is not None

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

    def test_datepicker_base_hide_calendar_no_popup(self, root):
        """Test hide_calendar when no popup exists."""
        base = _DatePickerBase(root)
        base.popup = None
        
        # Should not raise exception
        base.hide_calendar()

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

    def test_datepicker_base_show_year_view_already_exists(self, root):
        """Test show_year_view when year view already exists."""
        base = _DatePickerBase(root)
        base.year_view_window = Mock()
        
        base.show_year_view()
        
        # Should return early without creating new year view
        assert base.year_view_window is not None

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

    def test_datepicker_base_hide_year_view_no_window(self, root):
        """Test hide_year_view when no year view window exists."""
        base = _DatePickerBase(root)
        base.year_view_window = None
        
        # Should not raise exception
        base.hide_year_view()

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

    def test_datepicker_base_on_calendar_year_view_request_with_calendar(self, root):
        """Test _on_calendar_year_view_request with calendar."""
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

    def test_datepicker_base_on_calendar_year_view_request_without_calendar(self, root):
        """Test _on_calendar_year_view_request without calendar."""
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

    def test_datepicker_base_bind_parent_movement_events(self, root):
        """Test _bind_parent_movement_events."""
        base = _DatePickerBase(root)
        base.popup = Mock()
        base.winfo_toplevel = Mock(return_value=Mock())
        base._on_parent_configure = Mock()
        
        base._bind_parent_movement_events()
        
        assert hasattr(base, '_parent_configure_binding')

    def test_datepicker_base_bind_parent_movement_events_no_popup(self, root):
        """Test _bind_parent_movement_events without popup."""
        base = _DatePickerBase(root)
        base.popup = None
        base.year_view_window = None
        
        base._bind_parent_movement_events()
        
        # Should not bind events

    def test_datepicker_base_unbind_parent_movement_events(self, root):
        """Test _unbind_parent_movement_events."""
        base = _DatePickerBase(root)
        base._parent_configure_binding = "test_binding"
        base.winfo_toplevel = Mock(return_value=Mock())
        
        base._unbind_parent_movement_events()
        
        assert not hasattr(base, '_parent_configure_binding')

    def test_datepicker_base_unbind_parent_movement_events_no_binding(self, root):
        """Test _unbind_parent_movement_events without binding."""
        base = _DatePickerBase(root)
        base.winfo_toplevel = Mock(return_value=Mock())
        
        # Should not raise exception
        base._unbind_parent_movement_events()

    def test_datepicker_base_on_parent_configure(self, root):
        """Test _on_parent_configure."""
        with patch('tkface.dialog.datepicker.re') as mock_re:
            base = _DatePickerBase(root)
            base.popup = Mock()
            base.popup.winfo_exists.return_value = True
            base.calendar = Mock()
            base.calendar.get_popup_geometry.return_value = "300x200+100+100"
            base.year_view_window = None
            base.dpi_scaling_factor = 1.0
            
            mock_re.match.return_value = None
            
            base._on_parent_configure(Mock())
            
            base.popup.geometry.assert_called_once_with("300x200+100+100")

    def test_datepicker_base_on_parent_configure_with_year_view(self, root):
        """Test _on_parent_configure with year view active."""
        with patch('tkface.dialog.datepicker.re') as mock_re:
            base = _DatePickerBase(root)
            base.popup = Mock()
            base.year_view_window = Mock()
            base.year_view_window.winfo_exists.return_value = True
            base.year_view_calendar = Mock()
            base.year_view_calendar.get_popup_geometry.return_value = "300x200+100+100"
            base.dpi_scaling_factor = 1.0
            
            mock_re.match.return_value = None
            
            base._on_parent_configure(Mock())
            
            base.year_view_window.geometry.assert_called_once_with("300x200+100+100")


class TestDatePickerDpiScaling:
    """Test cases for DatePicker DPI scaling functionality."""

    def test_datepicker_base_update_dpi_scaling_with_change(self, root):
        """Test update_dpi_scaling with significant change."""
        with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling, \
             patch('tkface.dialog.datepicker.re') as mock_re:
            
            base = _DatePickerBase(root)
            base.dpi_scaling_factor = 1.0
            base.calendar = Mock()
            base.calendar.update_dpi_scaling = Mock()
            base.popup = Mock()
            base.popup.winfo_exists.return_value = True
            base.calendar.get_popup_geometry.return_value = "300x200+100+100"
            
            mock_get_scaling.return_value = 2.0
            mock_match = Mock()
            mock_match.groups.return_value = (300, 200, 100, 100)
            mock_re.match.return_value = mock_match
            
            base.update_dpi_scaling()
            
            assert base.dpi_scaling_factor == 2.0
            base.calendar.update_dpi_scaling.assert_called_once()
            base.popup.geometry.assert_called_once_with("600x400+100+100")

    def test_datepicker_base_update_dpi_scaling_no_popup(self, root):
        """Test update_dpi_scaling without popup."""
        with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling:
            base = _DatePickerBase(root)
            base.dpi_scaling_factor = 1.0
            base.popup = None
            
            mock_get_scaling.return_value = 2.0
            
            base.update_dpi_scaling()
            
            assert base.dpi_scaling_factor == 2.0

    def test_datepicker_base_update_dpi_scaling_popup_not_exists(self, root):
        """Test update_dpi_scaling with popup not existing."""
        with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling:
            base = _DatePickerBase(root)
            base.dpi_scaling_factor = 1.0
            base.popup = Mock()
            base.popup.winfo_exists.return_value = False
            
            mock_get_scaling.return_value = 2.0
            
            base.update_dpi_scaling()
            
            assert base.dpi_scaling_factor == 2.0

    def test_datepicker_base_update_dpi_scaling_geometry_error(self, root):
        """Test update_dpi_scaling with geometry parsing error."""
        with patch('tkface.dialog.datepicker.get_scaling_factor') as mock_get_scaling, \
             patch('tkface.dialog.datepicker.re') as mock_re:
            
            base = _DatePickerBase(root)
            base.dpi_scaling_factor = 1.0
            base.popup = Mock()
            base.popup.winfo_exists.return_value = True
            base.calendar = Mock()
            base.calendar.get_popup_geometry.return_value = "invalid_geometry"
            
            mock_get_scaling.return_value = 2.0
            mock_re.match.return_value = None
            
            base.update_dpi_scaling()
            
            assert base.dpi_scaling_factor == 2.0
            base.popup.geometry.assert_called_once_with("invalid_geometry")


class TestDateEntrySpecific:
    """Test cases for DateEntry specific functionality."""

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

    def test_dateentry_on_key_down(self, root):
        """Test DateEntry _on_key with Down key."""
        de = DateEntry(root)
        de.show_calendar = Mock()
        
        event = Mock()
        event.keysym = "Down"
        
        de._on_key(event)
        
        de.show_calendar.assert_called_once()

    def test_dateentry_on_key_space(self, root):
        """Test DateEntry _on_key with space key."""
        de = DateEntry(root)
        de.show_calendar = Mock()
        
        event = Mock()
        event.keysym = "space"
        
        de._on_key(event)
        
        de.show_calendar.assert_called_once()

    def test_dateentry_on_key_other(self, root):
        """Test DateEntry _on_key with other key."""
        de = DateEntry(root)
        de.show_calendar = Mock()
        
        event = Mock()
        event.keysym = "Return"
        
        de._on_key(event)
        
        de.show_calendar.assert_not_called()

    def test_dateentry_setup_style_with_configure(self, root):
        """Test DateEntry _setup_style with configure."""
        de = DateEntry(root)
        de.style.configure = Mock(return_value={"background": "white"})
        de.style.layout = Mock()
        de.style.map = Mock(return_value={"background": [("active", "blue")]})
        
        # Should not raise exception
        de._setup_style()

    def test_dateentry_setup_style_without_configure(self, root):
        """Test DateEntry _setup_style without configure."""
        de = DateEntry(root)
        de.style.configure = Mock(return_value=None)
        de.style.layout = Mock()
        de.style.map = Mock(return_value=None)
        
        # Should not raise exception
        de._setup_style()


class TestDatePickerComplexEventHandling:
    """Test cases for complex DatePicker event handling scenarios."""

    def test_datepicker_base_on_popup_click_string_widget(self, root):
        """Test _on_popup_click with string widget."""
        base = _DatePickerBase(root)
        popup_window = Mock()
        popup_window.winfo_pointerxy.return_value = (150, 150)
        popup_window.winfo_rootx.return_value = 100
        popup_window.winfo_rooty.return_value = 100
        popup_window.winfo_width.return_value = 200
        popup_window.winfo_height.return_value = 200
        
        calendar_widget = Mock()
        hide_callback = Mock()
        
        event = Mock()
        event.widget = "string"
        
        result = base._on_popup_click(event, popup_window, calendar_widget, hide_callback)
        
        assert result == "break"
        calendar_widget.focus_set.assert_called_once()

    def test_datepicker_base_on_popup_click_outside_popup(self, root):
        """Test _on_popup_click with click outside popup."""
        base = _DatePickerBase(root)
        popup_window = Mock()
        popup_window.winfo_pointerxy.return_value = (50, 50)
        popup_window.winfo_rootx.return_value = 100
        popup_window.winfo_rooty.return_value = 100
        popup_window.winfo_width.return_value = 200
        popup_window.winfo_height.return_value = 200
        
        calendar_widget = Mock()
        hide_callback = Mock()
        
        event = Mock()
        event.widget = "string"
        
        result = base._on_popup_click(event, popup_window, calendar_widget, hide_callback)
        
        assert result == "break"
        hide_callback.assert_called_once()

    def test_datepicker_base_on_popup_click_with_calendar_selection_mode(self, root):
        """Test _on_popup_click with calendar in selection mode."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.calendar.year_selection_mode = True
        base._is_child_of_calendar = Mock(return_value=True)
        
        popup_window = Mock()
        calendar_widget = Mock()
        hide_callback = Mock()
        
        event = Mock()
        event.widget = Mock()
        
        result = base._on_popup_click(event, popup_window, calendar_widget, hide_callback)
        
        assert result == "break"
        calendar_widget.focus_set.assert_called_once()
        hide_callback.assert_not_called()

    def test_datepicker_base_on_popup_click_with_calendar_selection_mode_outside(self, root):
        """Test _on_popup_click with calendar in selection mode, click outside."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.calendar.year_selection_mode = True
        base._is_child_of_calendar = Mock(return_value=False)
        
        popup_window = Mock()
        calendar_widget = Mock()
        hide_callback = Mock()
        
        event = Mock()
        event.widget = Mock()
        
        result = base._on_popup_click(event, popup_window, calendar_widget, hide_callback)
        
        assert result == "break"
        hide_callback.assert_called_once()

    def test_datepicker_base_on_popup_click_exception_handling(self, root):
        """Test _on_popup_click with exception handling."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.calendar.year_selection_mode = True
        base._is_child_of_calendar = Mock(side_effect=Exception("Test error"))
        
        popup_window = Mock()
        calendar_widget = Mock()
        hide_callback = Mock()
        
        event = Mock()
        event.widget = Mock()
        
        result = base._on_popup_click(event, popup_window, calendar_widget, hide_callback)
        
        assert result == "break"
        # Should handle exception gracefully

    def test_datepicker_base_on_focus_out_with_calendar_focus(self, root):
        """Test _on_focus_out with focus on calendar."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.focus_get = Mock(return_value=Mock())
        base._is_child_of_calendar = Mock(return_value=True)
        
        result = base._on_focus_out(Mock())
        
        assert result == "break"

    def test_datepicker_base_on_focus_out_with_self_focus(self, root):
        """Test _on_focus_out with focus on self."""
        base = _DatePickerBase(root)
        base.focus_get = Mock(return_value=base)
        
        result = base._on_focus_out(Mock())
        
        assert result == "break"

    def test_datepicker_base_on_focus_out_with_calendar_selection_mode(self, root):
        """Test _on_focus_out with calendar in selection mode."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.calendar.year_selection_mode = True
        base.popup = Mock()
        base.popup.winfo_pointerxy.return_value = (150, 150)
        base.popup.winfo_rootx.return_value = 100
        base.popup.winfo_rooty.return_value = 100
        base.popup.winfo_width.return_value = 200
        base.popup.winfo_height.return_value = 200
        base.focus_get = Mock(return_value=None)
        
        result = base._on_focus_out(Mock())
        
        assert result == "break"
        base.calendar.focus_force.assert_called_once()

    def test_datepicker_base_on_focus_out_with_calendar_selection_mode_outside(self, root):
        """Test _on_focus_out with calendar in selection mode, pointer outside."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.calendar.year_selection_mode = True
        base.popup = Mock()
        base.popup.winfo_pointerxy.return_value = (50, 50)
        base.popup.winfo_rootx.return_value = 100
        base.popup.winfo_rooty.return_value = 100
        base.popup.winfo_width.return_value = 200
        base.popup.winfo_height.return_value = 200
        base.focus_get = Mock(return_value=None)
        base.hide_calendar = Mock()
        
        result = base._on_focus_out(Mock())
        
        assert result == "break"
        base.hide_calendar.assert_called_once()

    def test_datepicker_base_on_focus_out_with_pointer_inside(self, root):
        """Test _on_focus_out with pointer inside popup."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.popup = Mock()
        base.popup.winfo_pointerxy.return_value = (150, 150)
        base.popup.winfo_rootx.return_value = 100
        base.popup.winfo_rooty.return_value = 100
        base.popup.winfo_width.return_value = 200
        base.popup.winfo_height.return_value = 200
        base.focus_get = Mock(return_value=None)
        
        result = base._on_focus_out(Mock())
        
        assert result == "break"
        base.calendar.focus_force.assert_called_once()

    def test_datepicker_base_on_focus_out_with_pointer_outside(self, root):
        """Test _on_focus_out with pointer outside popup."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.popup = Mock()
        base.popup.winfo_pointerxy.return_value = (50, 50)
        base.popup.winfo_rootx.return_value = 100
        base.popup.winfo_rooty.return_value = 100
        base.popup.winfo_width.return_value = 200
        base.popup.winfo_height.return_value = 200
        base.focus_get = Mock(return_value=None)
        base.hide_calendar = Mock()
        
        result = base._on_focus_out(Mock())
        
        assert result == "break"
        base.hide_calendar.assert_called_once()

    def test_datepicker_base_on_focus_out_exception_handling(self, root):
        """Test _on_focus_out with exception handling."""
        base = _DatePickerBase(root)
        base.calendar = Mock()
        base.calendar.year_selection_mode = True
        base.popup = Mock()
        base.popup.winfo_pointerxy.side_effect = Exception("Test error")
        base.focus_get = Mock(return_value=None)
        
        result = base._on_focus_out(Mock())
        
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

    def test_datepicker_base_show_calendar_with_theme_error(self, root):
        """Test show_calendar with theme error."""
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

    def test_datepicker_base_show_year_view_with_theme_error(self, root):
        """Test show_year_view with theme error."""
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

    def test_datepicker_base_show_calendar_with_dpi_scaling(self, root):
        """Test show_calendar with DPI scaling."""
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
            
            base = _DatePickerBase(root)
            base.dpi_scaling_factor = 2.0
            base.winfo_toplevel = Mock(return_value=Mock())  # Add missing method
            base.show_calendar()
            
            assert base.popup is not None
            assert base.calendar is not None
            # Should scale geometry
            mock_popup.geometry.assert_called_with("600x400+100+100")

    def test_datepicker_base_show_year_view_with_dpi_scaling(self, root):
        """Test show_year_view with DPI scaling."""
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
            
            base = _DatePickerBase(root)
            base.dpi_scaling_factor = 2.0
            base.popup = Mock()
            base.show_year_view()
            
            assert base.year_view_window is not None
            assert base.year_view_calendar is not None
            # Should scale geometry
            mock_year_view_window.geometry.assert_called_with("600x400+100+100")

    def test_datepicker_base_show_calendar_with_dpi_scaling_error(self, root):
        """Test show_calendar with DPI scaling error."""
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
            
            base = _DatePickerBase(root)
            base.dpi_scaling_factor = 2.0
            base.winfo_toplevel = Mock(return_value=Mock())  # Add missing method
            base.show_calendar()
            
            assert base.popup is not None
            assert base.calendar is not None
            # Should use original geometry on error
            mock_popup.geometry.assert_called_with("300x200+100+100")

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

    def test_datepicker_base_on_parent_configure_with_dpi_scaling(self, root):
        """Test _on_parent_configure with DPI scaling."""
        with patch('tkface.dialog.datepicker.re') as mock_re:
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

    def test_datepicker_base_on_parent_configure_with_year_view_dpi_scaling(self, root):
        """Test _on_parent_configure with year view and DPI scaling."""
        with patch('tkface.dialog.datepicker.re') as mock_re:
            base = _DatePickerBase(root)
            base.popup = Mock()
            base.year_view_window = Mock()
            base.year_view_window.winfo_exists.return_value = True
            base.year_view_calendar = Mock()
            base.year_view_calendar.get_popup_geometry.return_value = "300x200+100+100"
            base.dpi_scaling_factor = 2.0
            
            mock_match = Mock()
            mock_match.groups.return_value = (300, 200, 100, 100)
            mock_re.match.return_value = mock_match
            
            base._on_parent_configure(Mock())
            
            base.year_view_window.geometry.assert_called_once_with("600x400+100+100")

    def test_datepicker_base_on_parent_configure_with_geometry_error(self, root):
        """Test _on_parent_configure with geometry parsing error."""
        with patch('tkface.dialog.datepicker.re') as mock_re:
            base = _DatePickerBase(root)
            base.popup = Mock()
            base.popup.winfo_exists.return_value = True
            base.calendar = Mock()
            base.calendar.get_popup_geometry.return_value = "invalid_geometry"
            base.year_view_window = None
            base.dpi_scaling_factor = 2.0
            
            mock_re.match.side_effect = ValueError("Invalid geometry")
            
            base._on_parent_configure(Mock())
            
            # Should use original geometry on error
            base.popup.geometry.assert_called_once_with("invalid_geometry")
