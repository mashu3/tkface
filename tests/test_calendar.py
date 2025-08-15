# pylint: disable=import-outside-toplevel,protected-access
"""
Tests for tkface Calendar and DatePicker widgets
"""

import datetime
import tkinter as tk

import pytest

from tkface import Calendar, DateEntry, DateFrame, lang


class TestCalendarBasic:
    """Basic test cases for Calendar widget creation and configuration."""

    @pytest.fixture
    def calendar_widget(self, root):
        """Create a Calendar widget for testing."""
        return Calendar(root, year=2024, month=1)

    def test_calendar_creation(self, root):
        """Test basic calendar creation."""
        cal = Calendar(root)
        assert cal is not None
        assert cal.year == datetime.date.today().year
        assert cal.month == datetime.date.today().month

    def test_calendar_with_specific_date(self, root):
        """Test calendar creation with specific year and month."""
        cal = Calendar(root, year=2024, month=3)
        assert cal.year == 2024
        assert cal.month == 3

    def test_multiple_months(self, root):
        """Test multiple months display."""
        cal = Calendar(root, year=2024, month=1, months=3)
        assert cal.months == 3
        assert len(cal.month_frames) == 3

    def test_week_numbers(self, root):
        """Test week numbers display."""
        cal = Calendar(root, year=2024, month=1, show_week_numbers=True)
        assert cal.show_week_numbers is True
        assert len(cal.week_labels) > 0

    def test_week_start_sunday(self, root):
        """Test week start with Sunday."""
        cal = Calendar(root, year=2024, month=1, week_start="Sunday")
        assert cal.week_start == "Sunday"
        assert cal.cal.getfirstweekday() == 6  # calendar.SUNDAY

    def test_week_start_monday(self, root):
        """Test week start with Monday."""
        cal = Calendar(root, year=2024, month=1, week_start="Monday")
        assert cal.week_start == "Monday"
        assert cal.cal.getfirstweekday() == 0  # calendar.MONDAY

    def test_week_start_saturday(self, root):
        """Test week start with Saturday."""
        cal = Calendar(root, year=2024, month=1, week_start="Saturday")
        assert cal.week_start == "Saturday"
        assert cal.cal.getfirstweekday() == 5  # calendar.SATURDAY

    def test_invalid_week_start(self, root):
        """Test invalid week start raises error."""
        with pytest.raises(ValueError):
            Calendar(root, year=2024, month=1, week_start="Tuesday")

    def test_holidays(self, root):
        """Test holiday highlighting."""
        holidays = {"2024-01-01": "red", "2024-01-15": "blue"}
        cal = Calendar(root, year=2024, month=1, holidays=holidays)
        assert cal.holidays == holidays

    def test_day_colors(self, root):
        """Test day of week colors."""
        day_colors = {"Sunday": "red", "Saturday": "blue"}
        cal = Calendar(root, year=2024, month=1, day_colors=day_colors)
        assert cal.day_colors == day_colors


