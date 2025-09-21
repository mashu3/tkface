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
        
        # File type checkboxes
        self.filetype_vars = {
            "Text Files": tk.BooleanVar(value=True),
            "Python Files": tk.BooleanVar(value=True),
            "Image Files": tk.BooleanVar(value=False),
            "Document Files": tk.BooleanVar(value=False),
            "Audio Files": tk.BooleanVar(value=False),
            "Video Files": tk.BooleanVar(value=False)
        }
        
        # File type definitions
        self.filetype_definitions = {
            "Text Files": ("Text files", "*.txt"),
            "Python Files": ("Python files", "*.py"),
            "Image Files": ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
            "Document Files": ("Document files", "*.pdf *.doc *.docx"),
            "Audio Files": ("Audio files", "*.mp3 *.wav *.flac *.aac"),
            "Video Files": ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv")
        }
        
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
        
        # Configuration controls - Row 3 (File Types Checkboxes)
        config_row3 = tk.Frame(config_frame)
        config_row3.pack(fill="x", pady=(0, 10))
        
        # File types label
        ttk.Label(config_row3, text="File Types:").pack(side=tk.LEFT)
        
        # File types checkboxes frame
        filetypes_frame = tk.Frame(config_row3)
        filetypes_frame.pack(side=tk.LEFT, padx=(5, 0), fill="x", expand=True)
        
        # Create checkboxes in two rows
        checkbox_row1 = tk.Frame(filetypes_frame)
        checkbox_row1.pack(fill="x", pady=(0, 5))
        
        checkbox_row2 = tk.Frame(filetypes_frame)
        checkbox_row2.pack(fill="x")
        
        # Row 1 checkboxes (3 items)
        self.text_files_check = ttk.Checkbutton(
            checkbox_row1, 
            text="Text Files", 
            variable=self.filetype_vars["Text Files"],
            command=self.update_filetypes_from_checkboxes
        )
        self.text_files_check.pack(side=tk.LEFT, padx=(0, 15))
        
        self.python_files_check = ttk.Checkbutton(
            checkbox_row1, 
            text="Python Files", 
            variable=self.filetype_vars["Python Files"],
            command=self.update_filetypes_from_checkboxes
        )
        self.python_files_check.pack(side=tk.LEFT, padx=(0, 15))
        
        self.image_files_check = ttk.Checkbutton(
            checkbox_row1, 
            text="Image Files", 
            variable=self.filetype_vars["Image Files"],
            command=self.update_filetypes_from_checkboxes
        )
        self.image_files_check.pack(side=tk.LEFT, padx=(0, 15))
        
        # Row 2 checkboxes (3 items)
        self.document_files_check = ttk.Checkbutton(
            checkbox_row2, 
            text="Document Files", 
            variable=self.filetype_vars["Document Files"],
            command=self.update_filetypes_from_checkboxes
        )
        self.document_files_check.pack(side=tk.LEFT, padx=(0, 15))
        
        self.audio_files_check = ttk.Checkbutton(
            checkbox_row2, 
            text="Audio Files", 
            variable=self.filetype_vars["Audio Files"],
            command=self.update_filetypes_from_checkboxes
        )
        self.audio_files_check.pack(side=tk.LEFT, padx=(0, 15))
        
        self.video_files_check = ttk.Checkbutton(
            checkbox_row2, 
            text="Video Files", 
            variable=self.filetype_vars["Video Files"],
            command=self.update_filetypes_from_checkboxes
        )
        self.video_files_check.pack(side=tk.LEFT, padx=(0, 15))
        
        # Configuration controls - Row 4 (Initial Directory)
        config_row4 = tk.Frame(config_frame)
        config_row4.pack(fill="x", pady=(0, 10))
        
        # Initial directory entry
        ttk.Label(config_row4, text="Initial Dir:").pack(side=tk.LEFT)
        initialdir_entry = ttk.Entry(config_row4, textvariable=self.initialdir_var, width=60)
        initialdir_entry.pack(side=tk.LEFT, padx=(5, 0), fill="x", expand=True)
        initialdir_entry.bind("<KeyRelease>", lambda e: self.generate_code())
        
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
        code_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Code display
        self.code_text = tk.Text(
            code_frame, height=8, wrap="word", font=("Courier", 9)
        )
        self.code_text.pack(fill="both", expand=True)
        
        # Result display section (moved to bottom)
        result_frame = tk.LabelFrame(
            main_frame, text="Selected Items (Result of 'Run Dialog' button)", padx=10, pady=10
        )
        result_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Text widget for displaying results
        self.result_text = tk.Text(result_frame, wrap="word", height=4)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        # Initialize dialog type settings and generate initial code
        self.update_dialog_type()
    
    def test_current_settings(self):
        """Test the current dialog settings."""
        dialog_type = self.dialog_type_var.get()
        
        try:
            # Parse filetypes if provided
            filetypes = None
            if self.filetypes_var.get():
                try:
                    filetypes = eval(self.filetypes_var.get())
                except:
                    # If evaluation fails, use default
                    filetypes = None
            
            # Parse position parameters
            if self.x_var.get() == "None" and self.y_var.get() == "None":
                # Position dialog to the right of the demo window
                self.root.update_idletasks()  # Ensure window is fully rendered
                demo_x = self.root.winfo_x()
                demo_y = self.root.winfo_y()
                demo_width = self.root.winfo_width()
                x_pos = demo_x + demo_width + 10  # 10px offset from right edge
                y_pos = demo_y  # Same vertical position as demo window
            else:
                x_pos = None if self.x_var.get() == "None" else int(self.x_var.get())
                y_pos = None if self.y_var.get() == "None" else int(self.y_var.get())
            
            # Parse parent parameter
            parent = self.root if self.parent_var.get() == "self.root" else eval(self.parent_var.get())
            
            # Execute dialog based on type
            if dialog_type == "askopenfile":
                result = tkface.pathchooser.askopenfile(
                    title=self.title_var.get(),
                    filetypes=filetypes,
                    parent=parent,
                    x=x_pos,
                    y=y_pos,
                    unround=self.unround_var.get()
                )
            elif dialog_type == "askopenfiles":
                result = tkface.pathchooser.askopenfiles(
                    title=self.title_var.get(),
                    filetypes=filetypes,
                    parent=parent,
                    x=x_pos,
                    y=y_pos,
                    unround=self.unround_var.get()
                )
            elif dialog_type == "askdirectory":
                result = tkface.pathchooser.askdirectory(
                    title=self.title_var.get(),
                    parent=parent,
                    x=x_pos,
                    y=y_pos,
                    unround=self.unround_var.get()
                )
            elif dialog_type == "askpath":
                result = tkface.pathchooser.askpath(
                    select=self.select_var.get(),
                    multiple=self.multiple_var.get(),
                    title=self.title_var.get(),
                    filetypes=filetypes,
                    parent=parent,
                    x=x_pos,
                    y=y_pos,
                    unround=self.unround_var.get()
                )
            elif dialog_type == "asksavefile":
                result = tkface.pathchooser.asksavefile(
                    title=self.title_var.get(),
                    initialfile="document.txt",
                    parent=parent,
                    x=x_pos,
                    y=y_pos,
                    unround=self.unround_var.get()
                )
            
            self.display_result(f"Test: {dialog_type}", result)
            
        except Exception as e:
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
        checkboxes = [
            self.text_files_check,
            self.python_files_check,
            self.image_files_check,
            self.document_files_check,
            self.audio_files_check,
            self.video_files_check
        ]
        
        for checkbox in checkboxes:
            checkbox.config(state=state)
    
    def update_filetypes_from_checkboxes(self):
        """Update file types from checkbox selections."""
        selected_types = []
        
        for filetype, var in self.filetype_vars.items():
            if var.get():
                description, pattern = self.filetype_definitions[filetype]
                selected_types.append((description, pattern))
        
        # "All files" is automatically added by PathBrowser when filetypes is None or empty
        
        # Convert to string format
        filetypes_str = str(selected_types)
        self.filetypes_var.set(filetypes_str)
        self.generate_code()
    
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
        if dialog_type == "askopenfile":
            code_lines.append("result = tkface.pathchooser.askopenfile(")
        elif dialog_type == "askopenfiles":
            code_lines.append("result = tkface.pathchooser.askopenfiles(")
        elif dialog_type == "askdirectory":
            code_lines.append("result = tkface.pathchooser.askdirectory(")
        elif dialog_type == "askpath":
            code_lines.append("result = tkface.pathchooser.askpath(")
        elif dialog_type == "asksavefile":
            code_lines.append("result = tkface.pathchooser.asksavefile(")
        
        # Add parameters
        if self.title_var.get():
            code_lines.append(f"    title='{self.title_var.get()}',")
        
        # Add filetypes for appropriate dialogs (not for asksavefile with fixed filename)
        if dialog_type in ["askopenfile", "askopenfiles", "askpath"] and self.filetypes_var.get():
            try:
                # Try to evaluate the filetypes string
                filetypes = eval(self.filetypes_var.get())
                if filetypes:
                    code_lines.append("    filetypes=[")
                    for filetype in filetypes:
                        code_lines.append(f"        {filetype},")
                    code_lines.append("    ],")
            except:
                # If evaluation fails, add as string
                code_lines.append(f"    filetypes={self.filetypes_var.get()},")
        
        # Add select parameter for askpath
        if dialog_type == "askpath" and self.select_var.get() != "file":
            code_lines.append(f"    select='{self.select_var.get()}',")
        
        # Add multiple parameter for askpath
        if dialog_type == "askpath" and self.multiple_var.get():
            code_lines.append("    multiple=True,")
        
        # Add initialfile for asksavefile
        if dialog_type == "asksavefile":
            code_lines.append("    initialfile='document.txt',")
        
        # Add initialdir if specified
        if self.initialdir_var.get():
            code_lines.append(f"    initialdir='{self.initialdir_var.get()}',")
        
        # Add parent parameter
        if self.parent_var.get() != "self.root":
            code_lines.append(f"    parent={self.parent_var.get()},")
        
        # Add position parameters
        if self.x_var.get() != "None":
            code_lines.append(f"    x={self.x_var.get()},")
        if self.y_var.get() != "None":
            code_lines.append(f"    y={self.y_var.get()},")
        
        # Add unround parameter
        if self.unround_var.get():
            code_lines.append("    unround=True")
        
        code_lines.append(")")
        code_lines.extend([
            "",
            "# Handle the result:",
            "if result:",
            "    print('Selected:', result)",
            "else:",
            "    print('Cancelled')"
        ])
        
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
    root.geometry("500x700+0+0")
    # Force another update to ensure geometry is properly applied
    root.update_idletasks()
    # Show window after all setup is complete
    root.deiconify()
    
    app = FileDialogDemo(root)
    
    root.mainloop()


if __name__ == "__main__":
    main()
