"""
Tests for tkface.calendar module
"""

import pytest
import tkinter as tk
import datetime
from tkface import calendar as tkface_calendar
from tkface import lang


class TestCalendar:
    """Test cases for Calendar widget."""
    
    @pytest.fixture
    def calendar_widget(self, root):
        """Create a Calendar widget for testing."""
        return tkface_calendar.Calendar(root, year=2024, month=1)
        
    def test_calendar_creation(self, root):
        """Test basic calendar creation."""
        cal = tkface_calendar.Calendar(root)
        assert cal is not None
        assert cal.year == datetime.date.today().year
        assert cal.month == datetime.date.today().month
        
    def test_calendar_with_specific_date(self, root):
        """Test calendar creation with specific year and month."""
        cal = tkface_calendar.Calendar(root, year=2024, month=3)
        assert cal.year == 2024
        assert cal.month == 3
        
    def test_multiple_months(self, root):
        """Test multiple months display."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1, months=3)
        assert cal.months == 3
        assert len(cal.month_frames) == 3
        
    def test_week_numbers(self, root):
        """Test week numbers display."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1, show_week_numbers=True)
        assert cal.show_week_numbers is True
        assert len(cal.week_labels) > 0
        
    def test_week_start_sunday(self, root):
        """Test week start with Sunday."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1, week_start="Sunday")
        assert cal.week_start == "Sunday"
        assert cal.cal.getfirstweekday() == 6  # calendar.SUNDAY
        
    def test_week_start_monday(self, root):
        """Test week start with Monday."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1, week_start="Monday")
        assert cal.week_start == "Monday"
        assert cal.cal.getfirstweekday() == 0  # calendar.MONDAY
        
    def test_invalid_week_start(self, root):
        """Test invalid week start raises error."""
        with pytest.raises(ValueError):
            tkface_calendar.Calendar(root, year=2024, month=1, week_start="Tuesday")
            
    def test_holidays(self, root):
        """Test holiday highlighting."""
        holidays = {"2024-01-01": "red", "2024-01-15": "blue"}
        cal = tkface_calendar.Calendar(root, year=2024, month=1, holidays=holidays)
        assert cal.holidays == holidays
        
    def test_day_colors(self, root):
        """Test day of week colors."""
        day_colors = {"Sunday": "red", "Saturday": "blue"}
        cal = tkface_calendar.Calendar(root, year=2024, month=1, day_colors=day_colors)
        assert cal.day_colors == day_colors
        
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
        
    def test_set_show_week_numbers(self, calendar_widget):
        """Test toggling week numbers."""
        calendar_widget.set_show_week_numbers(True)
        assert calendar_widget.show_week_numbers is True
        
    def test_get_day_names_sunday_start(self, root):
        """Test day names with Sunday start."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1, week_start="Sunday")
        day_names = cal._get_day_names()
        assert day_names[0] == lang.get("Sunday")
        assert day_names[6] == lang.get("Saturday")
        
    def test_get_day_names_monday_start(self, root):
        """Test day names with Monday start."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1, week_start="Monday")
        day_names = cal._get_day_names()
        assert day_names[0] == lang.get("Monday")
        assert day_names[6] == lang.get("Sunday")
        
    def test_get_month_name(self, root):
        """Test month name localization."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1)
        assert cal._get_month_name(1) == lang.get("January")
        assert cal._get_month_name(12) == lang.get("December")
        
    def test_month_overflow(self, root):
        """Test month overflow handling."""
        cal = tkface_calendar.Calendar(root, year=2024, month=12, months=2)
        # Should handle December + January correctly
        assert len(cal.month_frames) == 2
        
    def test_year_overflow(self, root):
        """Test year overflow handling."""
        cal = tkface_calendar.Calendar(root, year=2024, month=12, months=3)
        # Should handle December + January + February correctly
        assert len(cal.month_frames) == 3
        
    def test_placeholder_methods(self, calendar_widget):
        """Test placeholder methods for future functionality."""
        # These methods are placeholders for future selection functionality
        assert calendar_widget.get_selected_date() is None
        # bind_date_selected should not raise an error
        calendar_widget.bind_date_selected(lambda: None)
        
    def test_settings_preserved_on_week_start_change(self, root):
        """Test that settings are preserved when changing week start."""
        # Create calendar with custom settings
        day_colors = {"Sunday": "red", "Saturday": "blue"}
        holidays = {"2024-01-01": "green"}
        cal = tkface_calendar.Calendar(
            root, year=2024, month=1, 
            day_colors=day_colors, 
            holidays=holidays,
            show_week_numbers=True
        )
        
        # Change week start
        cal.set_week_start("Monday")
        
        # Check that settings are preserved
        assert cal.day_colors == day_colors
        assert cal.holidays == holidays
        assert cal.show_week_numbers is True
        
    def test_settings_preserved_on_week_numbers_change(self, root):
        """Test that settings are preserved when changing week numbers display."""
        # Create calendar with custom settings
        day_colors = {"Sunday": "red", "Saturday": "blue"}
        holidays = {"2024-01-01": "green"}
        cal = tkface_calendar.Calendar(
            root, year=2024, month=1, 
            day_colors=day_colors, 
            holidays=holidays,
            show_week_numbers=True
        )
        
        # Change week numbers display
        cal.set_show_week_numbers(False)
        
        # Check that settings are preserved
        assert cal.day_colors == day_colors
        assert cal.holidays == holidays
        assert cal.show_week_numbers is False
        
    def test_day_header_width_prevents_overlap(self, root):
        """Test that day headers have sufficient width to prevent overlap."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1, show_week_numbers=True)
        
        # Get the days frame
        month_frame = cal.month_frames[0]
        days_frame = month_frame.winfo_children()[1]  # Second child is days frame
        
        # Check that day headers have reasonable width
        for child in days_frame.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Week"]:
                width = child.winfo_width()
                assert width > 0, f"Day header has zero width: {child.cget('text')}"
                
    def test_day_names_update_on_language_change(self, root):
        """Test that day names update when language changes."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1)
        
        # Get initial day names in English
        lang.set("en", root)
        cal._update_display()
        
        # Get the days frame
        month_frame = cal.month_frames[0]
        days_frame = month_frame.winfo_children()[1]
        
        # Get English day names (only header row)
        english_names = []
        for child in days_frame.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") not in [lang.get("Week")]:
                # Only get first 7 labels (header row)
                if len(english_names) < 7:
                    english_names.append(child.cget("text"))
        
        # Change to Japanese
        lang.set("ja", root)
        cal._update_display()
        
        # Get Japanese day names (only header row)
        japanese_names = []
        for child in days_frame.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") not in [lang.get("Week")]:
                # Only get first 7 labels (header row)
                if len(japanese_names) < 7:
                    japanese_names.append(child.cget("text"))
        
        # Names should be different
        assert english_names != japanese_names, "Day names should change with language"
        assert len(english_names) == len(japanese_names), "Should have same number of day names"
        
    def test_day_names_update_on_week_start_change(self, root):
        """Test that day names update when week start changes."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1, week_start="Sunday")
        
        # Get initial day names with Sunday start
        cal._update_display()
        
        # Get the days frame
        month_frame = cal.month_frames[0]
        days_frame = month_frame.winfo_children()[1]
        
        # Get Sunday-start day names (only header row)
        sunday_names = []
        for child in days_frame.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") not in [lang.get("Week")]:
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
            if isinstance(child, tk.Label) and child.cget("text") not in [lang.get("Week")]:
                # Only get first 7 labels (header row)
                if len(monday_names) < 7:
                    monday_names.append(child.cget("text"))
        
        # First day should be different
        assert sunday_names[0] != monday_names[0], "First day should change with week start"
        assert sunday_names[-1] != monday_names[-1], "Last day should change with week start"
        
    def test_initial_language_setting(self, root):
        """Test that initial language setting is correctly applied."""
        # Set language before creating calendar
        lang.set("ja", root)
        
        # Create calendar
        cal = tkface_calendar.Calendar(root, year=2024, month=1)
        
        # Get the days frame
        month_frame = cal.month_frames[0]
        days_frame = month_frame.winfo_children()[1]
        
        # Get day names (only header row)
        day_names = []
        for child in days_frame.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") not in [lang.get("Week")]:
                # Only get first 7 labels (header row)
                if len(day_names) < 7:
                    day_names.append(child.cget("text"))
        
        # Should be Japanese day names
        expected_japanese = ["日", "月", "火", "水", "木", "金", "土"]
        assert day_names == expected_japanese, f"Expected Japanese day names, got {day_names}"
        
    def test_initial_language_setting_english(self, root):
        """Test that initial language setting is correctly applied for English."""
        # Set language before creating calendar
        lang.set("en", root)
        
        # Create calendar
        cal = tkface_calendar.Calendar(root, year=2024, month=1)
        
        # Get the days frame
        month_frame = cal.month_frames[0]
        days_frame = month_frame.winfo_children()[1]
        
        # Get day names (only header row)
        day_names = []
        for child in days_frame.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") not in [lang.get("Week")]:
                # Only get first 7 labels (header row)
                if len(day_names) < 7:
                    day_names.append(child.cget("text"))
        
        # Should be English day names
        expected_english = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        assert day_names == expected_english, f"Expected English day names, got {day_names}"
        
    def test_set_months(self, root):
        """Test setting the number of months to display."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1, months=1)
        
        # Initially should have 1 month
        assert cal.months == 1
        assert len(cal.month_frames) == 1
        
        # Change to 3 months
        cal.set_months(3)
        assert cal.months == 3
        assert len(cal.month_frames) == 3
        
        # Change to 6 months
        cal.set_months(6)
        assert cal.months == 6
        assert len(cal.month_frames) == 6
        
    def test_set_months_preserves_settings(self, root):
        """Test that changing months preserves other settings."""
        # Create calendar with custom settings
        day_colors = {"Sunday": "red", "Saturday": "blue"}
        holidays = {"2024-01-01": "green"}
        cal = tkface_calendar.Calendar(
            root, year=2024, month=1, 
            months=1,
            day_colors=day_colors, 
            holidays=holidays,
            show_week_numbers=True
        )
        
        # Change months
        cal.set_months(3)
        
        # Check that settings are preserved
        assert cal.day_colors == day_colors
        assert cal.holidays == holidays
        assert cal.show_week_numbers is True
        assert cal.months == 3
        
    def test_set_months_invalid_value(self, root):
        """Test that setting invalid months raises error."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1)
        
        with pytest.raises(ValueError):
            cal.set_months(0)
        
        with pytest.raises(ValueError):
            cal.set_months(-1)
            
    def test_grid_layout_auto_calculation(self, root):
        """Test automatic grid layout calculation."""
        # Test 1 month
        cal = tkface_calendar.Calendar(root, year=2024, month=1, months=1)
        assert cal.grid_rows == 1
        assert cal.grid_cols == 1
        
        # Test 3 months
        cal = tkface_calendar.Calendar(root, year=2024, month=1, months=3)
        assert cal.grid_rows == 1
        assert cal.grid_cols == 3
        
        # Test 6 months
        cal = tkface_calendar.Calendar(root, year=2024, month=1, months=6)
        assert cal.grid_rows == 2
        assert cal.grid_cols == 3
        
        # Test 12 months
        cal = tkface_calendar.Calendar(root, year=2024, month=1, months=12)
        assert cal.grid_rows == 3
        assert cal.grid_cols == 4
        
    def test_custom_grid_layout(self, root):
        """Test custom grid layout."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1, months=4, grid_layout=(2, 2))
        assert cal.grid_rows == 2
        assert cal.grid_cols == 2
        assert len(cal.month_frames) == 4
        
    def test_scrollable_container(self, root):
        """Test that scrollable container is created."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1, months=6)
        
        # Check that canvas and scrollbar exist
        assert hasattr(cal, 'canvas')
        assert hasattr(cal, 'scrollbar')
        assert hasattr(cal, 'scrollable_frame')
        
        # Check that scrollbar is configured
        assert cal.scrollbar.cget('orient') == 'horizontal'
        
    def test_adjacent_month_days_display(self, root):
        """Test that adjacent month days are displayed."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1, months=1)
        
        # Find a day label that should show previous month day
        # January 1, 2024 is a Monday, so the first week should show December 2023 days
        prev_month_day_found = False
        for m, w, d, label in cal.day_labels:
            if w == 0 and d < 1:  # First week, before Monday
                if label.cget("text") and label.cget("text").isdigit():
                    prev_month_day_found = True
                    # Should be gray (adjacent day colors)
                    assert label.cget("bg") in ["lightgray", "white"], f"Expected lightgray or white, got {label.cget('bg')}"
                    break
        
        assert prev_month_day_found, "Previous month days should be displayed"
        
    def test_month_headers_toggle(self, root):
        """Test that month headers can be toggled."""
        # Test with headers
        cal = tkface_calendar.Calendar(root, year=2024, month=1, months=1, show_month_headers=True)
        assert cal.show_month_headers == True
        
        # Test without headers
        cal = tkface_calendar.Calendar(root, year=2024, month=1, months=1, show_month_headers=False)
        assert cal.show_month_headers == False
        
    def test_single_date_selection(self, root):
        """Test single date selection."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1, months=1, selectmode="single")
        
        # Simulate clicking on January 15, 2024
        # January 15, 2024 is a Monday in the third week
        # With Monday as week start: week=2, day=1 (Tuesday)
        cal._on_date_click(0, 2, 1)  # month_index=0, week=2, day=1 (Tuesday)
        
        expected_date = datetime.date(2024, 1, 15)
        assert cal.get_selected_date() == expected_date
        
    def test_range_date_selection(self, root):
        """Test range date selection."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1, months=1, selectmode="range")
        
        # Simulate clicking on January 15, 2024 (start)
        cal._on_date_click(0, 2, 1)  # January 15 (Tuesday)
        # Simulate clicking on January 20, 2024 (end)
        cal._on_date_click(0, 2, 6)  # January 20 (Saturday)
        
        expected_range = (datetime.date(2024, 1, 15), datetime.date(2024, 1, 20))
        assert cal.get_selected_range() == expected_range
        
    def test_selection_callback(self, root):
        """Test selection callback."""
        callback_called = False
        callback_value = None
        
        def callback(selection):
            nonlocal callback_called, callback_value
            callback_called = True
            callback_value = selection
        
        cal = tkface_calendar.Calendar(root, year=2024, month=1, months=1, selectmode="single")
        cal.bind_date_selected(callback)
        
        # Simulate clicking on January 15, 2024
        cal._on_date_click(0, 2, 1)
        
        assert callback_called
        assert callback_value == datetime.date(2024, 1, 15)


class TestDateEntry:
    """Test cases for DateEntry widget."""
    
    @pytest.fixture
    def dateentry_widget(self, root):
        """Create a DateEntry widget for testing."""
        return tkface_calendar.DateEntry(root)
        
    def test_dateentry_creation(self, root):
        """Test basic DateEntry creation."""
        de = tkface_calendar.DateEntry(root)
        assert de is not None
        assert de.date_format == "%Y-%m-%d"
        assert de.selected_date is None
        
    def test_dateentry_with_custom_format(self, root):
        """Test DateEntry with custom date format."""
        de = tkface_calendar.DateEntry(root, date_format="%d/%m/%Y")
        assert de.date_format == "%d/%m/%Y"
        
    def test_dateentry_with_specific_date(self, root):
        """Test DateEntry with specific year and month."""
        de = tkface_calendar.DateEntry(root, year=2024, month=3)
        assert de.calendar_config['year'] == 2024
        assert de.calendar_config['month'] == 3
        
    def test_dateentry_with_theme(self, root):
        """Test DateEntry with theme setting."""
        de = tkface_calendar.DateEntry(root, theme="dark")
        assert de.calendar_config['theme'] == "dark"
        
    def test_dateentry_with_language(self, root):
        """Test DateEntry with language setting."""
        de = tkface_calendar.DateEntry(root, language="ja")
        # Language should be set in the parent window
        assert True  # Just check that no error occurs
        
    def test_dateentry_with_today_color(self, root):
        """Test DateEntry with today color setting."""
        de = tkface_calendar.DateEntry(root, today_color="red")
        assert de.today_color == "red"
        
    def test_dateentry_with_day_colors(self, root):
        """Test DateEntry with day colors setting."""
        day_colors = {"Sunday": "red", "Saturday": "blue"}
        de = tkface_calendar.DateEntry(root, day_colors=day_colors)
        assert de.calendar_config['day_colors'] == day_colors
        
    def test_dateentry_with_holidays(self, root):
        """Test DateEntry with holidays setting."""
        holidays = {"2024-01-01": "red", "2024-01-15": "blue"}
        de = tkface_calendar.DateEntry(root, holidays=holidays)
        assert de.calendar_config['holidays'] == holidays
        
    def test_dateentry_with_week_start(self, root):
        """Test DateEntry with week start setting."""
        de = tkface_calendar.DateEntry(root, week_start="Monday")
        assert de.calendar_config['week_start'] == "Monday"
        
    def test_dateentry_with_show_week_numbers(self, root):
        """Test DateEntry with week numbers setting."""
        de = tkface_calendar.DateEntry(root, show_week_numbers=True)
        assert de.calendar_config['show_week_numbers'] is True
        
    def test_dateentry_with_selectmode(self, root):
        """Test DateEntry with select mode setting."""
        de = tkface_calendar.DateEntry(root, selectmode="range")
        assert de.calendar_config['selectmode'] == "range"
        
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
        de = tkface_calendar.DateEntry(root, date_format="%d/%m/%Y")
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
        
        de = tkface_calendar.DateEntry(root, date_callback=callback)
        test_date = datetime.date(2024, 3, 15)
        
        # Simulate date selection
        de._on_date_selected(test_date)
        
        assert callback_called
        assert callback_value == test_date
        
    def test_refresh_language(self, dateentry_widget):
        """Test language refresh functionality."""
        # Should not raise an error
        dateentry_widget.refresh_language()
        
    def test_set_today_color(self, dateentry_widget):
        """Test setting today color."""
        dateentry_widget.set_today_color("red")
        assert dateentry_widget.today_color == "red"
        
    def test_set_theme(self, dateentry_widget):
        """Test setting theme."""
        dateentry_widget.set_theme("dark")
        assert dateentry_widget.calendar_config['theme'] == "dark"
        
    def test_set_day_colors(self, dateentry_widget):
        """Test setting day colors."""
        day_colors = {"Friday": "green"}
        dateentry_widget.set_day_colors(day_colors)
        assert dateentry_widget.calendar_config['day_colors'] == day_colors
        
    def test_set_week_start(self, dateentry_widget):
        """Test setting week start."""
        dateentry_widget.set_week_start("Monday")
        assert dateentry_widget.calendar_config['week_start'] == "Monday"
        
    def test_set_show_week_numbers(self, dateentry_widget):
        """Test setting week numbers display."""
        dateentry_widget.set_show_week_numbers(True)
        assert dateentry_widget.calendar_config['show_week_numbers'] is True


class TestCalendarIntegration:
    """Integration tests for Calendar widget."""
    
    def test_language_switching(self, root):
        """Test calendar updates when language changes."""
        cal = tkface_calendar.Calendar(root, year=2024, month=1)
        
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
        cal = tkface_calendar.Calendar(root, year=today.year, month=today.month)
        
        # Find today's label and check if it's highlighted
        today_found = False
        for month_idx, week, day, label in cal.day_labels:
            if label.cget("text") == str(today.day):
                # Check if it's highlighted (yellow or custom today color)
                bg_color = label.cget("bg")
                if bg_color in ["yellow", "#ffeb3b"]:  # Default today colors
                    today_found = True
                    break
                    
        assert today_found, "Today's date should be highlighted" 