class TestCalendarConfiguration:
    """Test cases for Calendar widget configuration changes."""

    @pytest.fixture
    def calendar_widget(self, root):
        """Create a Calendar widget for testing."""
        return Calendar(root, year=2024, month=1)

    def test_set_date(self, calendar_widget):
        """Test setting date."""
        calendar_widget.set_date(2025, 6)
        assert calendar_widget.year == 2025
        assert calendar_widget.month == 6

    def test_set_holidays(self, calendar_widget):
        """Test setting holidays."""
        new_holidays = {"2024-02-14": "pink"}
        calendar_widget.set_holidays(new_holidays)
        assert calendar_widget.holidays == new_holidays

    def test_set_day_colors(self, calendar_widget):
        """Test setting day colors."""
        new_colors = {"Friday": "green"}
        calendar_widget.set_day_colors(new_colors)
        assert calendar_widget.day_colors == new_colors

    def test_set_week_start(self, calendar_widget):
        """Test changing week start."""
        calendar_widget.set_week_start("Monday")
        assert calendar_widget.week_start == "Monday"
        assert calendar_widget.cal.getfirstweekday() == 0
        calendar_widget.set_week_start("Saturday")
        assert calendar_widget.week_start == "Saturday"
        assert calendar_widget.cal.getfirstweekday() == 5

    def test_set_show_week_numbers(self, calendar_widget):
        """Test toggling week numbers."""
        calendar_widget.set_show_week_numbers(True)
        assert calendar_widget.show_week_numbers is True

    def test_get_day_names_sunday_start(self, root):
        """Test day names with Sunday start."""
        cal = Calendar(root, year=2024, month=1, week_start="Sunday")
        day_names = cal._get_day_names()
        assert len(day_names) == 7
        assert day_names[0] == "Sunday" or day_names[0] == "日"

    def test_get_day_names_monday_start(self, root):
        """Test day names with Monday start."""
        cal = Calendar(root, year=2024, month=1, week_start="Monday")
        day_names = cal._get_day_names()
        assert len(day_names) == 7
        assert day_names[0] == "Monday" or day_names[0] == "月"

    def test_get_day_names_saturday_start(self, root):
        """Test day names with Saturday start."""
        cal = Calendar(root, year=2024, month=1, week_start="Saturday")
        day_names = cal._get_day_names()
        assert len(day_names) == 7
        assert day_names[0] == "Saturday" or day_names[0] == "土"

    def test_get_month_name(self, root):
        """Test month name retrieval."""
        cal = Calendar(root, year=2024, month=1)
        month_name = cal._get_month_name(1)
        assert month_name in ("January", "1月")
        month_name = cal._get_month_name(12)
        assert month_name in ("December", "12月")

    def test_month_overflow(self, root):
        """Test month overflow handling."""
        cal = Calendar(root, year=2024, month=12)
        # Test that setting month 13 raises an error (not handled automatically)
        with pytest.raises(ValueError):
            cal.set_date(2024, 13)

    def test_year_overflow(self, root):
        """Test year overflow handling."""
        cal = Calendar(root, year=2024, month=1)
        # Test that setting month 0 raises an error (not handled automatically)
        with pytest.raises(ValueError):
            cal.set_date(2024, 0)

    def test_placeholder_methods(self, calendar_widget):
        """Test placeholder methods that should not raise errors."""
        # These methods exist but may not be fully implemented
        calendar_widget.refresh_language()
        calendar_widget.set_today_color("red")
        calendar_widget.set_theme("dark")

    def test_settings_preserved_on_week_start_change(self, calendar_widget):
        """Test that settings are preserved when week start changes."""
        # Set some custom settings
        calendar_widget.set_day_colors({"Friday": "green"})
        calendar_widget.set_holidays({"2024-01-01": "red"})
        # Change week start
        calendar_widget.set_week_start("Monday")
        # Settings should be preserved
        assert calendar_widget.day_colors == {"Friday": "green"}
        assert calendar_widget.holidays == {"2024-01-01": "red"}

    def test_settings_preserved_on_week_numbers_change(self, calendar_widget):
        """Test that settings are preserved when week numbers change."""
        # Set some custom settings
        calendar_widget.set_day_colors({"Friday": "green"})
        calendar_widget.set_holidays({"2024-01-01": "red"})
        # Change week numbers
        calendar_widget.set_show_week_numbers(True)
        # Settings should be preserved
        assert calendar_widget.day_colors == {"Friday": "green"}
        assert calendar_widget.holidays == {"2024-01-01": "red"}


