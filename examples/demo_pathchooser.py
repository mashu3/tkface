"""
Demo for tkface pathchooser module.

This demo shows how to use the file and directory selection dialogs.
"""

import tkinter as tk
from tkinter import ttk

import tkface
from tkface.win.dpi import is_windows


class FileDialogDemo:
    """Demo application for file dialogs."""
    
    def __init__(self, root):
        """Initialize the demo application."""
        self.root = root
        
        # Initialize configuration variables
        self.dialog_type_var = tk.StringVar(value="askopenfile")
        self.title_var = tk.StringVar(value="Select a File")
        self.filetypes_var = tk.StringVar(value="[('Text files', '*.txt'), ('Python files', '*.py')]")
        self.select_var = tk.StringVar(value="file")
        self.multiple_var = tk.BooleanVar(value=False)
        self.initialdir_var = tk.StringVar(value="")
        self.parent_var = tk.StringVar(value="self.root")
        self.x_var = tk.StringVar(value="None")
        self.y_var = tk.StringVar(value="None")
        self.unround_var = tk.BooleanVar(value=True)
        
        
        # File type definitions (including "All files")
        self.filetype_definitions = {
            "All Files": ("All files", "*.*"),
            "Text Files": ("Text files", "*.txt"),
            "Python Files": ("Python files", "*.py"),
            "Image Files": ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
            "Document Files": ("Document files", "*.pdf *.doc *.docx"),
            "Audio Files": ("Audio files", "*.mp3 *.wav *.flac *.aac"),
            "Video Files": ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv")
        }
        
        # File type variables for checkboxes
        self.filetype_vars = {}
        for filetype in self.filetype_definitions.keys():
            self.filetype_vars[filetype] = tk.BooleanVar(value=filetype in ["Text Files", "Python Files"])
        
        # File type order (for drag and drop)
        self.filetype_order = list(self.filetype_definitions.keys())
        
        # Main frame
        main_frame = tk.Frame(root)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Title
        title = tk.Label(
            main_frame,
            text="tkface.pathchooser Demo",
            font=("TkDefaultFont", 16, "bold"),
        )
        title.pack(pady=(0, 20))
        
        # Configuration section
        config_frame = tk.LabelFrame(
            main_frame, text="Configuration", padx=10, pady=10
        )
        config_frame.pack(fill="x", pady=(0, 20))
        
        # Configuration controls - Row 1
        config_row1 = tk.Frame(config_frame)
        config_row1.pack(fill="x", pady=(0, 10))
        
        # Dialog type selection
        ttk.Label(config_row1, text="Dialog Type:").pack(side=tk.LEFT)
        dialog_combo = ttk.Combobox(
            config_row1,
            textvariable=self.dialog_type_var,
            values=["askopenfile", "askopenfiles", "askdirectory", "askpath", "asksavefile"],
            state="readonly",
            width=15
        )
        dialog_combo.pack(side=tk.LEFT, padx=(5, 20))
        dialog_combo.bind("<<ComboboxSelected>>", lambda e: self.update_dialog_type())
        
        # Title entry
        ttk.Label(config_row1, text="Title:").pack(side=tk.LEFT)
        title_entry = ttk.Entry(config_row1, textvariable=self.title_var, width=20)
        title_entry.pack(side=tk.LEFT, padx=(5, 20))
        title_entry.bind("<KeyRelease>", lambda e: self.generate_code())
        
        # Configuration controls - Row 2
        config_row2 = tk.Frame(config_frame)
        config_row2.pack(fill="x", pady=(0, 10))
        
        # Select type (for askpath)
        ttk.Label(config_row2, text="Select:").pack(side=tk.LEFT)
        self.select_combo = ttk.Combobox(
            config_row2,
            textvariable=self.select_var,
            values=["file", "directory", "both"],
            state="readonly",
            width=10
        )
        self.select_combo.pack(side=tk.LEFT, padx=(5, 20))
        self.select_combo.bind("<<ComboboxSelected>>", lambda e: self.generate_code())
        
        # Multiple selection checkbox
        self.multiple_check = ttk.Checkbutton(
            config_row2,
            text="Multiple Selection",
            variable=self.multiple_var,
            command=self.generate_code
        )
        self.multiple_check.pack(side=tk.LEFT, padx=(0, 20))
        
        # Unround checkbox (Windows only)
        if is_windows():
            unround_check = ttk.Checkbutton(
                config_row2,
                text="Unround (Windows)",
                variable=self.unround_var,
                command=self.generate_code
            )
            unround_check.pack(side=tk.LEFT)
        
        # Configuration controls - Row 3 (Integrated File Types Management)
        config_row3 = tk.Frame(config_frame)
        config_row3.pack(fill="x", pady=(0, 10))
        
        # File types label
        ttk.Label(config_row3, text="File Types:").pack(side=tk.LEFT)
        
        # File types checkboxes in simple rows
        filetypes_frame = tk.Frame(config_row3)
        filetypes_frame.pack(side=tk.LEFT, padx=(5, 0), fill="x", expand=True)
        
        # Create checkboxes in rows
        checkbox_row1 = tk.Frame(filetypes_frame)
        checkbox_row1.pack(fill="x", pady=(0, 5))
        
        checkbox_row2 = tk.Frame(filetypes_frame)
        checkbox_row2.pack(fill="x")
        
        # Create checkboxes for all file types
        self.filetype_checkboxes = {}
        row1_filetypes = self.filetype_order[:4]  # First 4 filetypes
        row2_filetypes = self.filetype_order[4:]  # Remaining filetypes
        
        # Row 1 checkboxes
        for i, filetype in enumerate(row1_filetypes):
            var = self.filetype_vars[filetype]
            checkbox = ttk.Checkbutton(
                checkbox_row1,
                text=filetype,
                variable=var,
                command=self.update_filetypes_from_checkboxes
            )
            checkbox.pack(side=tk.LEFT, padx=(0, 15))
            self.filetype_checkboxes[filetype] = checkbox
        
        # Row 2 checkboxes
        for i, filetype in enumerate(row2_filetypes):
            var = self.filetype_vars[filetype]
            checkbox = ttk.Checkbutton(
                checkbox_row2,
                text=filetype,
                variable=var,
                command=self.update_filetypes_from_checkboxes
            )
            checkbox.pack(side=tk.LEFT, padx=(0, 15))
            self.filetype_checkboxes[filetype] = checkbox
        
        # Configuration controls - Row 4 (Selected File Types Order)
        config_row4 = tk.Frame(config_frame)
        config_row4.pack(fill="x", pady=(0, 10))
        
        # Selected file types order label
        ttk.Label(config_row4, text="Selected File Types Order:").pack(side=tk.LEFT)
        
        # Selected file types order management frame
        selected_order_frame = tk.Frame(config_row4)
        selected_order_frame.pack(side=tk.LEFT, padx=(5, 0), fill="x", expand=True)
        
        # Selected file types listbox
        self.selected_filetypes_listbox = tk.Listbox(selected_order_frame, height=5, selectmode=tk.SINGLE)
        self.selected_filetypes_listbox.pack(side=tk.LEFT, fill="x", expand=True)
        
        # Selected order control buttons
        selected_order_buttons_frame = tk.Frame(selected_order_frame)
        selected_order_buttons_frame.pack(side=tk.LEFT, padx=(5, 0))
        
        ttk.Label(selected_order_buttons_frame, text="Order:").pack(side=tk.TOP, pady=(0, 5))
        ttk.Button(selected_order_buttons_frame, text="↑", width=4, command=self.move_selected_filetype_up).pack(side=tk.TOP, pady=(0, 2))
        ttk.Button(selected_order_buttons_frame, text="↓", width=4, command=self.move_selected_filetype_down).pack(side=tk.TOP, pady=(0, 2))
        
        # Configuration controls - Row 5 (Initial Directory)
        config_row5 = tk.Frame(config_frame)
        config_row5.pack(fill="x", pady=(0, 10))
        
        # Initial directory entry
        ttk.Label(config_row5, text="Initial Dir:").pack(side=tk.LEFT)
        initialdir_entry = ttk.Entry(config_row5, textvariable=self.initialdir_var, width=60)
        initialdir_entry.pack(side=tk.LEFT, padx=(5, 0), fill="x", expand=True)
        initialdir_entry.bind("<KeyRelease>", lambda e: self.validate_and_generate_code())
        
        # Button frame inside configuration section
        button_frame = tk.Frame(config_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        # Test button
        test_button = ttk.Button(
            button_frame, 
            text="Choose", 
            command=self.test_current_settings
        )
        test_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear results button
        clear_button = ttk.Button(
            button_frame, 
            text="Clear Results", 
            command=self.clear_results
        )
        clear_button.pack(side=tk.LEFT)
        
        # Code generation section
        code_frame = tk.LabelFrame(
            main_frame, text="Generated Code", padx=10, pady=10
        )
        code_frame.pack(fill="x", pady=(10, 0))
        
        # Code display
        self.code_text = tk.Text(
            code_frame, height=12, wrap="word", font=("Courier", 9)
        )
        self.code_text.pack(fill="x")
        
        # Result display section (moved to bottom)
        result_frame = tk.LabelFrame(
            main_frame, text="Selected Items (Result of 'Run Dialog' button)", padx=10, pady=10
        )
        result_frame.pack(fill="x", pady=(10, 0))
        
        # Text widget for displaying results
        self.result_text = tk.Text(result_frame, wrap="word", height=4)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        # Initialize selected filetypes listbox
        self.update_selected_filetypes_listbox()
        
        # Initialize dialog type settings and generate initial code
        self.update_dialog_type()
    
    def _validate_initialdir(self):
        """Validate initial directory if provided. Returns True if valid or empty, False otherwise."""
        import os
        try:
            initialdir_raw = self.initialdir_var.get()
            initialdir = initialdir_raw.strip()
            if not initialdir:  # Empty is valid
                return True

            # Reject multi-line or embedded newlines to avoid dumping logs into message body
            if ("\n" in initialdir) or ("\r" in initialdir):
                tkface.messagebox.showerror(
                    title="Invalid Path",
                    message="Path must be a single line without newlines.",
                    master=self.root,
                )
                return False
            # Prepare safe display string (truncate long text)
            display_path = initialdir
            if len(display_path) > 160:
                display_path = display_path[:160] + "..."
            # Normalize for filesystem checks
            initialdir_fs = os.path.normpath(os.path.expanduser(initialdir))
            if not os.path.exists(initialdir_fs):
                tkface.messagebox.showerror(
                    title="Invalid Path",
                    message=f"Path does not exist: {display_path}",
                    master=self.root,
                )
                return False
            if not os.path.isdir(initialdir_fs):
                tkface.messagebox.showerror(
                    title="Invalid Path",
                    message=f"Not a directory: {display_path}",
                    master=self.root,
                )
                return False
            return True
        except Exception as e:
            # Log detailed error to console
            print(f"Validation error: {e}")
            import traceback
            traceback.print_exc()
            # Show user-friendly error message
            tkface.messagebox.showerror(
                title="Validation Error",
                message="An error occurred while validating the path. Please check the console for details.",
                master=self.root
            )
            return False

    def validate_and_generate_code(self):
        """Validate initial directory and generate code."""
        if self._validate_initialdir():
            self.generate_code()
    
    def _parse_filetypes(self):
        """Parse filetypes from the filetypes variable. Returns parsed filetypes or None."""
        filetypes_value = self.filetypes_var.get()
        if filetypes_value and filetypes_value != "None":
            try:
                return eval(filetypes_value)
            except (SyntaxError, NameError, TypeError, ValueError):
                # If evaluation fails, use default
                return None
        return None

    def _parse_position_params(self):
        """Parse position parameters. Returns tuple (x_pos, y_pos)."""
        if self.x_var.get() == "None" and self.y_var.get() == "None":
            # Position dialog to the right of the demo window
            self.root.update_idletasks()  # Ensure window is fully rendered
            demo_x = self.root.winfo_x()
            demo_y = self.root.winfo_y()
            demo_width = self.root.winfo_width()
            x_pos = demo_x + demo_width + 10  # 10px offset from right edge
            y_pos = demo_y  # Same vertical position as demo window
            return x_pos, y_pos
        x_pos = None if self.x_var.get() == "None" else int(self.x_var.get())
        y_pos = None if self.y_var.get() == "None" else int(self.y_var.get())
        return x_pos, y_pos

    def _parse_parent_param(self):
        """Parse parent parameter. Returns parent widget."""
        return self.root if self.parent_var.get() == "self.root" else eval(self.parent_var.get())

    def _get_initialdir_value(self):
        """Get initialdir value or None if empty."""
        initialdir = self.initialdir_var.get()
        return initialdir if initialdir else None

    def _execute_dialog(self, dialog_type, filetypes, parent, x_pos, y_pos):
        """Execute dialog based on type. Returns dialog result."""
        initialdir = self._get_initialdir_value()
        common_params = {
            "title": self.title_var.get(),
            "initialdir": initialdir,
            "parent": parent,
            "x": x_pos,
            "y": y_pos,
            "unround": self.unround_var.get()
        }

        if dialog_type == "askopenfile":
            return tkface.pathchooser.askopenfile(
                filetypes=filetypes,
                **common_params
            )
        if dialog_type == "askopenfiles":
            return tkface.pathchooser.askopenfiles(
                filetypes=filetypes,
                **common_params
            )
        if dialog_type == "askdirectory":
            return tkface.pathchooser.askdirectory(**common_params)
        if dialog_type == "askpath":
            return tkface.pathchooser.askpath(
                select=self.select_var.get(),
                multiple=self.multiple_var.get(),
                filetypes=filetypes,
                **common_params
            )
        if dialog_type == "asksavefile":
            return tkface.pathchooser.asksavefile(
                initialfile="document.txt",
                **common_params
            )
        return None

    def test_current_settings(self):
        """Test the current dialog settings."""
        if not self._validate_initialdir():
            return

        dialog_type = self.dialog_type_var.get()

        try:
            filetypes = self._parse_filetypes()
            x_pos, y_pos = self._parse_position_params()
            parent = self._parse_parent_param()
            result = self._execute_dialog(dialog_type, filetypes, parent, x_pos, y_pos)
            self.display_result(f"Test: {dialog_type}", result)
        except Exception as e:
            # Log detailed error to console
            print(f"Error executing dialog: {e}")
            import traceback
            traceback.print_exc()
            # Show user-friendly error message
            error_msg = f"Error executing dialog: {e}"
            self.display_result("Error", [f"❌ {error_msg}"])
    
    def display_result(self, dialog_type, result):
        """Display the dialog result."""
        self.result_text.insert(tk.END, f"\n=== {dialog_type} ===\n")
        
        if not result:
            self.result_text.insert(tk.END, "Cancelled or no selection\n")
        else:
            for i, path in enumerate(result, 1):
                self.result_text.insert(tk.END, f"{i}. {path}\n")
        
        self.result_text.see(tk.END)
    
    def clear_results(self):
        """Clear the result display."""
        self.result_text.delete(1.0, tk.END)
    
    def update_dialog_type(self):
        """Update dialog type and related settings."""
        dialog_type = self.dialog_type_var.get()
        
        # Update title based on dialog type
        if dialog_type == "askopenfile":
            self.title_var.set("Select a File")
            self.multiple_var.set(False)
            self.multiple_check.config(state="disabled")
            self.select_combo.config(state="disabled")
            # Enable file type checkboxes
            self._set_filetype_checkboxes_state("normal")
        elif dialog_type == "askopenfiles":
            self.title_var.set("Select Multiple Files")
            self.multiple_var.set(True)
            self.multiple_check.config(state="disabled")
            self.select_combo.config(state="disabled")
            # Enable file type checkboxes
            self._set_filetype_checkboxes_state("normal")
        elif dialog_type == "askdirectory":
            self.title_var.set("Select a Directory")
            self.multiple_var.set(False)
            self.multiple_check.config(state="disabled")
            self.select_combo.config(state="disabled")
            # Disable file type checkboxes (not applicable for directory selection)
            self._set_filetype_checkboxes_state("disabled")
        elif dialog_type == "askpath":
            self.title_var.set("Select Files or Directories")
            self.multiple_var.set(True)
            self.multiple_check.config(state="normal")
            self.select_combo.config(state="readonly")
            # Enable file type checkboxes
            self._set_filetype_checkboxes_state("normal")
        elif dialog_type == "asksavefile":
            self.title_var.set("Save File")
            self.multiple_var.set(False)
            self.multiple_check.config(state="disabled")
            self.select_combo.config(state="disabled")
            # Disable file type checkboxes (not applicable for save file with fixed filename)
            self._set_filetype_checkboxes_state("disabled")
        
        self.generate_code()
    
    def _set_filetype_checkboxes_state(self, state):
        """Set the state of all file type checkboxes."""
        for checkbox in self.filetype_checkboxes.values():
            checkbox.config(state=state)
    
    def update_filetypes_from_checkboxes(self):
        """Update file types from checkbox selections."""
        selected_types = []
        
        # Use the order from filetype_order
        for filetype in self.filetype_order:
            if filetype in self.filetype_vars and self.filetype_vars[filetype].get():
                description, pattern = self.filetype_definitions[filetype]
                selected_types.append((description, pattern))
        
        # Update selected filetypes listbox
        self.update_selected_filetypes_listbox()
        
        # Convert to string format
        filetypes_str = str(selected_types) if selected_types else "None"
        self.filetypes_var.set(filetypes_str)
        
        self.generate_code()
    
    
    def update_selected_filetypes_listbox(self):
        """Update the selected filetypes listbox display."""
        self.selected_filetypes_listbox.delete(0, tk.END)
        
        # Get selected filetypes in order
        selected_filetypes = []
        for filetype in self.filetype_order:
            if filetype in self.filetype_vars and self.filetype_vars[filetype].get():
                selected_filetypes.append(filetype)
        
        # Add to listbox
        for filetype in selected_filetypes:
            self.selected_filetypes_listbox.insert(tk.END, filetype)
    
    def move_selected_filetype_up(self):
        """Move selected filetype up in the selected list."""
        selection = self.selected_filetypes_listbox.curselection()
        if selection and selection[0] > 0:
            index = selection[0]
            # Get the selected filetype from the listbox
            selected_filetype = self.selected_filetypes_listbox.get(index)
            
            # Find its position in the main order
            main_index = self.filetype_order.index(selected_filetype)
            prev_index = None
            
            # Find the previous selected filetype in main order
            for i in range(main_index - 1, -1, -1):
                if self.filetype_order[i] in self.filetype_vars and self.filetype_vars[self.filetype_order[i]].get():
                    prev_index = i
                    break
            
            if prev_index is not None:
                # Swap in main order
                self.filetype_order[main_index], self.filetype_order[prev_index] = \
                    self.filetype_order[prev_index], self.filetype_order[main_index]
                self.update_selected_filetypes_listbox()
                # Keep the same item selected
                self.selected_filetypes_listbox.selection_set(index - 1)
                self.update_filetypes_from_checkboxes()
    
    def move_selected_filetype_down(self):
        """Move selected filetype down in the selected list."""
        selection = self.selected_filetypes_listbox.curselection()
        if selection and selection[0] < self.selected_filetypes_listbox.size() - 1:
            index = selection[0]
            # Get the selected filetype from the listbox
            selected_filetype = self.selected_filetypes_listbox.get(index)
            
            # Find its position in the main order
            main_index = self.filetype_order.index(selected_filetype)
            next_index = None
            
            # Find the next selected filetype in main order
            for i in range(main_index + 1, len(self.filetype_order)):
                if self.filetype_order[i] in self.filetype_vars and self.filetype_vars[self.filetype_order[i]].get():
                    next_index = i
                    break
            
            if next_index is not None:
                # Swap in main order
                self.filetype_order[main_index], self.filetype_order[next_index] = \
                    self.filetype_order[next_index], self.filetype_order[main_index]
                self.update_selected_filetypes_listbox()
                # Keep the same item selected
                self.selected_filetypes_listbox.selection_set(index + 1)
                self.update_filetypes_from_checkboxes()
    
    def _get_function_call_line(self, dialog_type):
        """Get the function call line for the given dialog type."""
        function_map = {
            "askopenfile": "askopenfile",
            "askopenfiles": "askopenfiles",
            "askdirectory": "askdirectory",
            "askpath": "askpath",
            "asksavefile": "asksavefile"
        }
        function_name = function_map.get(dialog_type, "askopenfile")
        return f"result = tkface.pathchooser.{function_name}("

    def _add_title_param(self, code_lines):
        """Add title parameter to code lines if specified."""
        if self.title_var.get():
            code_lines.append(f"    title='{self.title_var.get()}',")

    def _add_filetypes_param(self, code_lines, dialog_type):
        """Add filetypes parameter to code lines if applicable."""
        if dialog_type not in ["askopenfile", "askopenfiles", "askpath"]:
            return
        if not self.filetypes_var.get():
            return

        filetypes_value = self.filetypes_var.get()
        if filetypes_value == "None":
            # Don't add filetypes parameter when None (will use default "All files")
            return

        try:
            # Try to evaluate the filetypes string
            filetypes = eval(filetypes_value)
            if filetypes:
                code_lines.append("    filetypes=[")
                for filetype in filetypes:
                    code_lines.append(f"        {filetype},")
                code_lines.append("    ],")
        except (SyntaxError, NameError, TypeError, ValueError):
            # If evaluation fails, add as string
            code_lines.append(f"    filetypes={filetypes_value},")

    def _add_select_param(self, code_lines, dialog_type):
        """Add select parameter to code lines if applicable."""
        if dialog_type == "askpath" and self.select_var.get() != "file":
            code_lines.append(f"    select='{self.select_var.get()}',")

    def _add_multiple_param(self, code_lines, dialog_type):
        """Add multiple parameter to code lines if applicable."""
        if dialog_type == "askpath" and self.multiple_var.get():
            code_lines.append("    multiple=True,")

    def _add_initialfile_param(self, code_lines, dialog_type):
        """Add initialfile parameter to code lines if applicable."""
        if dialog_type == "asksavefile":
            code_lines.append("    initialfile='document.txt',")

    def _add_initialdir_param(self, code_lines):
        """Add initialdir parameter to code lines if specified."""
        if self.initialdir_var.get():
            code_lines.append(f"    initialdir='{self.initialdir_var.get()}',")

    def _add_parent_param(self, code_lines):
        """Add parent parameter to code lines if not default."""
        if self.parent_var.get() != "self.root":
            code_lines.append(f"    parent={self.parent_var.get()},")

    def _add_position_params(self, code_lines):
        """Add position parameters to code lines if specified."""
        if self.x_var.get() != "None":
            code_lines.append(f"    x={self.x_var.get()},")
        if self.y_var.get() != "None":
            code_lines.append(f"    y={self.y_var.get()},")

    def _add_unround_param(self, code_lines):
        """Add unround parameter to code lines if enabled."""
        if self.unround_var.get():
            code_lines.append("    unround=True")

    def _add_result_handling_code(self, code_lines):
        """Add result handling code to code lines."""
        code_lines.extend([
            "",
            "# Handle the result:",
            "if result:",
            "    print('Selected:', result)",
            "else:",
            "    print('Cancelled')"
        ])

    def generate_code(self):
        """Generate Python code for the current pathchooser configuration."""
        dialog_type = self.dialog_type_var.get()
        
        # Build the code string
        code_lines = [
            "import tkinter as tk",
            "import tkface",
            "",
            f"# Create {dialog_type} with current settings:",
        ]
        
        # Generate the function call
        code_lines.append(self._get_function_call_line(dialog_type))
        
        # Add parameters
        self._add_title_param(code_lines)
        self._add_filetypes_param(code_lines, dialog_type)
        self._add_select_param(code_lines, dialog_type)
        self._add_multiple_param(code_lines, dialog_type)
        self._add_initialfile_param(code_lines, dialog_type)
        self._add_initialdir_param(code_lines)
        self._add_parent_param(code_lines)
        self._add_position_params(code_lines)
        self._add_unround_param(code_lines)
        
        code_lines.append(")")
        self._add_result_handling_code(code_lines)
        
        # Update code display
        self.code_text.delete("1.0", tk.END)
        code_text = "\n".join(code_lines)
        self.code_text.insert("1.0", code_text)


def main():
    """Main function to run the demo."""
    root = tk.Tk()
    root.title("tkface Path Chooser Demo")
    # Hide window initially until setup is complete
    root.withdraw()
    # Enable DPI-aware geometry (automatically adjusts window size)
    tkface.win.dpi(root)
    # Force update to ensure DPI scaling is applied before setting geometry
    root.update_idletasks()
    # Set window size and position (will be automatically adjusted for DPI if enabled)
    root.geometry("500x730+0+0")
    # Force another update to ensure geometry is properly applied
    root.update_idletasks()
    # Show window after all setup is complete
    root.deiconify()
    
    app = FileDialogDemo(root)
    
    root.mainloop()


if __name__ == "__main__":
    main()
