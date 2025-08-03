import tkinter as tk
from tkinter import ttk
import tkface
import datetime

class DateEntryDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("tkface.calendar DateEntry Demo")
        
        # Enable DPI-aware geometry (automatically adjusts window size)
        tkface.win.dpi(self.root)
        
        # Set window size (will be automatically adjusted for DPI if enabled)
        self.root.geometry("600x700")
        
        # Weekend colors (will be set based on theme)
        self.weekend_colors = {}
        
        # Date formats
        self.date_formats = {
            "Standard": "%Y-%m-%d",
            "European": "%d/%m/%Y",
            "US": "%m/%d/%Y",
            "Japanese": "%Y年%m月%d日",
            "ISO": "%d-%m-%Y"
        }
        
        # Initialize format variable
        self.format_var = tk.StringVar(value="Standard")
        
        # Initialize language variable
        self.lang_var = tk.StringVar(value="en")
        
        # Initialize today color variable
        self.today_color_var = tk.StringVar(value="yellow")
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the DateEntry demo interface."""
        # Initialize year and month variables
        current_date = datetime.date.today()
        self.year_var = tk.IntVar(value=current_date.year)
        self.month_var = tk.IntVar(value=current_date.month)
        
        # Initialize theme variable
        self.theme_var = tk.StringVar(value="light")
        
        # Store previous initial date for comparison
        self.previous_initial_date = current_date
        
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Title
        title = tk.Label(main_frame, text="tkface.calendar DateEntry Demo", 
                        font=('TkDefaultFont', 16, 'bold'))
        title.pack(pady=(0, 20))
        
        # Date Selection Section
        date_frame = tk.LabelFrame(main_frame, text="Date Selection", padx=10, pady=10)
        date_frame.pack(fill='x', pady=(0, 20))
        
        # DateEntry widget
        entry_row = tk.Frame(date_frame)
        entry_row.pack(fill='x', pady=(0, 10))
        
        tk.Label(entry_row, text="Sample Date Entry:").pack(side='left')
        self.dateentry = tkface.DateEntry(
            entry_row, 
            date_format=self.date_formats[self.format_var.get()],
            day_colors=self.weekend_colors,
            holidays={},
            theme="light",
            language=self.lang_var.get(),
            today_color=self.today_color_var.get(),
            year=self.year_var.get(),
            month=self.month_var.get()
        )
        self.dateentry.pack(side='left', padx=(5, 10))
        
        # Set initial date to current date
        self.dateentry.set_selected_date(current_date)
        
        # Configuration Section
        config_frame = tk.LabelFrame(main_frame, text="Configuration", padx=10, pady=10)
        config_frame.pack(fill='x', pady=(0, 20))
        
        # Configuration controls - Row 1
        config_row1 = tk.Frame(config_frame)
        config_row1.pack(fill='x', pady=(0, 10))
        
        # Date format selection
        tk.Label(config_row1, text="Date Format:").pack(side='left')
        format_combo = ttk.Combobox(config_row1, textvariable=self.format_var, 
                                  values=list(self.date_formats.keys()), 
                                  state="readonly", width=12)
        format_combo.pack(side='left', padx=(5, 20))
        format_combo.bind('<<ComboboxSelected>>', lambda e: self.update_dateentry())
        
        # Theme selection
        tk.Label(config_row1, text="Theme:").pack(side='left')
        theme_combo = ttk.Combobox(config_row1, textvariable=self.theme_var, 
                                 values=["light", "dark"], state="readonly", width=8)
        theme_combo.pack(side='left', padx=(5, 20))
        theme_combo.bind('<<ComboboxSelected>>', lambda e: self.change_theme())
        
        # Configuration controls - Row 2 (Language and Week Start)
        config_row2 = tk.Frame(config_frame)
        config_row2.pack(fill='x', pady=(0, 10))
        
        # Language selection
        tk.Label(config_row2, text="Language:").pack(side='left')
        lang_combo = ttk.Combobox(config_row2, textvariable=self.lang_var, 
                                values=["en", "ja"], state="readonly", width=8)
        lang_combo.pack(side='left', padx=(5, 20))
        lang_combo.bind('<<ComboboxSelected>>', lambda e: self.change_language())
        
        # Week start selection
        tk.Label(config_row2, text="Week Start:").pack(side='left')
        self.week_start_var = tk.StringVar(value="Sunday")
        week_combo = ttk.Combobox(config_row2, textvariable=self.week_start_var, 
                                values=["Sunday", "Monday"], state="readonly", width=8)
        week_combo.pack(side='left', padx=(5, 20))
        week_combo.bind('<<ComboboxSelected>>', lambda e: self.change_week_start())
        
        # Configuration controls - Row 3
        config_row3 = tk.Frame(config_frame)
        config_row3.pack(fill='x', pady=(0, 10))
        
        # Weekend colors selection
        tk.Label(config_row3, text="Sunday Color:").pack(side='left')
        self.sunday_color_var = tk.StringVar(value="lightcoral")
        sunday_combo = ttk.Combobox(config_row3, textvariable=self.sunday_color_var, 
                                  values=["lightcoral", "lightpink", "lightblue", "lightgreen", "lightyellow", "lightgray", "gray", "darkgray", "none"], 
                                  state="readonly", width=10)
        sunday_combo.pack(side='left', padx=(5, 10))
        sunday_combo.bind('<<ComboboxSelected>>', lambda e: self.change_weekend_colors())
        
        tk.Label(config_row3, text="Saturday Color:").pack(side='left')
        self.saturday_color_var = tk.StringVar(value="lightblue")
        saturday_combo = ttk.Combobox(config_row3, textvariable=self.saturday_color_var, 
                                    values=["lightblue", "lightcoral", "lightpink", "lightgreen", "lightyellow", "lightgray", "gray", "darkgray", "none"], 
                                    state="readonly", width=10)
        saturday_combo.pack(side='left', padx=(5, 10))
        saturday_combo.bind('<<ComboboxSelected>>', lambda e: self.change_weekend_colors())
        
        # Configuration controls - Row 4
        config_row4 = tk.Frame(config_frame)
        config_row4.pack(fill='x', pady=(0, 10))
        
        # Today color selection
        tk.Label(config_row4, text="Today Color:").pack(side='left')
        today_combo = ttk.Combobox(config_row4, textvariable=self.today_color_var, 
                                 values=["yellow", "orange", "red", "pink", "lightblue", "lightgreen", "lightgray", "none"], 
                                 state="readonly", width=10)
        today_combo.pack(side='left', padx=(5, 20))
        today_combo.bind('<<ComboboxSelected>>', lambda e: self.change_today_color())
        
        # Week numbers checkbox
        self.show_week_var = tk.BooleanVar(value=False)
        week_check = tk.Checkbutton(config_row4, text="Show Week Numbers", 
                                  variable=self.show_week_var, 
                                  command=self.toggle_week_numbers)
        week_check.pack(side='left')
        
        # Configuration controls - Row 5 (Calendar Initial Date)
        config_row5 = tk.Frame(config_frame)
        config_row5.pack(fill='x', pady=(0, 5))
        
        # Calendar Initial Date
        tk.Label(config_row5, text="Initial Date:").pack(side='left')
        self.initial_dateentry = tkface.DateEntry(
            config_row5,
            date_format="%Y-%m-%d",
            theme=self.theme_var.get(),
            language=self.lang_var.get(),
            date_callback=self._on_initial_date_selected
        )
        self.initial_dateentry.pack(side='left', padx=(5, 20))
        
        # Set current date to initial dateentry
        self.initial_dateentry.set_selected_date(current_date)
        
        # Reset to current date button
        reset_button = tk.Button(config_row5, text="Reset to Current Date", 
                               command=self.reset_to_current_date)
        reset_button.pack(side='left', padx=(20, 0))
        
        # Code generation section
        code_frame = tk.LabelFrame(main_frame, text="Generated Code", padx=10, pady=10)
        code_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        # Code display
        self.code_text = tk.Text(code_frame, height=8, wrap='word', font=('Courier', 9))
        self.code_text.pack(fill='both', expand=True)
        
        # Set default weekend colors based on initial theme
        if self.theme_var.get() == "light":
            self.sunday_color_var.set("lightgray")
            self.saturday_color_var.set("lightgray")
        else:
            self.sunday_color_var.set("darkgray")
            self.saturday_color_var.set("darkgray")
        
        # Apply initial weekend colors
        self.change_weekend_colors()
        
        # Generate initial code
        self.generate_code()
        
    def reset_to_current_date(self):
        """Reset the calendar to current date."""
        current_date = datetime.date.today()
        self.initial_dateentry.set_selected_date(current_date)
        self.previous_initial_date = current_date
        self.year_var.set(current_date.year)
        self.month_var.set(current_date.month)
        self.update_calendar_date()
        self.generate_code()
        
    def _on_initial_date_selected(self, date):
        """Handle date selection from initial dateentry."""
        if date and date != self.previous_initial_date:
            self.previous_initial_date = date
            self.year_var.set(date.year)
            self.month_var.set(date.month)
            
            # Set the selected date in the main DateEntry
            self.dateentry.set_selected_date(date)
            
            self.update_calendar_date()
            self.generate_code()
        
    def update_calendar_date(self):
        """Update the calendar with new year and month."""
        # Store current position and parent
        parent = self.dateentry.master
        pack_info = self.dateentry.pack_info()
        
        # Get the selected date from initial dateentry
        initial_selected_date = self.initial_dateentry.get_date()
        
        # Destroy old DateEntry
        self.dateentry.destroy()
        
        # Create new DateEntry with updated year and month
        self.dateentry = tkface.DateEntry(
            parent, 
            date_format=self.date_formats[self.format_var.get()],
            day_colors=self.weekend_colors,
            holidays={},
            theme=self.theme_var.get(),
            language=self.lang_var.get(),
            today_color=self.today_color_var.get(),
            year=self.year_var.get(),
            month=self.month_var.get(),
            show_week_numbers=self.show_week_var.get(),
            week_start=self.week_start_var.get()
        )
        
        # Set the selected date from initial dateentry
        if initial_selected_date:
            self.dateentry.set_selected_date(initial_selected_date)
        
        # Repack with same settings
        self.dateentry.pack(**pack_info)
        
        self.generate_code()
        
    def update_dateentry(self):
        """Update the DateEntry with new format."""
        # Store current position and parent
        parent = self.dateentry.master
        pack_info = self.dateentry.pack_info()
        
        # Get current selected date before destroying
        current_selected_date = self.dateentry.get_date()
        
        # Destroy old DateEntry
        self.dateentry.destroy()
        
        # Create new DateEntry
        new_format = self.date_formats[self.format_var.get()]
        self.dateentry = tkface.DateEntry(
            parent, 
            date_format=new_format,
            day_colors=self.weekend_colors,
            holidays={},
            theme=self.theme_var.get(),
            language=self.lang_var.get(),
            today_color=self.today_color_var.get(),
            year=self.year_var.get(),
            month=self.month_var.get(),
            show_week_numbers=self.show_week_var.get(),
            week_start=self.week_start_var.get()
        )
        
        # Set the selected date if it exists
        if current_selected_date:
            self.dateentry.set_selected_date(current_selected_date)
        
        # Repack with same settings
        self.dateentry.pack(**pack_info)
        
        self.generate_code()
                    
    def change_language(self):
        """Change the calendar language."""
        lang = self.lang_var.get()
        tkface.lang.set(lang, self.root)
        self.dateentry.refresh_language()
        self.generate_code()
        
    def change_theme(self):
        """Change the calendar theme."""
        theme = self.theme_var.get()
        self.dateentry.set_theme(theme)
        
        # Reset weekend colors to default based on theme
        if theme == "light":
            self.sunday_color_var.set("lightgray")
            self.saturday_color_var.set("lightgray")
        else:  # dark theme
            self.sunday_color_var.set("darkgray")
            self.saturday_color_var.set("darkgray")
        
        # Apply the default colors
        self.change_weekend_colors()
        
        self.generate_code()
        
    def change_week_start(self):
        """Change the week start day."""
        week_start = self.week_start_var.get()
        self.dateentry.set_week_start(week_start)
        self.generate_code()
        
    def change_weekend_colors(self):
        """Change the weekend colors."""
        # Update weekend colors dictionary
        self.weekend_colors = {}
        if self.sunday_color_var.get() != "none":
            self.weekend_colors["Sunday"] = self.sunday_color_var.get()
        if self.saturday_color_var.get() != "none":
            self.weekend_colors["Saturday"] = self.saturday_color_var.get()
        
        self.dateentry.set_day_colors(self.weekend_colors)
        self.generate_code()
            
    def change_today_color(self):
        """Change the today color."""
        today_color = self.today_color_var.get()
        self.dateentry.set_today_color(today_color)
        self.generate_code()
            
    def toggle_week_numbers(self):
        """Toggle week numbers on/off."""
        show_week = self.show_week_var.get()
        self.dateentry.set_show_week_numbers(show_week)
        self.generate_code()
            
    def generate_code(self):
        """Generate Python code for the current DateEntry configuration."""
        # Build the code string
        code_lines = [
            "import tkinter as tk",
            "import tkface",
            "",
            "# Create DateEntry with current settings:",
            "dateentry = tkface.DateEntry(",
            f"    parent,  # Replace 'parent' with your parent widget",
            f"    date_format='{self.date_formats[self.format_var.get()]}',",
        ]
        
        # Add year and month if initial date is set
        initial_date = self.initial_dateentry.get_date()
        if initial_date:
            code_lines.append(f"    year={initial_date.year},")
            code_lines.append(f"    month={initial_date.month},")
        
        # Add optional parameters based on current settings
        if self.theme_var.get() != "light":
            code_lines.append(f"    theme='{self.theme_var.get()}',")
            
        if self.lang_var.get() != "en":
            code_lines.append(f"    language='{self.lang_var.get()}',")
            
        if self.week_start_var.get() != "Sunday":
            code_lines.append(f"    week_start='{self.week_start_var.get()}',")
            
        # Add weekend colors if not default
        if self.sunday_color_var.get() != "lightgray" or self.saturday_color_var.get() != "lightgray":
            code_lines.append("    day_colors={")
            if self.sunday_color_var.get() != "lightgray":
                code_lines.append(f"        'Sunday': '{self.sunday_color_var.get()}',")
            if self.saturday_color_var.get() != "lightgray":
                code_lines.append(f"        'Saturday': '{self.saturday_color_var.get()}',")
            code_lines.append("    },")
            
        # Add holidays (only if not empty)
        # Note: holidays parameter is omitted when empty (default behavior)
            
        # Add today color if not default
        if self.today_color_var.get() != "yellow":
            code_lines.append(f"    today_color='{self.today_color_var.get()}',")
            
        # Add week numbers if enabled
        if self.show_week_var.get():
            code_lines.append("    show_week_numbers=True,")
            
        code_lines.extend([
            ")",
            "",
            "# Additional setup if needed:",
        ])
        
        # Add initial date setting if available
        if initial_date:
            code_lines.extend([
                f"# Set initial date",
                f"dateentry.set_selected_date(datetime.date({initial_date.year}, {initial_date.month}, {initial_date.day}))",
                ""
            ])
        
        code_lines.extend([
            "if dateentry.get_date():",
            "    print(f'Selected date: {dateentry.get_date_string()}')",
        ])
        
        # Update code display
        self.code_text.delete('1.0', tk.END)
        self.code_text.insert('1.0', '\n'.join(code_lines))
        
    def run(self):
        """Run the demo."""
        self.root.mainloop()

if __name__ == "__main__":
    demo = DateEntryDemo()
    demo.run() 