class TestCalendarDisplay:
    """Test cases for Calendar widget display functionality."""

    def test_day_header_width_prevents_overlap(self, root):
        """Test that day headers have sufficient width to prevent overlap."""
        cal = Calendar(root, year=2024, month=1)
        # Get the days frame
        month_frame = cal.month_frames[0]
        days_frame = month_frame.winfo_children()[1]
        # Check each day header has reasonable width
        for child in days_frame.winfo_children():
            if isinstance(child, tk.Label):
                width = child.winfo_reqwidth()
                assert width > 0, f"Day header has zero width: {child.cget('text')}"

    def test_day_names_update_on_language_change(self, root):
        """Test that day names update when language changes."""
        cal = Calendar(root, year=2024, month=1)
        # Get initial day names in English
        lang.set("en", root)
        cal._update_display()
        # Get the days frame
        month_frame = cal.month_frames[0]
        days_frame = month_frame.winfo_children()[1]
        # Get English day names (only header row)
        english_names = []
        for child in days_frame.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") not in [
                lang.get("Week")
            ]:
                # Only get first 7 labels (header row)
                if len(english_names) < 7:
                    english_names.append(child.cget("text"))
        # Change to Japanese
        lang.set("ja", root)
        cal._update_display()
        # Get Japanese day names (only header row)
        japanese_names = []
        for child in days_frame.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") not in [
                lang.get("Week")
            ]:
                # Only get first 7 labels (header row)
                if len(japanese_names) < 7:
                    japanese_names.append(child.cget("text"))
        # Names should be different
        assert english_names != japanese_names, "Day names should change with language"
        assert len(english_names) == len(
            japanese_names
        ), "Should have same number of day names"

    def test_day_names_update_on_week_start_change(self, root):
        """Test that day names update when week start changes."""
        cal = Calendar(root, year=2024, month=1, week_start="Sunday")
        # Get initial day names with Sunday start
        cal._update_display()
        # Get the days frame
        month_frame = cal.month_frames[0]
        days_frame = month_frame.winfo_children()[1]
        # Get Sunday-start day names (only header row)
        sunday_names = []
        for child in days_frame.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") not in [
                lang.get("Week")
            ]:
                # Only get first 7 labels (header row)
                if len(sunday_names) < 7:
                    sunday_names.append(child.cget("text"))
        # Change to Monday start
        cal.set_week_start("Monday")
        # Get the new days frame (widgets were recreated)
        month_frame = cal.month_frames[0]
        days_frame = month_frame.winfo_children()[1]
        # Get Monday-start day names (only header row)
        monday_names = []
        for child in days_frame.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") not in [
                lang.get("Week")
            ]:
                # Only get first 7 labels (header row)
                if len(monday_names) < 7:
                    monday_names.append(child.cget("text"))
        # First day should be different
        assert (
            sunday_names[0] != monday_names[0]
        ), "First day should change with week start"
        assert (
            sunday_names[-1] != monday_names[-1]
        ), "Last day should change with week start"

    def test_initial_language_setting(self, root):
        """Test that initial language setting is correctly applied."""
        # Set language before creating calendar
        lang.set("ja", root)
        # Create calendar
        cal = Calendar(root, year=2024, month=1)
        # Get the days frame
        month_frame = cal.month_frames[0]
        days_frame = month_frame.winfo_children()[1]
        # Get day names (only header row)
        day_names = []
        for child in days_frame.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") not in [
                lang.get("Week")
            ]:
                # Only get first 7 labels (header row)
                if len(day_names) < 7:
                    day_names.append(child.cget("text"))
        # Should be in Japanese
        assert len(day_names) == 7, "Should have 7 day names"

    def test_initial_language_setting_english(self, root):
        """Test that initial language setting works for English."""
        # Set language before creating calendar
        lang.set("en", root)
        # Create calendar
        cal = Calendar(root, year=2024, month=1)
        # Get the days frame
        month_frame = cal.month_frames[0]
        days_frame = month_frame.winfo_children()[1]
        # Get day names (only header row)
        day_names = []
        for child in days_frame.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") not in [
                lang.get("Week")
            ]:
                # Only get first 7 labels (header row)
                if len(day_names) < 7:
                    day_names.append(child.cget("text"))
        # Should be in English
        assert len(day_names) == 7, "Should have 7 day names"

    def test_set_months(self, root):
        """Test setting number of months."""
        cal = Calendar(root, year=2024, month=1, months=1)
        cal.set_months(3)
        assert cal.months == 3
        assert len(cal.month_frames) == 3

    def test_set_months_preserves_settings(self, root):
        """Test that settings are preserved when changing months."""
        cal = Calendar(root, year=2024, month=1, months=1)
        # Set some custom settings
        cal.set_day_colors({"Friday": "green"})
        cal.set_holidays({"2024-01-01": "red"})
        # Change months
        cal.set_months(3)
        # Settings should be preserved
        assert cal.day_colors == {"Friday": "green"}
        assert cal.holidays == {"2024-01-01": "red"}

    def test_set_months_invalid_value(self, root):
        """Test that invalid months value raises error."""
        cal = Calendar(root, year=2024, month=1)
        with pytest.raises(ValueError):
            cal.set_months(0)

    def test_grid_layout_auto_calculation(self, root):
        """Test automatic grid layout calculation."""
        # Test 1 month
        cal = Calendar(root, year=2024, month=1, months=1)
        assert cal.grid_rows == 1
        assert cal.grid_cols == 1
        # Test 3 months
        cal = Calendar(root, year=2024, month=1, months=3)
        assert cal.grid_rows == 1
        assert cal.grid_cols == 3
        # Test 6 months
        cal = Calendar(root, year=2024, month=1, months=6)
        assert cal.grid_rows == 2
        assert cal.grid_cols == 3

    def test_custom_grid_layout(self, root):
        """Test custom grid layout."""
        cal = Calendar(root, year=2024, month=1, months=4, grid_layout=(2, 2))
        assert cal.grid_rows == 2
        assert cal.grid_cols == 2

    def test_scrollable_container(self, root):
        """Test scrollable container for multiple months."""
        cal = Calendar(root, year=2024, month=1, months=12)
        # Should have canvas and scrollbar for many months
        assert hasattr(cal, "canvas")
        assert hasattr(cal, "scrollbar")

    def test_adjacent_month_days_display(self, root):
        """Test that adjacent month days are displayed correctly."""
        cal = Calendar(root, year=2024, month=1)
        # January 2024 starts on Monday, so we should see some December 2023 days
        # and some February 2024 days
        day_labels = [label for _, _, _, label in cal.day_labels]
        # Should have some days from adjacent months
        assert len(day_labels) > 28  # More than just January days

    def test_month_headers_toggle(self, root):
        """Test month headers toggle functionality."""
        cal = Calendar(root, year=2024, month=1, months=3, show_month_headers=True)
        # Should have month headers
        assert cal.show_month_headers is True
        # Test disabling headers
        cal = Calendar(root, year=2024, month=1, months=3, show_month_headers=False)
        assert cal.show_month_headers is False


