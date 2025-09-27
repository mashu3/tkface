"""
Time spinner widget for tkface.

This module provides TimeSpinner widget that displays time selection
using spinboxes for hours, minutes, seconds, and AM/PM.
"""

import datetime
import tkinter as tk
from typing import Optional

from ..lang import get as lang_get


class CustomSpinbox(tk.Frame):
    """Custom spinbox with up/down buttons above and below the number field."""

    def __init__(  # pylint: disable=too-many-positional-arguments
        self,
        parent,
        from_=0,
        to=99,
        width=2,
        textvariable=None,
        format_str="%02.0f",
        font=None,
        callback=None,
        **kwargs,  # pylint: disable=unused-argument
    ):
        super().__init__(parent)
        self.from_ = from_
        self.to = to
        self.width = width
        self.textvariable = textvariable
        self.format_str = format_str
        self.font = font or ("Arial", 14, "bold")
        self.callback = callback
        self.value = from_

        if textvariable:
            self.value = (
                int(textvariable.get()) if textvariable.get().isdigit() else from_
            )

        self._create_widgets()
        self._bind_events()

    def _create_widgets(self):
        """Create the custom spinbox widgets."""
        # Up button
        self.up_button = tk.Button(
            self,
            text="▲",
            font=("Arial", 8),
            width=1,
            height=1,
            command=self._increment,
        )
        self.up_button.pack()

        # Number entry
        self.entry = tk.Entry(
            self,
            textvariable=self.textvariable,
            width=self.width,
            font=self.font,
            justify="center",
            state="readonly",
        )
        self.entry.pack()

        # Down button
        self.down_button = tk.Button(
            self,
            text="▼",
            font=("Arial", 8),
            width=1,
            height=1,
            command=self._decrement,
        )
        self.down_button.pack()

        self._update_display()

    def _bind_events(self):
        """Bind events to widgets."""
        self.entry.bind("<Button-1>", self._on_entry_click)
        self.entry.bind("<KeyPress>", self._on_key_press)
        self.entry.bind("<MouseWheel>", self._on_mouse_wheel)

    def _increment(self):
        """Increment the value with wraparound."""
        self.value += 1
        if self.value > self.to:
            self.value = self.from_
        self._update_display()
        if self.callback:
            self.callback()

    def _decrement(self):
        """Decrement the value with wraparound."""
        self.value -= 1
        if self.value < self.from_:
            self.value = self.to
        self._update_display()
        if self.callback:
            self.callback()

    def _update_display(self):
        """Update the display value."""
        if self.textvariable:
            self.textvariable.set(self.format_str % self.value)
        else:
            self.entry.config(state="normal")
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.format_str % self.value)
            self.entry.config(state="readonly")

    def _on_entry_click(self, event):  # pylint: disable=unused-argument
        """Handle entry click - allow editing."""
        self.entry.config(state="normal")
        self.entry.select_range(0, tk.END)

    def _on_key_press(self, event):
        """Handle key press in entry."""
        if event.keysym == "Return":
            self._validate_and_set()
        elif event.keysym == "Up":
            self._increment()
        elif event.keysym == "Down":
            self._decrement()

    def _on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling."""
        if event.delta > 0:
            self._increment()
        else:
            self._decrement()

    def _validate_and_set(self):
        """Validate and set the value from entry."""
        try:
            new_value = int(self.entry.get())
            if self.from_ <= new_value <= self.to:
                self.value = new_value
                self._update_display()
                if self.callback:
                    self.callback()
            else:
                self._update_display()  # Reset to current value
        except ValueError:
            self._update_display()  # Reset to current value
        finally:
            self.entry.config(state="readonly")

    def get(self):
        """Get the current value."""
        return self.value

    def set(self, value):
        """Set the value."""
        if self.from_ <= value <= self.to:
            self.value = value
            self._update_display()


class CustomAMPMSpinbox(tk.Frame):
    """Custom AM/PM spinbox with up/down buttons above and below the text field."""

    def __init__(
        self, parent, textvariable=None, font=None, callback=None, **kwargs
    ):  # pylint: disable=unused-argument
        super().__init__(parent)
        self.textvariable = textvariable
        self.font = font or ("Arial", 12, "bold")
        self.callback = callback
        self.values = ["AM", "PM"]
        self.current_index = 0

        if textvariable:
            current_value = textvariable.get()
            if current_value in self.values:
                self.current_index = self.values.index(current_value)

        self._create_widgets()
        self._bind_events()

    def _create_widgets(self):
        """Create the custom AM/PM spinbox widgets."""
        # Up button
        self.up_button = tk.Button(
            self,
            text="▲",
            font=("Arial", 8),
            width=1,
            height=1,
            command=self._increment,
        )
        self.up_button.pack()

        # Text entry
        self.entry = tk.Entry(
            self,
            textvariable=self.textvariable,
            width=3,
            font=self.font,
            justify="center",
            state="readonly",
        )
        self.entry.pack()

        # Down button
        self.down_button = tk.Button(
            self,
            text="▼",
            font=("Arial", 8),
            width=1,
            height=1,
            command=self._decrement,
        )
        self.down_button.pack()

        self._update_display()
        self._update_button_visibility()

    def _bind_events(self):
        """Bind events to widgets."""
        self.entry.bind("<Button-1>", self._on_entry_click)
        self.entry.bind("<KeyPress>", self._on_key_press)
        self.entry.bind("<MouseWheel>", self._on_mouse_wheel)

    def _increment(self):
        """Increment the value (AM -> PM)."""
        self.current_index = (self.current_index + 1) % len(self.values)
        self._update_display()
        self._update_button_visibility()
        if self.callback:
            self.callback()

    def _decrement(self):
        """Decrement the value (PM -> AM)."""
        self.current_index = (self.current_index - 1) % len(self.values)
        self._update_display()
        self._update_button_visibility()
        if self.callback:
            self.callback()

    def _update_display(self):
        """Update the display value."""
        current_value = self.values[self.current_index]
        if self.textvariable:
            self.textvariable.set(current_value)
        else:
            self.entry.config(state="normal")
            self.entry.delete(0, tk.END)
            self.entry.insert(0, current_value)
            self.entry.config(state="readonly")

    def _update_button_visibility(self):
        """Update button visibility based on current value."""
        current_value = self.values[self.current_index]
        if current_value == "AM":
            # When AM: only down button (▼) is enabled (to go to PM)
            self.up_button.config(state="disabled")
            self.down_button.config(state="normal")
        else:  # PM
            # When PM: only up button (▲) is enabled (to go back to AM)
            self.up_button.config(state="normal")
            self.down_button.config(state="disabled")

    def _on_entry_click(self, event):  # pylint: disable=unused-argument
        """Handle entry click - allow editing."""
        self.entry.config(state="normal")
        self.entry.select_range(0, tk.END)

    def _on_key_press(self, event):
        """Handle key press in entry."""
        if event.keysym == "Return":
            self._validate_and_set()
        elif event.keysym == "Up":
            self._increment()
        elif event.keysym == "Down":
            self._decrement()

    def _on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling."""
        if event.delta > 0:
            self._increment()
        else:
            self._decrement()

    def _validate_and_set(self):
        """Validate and set the value from entry."""
        try:
            new_value = self.entry.get().upper()
            if new_value in self.values:
                self.current_index = self.values.index(new_value)
                self._update_display()
                self._update_button_visibility()
                if self.callback:
                    self.callback()
            else:
                self._update_display()  # Reset to current value
        except ValueError:
            self._update_display()  # Reset to current value
        finally:
            self.entry.config(state="readonly")

    def get(self):
        """Get the current value."""
        return self.values[self.current_index]

    def set(self, value):
        """Set the value."""
        if value in self.values:
            self.current_index = self.values.index(value)
            self._update_display()
            self._update_button_visibility()


