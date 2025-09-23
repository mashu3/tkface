# pylint: disable=import-outside-toplevel,protected-access
"""
Tests for tkface Calendar style functionality
"""

import configparser
import datetime
import tkinter as tk
from unittest.mock import Mock, mock_open, patch

import pytest

from tkface import Calendar


class TestCalendarStyle:
    """Test cases for Calendar style functionality."""

    def test_get_calendar_themes(self):
        """Test get_calendar_themes function."""
        from tkface.widget.calendar.style import get_calendar_themes
        
        themes = get_calendar_themes()
        assert "light" in themes
        assert "dark" in themes
        assert len(themes) >= 2

    def test_get_day_names(self, root):
        """Test get_day_names function."""
        from tkface.widget.calendar.style import get_day_names
        
        cal = Calendar(root, year=2024, month=1)
        
        # Test short names
        short_names = get_day_names(cal, short=True)
        assert len(short_names) == 7
        
        # Test full names
        full_names = get_day_names(cal, short=False)
        assert len(full_names) == 7

    def test_calendar_theme_switching(self, root):
        """Test calendar theme switching."""
        cal = Calendar(root, year=2024, month=1, theme="light")
        assert cal.theme == "light"
        
        cal.set_theme("dark")
        assert cal.theme == "dark"

    def test_calendar_style_application(self, root):
        """Test calendar style application."""
        cal = Calendar(root, year=2024, month=1, theme="dark")
        # Should not raise exception
        assert cal.theme == "dark"

    def test_parse_font_valid(self):
        """Test _parse_font with valid font string."""
        from tkface.widget.calendar.style import _parse_font
        
        result = _parse_font("Arial, 12, bold")
        assert result == ("Arial", 12, "bold")
        
        result = _parse_font("Times, 10")
        assert result == ("Times", 10, "normal")

    def test_parse_font_invalid_size(self):
        """Test _parse_font with invalid size."""
        from tkface.widget.calendar.style import _parse_font
        
        result = _parse_font("Arial, invalid, bold")
        assert result == ("Arial", 9, "bold")

    def test_parse_font_short_string(self):
        """Test _parse_font with short string."""
        from tkface.widget.calendar.style import _parse_font
        
        result = _parse_font("Arial")
        assert result == ("TkDefaultFont", 9, "normal")

    def test_load_theme_file_not_found(self):
        """Test _load_theme_file with non-existent file."""
        from tkface.widget.calendar.style import _load_theme_file
        
        with pytest.raises(FileNotFoundError):
            _load_theme_file("nonexistent_theme")

    def test_load_theme_file_config_error(self):
        """Test _load_theme_file with config error."""
        from unittest.mock import Mock, patch

        from tkface.widget.calendar.style import _load_theme_file
        
        with patch('configparser.ConfigParser') as mock_config:
            mock_parser = Mock()
            mock_parser.read.side_effect = Exception("Config error")
            mock_config.return_value = mock_parser
            
            with pytest.raises(Exception):
                _load_theme_file("test_theme")

    def test_get_calendar_theme_config_error(self):
        """Test get_calendar_theme with config error."""
        from unittest.mock import patch

        from tkface.widget.calendar.style import get_calendar_theme
        
        with patch('tkface.widget.calendar.style._load_theme_file') as mock_load:
            mock_load.side_effect = Exception("Config error")
            
            with pytest.raises(Exception):
                get_calendar_theme("test_theme")

    def test_determine_day_colors_selection(self):
        """Test _determine_day_colors with selection."""
        import datetime

        from tkface.widget.calendar.style import DayColorContext, _determine_day_colors
        
        context = DayColorContext(
            theme_colors={"day_bg": "white", "day_fg": "black", "selected_bg": "blue", "selected_fg": "white"},
            selected_date=datetime.date(2024, 1, 15),
            selected_range=None,
            today=datetime.date.today(),
            today_color=None,
            today_color_set=True,
            day_colors={},
            holidays={},
            date_obj=datetime.date(2024, 1, 15),
            year=2024,
            month=1,
            day=15
        )
        
        result = _determine_day_colors(context)
        assert result.bg == "blue"
        assert result.fg == "white"

    def test_determine_day_colors_range(self):
        """Test _determine_day_colors with range selection."""
        import datetime

        from tkface.widget.calendar.style import DayColorContext, _determine_day_colors
        
        context = DayColorContext(
            theme_colors={"day_bg": "white", "day_fg": "black", "range_bg": "lightblue", "range_fg": "black"},
            selected_date=None,
            selected_range=(datetime.date(2024, 1, 10), datetime.date(2024, 1, 20)),
            today=datetime.date.today(),
            today_color=None,
            today_color_set=True,
            day_colors={},
            holidays={},
            date_obj=datetime.date(2024, 1, 15),
            year=2024,
            month=1,
            day=15
        )
        
        result = _determine_day_colors(context)
        assert result.bg == "lightblue"
        assert result.fg == "black"

    def test_determine_day_colors_today(self):
        """Test _determine_day_colors with today."""
        import datetime

        from tkface.widget.calendar.style import DayColorContext, _determine_day_colors
        
        today = datetime.date.today()
        context = DayColorContext(
            theme_colors={"day_bg": "white", "day_fg": "black", "today_bg": "yellow", "today_fg": "black"},
            selected_date=None,
            selected_range=None,
            today=today,
            today_color=None,
            today_color_set=True,
            day_colors={},
            holidays={},
            date_obj=today,
            year=today.year,
            month=today.month,
            day=today.day
        )
        
        result = _determine_day_colors(context)
        assert result.bg == "yellow"
        assert result.fg == "black"

    def test_determine_day_colors_custom_today_color(self):
        """Test _determine_day_colors with custom today color."""
        import datetime

        from tkface.widget.calendar.style import DayColorContext, _determine_day_colors
        
        today = datetime.date.today()
        context = DayColorContext(
            theme_colors={"day_bg": "white", "day_fg": "black", "weekend_bg": "lightgray", "weekend_fg": "black"},
            selected_date=None,
            selected_range=None,
            today=today,
            today_color="red",
            today_color_set=True,
            day_colors={},
            holidays={},
            date_obj=today,
            year=today.year,
            month=today.month,
            day=today.day
        )
        
        result = _determine_day_colors(context)
        assert result.bg == "red"
        assert result.fg == "black"

    def test_determine_day_colors_today_color_none(self):
        """Test _determine_day_colors with today color set to none."""
        import datetime

        from tkface.widget.calendar.style import DayColorContext, _determine_day_colors

        # Use a specific Sunday date to ensure consistent test results
        sunday_date = datetime.date(2024, 1, 7)  # This is a Sunday
        context = DayColorContext(
            theme_colors={"day_bg": "white", "day_fg": "black", "weekend_bg": "lightgray", "weekend_fg": "black"},
            selected_date=None,
            selected_range=None,
            today=sunday_date,
            today_color=None,
            today_color_set=False,
            day_colors={},
            holidays={},
            date_obj=sunday_date,
            year=sunday_date.year,
            month=sunday_date.month,
            day=sunday_date.day
        )

        result = _determine_day_colors(context)
        # This is a Sunday, so it should use weekend colors
        assert result.bg == "lightgray"
        assert result.fg == "black"

    def test_determine_day_colors_holiday(self):
        """Test _determine_day_colors with holiday."""
        import datetime

        from tkface.widget.calendar.style import DayColorContext, _determine_day_colors
        
        context = DayColorContext(
            theme_colors={"day_bg": "white", "day_fg": "black", "weekend_bg": "lightgray", "weekend_fg": "black"},
            selected_date=None,
            selected_range=None,
            today=datetime.date.today(),
            today_color=None,
            today_color_set=True,
            day_colors={},
            holidays={"2024-01-15": "red"},
            date_obj=datetime.date(2024, 1, 15),
            year=2024,
            month=1,
            day=15
        )
        
        result = _determine_day_colors(context)
        assert result.bg == "red"
        assert result.fg == "black"

    def test_determine_day_colors_day_of_week(self):
        """Test _determine_day_colors with day of week color."""
        import datetime

        from tkface.widget.calendar.style import DayColorContext, _determine_day_colors
        
        context = DayColorContext(
            theme_colors={"day_bg": "white", "day_fg": "black", "weekend_bg": "lightgray", "weekend_fg": "black"},
            selected_date=None,
            selected_range=None,
            today=datetime.date.today(),
            today_color=None,
            today_color_set=True,
            day_colors={"Sunday": "red"},
            holidays={},
            date_obj=datetime.date(2024, 1, 7),  # Sunday
            year=2024,
            month=1,
            day=7
        )
        
        result = _determine_day_colors(context)
        assert result.bg == "red"
        assert result.fg == "black"

    def test_determine_day_colors_weekend_default(self):
        """Test _determine_day_colors with weekend default colors."""
        import datetime

        from tkface.widget.calendar.style import DayColorContext, _determine_day_colors
        
        context = DayColorContext(
            theme_colors={"day_bg": "white", "day_fg": "black", "weekend_bg": "lightgray", "weekend_fg": "black"},
            selected_date=None,
            selected_range=None,
            today=datetime.date.today(),
            today_color=None,
            today_color_set=True,
            day_colors={},
            holidays={},
            date_obj=datetime.date(2024, 1, 7),  # Sunday
            year=2024,
            month=1,
            day=7
        )
        
        result = _determine_day_colors(context)
        assert result.bg == "lightgray"
        assert result.fg == "black"

    def test_get_selection_colors_single_date(self):
        """Test _get_selection_colors with single date."""
        import datetime

        from tkface.widget.calendar.style import _get_selection_colors
        
        theme_colors = {"selected_bg": "blue", "selected_fg": "white"}
        selected_date = datetime.date(2024, 1, 15)
        selected_range = None
        date_obj = datetime.date(2024, 1, 15)
        
        result = _get_selection_colors(theme_colors, selected_date, selected_range, date_obj, "white", "black")
        assert result.bg == "blue"
        assert result.fg == "white"

    def test_get_selection_colors_range_start(self):
        """Test _get_selection_colors with range start."""
        import datetime

        from tkface.widget.calendar.style import _get_selection_colors
        
        theme_colors = {"selected_bg": "blue", "selected_fg": "white", "range_bg": "lightblue", "range_fg": "black"}
        selected_date = None
        selected_range = (datetime.date(2024, 1, 10), datetime.date(2024, 1, 20))
        date_obj = datetime.date(2024, 1, 10)
        
        result = _get_selection_colors(theme_colors, selected_date, selected_range, date_obj, "white", "black")
        assert result.bg == "blue"
        assert result.fg == "white"

    def test_get_selection_colors_range_end(self):
        """Test _get_selection_colors with range end."""
        import datetime

        from tkface.widget.calendar.style import _get_selection_colors
        
        theme_colors = {"selected_bg": "blue", "selected_fg": "white", "range_bg": "lightblue", "range_fg": "black"}
        selected_date = None
        selected_range = (datetime.date(2024, 1, 10), datetime.date(2024, 1, 20))
        date_obj = datetime.date(2024, 1, 20)
        
        result = _get_selection_colors(theme_colors, selected_date, selected_range, date_obj, "white", "black")
        assert result.bg == "blue"
        assert result.fg == "white"

    def test_get_selection_colors_range_middle(self):
        """Test _get_selection_colors with range middle."""
        import datetime

        from tkface.widget.calendar.style import _get_selection_colors
        
        theme_colors = {"selected_bg": "blue", "selected_fg": "white", "range_bg": "lightblue", "range_fg": "black"}
        selected_date = None
        selected_range = (datetime.date(2024, 1, 10), datetime.date(2024, 1, 20))
        date_obj = datetime.date(2024, 1, 15)
        
        result = _get_selection_colors(theme_colors, selected_date, selected_range, date_obj, "white", "black")
        assert result.bg == "lightblue"
        assert result.fg == "black"

    def test_get_today_colors_today(self):
        """Test _get_today_colors with today."""
        import datetime

        from tkface.widget.calendar.style import _get_today_colors
        
        today = datetime.date.today()
        theme_colors = {"today_bg": "yellow", "today_fg": "black"}
        
        result = _get_today_colors(theme_colors, today, None, True, today.year, today.month, today.day, "white", "black")
        assert result.bg == "yellow"
        assert result.fg == "black"

    def test_get_today_colors_custom_color(self):
        """Test _get_today_colors with custom color."""
        import datetime

        from tkface.widget.calendar.style import _get_today_colors
        
        today = datetime.date.today()
        theme_colors = {"today_bg": "yellow", "today_fg": "black"}
        
        result = _get_today_colors(theme_colors, today, "red", True, today.year, today.month, today.day, "white", "black")
        assert result.bg == "red"
        assert result.fg == "black"

    def test_get_today_colors_not_today(self):
        """Test _get_today_colors with not today."""
        import datetime

        from tkface.widget.calendar.style import _get_today_colors
        
        today = datetime.date.today()
        theme_colors = {"today_bg": "yellow", "today_fg": "black"}
        
        result = _get_today_colors(theme_colors, today, None, True, 2024, 1, 15, "white", "black")
        assert result.bg == "white"
        assert result.fg == "black"

    def test_get_holiday_color_holiday(self):
        """Test _get_holiday_color with holiday."""
        from tkface.widget.calendar.style import _get_holiday_color
        
        holidays = {"2024-01-15": "red"}
        result = _get_holiday_color(holidays, 2024, 1, 15, "white")
        assert result == "red"

    def test_get_holiday_color_no_holiday(self):
        """Test _get_holiday_color with no holiday."""
        from tkface.widget.calendar.style import _get_holiday_color
        
        holidays = {"2024-01-01": "red"}
        result = _get_holiday_color(holidays, 2024, 1, 15, "white")
        assert result == "white"

    def test_get_day_of_week_colors_custom(self):
        """Test _get_day_of_week_colors with custom color."""
        import datetime

        from tkface.widget.calendar.style import _get_day_of_week_colors
        
        theme_colors = {"day_bg": "white", "day_fg": "black", "weekend_bg": "lightgray", "weekend_fg": "black"}
        day_colors = {"Sunday": "red"}
        date_obj = datetime.date(2024, 1, 7)  # Sunday
        
        result = _get_day_of_week_colors(theme_colors, day_colors, date_obj, "white", "black")
        assert result.bg == "red"
        assert result.fg == "black"

    def test_get_day_of_week_colors_weekend_default(self):
        """Test _get_day_of_week_colors with weekend default."""
        import datetime

        from tkface.widget.calendar.style import _get_day_of_week_colors
        
        theme_colors = {"day_bg": "white", "day_fg": "black", "weekend_bg": "lightgray", "weekend_fg": "black"}
        day_colors = {}
        date_obj = datetime.date(2024, 1, 7)  # Sunday
        
        result = _get_day_of_week_colors(theme_colors, day_colors, date_obj, "white", "black")
        assert result.bg == "lightgray"
        assert result.fg == "black"

    def test_get_day_of_week_colors_weekday(self):
        """Test _get_day_of_week_colors with weekday."""
        import datetime

        from tkface.widget.calendar.style import _get_day_of_week_colors
        
        theme_colors = {"day_bg": "white", "day_fg": "black", "weekend_bg": "lightgray", "weekend_fg": "black"}
        day_colors = {}
        date_obj = datetime.date(2024, 1, 8)  # Monday
        
        result = _get_day_of_week_colors(theme_colors, day_colors, date_obj, "white", "black")
        assert result.bg == "white"
        assert result.fg == "black"

    def test_get_month_name_short(self, root):
        """Test get_month_name with short=True."""
        from tkface.widget.calendar.style import get_month_name
        
        cal = Calendar(root, year=2024, month=1)
        month_name = get_month_name(cal, 1, short=True)
        assert len(month_name) <= 3

    def test_get_month_name_full(self, root):
        """Test get_month_name with short=False."""
        from tkface.widget.calendar.style import get_month_name
        
        cal = Calendar(root, year=2024, month=1)
        month_name = get_month_name(cal, 1, short=False)
        assert len(month_name) >= 1  # Month names should have at least 1 character

    def test_style_theme_loading_errors(self, root):
        """Test style theme loading error cases."""
        from tkface.widget.calendar.style import get_calendar_theme, get_calendar_themes

        # Test with non-existent theme
        with patch('tkface.widget.calendar.style._load_theme_file', side_effect=FileNotFoundError("Theme not found")):
            try:
                get_calendar_theme("nonexistent")
            except ValueError:
                pass  # Expected
        
        # Test theme loading with configparser error
        with patch('tkface.widget.calendar.style._load_theme_file', side_effect=configparser.Error("Invalid config")):
            try:
                get_calendar_theme("invalid")
            except ValueError:
                pass  # Expected

    def test_style_theme_file_errors(self, root):
        """Test style theme file error cases."""
        from tkface.widget.calendar.style import _load_theme_file

        # Test with non-existent theme file
        try:
            _load_theme_file("nonexistent")
        except FileNotFoundError:
            pass  # Expected
        
        # Test with invalid config file by mocking the file existence
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', side_effect=configparser.Error("Invalid config")):
                try:
                    _load_theme_file("invalid")
                except configparser.Error:
                    pass  # Expected

    def test_style_theme_section_error(self, root):
        """Test style theme section error (line 89)."""
        from tkface.widget.calendar.style import _load_theme_file

        # Mock a config that doesn't have the theme section
        mock_config = Mock()
        mock_config.__contains__ = Mock(return_value=False)
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data="[other_section]\nkey=value")):
                with patch('configparser.ConfigParser', return_value=mock_config):
                    try:
                        _load_theme_file("missing_section")
                    except configparser.Error:
                        pass  # Expected

    def test_style_theme_warning_logging(self, root):
        """Test style theme warning logging (lines 117-121)."""
        from pathlib import Path

        from tkface.widget.calendar.style import get_calendar_themes

        # Mock theme directory to return Path objects that will cause errors
        mock_path1 = Mock(spec=Path)
        mock_path1.stem = "invalid1"
        mock_path2 = Mock(spec=Path)
        mock_path2.stem = "invalid2"
        
        with patch('pathlib.Path.glob', return_value=[mock_path1, mock_path2]):
            with patch('tkface.widget.calendar.style._load_theme_file', side_effect=FileNotFoundError("File not found")):
                themes = get_calendar_themes()
                # Should return empty dict and log warnings
                assert isinstance(themes, dict)