class TestCalendarSelection:
    """Test cases for Calendar widget date selection functionality."""

    def test_single_date_selection(self, root):
        """Test single date selection."""
        cal = Calendar(root, year=2024, month=1, selectmode="single")
        # Simulate clicking on January 15, 2024 (week 2, day 1)
        cal._on_date_click(0, 2, 1)  # month_index=0, week=2, day=1
        assert cal.selected_date == datetime.date(2024, 1, 15)
        assert cal.selected_range is None

    def test_range_date_selection(self, root):
        """Test range date selection."""
        cal = Calendar(root, year=2024, month=1, selectmode="range")
        # Simulate clicking on start date (January 10, 2024)
        cal._on_date_click(0, 1, 3)  # month_index=0, week=1, day=3
        # Simulate clicking on end date (January 15, 2024)
        cal._on_date_click(0, 2, 1)  # month_index=0, week=2, day=1
        assert cal.selected_range is not None
        assert cal.selected_range[0] == datetime.date(2024, 1, 10)
        assert cal.selected_range[1] == datetime.date(2024, 1, 15)

    def test_selection_callback(self, root):
        """Test selection callback functionality."""
        callback_called = False
        callback_value = None

        def selection_callback(value):
            nonlocal callback_called, callback_value
            callback_called = True
            callback_value = value

        cal = Calendar(root, year=2024, month=1, selectmode="single")
        cal.selection_callback = selection_callback
        # Simulate clicking on a date (January 15, 2024)
        cal._on_date_click(0, 2, 1)  # month_index=0, week=2, day=1
        assert callback_called
        assert callback_value == datetime.date(2024, 1, 15)


