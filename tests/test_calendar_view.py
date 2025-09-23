# pylint: disable=import-outside-toplevel,protected-access
"""
Tests for tkface Calendar view functionality
"""

import datetime
import tkinter as tk
from unittest.mock import Mock, patch

import pytest

from tkface import Calendar


class TestCalendarView:
    """Test cases for Calendar view functionality."""

    def test_calendar_view_creation(self, root):
        """Test calendar view creation."""
        cal = Calendar(root, year=2024, month=1)
        assert hasattr(cal, 'month_frames')
        assert len(cal.month_frames) == 1

    def test_calendar_view_multiple_months(self, root):
        """Test calendar view with multiple months."""
        cal = Calendar(root, year=2024, month=1, months=3)
        assert len(cal.month_frames) == 3

    def test_calendar_view_week_numbers(self, root):
        """Test calendar view with week numbers."""
        cal = Calendar(root, year=2024, month=1, show_week_numbers=True)
        assert hasattr(cal, 'week_labels')
        assert len(cal.week_labels) > 0

    def test_calendar_view_day_labels(self, root):
        """Test calendar view day labels."""
        cal = Calendar(root, year=2024, month=1)
        assert hasattr(cal, 'day_labels')
        assert len(cal.day_labels) > 0

    def test_calendar_view_update_display(self, root):
        """Test calendar view update display."""
        cal = Calendar(root, year=2024, month=1)
        # Should not raise exception
        cal._update_display()

    def test_calendar_view_month_navigation(self, root):
        """Test calendar view month navigation."""
        cal = Calendar(root, year=2024, month=1)
        
        # Test month navigation
        cal.set_date(2024, 2)
        assert cal.month == 2
        
        cal.set_date(2024, 12)
        assert cal.month == 12

    def test_calendar_view_year_navigation(self, root):
        """Test calendar view year navigation."""
        cal = Calendar(root, year=2024, month=1)
        
        # Test year navigation
        cal.set_date(2025, 1)
        assert cal.year == 2025
        
        cal.set_date(2023, 1)
        assert cal.year == 2023

    def test_handle_year_view_mouse_enter(self, root):
        """Test handle_year_view_mouse_enter."""
        from tkface.widget.calendar.style import handle_year_view_mouse_enter
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {"selected_bg": "blue", "hover_bg": "lightgray", "hover_fg": "black"}
        
        # Create a mock label
        mock_label = Mock()
        mock_label.cget.return_value = "white"
        mock_label.config = Mock()
        
        handle_year_view_mouse_enter(cal, mock_label)
        mock_label.config.assert_called()

    def test_handle_year_view_mouse_leave(self, root):
        """Test handle_year_view_mouse_leave."""
        from tkface.widget.calendar.style import handle_year_view_mouse_leave
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {
            "selected_bg": "blue", 
            "selected_fg": "white",
            "day_bg": "white", 
            "day_fg": "black", 
            "hover_bg": "lightgray"
        }
        cal.year_view_labels = [(1, Mock())]
        cal.month = 1
        
        # Create a mock label
        mock_label = Mock()
        mock_label.cget.return_value = "lightgray"
        mock_label.config = Mock()
        
        # Mock the year_view_labels to include our label
        cal.year_view_labels[0] = (1, mock_label)
        
        handle_year_view_mouse_leave(cal, mock_label)
        mock_label.config.assert_called()

    def test_hide_normal_calendar_views(self, root):
        """Test _hide_normal_calendar_views."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {
            "background": "white",
            "month_header_bg": "white",
            "month_header_fg": "black"
        }
        
        # Create containers first
        view._create_container(cal)
        
        # Test hiding
        view._hide_normal_calendar_views(cal)
        # Should not raise exception

    def test_handle_year_selection_mouse_enter(self, root):
        """Test handle_year_selection_mouse_enter."""
        from tkface.widget.calendar.style import handle_year_selection_mouse_enter
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {"selected_bg": "blue", "hover_bg": "lightgray", "hover_fg": "black"}
        
        # Create a mock label
        mock_label = Mock()
        mock_label.cget.return_value = "white"
        mock_label.config = Mock()
        
        handle_year_selection_mouse_enter(cal, mock_label)
        mock_label.config.assert_called()

    def test_handle_year_selection_mouse_leave(self, root):
        """Test handle_year_selection_mouse_leave."""
        from tkface.widget.calendar.style import handle_year_selection_mouse_leave
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {
            "selected_bg": "blue", 
            "selected_fg": "white",
            "day_bg": "white", 
            "day_fg": "black", 
            "hover_bg": "lightgray"
        }
        cal.year_selection_labels = [(2024, Mock())]
        cal.year = 2024
        
        # Create a mock label
        mock_label = Mock()
        mock_label.cget.return_value = "lightgray"
        mock_label.config = Mock()
        
        # Mock the year_selection_labels to include our label
        cal.year_selection_labels[0] = (2024, mock_label)
        
        handle_year_selection_mouse_leave(cal, mock_label)
        mock_label.config.assert_called()

    def test_ensure_year_container(self, root):
        """Test _ensure_year_container."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {
            "background": "white",
            "month_header_bg": "white",
            "month_header_fg": "black"
        }
        
        view._ensure_year_container(cal)
        assert hasattr(cal, "year_container")

    def test_clear_year_container_children(self, root):
        """Test _clear_year_container_children."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {
            "background": "white",
            "month_header_bg": "white",
            "month_header_fg": "black"
        }
        
        # Create year container first
        view._ensure_year_container(cal)
        
        # Test clearing children
        view._clear_year_container_children(cal)
        # Should not raise exception

    def test_destroy_year_container(self, root):
        """Test _destroy_year_container."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {
            "background": "white",
            "month_header_bg": "white",
            "month_header_fg": "black"
        }
        
        # Create year container first
        view._ensure_year_container(cal)
        
        # Test destroying year container
        view._destroy_year_container(cal)
        # Should not raise exception

    def test_update_display_year_selection_mode(self, root, calendar_theme_colors):
        """Test _update_display in year selection mode."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.year_selection_mode = True
        cal.theme_colors = calendar_theme_colors
        
        # Test updating display
        view._update_display(cal)
        # Should not raise exception

    def test_create_year_view_content(self, root, calendar_theme_colors):
        """Test _create_year_view_content."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = calendar_theme_colors
        
        # Test creating year view content
        view._create_year_view_content(cal)
        # Should not raise exception

    def test_create_year_view_content_no_navigation(self, root, calendar_theme_colors):
        """Test _create_year_view_content with no navigation."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1, show_navigation=False)
        cal.theme_colors = calendar_theme_colors
        
        # Test creating year view content
        view._create_year_view_content(cal)
        # Should not raise exception

    def test_create_year_selection_content(self, root, calendar_theme_colors):
        """Test _create_year_selection_content."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = calendar_theme_colors
        cal.year_range_start = 2020
        cal.year_range_end = 2030
        
        # Test creating year selection content
        view._create_year_selection_content(cal)
        # Should not raise exception

    def test_update_year_selection_display(self, root, calendar_theme_colors):
        """Test _update_year_selection_display."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = calendar_theme_colors
        cal.year_range_start = 2020
        cal.year_range_end = 2030
        
        # Create year selection content first
        view._create_year_selection_content(cal)
        
        # Test updating year selection display
        view._update_year_selection_display(cal)
        # Should not raise exception

    def test_update_year_view(self, root, calendar_theme_colors):
        """Test _update_year_view."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = calendar_theme_colors
        
        # Create year view content first
        view._create_year_view_content(cal)
        
        # Test updating year view
        view._update_year_view(cal)
        # Should not raise exception

    def test_recreate_widgets(self, root, calendar_theme_colors):
        """Test _recreate_widgets."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = calendar_theme_colors
        
        # Create widgets first
        view._create_widgets(cal)
        
        # Test recreating widgets
        view._recreate_widgets(cal)
        # Should not raise exception

    def test_recreate_widgets_year_selection_mode(self, root, calendar_theme_colors):
        """Test _recreate_widgets in year selection mode."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.year_selection_mode = True
        cal.theme_colors = calendar_theme_colors
        cal.year_range_start = 2020
        cal.year_range_end = 2030
        
        # Test recreating widgets
        view._recreate_widgets(cal)
        # Should not raise exception

    def test_recreate_widgets_month_selection_mode(self, root, calendar_theme_colors, calendar_mock_widgets):
        """Test _recreate_widgets in month selection mode."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1, month_selection_mode=True)
        cal.theme_colors = calendar_theme_colors
        
        # Mock the year_container to avoid TclError
        cal.year_container = calendar_mock_widgets["frame"]
        
        # Test recreating widgets
        view._recreate_widgets(cal)
        # Should not raise exception

    def test_create_year_view_navigation(self, root, calendar_theme_colors):
        """Test _create_year_view_navigation."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = calendar_theme_colors
        
        # Create header frame first
        header_frame = view._create_header_frame(cal, root)
        
        # Get center frame safely
        if header_frame.winfo_children():
            center_frame = header_frame.winfo_children()[0]
            if center_frame.winfo_children():
                center_frame = center_frame.winfo_children()[0]
                # Test creating year view navigation
                view._create_year_view_navigation(cal, center_frame)
                # Should not raise exception

    def test_create_year_selection_navigation(self, root, calendar_theme_colors):
        """Test _create_year_selection_navigation."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = calendar_theme_colors
        cal.year_range_start = 2020
        cal.year_range_end = 2030
        
        # Create header frame first
        header_frame = view._create_header_frame(cal, root)
        
        # Get center frame safely
        if header_frame.winfo_children():
            center_frame = header_frame.winfo_children()[0]
            if center_frame.winfo_children():
                center_frame = center_frame.winfo_children()[0]
                # Test creating year selection navigation
                view._create_year_selection_navigation(cal, center_frame)
                # Should not raise exception

    def test_year_selection_mode_creation(self, root, calendar_theme_colors):
        """Test year selection mode creation."""
        cal = Calendar(root, year=2024, month=1)
        cal.year_selection_mode = True
        cal.theme_colors = calendar_theme_colors
        cal.year_range_start = 2020
        cal.year_range_end = 2030
        
        # Should not raise exception
        assert cal.year_selection_mode is True

    def test_hide_normal_calendar_views_exception_handling(self, root):
        """Test exception handling in _hide_normal_calendar_views."""
        try:
            cal = Calendar(root)
            
            # Mock months_container to raise exception
            cal.months_container = Mock()
            cal.months_container.pack_forget.side_effect = Exception("Test exception")
            
            # Mock canvas to raise exception
            cal.canvas = Mock()
            cal.canvas.pack_forget.side_effect = Exception("Test exception")
            
            # Mock scrollbar to raise exception
            cal.scrollbar = Mock()
            cal.scrollbar.pack_forget.side_effect = Exception("Test exception")
            
            # This should not raise an exception due to try-except blocks
            from tkface.widget.calendar.view import _hide_normal_calendar_views
            _hide_normal_calendar_views(cal)
            
        finally:
            pass

    def test_clear_year_container_children_exception_handling(self, root):
        """Test exception handling in _clear_year_container_children."""
        try:
            cal = Calendar(root)
            
            # Create mock year_container with children that raise exceptions
            mock_child = Mock()
            mock_child.destroy.side_effect = Exception("Test exception")
            cal.year_container = Mock()
            cal.year_container.winfo_children.return_value = [mock_child]
            
            # This should not raise an exception due to try-except blocks
            from tkface.widget.calendar.view import _clear_year_container_children
            _clear_year_container_children(cal)
            
        finally:
            pass

    def test_destroy_year_container_exception_handling(self, root):
        """Test exception handling in _destroy_year_container."""
        try:
            cal = Calendar(root)
            
            # Mock year_container to raise exception
            cal.year_container = Mock()
            cal.year_container.destroy.side_effect = Exception("Test exception")
            
            # Mock months_container to raise exception
            cal.months_container = Mock()
            cal.months_container.pack.side_effect = Exception("Test exception")
            
            # Mock canvas to raise exception
            cal.canvas = Mock()
            cal.canvas.pack.side_effect = Exception("Test exception")
            
            # Mock scrollbar to raise exception
            cal.scrollbar = Mock()
            cal.scrollbar.pack.side_effect = Exception("Test exception")
            
            # This should not raise an exception due to try-except blocks
            from tkface.widget.calendar.view import _destroy_year_container
            _destroy_year_container(cal)
            
        finally:
            pass

    def test_create_navigation_button(self, root):
        """Test create_navigation_button."""
        from tkface.widget.calendar.style import create_navigation_button
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {
            "navigation_font": ("Arial", 10),
            "navigation_bg": "white",
            "navigation_fg": "black",
            "navigation_hover_bg": "lightgray",
            "navigation_hover_fg": "black"
        }
        
        button = create_navigation_button(cal, root, "Test", lambda: None)
        assert button is not None

    def test_create_grid_label(self, root):
        """Test create_grid_label."""
        from tkface.widget.calendar.style import create_grid_label
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {
            "day_bg": "white",
            "day_fg": "black",
            "selected_bg": "blue",
            "selected_fg": "white"
        }
        
        # Create a proper parent frame for grid layout
        parent_frame = tk.Frame(root)
        parent_frame.pack()
        
        label = create_grid_label(cal, parent_frame, "Test", is_selected=True)
        assert label is not None

    def test_create_header_frame(self, root):
        """Test _create_header_frame."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {"month_header_bg": "white"}
        
        header_frame = view._create_header_frame(cal, root)
        assert header_frame is not None

    def test_create_grid_container(self, root):
        """Test _create_grid_container."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {
            "background": "white",
            "month_header_bg": "white",
            "month_header_fg": "black"
        }
        
        grid_frame = view._create_grid_container(cal, root, 3, 4)
        assert grid_frame is not None

    def test_create_container_single_month(self, root):
        """Test _create_container with single month."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1, months=1)
        cal.theme_colors = {
            "background": "white",
            "month_header_bg": "white",
            "month_header_fg": "black"
        }
        
        is_single = view._create_container(cal)
        assert is_single is True
        assert hasattr(cal, "months_container")

    def test_create_container_multiple_months(self, root):
        """Test _create_container with multiple months."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1, months=12)
        cal.theme_colors = {
            "background": "white",
            "month_header_bg": "white",
            "month_header_fg": "black"
        }
        
        is_single = view._create_container(cal)
        assert is_single is False
        assert hasattr(cal, "canvas")
        assert hasattr(cal, "scrollbar")

    def test_create_navigation_buttons(self, root):
        """Test _create_navigation_buttons."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {
            "month_header_bg": "white",
            "month_header_fg": "black",
            "navigation_bg": "white",
            "navigation_fg": "black",
            "navigation_font": ("Arial", 10),
            "navigation_hover_bg": "lightgray",
            "navigation_hover_fg": "black"
        }
        
        # Create header frame first
        header_frame = view._create_header_frame(cal, root)
        
        # Get center frame safely
        if header_frame.winfo_children():
            center_frame = header_frame.winfo_children()[0]
            if center_frame.winfo_children():
                center_frame = center_frame.winfo_children()[0]
                # Test creating navigation buttons
                view._create_navigation_buttons(cal, center_frame, 0)
                # Should not raise exception

    def test_create_navigation_item(self, root):
        """Test _create_navigation_item."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {
            "month_header_bg": "white",
            "month_header_fg": "black",
            "navigation_bg": "white",
            "navigation_fg": "black",
            "navigation_font": ("Arial", 10),
            "navigation_hover_bg": "lightgray",
            "navigation_hover_fg": "black"
        }
        
        # Create header frame first
        header_frame = view._create_header_frame(cal, root)
        
        # Get center frame safely
        if header_frame.winfo_children():
            center_frame = header_frame.winfo_children()[0]
            if center_frame.winfo_children():
                center_frame = center_frame.winfo_children()[0]
                # Test creating navigation item
                view._create_navigation_item(
                    cal, center_frame, 0, "month", "<", ">", 
                    lambda m: None, lambda m: None, False
                )
                # Should not raise exception

    def test_create_month_header(self, root):
        """Test _create_month_header."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {
            "month_header_bg": "white",
            "month_header_fg": "black",
            "navigation_bg": "white",
            "navigation_fg": "black",
            "navigation_font": ("Arial", 10),
            "navigation_hover_bg": "lightgray",
            "navigation_hover_fg": "black"
        }
        
        # Create month frame first
        month_frame = tk.Frame(root)
        
        # Test creating month header
        view._create_month_header(cal, month_frame, 0)
        # Should not raise exception

    def test_create_month_header_no_headers(self, root):
        """Test _create_month_header with no headers."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1, show_month_headers=False)
        cal.theme_colors = {
            "month_header_bg": "white",
            "month_header_fg": "black"
        }
        
        # Create month frame first
        month_frame = tk.Frame(root)
        
        # Test creating month header (should do nothing)
        view._create_month_header(cal, month_frame, 0)
        # Should not raise exception

    def test_create_calendar_grid(self, root):
        """Test _create_calendar_grid."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {
            "background": "white",
            "day_header_bg": "lightgray",
            "day_header_fg": "black",
            "day_header_font": ("Arial", 8),
            "day_bg": "white",
            "day_fg": "black",
            "day_font": ("Arial", 9)
        }
        
        # Create month frame first
        month_frame = tk.Frame(root)
        
        # Test creating calendar grid
        view._create_calendar_grid(cal, month_frame, 0)
        # Should not raise exception

    def test_create_calendar_grid_with_week_numbers(self, root):
        """Test _create_calendar_grid with week numbers."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1, show_week_numbers=True)
        cal.theme_colors = {
            "background": "white",
            "day_header_bg": "lightgray",
            "day_header_fg": "black",
            "day_header_font": ("Arial", 8),
            "day_bg": "white",
            "day_fg": "black",
            "day_font": ("Arial", 9),
            "week_number_bg": "lightgray",
            "week_number_fg": "black",
            "week_number_font": ("Arial", 8)
        }
        
        # Create month frame first
        month_frame = tk.Frame(root)
        
        # Test creating calendar grid with week numbers
        view._create_calendar_grid(cal, month_frame, 0)
        # Should not raise exception

    def test_update_month_headers(self, root, calendar_theme_colors):
        """Test _update_month_headers."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = calendar_theme_colors
        
        # Create widgets first
        view._create_widgets(cal)
        
        # Test updating month headers
        view._update_month_headers(cal, 0, 2024, 1)
        # Should not raise exception

    def test_update_day_name_headers(self, root, calendar_theme_colors):
        """Test _update_day_name_headers."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = calendar_theme_colors
        
        # Create widgets first
        view._create_widgets(cal)
        
        # Get days frame
        month_frame = cal.month_frames[0]
        days_frame = month_frame.winfo_children()[1]
        
        # Test updating day name headers
        view._update_day_name_headers(cal, days_frame)
        # Should not raise exception

    def test_update_single_day_label(self, root, calendar_theme_colors):
        """Test _update_single_day_label."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = calendar_theme_colors
        
        # Create widgets first
        view._create_widgets(cal)
        
        # Get a day label
        day_label = cal.day_labels[0][3]  # Get the label from first day
        
        # Test updating single day label
        month_days = [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 0, 0]
        view._update_single_day_label(cal, day_label, 2024, 1, 0, 0, 0, month_days)
        # Should not raise exception

    def test_update_week_numbers(self, root, calendar_theme_colors):
        """Test _update_week_numbers."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1, show_week_numbers=True)
        cal.theme_colors = calendar_theme_colors
        
        # Create widgets first
        view._create_widgets(cal)
        
        # Test updating week numbers
        week_label_index = view._update_week_numbers(cal, 2024, 1, 0)
        # The actual value depends on the implementation, so we just check it's a valid index
        assert week_label_index >= 0

    def test_update_year_view_exception_handling(self, root):
        """Test exception handling in _update_year_view."""
        try:
            cal = Calendar(root)
            
            # Mock required attributes
            cal.year_view_year_label = Mock()
            cal.year_view_year_label.config = Mock()
            cal.year_view_labels = []
            
            # Mock year_container to raise exception
            cal.year_container = Mock()
            cal.year_container.lift.side_effect = Exception("Test exception")
            cal.update_idletasks = Mock(side_effect=Exception("Test exception"))
            
            # This should not raise an exception due to try-except blocks
            from tkface.widget.calendar.view import _update_year_view
            _update_year_view(cal)
            
        finally:
            pass

    def test_update_year_selection_display_exception_handling(self, root):
        """Test exception handling in _update_year_selection_display."""
        try:
            cal = Calendar(root)
            
            # Mock required attributes
            cal.year_selection_header_label = Mock()
            cal.year_selection_header_label.config = Mock()
            cal.year_selection_labels = []
            cal._get_year_range_text = Mock(return_value="2020-2029")
            
            # Mock year_container to raise exception
            cal.year_container = Mock()
            cal.year_container.lift.side_effect = Exception("Test exception")
            cal.update_idletasks = Mock(side_effect=Exception("Test exception"))
            
            # This should not raise an exception due to try-except blocks
            from tkface.widget.calendar.view import _update_year_selection_display
            _update_year_selection_display(cal)
            
        finally:
            pass

    def test_recreate_widgets_exception_handling(self, root):
        """Test exception handling in _recreate_widgets."""
        try:
            cal = Calendar(root)
            
            # Mock update_dpi_scaling to raise exception
            with patch.object(cal, "update_dpi_scaling") as mock_dpi:
                mock_dpi.side_effect = OSError("DPI error")
                
                # This should not raise an exception due to try-except blocks
                from tkface.widget.calendar.view import _recreate_widgets
                _recreate_widgets(cal)
            
        finally:
            pass

    def test_recreate_widgets_destroy_exception_handling(self, root):
        """Test exception handling in _recreate_widgets when destroying widgets."""
        try:
            cal = Calendar(root)
            
            # Mock canvas to raise exception when destroyed
            cal.canvas = Mock()
            cal.canvas.destroy.side_effect = Exception("Destroy error")
            
            # Mock scrollbar to raise exception when destroyed
            cal.scrollbar = Mock()
            cal.scrollbar.destroy.side_effect = Exception("Destroy error")
            
            # Mock year_container to raise exception when destroyed
            cal.year_container = Mock()
            cal.year_container.destroy.side_effect = Exception("Destroy error")
            
            # This should raise an exception since there's no try-except block
            from tkface.widget.calendar.view import _recreate_widgets
            with pytest.raises(Exception, match="Destroy error"):
                _recreate_widgets(cal)
            
        finally:
            pass

    def test_create_widgets(self, root, calendar_theme_colors):
        """Test _create_widgets."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = calendar_theme_colors
        
        # Test creating widgets
        view._create_widgets(cal)
        # Should not raise exception

    def test_update_display_month_selection_mode(self, root, calendar_theme_colors):
        """Test _update_display in month selection mode."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1, month_selection_mode=True)
        cal.theme_colors = calendar_theme_colors
        
        # Test updating display
        view._update_display(cal)
        # Should not raise exception

    def test_update_day_labels(self, root, calendar_theme_colors):
        """Test _update_day_labels."""
        from tkface.widget.calendar import view
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = calendar_theme_colors
        
        # Create widgets first
        view._create_widgets(cal)
        
        # Test updating day labels
        month_days = [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 0, 0]
        view._update_day_labels(cal, 0, 2024, 1, month_days)
        # Should not raise exception

    def test_navigation_prev_next_month_year(self, root):
        """Test navigation prev/next month/year."""
        cal = Calendar(root, year=2024, month=1)
        with patch.object(cal, "set_date") as m_set_date:
            cal._on_prev_month(0)
            m_set_date.assert_called_with(2023, 12)
            m_set_date.reset_mock()

            cal._on_next_month(0)
            m_set_date.assert_called_with(2024, 2)
            m_set_date.reset_mock()

            cal._on_prev_year(0)
            m_set_date.assert_called_with(2023, 1)
            m_set_date.reset_mock()

            cal._on_next_year(0)
            m_set_date.assert_called_with(2025, 1)

    def test_year_view_and_selection_toggles(self, root):
        """Test year view and selection toggles."""
        cal = Calendar(root, year=2024, month=6)
        with patch("tkface.widget.calendar.view._create_year_selection_content") as m_sel:
            cal._on_year_header_click()
            assert cal.year_selection_mode is True and cal.month_selection_mode is False
            assert cal.year_range_start == cal._calculate_year_range(cal.year)[0]
            assert m_sel.called

        with patch("tkface.widget.calendar.view._create_year_view_content") as m_view:
            cal._on_year_selection_header_click()
            assert cal.month_selection_mode is True and cal.year_selection_mode is False
            assert m_view.called

        with patch("tkface.widget.calendar.view._update_year_view") as m_update:
            cal._on_prev_year_view()
            assert cal.year == 2023
            cal._on_next_year_view()
            assert cal.year == 2024
            assert m_update.called

        cal._initialize_year_range(2020)
        with patch(
            "tkface.widget.calendar.view._update_year_selection_display"
        ) as m_range:
            start0 = cal.year_range_start
            end0 = cal.year_range_end
            cal._on_prev_year_range()
            assert cal.year_range_start == start0 - 10
            assert cal.year_range_end == end0 - 10
            cal._on_next_year_range()
            assert cal.year_range_start == start0
            assert cal.year_range_end == end0
            assert m_range.called

    def test_year_view_month_click_and_callbacks(self, root):
        """Test year view month click and callbacks."""
        config = {
            "month_selection_mode": True,
            "date_callback_called": False,
        }

        def date_cb(year, month):  # noqa: ANN001
            # simple recorder
            config["date_callback_called"] = True
            config["ym"] = (year, month)

        cal = Calendar(
            root,
            config=None,
            year=2024,
            month=5,
            month_selection_mode=True,
            date_callback=date_cb,
        )

        with patch("tkface.widget.calendar.view._destroy_year_container") as m_destroy, \
            patch("tkface.widget.calendar.view._create_widgets") as m_create, \
            patch("tkface.widget.calendar.view._update_display") as m_update:
            cal._on_year_view_month_click(3)
            assert cal.month == 3
            assert cal.month_selection_mode is False
            assert cal.year_selection_mode is False
            assert m_destroy.called and m_create.called and m_update.called
            assert config["date_callback_called"] is True
            assert config["ym"] == (cal.year, 3)

    def test_set_adjacent_month_day_adjacent_and_empty(self, root, calendar_theme_colors):
        """Test set adjacent month day adjacent and empty."""
        cal = Calendar(root, year=2024, month=1)
        # Inject known theme colors for assertions
        cal.theme_colors = calendar_theme_colors
        label = Mock()
        # Position before first day -> previous month date
        cal._set_adjacent_month_day(label, 2024, 1, week=0, day=0)
        assert label.config.called
        kwargs = label.config.call_args.kwargs
        assert kwargs["bg"] == cal.theme_colors["adjacent_day_bg"]
        assert kwargs["fg"] == cal.theme_colors["adjacent_day_fg"]
        assert kwargs["text"].isdigit()

        label.reset_mock()
        # Position exactly at first day -> empty cell in current month branch
        # Compute first weekday offset for (2024-01-01)
        first_day = datetime.date(2024, 1, 1)
        first_offset = cal._get_week_start_offset(first_day)
        cal._set_adjacent_month_day(label, 2024, 1, week=0, day=first_offset)
        kwargs = label.config.call_args.kwargs
        assert kwargs["text"] == ""
        assert kwargs["bg"] == cal.theme_colors["day_bg"]
        assert kwargs["fg"] == cal.theme_colors["day_fg"]

    def test_on_date_click_single_and_range_with_callback(self, root):
        """Test on date click single and range with callback."""
        cal = Calendar(root, year=2024, month=1, week_start="Sunday")
        captured = {}

        def cb(value):  # noqa: ANN001
            captured["value"] = value

        cal.bind_date_selected(cb)
        with patch("tkface.widget.calendar.view._update_display"):
            # Click a cell corresponding to Jan 1, 2024
            first_day = datetime.date(2024, 1, 1)
            offset = cal._get_week_start_offset(first_day)
            cal._on_date_click(month_index=0, week=0, day=offset)
            assert cal.selected_date == datetime.date(2024, 1, 1)
            assert isinstance(captured.get("value"), datetime.date)

            # Range selection
            cal.selectmode = "range"
            cal._on_date_click(0, 0, offset)  # start
            assert cal.selected_range is not None
            # end earlier than start -> swapped
            cal._on_date_click(0, 0, offset - 1)
            start, end = cal.selected_range
            assert start <= end

    def test_set_date_updates_based_on_mode(self, root):
        """Test set date updates based on mode."""
        cal = Calendar(root, year=2024, month=1)
        with patch("tkface.widget.calendar.view._update_display") as m_display:
            cal.month_selection_mode = False
            cal.set_date(2025, 2)
            assert cal.year == 2025 and cal.month == 2
            assert m_display.called

        with patch("tkface.widget.calendar.view._update_year_view") as m_year_view:
            cal.month_selection_mode = True
            cal.set_date(2026, 3)
            assert cal.year == 2026 and cal.month == 3
            assert m_year_view.called

    def test_set_today_color_variants(self, root):
        """Test set today color variants."""
        cal = Calendar(root)
        with patch("tkface.widget.calendar.view._update_display"):
            cal.set_today_color("none")
            assert cal.today_color is None and cal.today_color_set is False

            cal.set_today_color("red")
            assert cal.today_color == "red" and cal.today_color_set is True

    def test_calendar_popup_dimensions(self, root):
        """Test calendar popup dimensions."""
        cal = Calendar(root, year=2024, month=1, popup_width=300, popup_height=200)
        assert cal.popup_width == 300
        assert cal.popup_height == 200

    def test_calendar_get_popup_geometry(self, root):
        """Test calendar get_popup_geometry method."""
        cal = Calendar(root, year=2024, month=1, popup_width=300, popup_height=200)
        geometry = cal.get_popup_geometry(root)
        assert "300x200" in geometry

    def test_calendar_set_popup_size(self, root):
        """Test calendar set_popup_size method."""
        cal = Calendar(root, year=2024, month=1)
        cal.set_popup_size(400, 300)
        assert cal.popup_width == 400
        assert cal.popup_height == 300

    def test_datepicker_base_popup_click_handling(self, root):
        """Test popup click handling in _DatePickerBase."""
        from tkface.dialog.datepicker import _DatePickerBase
        
        base = _DatePickerBase(root)
        
        # Create mock objects
        mock_popup = Mock()
        mock_calendar = Mock()
        mock_hide_callback = Mock()
        
        # Mock event with string widget
        mock_event = Mock()
        mock_event.widget = "string_widget"
        mock_popup.winfo_pointerxy.return_value = (100, 100)
        mock_popup.winfo_rootx.return_value = 50
        mock_popup.winfo_rooty.return_value = 50
        mock_popup.winfo_width.return_value = 200
        mock_popup.winfo_height.return_value = 200
        
        # Test click inside popup
        result = base._on_popup_click(mock_event, mock_popup, mock_calendar, mock_hide_callback)
        assert result == "break"
        mock_calendar.focus_set.assert_called_once()

    def test_datepicker_base_popup_click_outside(self, root):
        """Test popup click outside handling."""
        from tkface.dialog.datepicker import _DatePickerBase
        
        base = _DatePickerBase(root)
        
        # Create mock objects
        mock_popup = Mock()
        mock_calendar = Mock()
        mock_hide_callback = Mock()
        
        # Mock event with string widget
        mock_event = Mock()
        mock_event.widget = "string_widget"
        mock_popup.winfo_pointerxy.return_value = (300, 300)  # Outside popup
        mock_popup.winfo_rootx.return_value = 50
        mock_popup.winfo_rooty.return_value = 50
        mock_popup.winfo_width.return_value = 200
        mock_popup.winfo_height.return_value = 200
        
        # Test click outside popup
        result = base._on_popup_click(mock_event, mock_popup, mock_calendar, mock_hide_callback)
        assert result == "break"
        mock_hide_callback.assert_called_once()

    def test_grid_calculation_edge_cases(self, root):
        """Test grid calculation edge cases."""
        # Test month selection mode with 16 months to trigger else case
        cal = Calendar(root, year=2024, month=1, months=16)
        # This should trigger the "else" case in grid calculation (line 208)
        assert cal.grid_rows == 4
        assert cal.grid_cols == 4

    def test_week_number_edge_cases(self, root):
        """Test week number calculation edge cases."""
        cal = Calendar(root, year=2024, month=1, show_week_numbers=True)
        
        # Test week reference date calculation
        week_dates = [
            datetime.date(2024, 1, 1),
            datetime.date(2024, 1, 2),
            datetime.date(2024, 1, 3),
            datetime.date(2024, 1, 4),
            datetime.date(2024, 1, 5),
            datetime.date(2024, 1, 6),
            datetime.date(2024, 1, 7),
        ]
        
        # Test with different week start settings
        cal.week_start = "Monday"
        cal._update_calendar_week_start()
        ref_date = cal._get_week_ref_date(week_dates)
        assert isinstance(ref_date, datetime.date)

    def test_navigation_edge_cases(self, root):
        """Test navigation edge cases."""
        cal = Calendar(root, year=2024, month=1)
        
        # Test previous month navigation from January (should go to December of previous year)
        cal.set_date(2024, 1)
        cal._on_prev_month(0)  # Month index 0 for first month
        assert cal.year == 2023
        assert cal.month == 12

    def test_week_number_empty_cases(self, root):
        """Test week number empty cases (line 359)."""
        cal = Calendar(root, year=2024, month=1, show_week_numbers=True)
        
        # Test with empty week dates to trigger line 359
        empty_week_dates = []
        # This should trigger the else case in week number calculation
        try:
            ref_date = cal._get_week_ref_date(empty_week_dates)
        except IndexError:
            # Expected when week_dates is empty
            pass

    def test_navigation_edge_cases_detailed(self, root):
        """Test navigation edge cases in detail (line 435)."""
        cal = Calendar(root, year=2024, month=1)
        
        # Test previous month navigation from January (line 435)
        cal.set_date(2024, 1)
        cal._on_prev_month(0)
        assert cal.year == 2023
        assert cal.month == 12

    def test_bind_hover_events(self, root):
        """Test bind_hover_events."""
        from tkface.widget.calendar.style import bind_hover_events
        
        cal = Calendar(root, year=2024, month=1)
        
        # Create a mock label
        mock_label = Mock()
        mock_label.bind = Mock()
        
        bind_hover_events(cal, mock_label, lambda c, l: None, lambda c, l: None)
        assert mock_label.bind.call_count == 2

    def test_handle_mouse_enter_not_selected(self, root):
        """Test handle_mouse_enter with not selected."""
        from tkface.widget.calendar.style import handle_mouse_enter
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {"selected_bg": "blue", "range_bg": "lightblue", "hover_bg": "lightgray", "hover_fg": "black"}
        cal.original_colors = {}
        
        # Create a mock label
        mock_label = Mock()
        mock_label.cget.return_value = "white"
        mock_label.config = Mock()
        
        handle_mouse_enter(cal, mock_label)
        mock_label.config.assert_called()

    def test_handle_mouse_enter_already_selected(self, root):
        """Test handle_mouse_enter with already selected."""
        from tkface.widget.calendar.style import handle_mouse_enter
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {"selected_bg": "blue", "range_bg": "lightblue", "hover_bg": "lightgray", "hover_fg": "black"}
        cal.original_colors = {}
        
        # Create a mock label
        mock_label = Mock()
        mock_label.cget.return_value = "blue"  # Already selected
        mock_label.config = Mock()
        
        handle_mouse_enter(cal, mock_label)
        # Should not call config since already selected
        mock_label.config.assert_not_called()

    def test_handle_mouse_leave_hover(self, root):
        """Test handle_mouse_leave with hover state."""
        from tkface.widget.calendar.style import handle_mouse_leave
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {"selected_bg": "blue", "selected_fg": "white", "day_bg": "white", "day_fg": "black", "hover_bg": "lightgray"}
        cal.original_colors = {"bg": "white", "fg": "black"}
        
        # Create a mock label
        mock_label = Mock()
        mock_label.cget.return_value = "lightgray"  # Hover state
        mock_label.config = Mock()
        
        handle_mouse_leave(cal, mock_label)
        mock_label.config.assert_called()

    def test_handle_mouse_leave_not_hover(self, root):
        """Test handle_mouse_leave with not hover state."""
        from tkface.widget.calendar.style import handle_mouse_leave
        
        cal = Calendar(root, year=2024, month=1)
        cal.theme_colors = {"selected_bg": "blue", "selected_fg": "white", "day_bg": "white", "day_fg": "black", "hover_bg": "lightgray"}
        cal.original_colors = {"bg": "white", "fg": "black"}
        
        # Create a mock label
        mock_label = Mock()
        mock_label.cget.return_value = "white"  # Not hover state
        mock_label.config = Mock()
        
        handle_mouse_leave(cal, mock_label)
        # Should not call config since not in hover state
        mock_label.config.assert_not_called()

    def test_handle_mouse_leave_fallback_colors(self, root):
        """Test handle_mouse_leave with fallback to default colors."""
        try:
            cal = Calendar(root)
            
            # Create a mock label without original_colors
            mock_label = Mock()
            mock_label.config = Mock()
            mock_label.cget.return_value = cal.theme_colors["hover_bg"]  # Simulate hover state
            cal.original_colors = {}  # Empty original_colors
            
            # Call handle_mouse_leave
            from tkface.widget.calendar.style import handle_mouse_leave
            handle_mouse_leave(cal, mock_label)
            
            # Verify fallback colors were applied
            mock_label.config.assert_called_once()
            args, kwargs = mock_label.config.call_args
            assert "bg" in kwargs
            assert "fg" in kwargs
            
        finally:
            pass

    def test_handle_mouse_enter_else_branch(self, root):
        """Test handle_mouse_enter else branch for non-selected dates."""
        try:
            cal = Calendar(root)
            
            # Create a mock label that's not selected
            mock_label = Mock()
            mock_label.config = Mock()
            mock_label.cget.return_value = "normal"  # Not selected
            
            # Call handle_mouse_enter
            from tkface.widget.calendar.style import handle_mouse_enter
            handle_mouse_enter(cal, mock_label)
            
            # Verify else branch was executed
            mock_label.config.assert_called_once()
            args, kwargs = mock_label.config.call_args
            assert "bg" in kwargs
            assert "fg" in kwargs
            
        finally:
            pass

    def test_handle_mouse_leave_else_branch(self, root):
        """Test handle_mouse_leave else branch for non-selected dates."""
        try:
            cal = Calendar(root)
            
            # Create a mock label that's not in hover state
            mock_label = Mock()
            mock_label.config = Mock()
            mock_label.cget.return_value = "normal"  # Not hover state
            
            # Call handle_mouse_leave
            from tkface.widget.calendar.style import handle_mouse_leave
            handle_mouse_leave(cal, mock_label)
            
            # When not in hover state, config should not be called
            mock_label.config.assert_not_called()
            
        finally:
            pass

    def test_week_number_empty_else_cases(self, root):
        """Test week number empty else cases (line 359)."""
        cal = Calendar(root, year=2024, month=1, show_week_numbers=True)
        
        # Test with empty week dates to trigger line 359
        empty_week_dates = []
        # This should trigger the else case in week number calculation
        try:
            ref_date = cal._get_week_ref_date(empty_week_dates)
        except IndexError:
            # Expected when week_dates is empty
            pass

    def test_navigation_prev_month_else_case(self, root):
        """Test navigation prev month else case (line 435)."""
        cal = Calendar(root, year=2024, month=1)
        
        # Test previous month navigation from February (should go to January)
        cal.set_date(2024, 2)
        cal._on_prev_month(0)
        assert cal.year == 2024
        assert cal.month == 1

    def test_popup_size_and_geometry(self, root):
        cal = Calendar(root, months=2, show_week_numbers=True)
        cal.set_popup_size(width=250, height=180)
        # Mock a parent widget
        parent = Mock()
        parent.update_idletasks = Mock()
        parent.winfo_rootx.return_value = 100
        parent.winfo_rooty.return_value = 200
        parent.winfo_height.return_value = 20
        parent.winfo_screenwidth.return_value = 300
        parent.winfo_screenheight.return_value = 250

        geom = cal.get_popup_geometry(parent)
        # width = (250 + 20) * 2 = 540, height = 180 -> will be clamped to screen
        assert isinstance(geom, str)
        assert "x" in geom and "+" in geom