class TimeSpinner(tk.Frame):
    """Time spinner widget with spinboxes for time selection."""

    def __init__(  # pylint: disable=too-many-positional-arguments
        self,
        parent,
        hour_format="24",
        show_seconds=True,
        time_callback=None,
        theme="light",
        initial_time=None,
    ):
        super().__init__(parent)
        self.hour_format = hour_format
        self.show_seconds = show_seconds
        self.time_callback = time_callback
        self.theme = theme
        self.selected_time = None

        # Create time components
        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()
        self.second_var = tk.StringVar()
        self.am_pm_var = tk.StringVar()

        # Set initial values
        if initial_time is not None:
            self.selected_time = initial_time
            self._set_initial_values(initial_time)
        else:
            current_time = datetime.datetime.now().time()
            self.selected_time = current_time
            self._set_initial_values(current_time)

        self._create_widgets()
        self._bind_events()

    def _set_initial_values(self, time_obj):
        """Set initial values for time components."""
        if self.hour_format == "12":
            hour = time_obj.hour
            if hour == 0:
                hour = 12
                am_pm = "AM"
            elif hour < 12:
                am_pm = "AM"
            else:
                if hour > 12:
                    hour -= 12
                am_pm = "PM"
            self.hour_var.set(f"{hour:02d}")
            self.am_pm_var.set(am_pm)
        else:
            self.hour_var.set(f"{time_obj.hour:02d}")

        self.minute_var.set(f"{time_obj.minute:02d}")
        if self.show_seconds:
            self.second_var.set(f"{time_obj.second:02d}")

    def _create_widgets(self):
        """Create the time picker widgets."""
        # Get root window for language support
        root = self.winfo_toplevel()

        # Main frame
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # Time display frame
        time_frame = tk.Frame(main_frame)
        time_frame.pack(pady=5)

        # Hour
        hour_frame = tk.Frame(time_frame)
        hour_frame.pack(side="left", padx=2)

        hour_label = lang_get("timepicker.hour", root)
        tk.Label(hour_frame, text=hour_label, font=("Arial", 10)).pack()
        self.hour_spinbox = CustomSpinbox(
            hour_frame,
            from_=1 if self.hour_format == "12" else 0,
            to=12 if self.hour_format == "12" else 23,
            width=2,
            textvariable=self.hour_var,
            format_str="%02.0f",
            font=("Arial", 14, "bold"),
            callback=self._on_time_change,
        )
        self.hour_spinbox.pack()

        # Separator
        tk.Label(time_frame, text=":", font=("Arial", 12, "bold")).pack(
            side="left", padx=1, pady=(15, 0)
        )

        # Minute
        minute_frame = tk.Frame(time_frame)
        minute_frame.pack(side="left", padx=2)

        minute_label = lang_get("timepicker.minute", root)
        tk.Label(minute_frame, text=minute_label, font=("Arial", 10)).pack()
        self.minute_spinbox = CustomSpinbox(
            minute_frame,
            from_=0,
            to=59,
            width=2,
            textvariable=self.minute_var,
            format_str="%02.0f",
            font=("Arial", 14, "bold"),
            callback=self._on_time_change,
        )
        self.minute_spinbox.pack()

        # Seconds (if enabled)
        if self.show_seconds:
            tk.Label(time_frame, text=":", font=("Arial", 12, "bold")).pack(
                side="left", padx=1, pady=(15, 0)
            )

            second_frame = tk.Frame(time_frame)
            second_frame.pack(side="left", padx=2)

            second_label = lang_get("timepicker.second", root)
            tk.Label(second_frame, text=second_label, font=("Arial", 10)).pack()
            self.second_spinbox = CustomSpinbox(
                second_frame,
                from_=0,
                to=59,
                width=2,
                textvariable=self.second_var,
                format_str="%02.0f",
                font=("Arial", 14, "bold"),
                callback=self._on_time_change,
            )
            self.second_spinbox.pack()

        # AM/PM (if 12-hour format)
        if self.hour_format == "12":
            am_pm_frame = tk.Frame(time_frame)
            am_pm_frame.pack(side="left", padx=3)

            am_pm_label = lang_get("timepicker.am_pm", root)
            tk.Label(am_pm_frame, text=am_pm_label, font=("Arial", 10)).pack()
            self.am_pm_spinbox = CustomAMPMSpinbox(
                am_pm_frame,
                textvariable=self.am_pm_var,
                font=("Arial", 14, "bold"),
                callback=self._on_time_change,
            )
            self.am_pm_spinbox.pack()

        # Buttons frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=5)

        # OK button
        ok_text = lang_get("timepicker.ok", root)
        self.ok_button = tk.Button(
            button_frame, text=ok_text, command=self._on_ok, width=6
        )
        self.ok_button.pack(side="left", padx=2)

        # Cancel button
        cancel_text = lang_get("timepicker.cancel", root)
        self.cancel_button = tk.Button(
            button_frame, text=cancel_text, command=self._on_cancel, width=6
        )
        self.cancel_button.pack(side="left", padx=2)

    def _bind_events(self):
        """Bind events to widgets."""
        # Bind Enter key to OK
        self.bind("<Return>", lambda e: self._on_ok())
        self.bind("<Escape>", lambda e: self._on_cancel())

        # Bind spinbox events
        self.hour_spinbox.entry.bind("<KeyRelease>", self._on_time_change)
        self.minute_spinbox.entry.bind("<KeyRelease>", self._on_time_change)
        if self.show_seconds:
            self.second_spinbox.entry.bind("<KeyRelease>", self._on_time_change)
        if self.hour_format == "12":
            self.am_pm_spinbox.entry.bind("<KeyRelease>", self._on_time_change)

    def _on_time_change(self, event=None):  # pylint: disable=unused-argument
        """Handle time component changes."""
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            second = int(self.second_var.get()) if self.show_seconds else 0

            if self.hour_format == "12":
                am_pm = self.am_pm_var.get()
                if am_pm == "PM" and hour != 12:
                    hour += 12
                elif am_pm == "AM" and hour == 12:
                    hour = 0

            # Validate time
            if 0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59:
                self.selected_time = datetime.time(hour, minute, second)
        except (ValueError, TypeError):
            pass

    def _on_ok(self):
        """Handle OK button click."""
        self._on_time_change()
        if self.time_callback:
            self.time_callback(self.selected_time)

    def _on_cancel(self):
        """Handle Cancel button click."""
        if self.time_callback:
            self.time_callback(None)

    def get_selected_time(self) -> Optional[datetime.time]:
        """Get the selected time."""
        return self.selected_time

    def set_selected_time(self, time_obj: datetime.time):
        """Set the selected time."""
        self.selected_time = time_obj
        if self.hour_format == "12":
            hour = time_obj.hour
            if hour == 0:
                hour = 12
                am_pm = "AM"
            elif hour < 12:
                am_pm = "AM"
            else:
                if hour > 12:
                    hour -= 12
                am_pm = "PM"
            self.hour_var.set(f"{hour:02d}")
            self.am_pm_var.set(am_pm)
        else:
            self.hour_var.set(f"{time_obj.hour:02d}")

        self.minute_var.set(f"{time_obj.minute:02d}")
        if self.show_seconds:
            self.second_var.set(f"{time_obj.second:02d}")

    def set_hour_format(self, hour_format: str):
        """Set the hour format (12 or 24)."""
        self.hour_format = hour_format
        # Recreate widgets with new format
        for widget in self.winfo_children():
            widget.destroy()
        self._create_widgets()
        self._bind_events()

    def set_show_seconds(self, show_seconds: bool):
        """Set whether to show seconds."""
        self.show_seconds = show_seconds
        # Recreate widgets with new seconds setting
        for widget in self.winfo_children():
            widget.destroy()
        self._create_widgets()
        self._bind_events()