class TestDateFrameBasic:
    """Basic test cases for DateFrame widget creation and configuration."""

    @pytest.fixture
    def dateframe_widget(self, root):
        """Create a DateFrame widget for testing."""
        return DateFrame(root)

    def test_dateframe_creation(self, root):
        """Test basic DateFrame creation."""
        df = DateFrame(root)
        assert df is not None
        assert hasattr(df, "entry")
        assert hasattr(df, "button")

    def test_dateframe_with_custom_button_text(self, root):
        """Test DateFrame with custom button text."""
        df = DateFrame(root, button_text="📆")
        assert df.button.cget("text") == "📆"

    def test_dateframe_set_button_text(self, root):
        """Test DateFrame set_button_text method."""
        df = DateFrame(root)
        df.set_button_text("📅")
        assert df.button.cget("text") == "📅"

    def test_dateframe_with_custom_format(self, root):
        """Test DateFrame with custom date format."""
        df = DateFrame(root, date_format="%d/%m/%Y")
        assert df.date_format == "%d/%m/%Y"

    def test_dateframe_with_specific_date(self, root):
        """Test DateFrame with specific year and month."""
        df = DateFrame(root, year=2024, month=3)
        assert df.calendar_config["year"] == 2024
        assert df.calendar_config["month"] == 3

    def test_dateframe_with_theme(self, root):
        """Test DateFrame with theme setting."""
        df = DateFrame(root, theme="dark")
        assert df.calendar_config["theme"] == "dark"

    def test_dateframe_with_language(self, root):
        """Test DateFrame with language setting."""
        df = DateFrame(root, language="ja")
        # Language is passed to Calendar widget, not stored in calendar_config
        # Just verify the widget was created successfully
        assert df is not None

    def test_dateframe_with_today_color(self, root):
        """Test DateFrame with today color setting."""
        df = DateFrame(root, today_color="red")
        assert df.today_color == "red"

    def test_dateframe_with_day_colors(self, root):
        """Test DateFrame with day colors setting."""
        day_colors = {"Sunday": "red", "Saturday": "blue"}
        df = DateFrame(root, day_colors=day_colors)
        assert df.calendar_config["day_colors"] == day_colors

    def test_dateframe_with_holidays(self, root):
        """Test DateFrame with holidays setting."""
        holidays = {"2024-01-01": "red", "2024-01-15": "blue"}
        df = DateFrame(root, holidays=holidays)
        assert df.calendar_config["holidays"] == holidays

    def test_dateframe_with_week_start(self, root):
        """Test DateFrame with week start setting."""
        df = DateFrame(root, week_start="Monday")
        assert df.calendar_config["week_start"] == "Monday"
        df = DateFrame(root, week_start="Saturday")
        assert df.calendar_config["week_start"] == "Saturday"

    def test_dateframe_with_show_week_numbers(self, root):
        """Test DateFrame with week numbers setting."""
        df = DateFrame(root, show_week_numbers=True)
        assert df.calendar_config["show_week_numbers"] is True

    def test_dateframe_with_selectmode(self, root):
        """Test DateFrame with select mode setting."""
        df = DateFrame(root, selectmode="range")
        assert df.calendar_config["selectmode"] == "range"


class TestDateFrameConfiguration:
    """Test cases for DateFrame widget configuration changes."""

    @pytest.fixture
    def dateframe_widget(self, root):
        """Create a DateFrame widget for testing."""
        return DateFrame(root)

    def test_set_today_color(self, dateframe_widget):
        """Test set_today_color method."""
        dateframe_widget.set_today_color("red")
        assert dateframe_widget.today_color == "red"

    def test_set_theme(self, dateframe_widget):
        """Test set_theme method."""
        dateframe_widget.set_theme("dark")
        assert dateframe_widget.calendar_config["theme"] == "dark"

    def test_set_day_colors(self, dateframe_widget):
        """Test set_day_colors method."""
        day_colors = {"Friday": "green"}
        dateframe_widget.set_day_colors(day_colors)
        assert dateframe_widget.calendar_config["day_colors"] == day_colors

    def test_set_week_start(self, dateframe_widget):
        """Test set_week_start method."""
        dateframe_widget.set_week_start("Monday")
        assert dateframe_widget.calendar_config["week_start"] == "Monday"
        dateframe_widget.set_week_start("Saturday")
        assert dateframe_widget.calendar_config["week_start"] == "Saturday"

    def test_set_show_week_numbers(self, dateframe_widget):
        """Test set_show_week_numbers method."""
        dateframe_widget.set_show_week_numbers(True)
        assert dateframe_widget.calendar_config["show_week_numbers"] is True


