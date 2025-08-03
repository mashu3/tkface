import tkinter as tk
import datetime
from typing import Dict, Optional, Any
from ..widget.calendar import Calendar, get_calendar_theme, get_calendar_themes
from .. import lang


class DateEntry(tk.Frame):
    """A DateEntry widget that shows a popup calendar."""
    
    def __init__(self, parent, date_format: str = "%Y-%m-%d", 
                 year: Optional[int] = None, month: Optional[int] = None,
                 show_week_numbers: bool = False, week_start: str = "Sunday",
                 day_colors: Optional[Dict[str, str]] = None,
                 holidays: Optional[Dict[str, str]] = None,
                 selectmode: str = "single", theme: str = "light", 
                 language: str = "en", today_color: str = "yellow", 
                 date_callback: Optional[callable] = None, **kwargs):
        super().__init__(parent)
        
        # Get platform information once
        import sys
        self.platform = sys.platform
        
        self.date_format = date_format
        self.selected_date = None  # Store selected date locally
        self.popup = None
        self.date_callback = date_callback
        
        # Create entry and button
        self.entry = tk.Entry(self, state='readonly', width=15)
        self.entry.pack(side='left', fill='x', expand=True)
        
        self.button = tk.Button(self, text="📅", command=self.show_calendar)
        self.button.pack(side='right')
        
        # Calendar will be created when popup is shown
        self.calendar = None
        self.calendar_config = {
            'year': year,
            'month': month,
            'months': 1,
            'show_week_numbers': show_week_numbers,
            'week_start': week_start,
            'day_colors': day_colors,
            'holidays': holidays,
            'selectmode': selectmode,
            'show_navigation': True,
            'theme': theme,
            'date_format': date_format
        }
        
        # Set language if specified
        if language != "en":
            import tkface
            tkface.lang.set(language, parent)
        
        # Set today color if specified
        self.today_color = None
        if today_color != "yellow":
            self.set_today_color(today_color)
        
        # Calendar selection will be bound when created
        
    def _on_date_selected(self, date):
        """Handle date selection from calendar."""
        if date:
            self.selected_date = date  # Update local selected_date
            self.entry.config(state='normal')
            self.entry.delete(0, tk.END)
            self.entry.insert(0, date.strftime(self.date_format))
            self.entry.config(state='readonly')
            self.hide_calendar()
            
            # Call the callback if provided
            if self.date_callback:
                self.date_callback(date)
        
    def _on_popup_click(self, event):
        """Handle click events in the popup to detect clicks outside the calendar (unified macOS logic for all platforms)."""
        # Handle case where event.widget might be a string
        if isinstance(event.widget, str):
            self.hide_calendar()
            return "break"
            
        if not self._is_child_of_calendar(event.widget, self.calendar):
            self.hide_calendar()
        else:
            self.calendar.focus_set()
        # Stop event propagation
        return "break"
        
    def _bind_calendar_events(self, widget):
        """Bind events to all child widgets of the calendar."""
        try:
            # Only bind events to prevent propagation outside calendar
            # Don't block Button-1 events that are needed for date selection
            widget.bind('<ButtonRelease-1>', lambda e: 'break')
            
            # Recursively bind events to child widgets
            for child in widget.winfo_children():
                self._bind_calendar_events(child)
        except Exception as e:
            pass
            
    def _setup_click_outside_handling(self):
        """Setup click outside handling (unified macOS logic for all platforms)."""
        # Use FocusOut event (same as tkcalendar)
        self.calendar.bind('<FocusOut>', self._on_focus_out)
        # Add mouse click events
        self.popup.bind('<Button-1>', self._on_popup_click)
        # Also bind mouse release events
        self.popup.bind('<ButtonRelease-1>', self._on_popup_click)
        # Also bind click events to main window
        self.winfo_toplevel().bind('<Button-1>', self._on_main_window_click)
            
    def _is_child_of_popup(self, widget):
        """Check if widget is a child of the popup window."""
        current = widget
        while current:
            if current == self.popup:
                return True
            current = current.master
        return False
        
    def _setup_focus(self):
        """Setup focus for the popup (unified macOS logic for all platforms)."""
        # Do not use grab_set, only manage focus
        try:
            # Bring popup to front
            self.popup.lift()
            # Set focus to calendar
            self.calendar.focus_set()
            # Set focus again after a short delay
            self.popup.after(50, lambda: self.calendar.focus_set())
            # Force focus after a longer delay
            self.popup.after(100, lambda: self.calendar.focus_force())
        except Exception as e:
            pass
                
    def _on_focus_out(self, event):
        """Handle focus out events (unified macOS logic for all platforms)."""
        # Use same approach as tkcalendar
        # Get the widget that received focus
        focus_widget = self.focus_get()
        
        # Check grab_current() status
        grab_widget = self.popup.grab_current()
        
        if focus_widget is not None:
            if focus_widget == self:
                # If focus returned to DateEntry itself
                x, y = event.x, event.y
                if (type(x) != int or type(y) != int):
                    self.hide_calendar()
            else:
                # If focus moved to another widget
                self.hide_calendar()
        else:
            # No focus (common state)
            try:
                x, y = self.popup.winfo_pointerxy()
                xc = self.popup.winfo_rootx()
                yc = self.popup.winfo_rooty()
                w = self.popup.winfo_width()
                h = self.popup.winfo_height()
                
                if xc <= x <= xc + w and yc <= y <= yc + h:
                    # If mouse is inside popup, return focus to calendar
                    self.calendar.focus_force()
                else:
                    # If mouse is outside popup, close calendar
                    self.hide_calendar()
            except Exception as e:
                # Close calendar even if error occurs
                self.hide_calendar()
                
        # Stop event propagation
        return "break"
        
    def _is_child_of_calendar(self, widget, calendar_widget):
        """Check if widget is a child of calendar widget."""
        # Handle case where widget might be a string
        if isinstance(widget, str):
            return False
            
        current = widget
        while current:
            if current == calendar_widget:
                return True
            current = current.master
        return False
        
    def _on_main_window_click(self, event):
        """Handle click events on the main window (unified macOS logic for all platforms)."""
        # Handle case where event.widget might be a string
        if isinstance(event.widget, str):
            return "break"
            
        # Only process if popup exists
        if self.popup and self.popup.winfo_exists():
            # Check if click position is outside popup
            popup_x = self.popup.winfo_rootx()
            popup_y = self.popup.winfo_rooty()
            popup_w = self.popup.winfo_width()
            popup_h = self.popup.winfo_height()
            
            # Convert main window click coordinates to root coordinates
            root_x = self.winfo_toplevel().winfo_rootx() + event.x
            root_y = self.winfo_toplevel().winfo_rooty() + event.y
            
            # If click is outside popup, close calendar
            if (root_x < popup_x or root_x > popup_x + popup_w or 
                root_y < popup_y or root_y > popup_y + popup_h):
                self.hide_calendar()
                
        # Stop event propagation
        return "break"
            
    def _on_calendar_month_selected(self, year, month):
        """Handle month selection in calendar."""
        self.hide_calendar()
        self.calendar_config['year'] = year
        self.calendar_config['month'] = month
        self.show_calendar()
        
    def _on_calendar_year_view_request(self):
        """Handle year view request from calendar."""
        self.show_year_view()

    def show_year_view(self):
        """Show year view calendar."""
        if hasattr(self, 'year_view_window') and self.year_view_window:
            return
            
        # Hide the popup calendar instead of destroying it
        if self.popup:
            self.popup.withdraw()
            
        # Create year view window as a child of DateEntry (same as popup)
        self.year_view_window = tk.Toplevel(self)
        self.year_view_window.withdraw()
        
        # Get theme colors from calendar config
        theme = self.calendar_config.get('theme', 'light')
        try:
            theme_colors = get_calendar_theme(theme)
        except ValueError:
            theme_colors = get_calendar_theme('light')
        
        # Make it look like part of the calendar
        self.year_view_window.overrideredirect(True)  # Remove title bar and borders
        self.year_view_window.resizable(False, False)
        self.year_view_window.configure(bg=theme_colors['background'])
        
        # Make year view window modal (same as popup)
        self.year_view_window.transient(self.winfo_toplevel())
        
        # Position it over the current popup
        if self.popup:
            popup_x = self.popup.winfo_rootx()
            popup_y = self.popup.winfo_rooty()
            popup_width = self.popup.winfo_width()
            popup_height = self.popup.winfo_height()
            
            self.year_view_window.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")
        else:
            # Fallback position and size
            self.year_view_window.geometry("223x161+135+194")
            
        # Create year view calendar with year view mode enabled
        year_view_config = self.calendar_config.copy()
        year_view_config['year_view_mode'] = True  # Enable year view mode
        self.year_view_calendar = Calendar(self.year_view_window, **year_view_config, date_callback=self._on_year_view_month_selected)
        
        # Pack the year view calendar to fill the window
        self.year_view_calendar.pack(fill='both', expand=True)
        
        # Show the year view window
        self.year_view_window.deiconify()
        self.year_view_window.lift()
        self.year_view_window.focus_force()
        
        # Force update to ensure window is visible and on top
        self.year_view_window.update()
        self.year_view_window.lift()
            
    def hide_year_view(self):
        """Hide year view calendar."""
        if hasattr(self, 'year_view_window') and self.year_view_window:
            self.year_view_window.destroy()
            self.year_view_window = None
            self.year_view_calendar = None
            
    def _update_year_view_position(self):
        """Update the year view window position relative to the DateEntry widget."""
        if self.year_view_window:
            # Get DateEntry widget position
            entry_x = self.winfo_rootx()
            entry_y = self.winfo_rooty() + self.winfo_height()
            entry_width = self.winfo_width()
            entry_height = self.winfo_height()
            
            # Use the same size as the popup would have
            popup_width = 237  # Default popup width
            popup_height = 175  # Default popup height
            
            self.year_view_window.geometry(f"{popup_width}x{popup_height}+{entry_x}+{entry_y}")
            
    def _on_parent_configure(self, event):
        """Handle parent window configuration changes (movement, resize, etc.)."""
        
        # Check if year view is active
        year_view_active = hasattr(self, 'year_view_window') and self.year_view_window and self.year_view_window.winfo_exists()
        
        # Update popup position if it exists and is visible, and year view is not active
        if self.popup and self.popup.winfo_exists() and not year_view_active:
            self._update_popup_position()
            
        # Update year view position if it exists and is visible
        if year_view_active:
            self._update_year_view_position()
            
    def _update_popup_position(self):
        """Update the popup position relative to the entry widget."""
        if self.popup:
            x = self.winfo_rootx()
            y = self.winfo_rooty() + self.winfo_height()
            self.popup.geometry(f"+{x}+{y}")
            
    def _bind_parent_movement_events(self):
        """Bind events to monitor parent window movement."""
        if self.popup or (hasattr(self, 'year_view_window') and self.year_view_window):
            # Get the main window (toplevel)
            main_window = self.winfo_toplevel()
            
            # Bind window movement events
            main_window.bind('<Configure>', self._on_parent_configure)
            
            # Store the binding for cleanup
            self._parent_configure_binding = main_window.bind('<Configure>', self._on_parent_configure)
            
    def _unbind_parent_movement_events(self):
        """Unbind parent window movement events."""
        if hasattr(self, '_parent_configure_binding'):
            main_window = self.winfo_toplevel()
            try:
                main_window.unbind('<Configure>', self._parent_configure_binding)
            except:
                pass
            delattr(self, '_parent_configure_binding')
            
    def _on_year_view_month_selected(self, year, month):
        """Handle month selection in year view."""
        self.hide_year_view()
        self.calendar_config['year'] = year
        self.calendar_config['month'] = month
        self.show_calendar()
            
    def show_calendar(self):
        """Show the popup calendar."""
        if self.popup:
            return
            
        # Create popup window
        self.popup = tk.Toplevel(self)
        
        # Hide window before setting properties
        self.popup.withdraw()
        
        # Use overrideredirect for all environments
        self.popup.overrideredirect(True)  # Remove title bar and borders
        self.popup.resizable(False, False)
        
        # Set popup background color to match calendar theme
        if hasattr(self, 'calendar_config') and 'theme' in self.calendar_config:
            theme = self.calendar_config['theme']
            try:
                theme_colors = get_calendar_theme(theme)
                self.popup.configure(bg=theme_colors['background'])
            except ValueError:
                # Use light theme as fallback
                theme_colors = get_calendar_theme('light')
                self.popup.configure(bg=theme_colors['background'])
        
        # Make popup modal (unified macOS logic for all platforms)
        self.popup.transient(self.winfo_toplevel())
        
        # Use macOS focus management for all platforms
        self.popup.after(100, self._setup_focus)
        
        # Create calendar in popup
        self.calendar = Calendar(self.popup, **self.calendar_config, date_callback=self._on_calendar_month_selected, year_view_callback=self._on_calendar_year_view_request)
        self.calendar.bind_date_selected(self._on_date_selected)
        
        # Bind events to all child widgets in calendar (unified for all platforms)
        self._bind_calendar_events(self.calendar)
        
        # Set today color if specified
        if self.today_color:
            self.calendar.set_today_color(self.today_color)
        
        self.calendar.pack(expand=True, fill='both', padx=2, pady=2)
        
        # Update popup to calculate proper size
        self.popup.update_idletasks()
        
        # Position popup near the entry
        self._update_popup_position()
        
        # Show window
        self.popup.deiconify()
        self.popup.lift()
        
        # Bind popup close events
        self.popup.bind('<Escape>', lambda e: self.hide_calendar())
        
        # Enable close-on-click-outside feature
        self._setup_click_outside_handling()
        
        # Bind parent window movement events to update popup position
        self._bind_parent_movement_events()
        
        # Focus popup
        self.popup.focus_set()
        
    def hide_calendar(self):
        """Hide the popup calendar."""
        if self.popup:
            # Unbind parent window movement events
            self._unbind_parent_movement_events()
            self.popup.destroy()
            self.popup = None
            self.calendar = None
            
    def get_date(self) -> Optional[datetime.date]:
        """Get the selected date."""
        return self.calendar.get_selected_date() if self.calendar else self.selected_date
        
    def set_selected_date(self, date: datetime.date):
        """Set the selected date."""
        self.selected_date = date
        if self.calendar:
            self.calendar.set_selected_date(date)
        self.entry.config(state='normal')
        self.entry.delete(0, tk.END)
        self.entry.insert(0, date.strftime(self.date_format))
        self.entry.config(state='readonly')
        
    def get_date_string(self) -> str:
        """Get the selected date as a string."""
        selected_date = self.get_date()
        return selected_date.strftime(self.date_format) if selected_date else ""
        
    def _delegate_to_calendar(self, method_name, *args, **kwargs):
        """Delegate method calls to calendar if it exists."""
        if self.calendar and hasattr(self.calendar, method_name):
            getattr(self.calendar, method_name)(*args, **kwargs)
    
    def _update_config_and_delegate(self, config_key, value, method_name):
        """Update config and delegate to calendar."""
        self.calendar_config[config_key] = value
        self._delegate_to_calendar(method_name, value)
        
    def refresh_language(self):
        """Refresh the calendar language."""
        self._delegate_to_calendar('refresh_language')
            
    def set_today_color(self, color: str):
        """Set the today color."""
        self.today_color = color
        self._delegate_to_calendar('set_today_color', color)
            
    def set_theme(self, theme: str):
        """Set the calendar theme."""
        self._update_config_and_delegate('theme', theme, 'set_theme')
            
    def set_day_colors(self, day_colors: Dict[str, str]):
        """Set day of week colors dictionary."""
        self._update_config_and_delegate('day_colors', day_colors, 'set_day_colors')
            
    def set_week_start(self, week_start: str):
        """Set the week start day."""
        self._update_config_and_delegate('week_start', week_start, 'set_week_start')
        
    def set_show_week_numbers(self, show: bool):
        """Set whether to show week numbers."""
        self._update_config_and_delegate('show_week_numbers', show, 'set_show_week_numbers')
