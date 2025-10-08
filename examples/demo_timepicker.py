#!/usr/bin/env python3
"""
Demo script for tkface TimePicker widgets with code generation.

This script demonstrates the usage of TimeFrame and TimeEntry widgets
with various configurations and generates Python code for the current settings.
"""

import datetime
import logging
import tkinter as tk
from tkinter import ttk

import tkface


class TimePickerDemo:
    def __init__(self):
        # Enable debug logging for investigation
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        )
        self.logger = logging.getLogger(__name__)
        self.root = tk.Tk()
        self.root.title("tkface TimePicker Demo")
        # Hide window initially until setup is complete
        self.root.withdraw()
        # Enable DPI-aware geometry (automatically adjusts window size and configures ttk widgets)
        tkface.win.dpi(self.root)
        # Force update to ensure DPI scaling is applied before setting geometry
        self.root.update_idletasks()
        # Set window size (will be automatically adjusted for DPI if enabled)
        self.root.geometry("600x700")
        # Force another update to ensure geometry is properly applied
        self.root.update_idletasks()

        # Initialize variables
        self.timepicker_type_var = tk.StringVar(value="TimeFrame")
        self.hour_format_var = tk.StringVar(value="24")
        self.show_seconds_var = tk.BooleanVar(value=True)
        self.theme_var = tk.StringVar(value="light")
        self.language_var = tk.StringVar(value="en")
        self.button_text_var = tk.StringVar(value="🕐")
        self.width_var = tk.StringVar(value="15")

        # Initial time setting
        self.initial_time = datetime.datetime.now().time()
        self.is_current_time = True  # Flag to track if initial time is current time

        # Initialize attributes that will be set in create_widgets
        self.timepicker = None

        # Set initial language
        tkface.lang.set("en", self.root)

        self.create_widgets()
        # Final update to ensure all widgets are properly sized
        self.root.update_idletasks()
        # Show window after all setup is complete
        self.root.deiconify()

    def create_widgets(self):
        """Create the TimePicker demo interface."""
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title
        title = tk.Label(
            main_frame,
            text="tkface TimePicker Demo",
            font=("TkDefaultFont", 16, "bold"),
        )
        title.pack(pady=(0, 20))

        # Time Selection Section
        time_frame = tk.LabelFrame(main_frame, text="Time Selection", padx=10, pady=10)
        time_frame.pack(fill="x", pady=(0, 20))

        # TimePicker widget
        entry_row = tk.Frame(time_frame)
        entry_row.pack(fill="x", pady=(0, 10))
        tk.Label(entry_row, text="Sample Time Picker:").pack(side="left")

        # Create TimePicker based on type
        self.create_timepicker(entry_row)

        # Configuration Section
        config_frame = tk.LabelFrame(main_frame, text="Configuration", padx=10, pady=10)
        config_frame.pack(fill="x", pady=(0, 20))

        # Configuration controls - Row 1
        config_row1 = tk.Frame(config_frame)
        config_row1.pack(fill="x", pady=(0, 10))

        # TimePicker type selection
        tk.Label(config_row1, text="TimePicker Type:").pack(side="left")
        type_combo = ttk.Combobox(
            config_row1,
            textvariable=self.timepicker_type_var,
            values=["TimeFrame", "TimeEntry"],
            state="readonly",
            width=10,
        )
        type_combo.pack(side="left", padx=(5, 20))
        type_combo.bind("<<ComboboxSelected>>", lambda e: self.change_timepicker_type())

        # Configuration controls - Row 1.5 (Hour format and seconds on new line)
        config_row1_5 = tk.Frame(config_frame)
        config_row1_5.pack(fill="x", pady=(0, 10))

        # Hour format selection
        tk.Label(config_row1_5, text="Hour Format:").pack(side="left")
        hour_format_frame = tk.Frame(config_row1_5)
        hour_format_frame.pack(side="left", padx=(5, 20))

        tk.Radiobutton(
            hour_format_frame,
            text="24-hour",
            variable=self.hour_format_var,
            value="24",
            command=self.update_timepicker,
        ).pack(side="left", padx=(0, 10))

        tk.Radiobutton(
            hour_format_frame,
            text="12-hour",
            variable=self.hour_format_var,
            value="12",
            command=self.update_timepicker,
        ).pack(side="left")

        # Show seconds checkbox
        self.show_seconds_check = tk.Checkbutton(
            config_row1_5,
            text="Show Seconds",
            variable=self.show_seconds_var,
            command=self.update_timepicker,
        )
        self.show_seconds_check.pack(side="left", padx=(0, 20))

        # Configuration controls - Row 1.7 (Theme selection)
        config_row1_7 = tk.Frame(config_frame)
        config_row1_7.pack(fill="x", pady=(0, 10))

        # Theme selection
        tk.Label(config_row1_7, text="Theme:").pack(side="left")
        theme_frame = tk.Frame(config_row1_7)
        theme_frame.pack(side="left", padx=(5, 20))

        tk.Radiobutton(
            theme_frame,
            text="Light",
            variable=self.theme_var,
            value="light",
            command=self.change_theme,
        ).pack(side="left", padx=(0, 10))

        tk.Radiobutton(
            theme_frame,
            text="Dark",
            variable=self.theme_var,
            value="dark",
            command=self.change_theme,
        ).pack(side="left")

        # Configuration controls - Row 2
        config_row2 = tk.Frame(config_frame)
        config_row2.pack(fill="x", pady=(0, 10))

        # Language selection
        tk.Label(config_row2, text="Language:").pack(side="left")
        lang_combo = ttk.Combobox(
            config_row2,
            textvariable=self.language_var,
            values=["en", "ja"],
            state="readonly",
            width=8,
        )
        lang_combo.pack(side="left", padx=(5, 20))
        lang_combo.bind("<<ComboboxSelected>>", lambda e: self.change_language())

        # Button text entry (only for TimeFrame type)
        tk.Label(config_row2, text="Button Text:").pack(side="left")
        self.button_text_entry = tk.Entry(
            config_row2,
            textvariable=self.button_text_var,
            width=8,
        )
        self.button_text_entry.pack(side="left", padx=(5, 20))
        self.button_text_entry.bind("<KeyRelease>", lambda e: self.change_button_text())
        # Also watch variable changes to be robust across IME/Key event differences
        try:
            self.button_text_var.trace_add(
                "write",
                lambda *_: (
                    self.logger.debug("trace button_text_var -> change_button_text"),
                    self.change_button_text(),
                ),
            )
        except Exception as exc:  # pylint: disable=broad-except
            self.logger.debug("Failed to add trace on button_text_var: %s", exc)
        # Install detailed debug bindings to detect user intent (click/focus/keys)
        self._install_field_debug("ButtonText", self.button_text_entry, self.button_text_var)

        # Width entry (for both TimeEntry and TimeFrame types)
        tk.Label(config_row2, text="Width:").pack(side="left")
        self.width_entry = tk.Entry(
            config_row2,
            textvariable=self.width_var,
            width=8,
        )
        self.width_entry.pack(side="left", padx=(5, 20))
        self.width_entry.bind("<KeyRelease>", lambda e: self.change_width())
        # Also watch variable changes (catch paste/programmatic updates as well)
        try:
            self.width_var.trace_add(
                "write",
                lambda *_: (
                    self.logger.debug("trace width_var -> change_width"),
                    self.change_width(),
                ),
            )
        except Exception as exc:  # pylint: disable=broad-except
            self.logger.debug("Failed to add trace on width_var: %s", exc)
        # Install detailed debug bindings
        self._install_field_debug("Width", self.width_entry, self.width_var)


        # Update entry states based on type
        self._update_entry_states()

        # Configuration controls - Row 3 (Initial time setting)
        config_row3 = tk.Frame(config_frame)
        config_row3.pack(fill="x", pady=(0, 10))

        # Initial time setting
        tk.Label(config_row3, text="Initial Time:").pack(side="left")

        # Create initial time picker
        self.create_initial_timepicker(config_row3)

        # Current time button
        self.current_time_button = tk.Button(
            config_row3,
            text="Set Current Time",
            command=self.set_current_time_as_initial,
            width=15,
        )
        self.current_time_button.pack(side="left", padx=(5, 0))

        # Code generation section
        code_frame = tk.LabelFrame(main_frame, text="Generated Code", padx=10, pady=10)
        code_frame.pack(fill="both", expand=True, pady=(10, 0))

        # Code display
        self.code_text = tk.Text(code_frame, height=6, wrap="word", font=("Courier", 9))
        self.code_text.pack(fill="both", expand=True)

        # Result display section
        result_frame = tk.LabelFrame(main_frame, text="Results", padx=10, pady=10)
        result_frame.pack(fill="both", expand=True, pady=(10, 0))

        # Text widget for displaying results
        self.result_text = tk.Text(result_frame, wrap="word", height=4)
        scrollbar = ttk.Scrollbar(
            result_frame, orient=tk.VERTICAL, command=self.result_text.yview
        )
        self.result_text.configure(yscrollcommand=scrollbar.set)

        self.result_text.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Generate initial code
        self.generate_code()

        # Ensure all widgets are properly initialized
        self.root.update_idletasks()

    def create_timepicker(self, parent):
        """Create a new TimePicker widget."""
        # Destroy existing timepicker if it exists
        if self.timepicker:
            self.logger.debug("Destroying existing timepicker: %r", self.timepicker)
            self.timepicker.destroy()

        # Get current format
        hour_format = self.hour_format_var.get()
        show_seconds = self.show_seconds_var.get()
        theme = self.theme_var.get()

        # Build time format string
        if hour_format == "24":
            if show_seconds:
                time_format = "%H:%M:%S"
            else:
                time_format = "%H:%M"
        else:  # 12-hour format
            if show_seconds:
                time_format = "%I:%M:%S %p"
            else:
                time_format = "%I:%M %p"

        # Create TimePicker based on type
        width = int(self.width_var.get()) if self.width_var.get().isdigit() else 15
        language = self.language_var.get()
        self.logger.debug(
            "Creating timepicker type=%s hour_format=%s show_seconds=%s theme=%s lang=%s width=%s",
            self.timepicker_type_var.get(),
            hour_format,
            show_seconds,
            theme,
            language,
            width,
        )
        if self.timepicker_type_var.get() == "TimeFrame":
            self.timepicker = tkface.TimeFrame(
                parent,
                time_format=time_format,
                hour_format=hour_format,
                show_seconds=show_seconds,
                theme=theme,
                language=language,
                time_callback=self.on_time_selected,
                button_text=self.button_text_var.get(),
                width=width,
            )
        else:  # TimeEntry
            self.timepicker = tkface.TimeEntry(
                parent,
                time_format=time_format,
                hour_format=hour_format,
                show_seconds=show_seconds,
                theme=theme,
                language=language,
                time_callback=self.on_time_selected,
                width=width,
            )

        self.timepicker.pack(side="left", padx=(5, 10))
        self.logger.debug("Created timepicker: %r", self.timepicker)

    def create_initial_timepicker(self, parent):
        """Create the initial time picker widget."""
        # Destroy existing initial timepicker if it exists
        if hasattr(self, "initial_timepicker") and self.initial_timepicker:
            self.initial_timepicker.destroy()

        # Create initial time picker
        self.initial_timepicker = tkface.TimeFrame(
            parent,
            time_format="%H:%M:%S",
            hour_format="24",
            show_seconds=True,
            theme=self.theme_var.get(),
            language=self.language_var.get(),
            time_callback=self.on_initial_time_selected,
            button_text="🕐",
            width=12,
            initial_time=self.initial_time,
        )
        # Pack before the current time button to maintain order
        if hasattr(self, "current_time_button"):
            self.initial_timepicker.pack(
                side="left", padx=(5, 10), before=self.current_time_button
            )
        else:
            self.initial_timepicker.pack(side="left", padx=(5, 10))

    def on_time_selected(self, time_obj):
        """Callback function for time selection."""
        if time_obj:
            self.display_result("Time Selected", time_obj.strftime("%H:%M:%S"))
        else:
            self.display_result("Time Selection", "Cancelled")
        self.logger.debug("on_time_selected called with: %r", time_obj)
        self.generate_code()

    def on_initial_time_selected(self, time_obj):
        """Callback function for initial time selection."""
        if time_obj:
            self.initial_time = time_obj
            self.is_current_time = False  # User selected a specific time
            # Recreate main timepicker with new initial time
            if self.timepicker:
                parent = self.timepicker.master
                self.create_timepicker(parent)
            self.display_result("Initial Time Set", time_obj.strftime("%H:%M:%S"))
        else:
            self.display_result("Initial Time Selection", "Cancelled")
        self.generate_code()

    def set_current_time_as_initial(self):
        """Set current time as initial time."""
        current_time = datetime.datetime.now().time()
        self.initial_time = current_time
        self.is_current_time = True  # Mark as current time
        # Recreate both timepickers with new initial time
        if self.timepicker:
            parent = self.timepicker.master
            self.create_timepicker(parent)
        if hasattr(self, "initial_timepicker") and self.initial_timepicker:
            parent = self.initial_timepicker.master
            self.create_initial_timepicker(parent)
        self.display_result(
            "Set Current Time as Initial", current_time.strftime("%H:%M:%S")
        )
        self.generate_code()

    def change_timepicker_type(self):
        """Change the TimePicker type."""
        # Recreate TimePicker with new type
        parent = self.timepicker.master if self.timepicker else None
        if parent:
            self.create_timepicker(parent)

        # Update entry states
        self._update_entry_states()
        self.generate_code()

    def update_timepicker(self):
        """Update the TimePicker with new format."""
        # Recreate TimePicker with new format
        parent = self.timepicker.master if self.timepicker else None
        if parent:
            self.create_timepicker(parent)

        self.generate_code()

    def change_button_text(self):
        """Change the button text."""
        self.logger.debug(
            "change_button_text invoked; current text entry=%r",
            self.button_text_var.get(),
        )
        if self.timepicker_type_var.get() == "TimeFrame" and self.timepicker:
            button_text = self.button_text_var.get()
            self.logger.debug("Calling set_button_text(%r) on %r", button_text, self.timepicker)
            self.timepicker.set_button_text(button_text)
        self.generate_code()

    def change_width(self):
        """Change the width."""
        self.logger.debug("change_width invoked; raw value=%r", self.width_var.get())
        if self.timepicker:
            width = int(self.width_var.get()) if self.width_var.get().isdigit() else 15
            self.logger.debug("Parsed width=%s; widget=%r", width, self.timepicker)
            # Prefer widget API when available
            if hasattr(self.timepicker, "set_width"):
                self.logger.debug("Calling set_width(%s) on %r", width, self.timepicker)
                self.timepicker.set_width(width)
            else:
                self.logger.debug("Fallback: config(width=%s) on %r", width, self.timepicker)
                self.timepicker.config(width=width)
        self.generate_code()

    def _update_entry_states(self):
        """Update entry states based on TimePicker type."""
        if self.timepicker_type_var.get() == "TimeFrame":
            self.button_text_entry.config(state="normal")
            self.width_entry.config(state="normal")
        else:  # TimeEntry
            self.button_text_entry.config(state="disabled")
            self.width_entry.config(state="normal")

    def display_result(self, action, result):
        """Display the result of an action."""
        self.result_text.insert(tk.END, f"\n=== {action} ===\n")
        self.result_text.insert(tk.END, f"{result}\n")
        self.result_text.see(tk.END)

    def change_language(self):
        """Change the language."""
        lang = self.language_var.get()
        tkface.lang.set(lang, self.root)
        # Recreate TimePicker to reflect language changes
        if self.timepicker:
            parent = self.timepicker.master
            self.create_timepicker(parent)
        # Recreate initial time picker to reflect language changes
        if hasattr(self, "initial_timepicker") and self.initial_timepicker:
            parent = self.initial_timepicker.master
            self.create_initial_timepicker(parent)
        self.generate_code()

    def change_theme(self):
        """Change the theme."""
        # Recreate TimePicker to reflect theme changes
        if self.timepicker:
            parent = self.timepicker.master
            self.create_timepicker(parent)
        # Recreate initial time picker to reflect theme changes
        if hasattr(self, "initial_timepicker") and self.initial_timepicker:
            parent = self.initial_timepicker.master
            self.create_initial_timepicker(parent)
        self.display_result("Theme Changed", self.theme_var.get())
        self.generate_code()

    def generate_code(self):
        """Generate Python code for the current TimePicker configuration."""
        # Build the code string
        timepicker_class = (
            "TimeEntry"
            if self.timepicker_type_var.get() == "TimeEntry"
            else "TimeFrame"
        )

        code_lines = [
            "import tkinter as tk",
            "import tkface",
            "",
        ]

        # Add current time function only if needed
        if self.initial_time and self.is_current_time:
            code_lines.extend(
                [
                    "# Define current time function",
                    "def get_current_time():",
                    "    return datetime.datetime.now().time()",
                    "",
                ]
            )

        code_lines.extend(
            [
                f"# Create {timepicker_class} with current settings:",
                f"timepicker = tkface.{timepicker_class}(",
                "    parent,  # Replace 'parent' with your parent widget",
            ]
        )

        # Get current format
        hour_format = self.hour_format_var.get()
        show_seconds = self.show_seconds_var.get()

        # Build time format string
        if hour_format == "24":
            if show_seconds:
                time_format = "%H:%M:%S"
            else:
                time_format = "%H:%M"
        else:  # 12-hour format
            if show_seconds:
                time_format = "%I:%M:%S %p"
            else:
                time_format = "%I:%M %p"

        code_lines.append(f"    time_format='{time_format}',")
        code_lines.append(f"    hour_format='{hour_format}',")
        code_lines.append(f"    show_seconds={show_seconds},")

        # Add theme if not default
        if self.theme_var.get() != "light":
            code_lines.append(f"    theme='{self.theme_var.get()}',")

        # Add time_callback
        code_lines.append(
            "    time_callback=on_time_selected,  # Define your callback function"
        )

        # Add language if not default
        if self.language_var.get() != "en":
            code_lines.append(f"    language='{self.language_var.get()}',")

        # Add initial time if available
        if self.initial_time:
            if self.is_current_time:
                code_lines.append("    initial_time=get_current_time(),")
            else:
                time_args = (
                    f"{self.initial_time.hour}, {self.initial_time.minute}, "
                    f"{self.initial_time.second}"
                )
                code_lines.append(f"    initial_time=datetime.time({time_args}),")

        # Add optional parameters based on current settings
        width = int(self.width_var.get()) if self.width_var.get().isdigit() else 15
        if self.timepicker_type_var.get() == "TimeFrame":
            # Always include button_text for TimeFrame
            button_text = self.button_text_var.get()
            code_lines.append(f"    button_text='{button_text}',")
            # Always include width for TimeFrame
            code_lines.append(f"    width={width},")
        else:  # TimeEntry
            # Always include width for TimeEntry
            code_lines.append(f"    width={width},")

        code_lines.extend(
            [
                ")",
                "",
                "# Additional setup if needed:",
            ]
        )

        code_lines.extend(
            [
                "if timepicker.get_time():",
                "    print('=== Time Selected ===')",
                "    print(timepicker.get_time())",
            ]
        )

        # Update code display
        self.code_text.delete("1.0", tk.END)
        code_text = "\n".join(code_lines)
        self.code_text.insert("1.0", code_text)

    # ===== Debug helpers =====
    def _install_field_debug(self, name, entry_widget, tk_var):
        """Attach concise debug bindings to an Entry-like widget."""
        # Ensure the widget can take focus when clicked
        try:
            entry_widget.configure(takefocus=1)
        except Exception:  # pylint: disable=broad-except
            pass

        def log_evt(evt_name, event):
            try:
                self.logger.debug(
                    "[%s] %s value=%r focus=%s",
                    name,
                    evt_name,
                    tk_var.get() if hasattr(tk_var, "get") else None,
                    str(entry_widget == entry_widget.focus_get()),
                )
            except Exception as exc:  # pylint: disable=broad-except
                self.logger.debug("[%s] log failed: %s", name, exc)

        def on_button1(event):
            try:
                entry_widget.focus_force()
                entry_widget.after_idle(entry_widget.focus_force)
            except Exception:
                pass
            log_evt("Button-1", event)

        entry_widget.bind("<Button-1>", on_button1, add="+")

        def on_focus_in(event):
            log_evt("FocusIn", event)
            try:
                entry_widget.select_range(0, tk.END)
                entry_widget.icursor(tk.END)
            except Exception:
                pass

        entry_widget.bind("<FocusIn>", on_focus_in, add="+")

    def run(self):
        """Run the demo."""
        self.root.mainloop()


if __name__ == "__main__":
    demo = TimePickerDemo()
    demo.run()