class TestDateFrameFunctionality:
    """Test cases for DateFrame widget functionality."""

    @pytest.fixture
    def dateframe_widget(self, root):
        """Create a DateFrame widget for testing."""
        return DateFrame(root)

    def test_get_date_none(self, dateframe_widget):
        """Test get_date returns None when no date is selected."""
        assert dateframe_widget.get_date() is None

    def test_get_date_string_none(self, dateframe_widget):
        """Test get_date_string returns empty string when no date is "
        "selected."""
        assert dateframe_widget.get_date_string() == ""

    def test_set_date(self, dateframe_widget):
        """Test setting date."""
        test_date = datetime.date(2024, 3, 15)
        dateframe_widget.set_selected_date(test_date)
        assert dateframe_widget.selected_date == test_date
        assert dateframe_widget.get_date_string() == "2024-03-15"

    def test_set_date_with_custom_format(self, root):
        """Test setting date with custom format."""
        df = DateFrame(root, date_format="%d/%m/%Y")
        test_date = datetime.date(2024, 3, 15)
        df.set_selected_date(test_date)
        assert df.get_date_string() == "15/03/2024"

    def test_date_callback(self, root):
        """Test date callback functionality."""
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

    def test_refresh_language(self, dateframe_widget):
        """Test refresh_language method."""
        # This should not raise an exception
        dateframe_widget.refresh_language()


class TestDateEntryBasic:
    """Basic test cases for DateEntry widget creation and configuration."""

    @pytest.fixture
    def dateentry_widget(self, root):
        """Create a DateEntry widget for testing."""
        return DateEntry(root)

    def test_dateentry_creation(self, root):
        """Test basic DateEntry creation."""
        de = DateEntry(root)
        assert de is not None
        assert de.date_format == "%Y-%m-%d"
        assert de.selected_date is None

    def test_dateentry_with_custom_format(self, root):
        """Test DateEntry with custom date format."""
        de = DateEntry(root, date_format="%d/%m/%Y")
        assert de.date_format == "%d/%m/%Y"

    def test_dateentry_with_specific_date(self, root):
        """Test DateEntry with specific year and month."""
        de = DateEntry(root, year=2024, month=3)
        assert de.calendar_config["year"] == 2024
        assert de.calendar_config["month"] == 3

    def test_dateentry_with_theme(self, root):
        """Test DateEntry with theme setting."""
        de = DateEntry(root, theme="dark")
        assert de.calendar_config["theme"] == "dark"

    def test_dateentry_with_language(self, root):
        """Test DateEntry with language setting."""
        DateEntry(root, language="ja")
        # Language should be set in the parent window
        assert True  # Just check that no error occurs

    def test_dateentry_with_today_color(self, root):
        """Test DateEntry with today color setting."""
        de = DateEntry(root, today_color="red")
        assert de.today_color == "red"

    def test_dateentry_with_day_colors(self, root):
        """Test DateEntry with day colors setting."""
        day_colors = {"Sunday": "red", "Saturday": "blue"}
        de = DateEntry(root, day_colors=day_colors)
        assert de.calendar_config["day_colors"] == day_colors

    def test_dateentry_with_holidays(self, root):
        """Test DateEntry with holidays setting."""
        holidays = {"2024-01-01": "red", "2024-01-15": "blue"}
        de = DateEntry(root, holidays=holidays)
        assert de.calendar_config["holidays"] == holidays

    def test_dateentry_with_week_start(self, root):
        """Test DateEntry with week start setting."""
        de = DateEntry(root, week_start="Monday")
        assert de.calendar_config["week_start"] == "Monday"
        de = DateEntry(root, week_start="Saturday")
        assert de.calendar_config["week_start"] == "Saturday"

    def test_dateentry_with_show_week_numbers(self, root):
        """Test DateEntry with week numbers setting."""
        de = DateEntry(root, show_week_numbers=True)
        assert de.calendar_config["show_week_numbers"] is True

    def test_dateentry_with_selectmode(self, root):
        """Test DateEntry with select mode setting."""
        de = DateEntry(root, selectmode="range")
        assert de.calendar_config["selectmode"] == "range"


class TestDateEntryConfiguration:
    """Test cases for DateEntry widget configuration changes."""

    @pytest.fixture
    def dateentry_widget(self, root):
        """Create a DateEntry widget for testing."""
        return DateEntry(root)

    def test_set_today_color(self, dateentry_widget):
        """Test setting today color."""
        dateentry_widget.set_today_color("red")
        assert dateentry_widget.today_color == "red"

    def test_set_theme(self, dateentry_widget):
        """Test setting theme."""
        dateentry_widget.set_theme("dark")
        assert dateentry_widget.calendar_config["theme"] == "dark"

    def test_set_day_colors(self, dateentry_widget):
        """Test setting day colors."""
        day_colors = {"Friday": "green"}
        dateentry_widget.set_day_colors(day_colors)
        assert dateentry_widget.calendar_config["day_colors"] == day_colors

    def test_set_week_start(self, dateentry_widget):
        """Test setting week start."""
        dateentry_widget.set_week_start("Monday")
        assert dateentry_widget.calendar_config["week_start"] == "Monday"
        dateentry_widget.set_week_start("Saturday")
        assert dateentry_widget.calendar_config["week_start"] == "Saturday"

    def test_set_show_week_numbers(self, dateentry_widget):
        """Test setting week numbers display."""
        dateentry_widget.set_show_week_numbers(True)
        assert dateentry_widget.calendar_config["show_week_numbers"] is True


class TestDateEntryFunctionality:
    """Test cases for DateEntry widget functionality."""

    @pytest.fixture
    def dateentry_widget(self, root):
        """Create a DateEntry widget for testing."""
        return DateEntry(root)

    def test_get_date_none(self, dateentry_widget):
        """Test getting date when none is selected."""
        assert dateentry_widget.get_date() is None

    def test_get_date_string_none(self, dateentry_widget):
        """Test getting date string when none is selected."""
        assert dateentry_widget.get_date_string() == ""

    def test_set_date(self, dateentry_widget):
        """Test setting a date."""
        test_date = datetime.date(2024, 3, 15)
        dateentry_widget.set_selected_date(test_date)
        assert dateentry_widget.selected_date == test_date
        assert dateentry_widget.get_date_string() == "2024-03-15"

    def test_set_date_with_custom_format(self, root):
        """Test setting a date with custom format."""
        de = DateEntry(root, date_format="%d/%m/%Y")
        test_date = datetime.date(2024, 3, 15)
        de.set_selected_date(test_date)
        assert de.get_date_string() == "15/03/2024"

    def test_date_callback(self, root):
        """Test date callback functionality."""
        callback_called = False
        callback_value = None

        def callback(date):
            nonlocal callback_called, callback_value
            callback_called = True
            callback_value = date

        de = DateEntry(root, date_callback=callback)
        test_date = datetime.date(2024, 3, 15)
        # Simulate date selection
        de._on_date_selected(test_date)
        assert callback_called
        assert callback_value == test_date

    def test_refresh_language(self, dateentry_widget):
        """Test language refresh functionality."""
        # Should not raise an error
        dateentry_widget.refresh_language()


class TestCalendarIntegration:
    """Integration tests for Calendar widget."""

    def test_language_switching(self, root):
        """Test calendar updates when language changes."""
        cal = Calendar(root, year=2024, month=1)
        # Test English
        lang.set("en", root)
        day_names_en = cal._get_day_names()
        month_name_en = cal._get_month_name(1)
        # Test Japanese
        lang.set("ja", root)
        day_names_ja = cal._get_day_names()
        month_name_ja = cal._get_month_name(1)
        # Names should be different
        assert day_names_en != day_names_ja
        assert month_name_en != month_name_ja

    def test_today_highlighting(self, root):
        """Test that today's date is highlighted."""
        today = datetime.date.today()
        cal = Calendar(root, year=today.year, month=today.month)
        # Find today's label and check if it's highlighted
        today_found = False
        for _, _, _, label in cal.day_labels:
            if label.cget("text") == str(today.day):
                # Check if it's highlighted (yellow or custom today color)
                bg_color = label.cget("bg")
                if bg_color in ["yellow", "#ffeb3b"]:  # Default today colors
                    today_found = True
                    break
        assert today_found, "Today's date should be highlighted"


def test_calendar_get_calendar_theme():
    """Test get_calendar_theme function."""
    from tkface.widget.calendar import get_calendar_theme

    # Test light theme
    light_theme = get_calendar_theme("light")
    assert "background" in light_theme
    assert "foreground" in light_theme
    # Test dark theme
    dark_theme = get_calendar_theme("dark")
    assert "background" in dark_theme
    assert "foreground" in dark_theme
    # Test invalid theme
    with pytest.raises(ValueError):
        get_calendar_theme("invalid_theme")


def test_dateframe_creation(root):
    """Test DateFrame widget creation."""
    df = DateFrame(root)
    assert df is not None


def test_dateframe_get_date_string(root):
    """Test DateFrame get_date_string method."""
    df = DateFrame(root)
    # Test with default format
    date_string = df.get_date_string()
    assert isinstance(date_string, str)


def test_dateframe_set_date_format(root):
    """Test DateFrame date_format property."""
    df = DateFrame(root)
    # Test setting custom format
    df.date_format = "%d/%m/%Y"
    assert df.date_format == "%d/%m/%Y"


def test_dateframe_set_selected_date(root):
    """Test DateFrame set_selected_date method."""
    df = DateFrame(root)
    # Test setting selected date
    test_date = datetime.date(2024, 3, 15)
    df.set_selected_date(test_date)
    assert df.selected_date == test_date


def test_dateframe_get_selected_date(root):
    """Test DateFrame selected_date property."""
    df = DateFrame(root)
    # Test getting selected date
    selected_date = df.selected_date
    assert selected_date is None  # No date selected initially


def test_dateframe_refresh_language(root):
    """Test DateFrame refresh_language method."""
    df = DateFrame(root)
    # Test language refresh (should not raise error)
    df.refresh_language()


def test_dateframe_set_today_color(root):
    """Test DateFrame set_today_color method."""
    df = DateFrame(root)
    # Test setting today color
    df.set_today_color("red")
    assert df.today_color == "red"


def test_dateframe_set_theme(root):
    """Test DateFrame set_theme method."""
    df = DateFrame(root)
    # Test setting theme
    df.set_theme("dark")
    assert df.calendar_config["theme"] == "dark"


def test_dateframe_set_day_colors(root):
    """Test DateFrame set_day_colors method."""
    df = DateFrame(root)
    # Test setting day colors
    day_colors = {"Friday": "green"}
    df.set_day_colors(day_colors)
    assert df.calendar_config["day_colors"] == day_colors


def test_dateframe_set_week_start(root):
    """Test DateFrame set_week_start method."""
    df = DateFrame(root)
    # Test setting week start
    df.set_week_start("Monday")
    assert df.calendar_config["week_start"] == "Monday"


def test_dateframe_set_show_week_numbers(root):
    """Test DateFrame set_show_week_numbers method."""
    df = DateFrame(root)
    # Test setting week numbers display
    df.set_show_week_numbers(True)
    assert df.calendar_config["show_week_numbers"] is True
