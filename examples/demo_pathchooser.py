"""
Demo for tkface pathchooser module.

This demo shows how to use the file and directory selection dialogs.
"""

import datetime
import os
import tkinter as tk
from tkinter import ttk

import tkface


class FileDialogDemo:
    """Demo application for file dialogs."""
    
    def __init__(self, root):
        """Initialize the demo application."""
        self.root = root
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Path Chooser Demo", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Create button frame with grid layout
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Configure grid columns to be equal width
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        # Buttons for different dialog types in a 2-column grid
        ttk.Button(
            button_frame, 
            text="📄 Select Single File", 
            command=self.select_single_file
        ).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        ttk.Button(
            button_frame, 
            text="📄📄 Select Multiple Files", 
            command=self.select_multiple_files
        ).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Button(
            button_frame, 
            text="📁 Select Directory", 
            command=self.select_directory
        ).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        ttk.Button(
            button_frame, 
            text="📄📁 Select File or Directory", 
            command=self.select_file_or_dir
        ).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Button(
            button_frame, 
            text="📝 Select Text Files Only", 
            command=self.select_text_files
        ).grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
        ttk.Button(
            button_frame, 
            text="🎨 Select Image Files", 
            command=self.select_image_files
        ).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Button(
            button_frame, 
            text="💾 Save Text File (Demo)", 
            command=self.save_text_file
        ).grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        
        # Result display
        result_frame = ttk.LabelFrame(main_frame, text="Selected Items", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Text widget for displaying results
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, height=10)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Clear button
        ttk.Button(main_frame, text="Clear Results", command=self.clear_results).pack(pady=10)
    
    def select_single_file(self):
        """Show single file selection dialog."""
        result = tkface.pathchooser.askopenfile(
            title="Select a File",
            filetypes=[
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("All files", "*.*")
            ],
            parent=self.root,
            x=None,  # Center horizontally
            y=None,  # Center vertically
            unround=True  # Enable unround for Windows
        )
        self.display_result("Single File Selection", result)
    
    def select_multiple_files(self):
        """Show multiple file selection dialog."""
        result = tkface.pathchooser.askopenfiles(
            title="Select Multiple Files",
            filetypes=[
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("All files", "*.*")
            ],
            parent=self.root,
            x=None,  # Center horizontally
            y=None,  # Center vertically
            unround=True  # Enable unround for Windows
        )
        self.display_result("Multiple File Selection", result)
    
    def select_directory(self):
        """Show directory selection dialog."""
        result = tkface.pathchooser.askdirectory(
            title="Select a Directory",
            parent=self.root,
            x=None,  # Center horizontally
            y=None,  # Center vertically
            unround=True  # Enable unround for Windows
        )
        self.display_result("Directory Selection", result)
    
    def select_file_or_dir(self):
        """Show file or directory selection dialog."""
        result = tkface.pathchooser.askpath(
            select="both",
            multiple=True,
            title="Select Files or Directories",
            parent=self.root,
            x=None,  # Center horizontally
            y=None,  # Center vertically
            unround=True  # Enable unround for Windows
        )
        self.display_result("File or Directory Selection", result)
    
    def select_text_files(self):
        """Show text file selection dialog."""
        result = tkface.pathchooser.askpath(
            select="file",
            multiple=True,
            filetypes=[("Text files", "*.txt"), ("Log files", "*.log")],
            parent=self.root,
            x=None,  # Center horizontally
            y=None,  # Center vertically
            unround=True  # Enable unround for Windows
        )
        self.display_result("Text File Selection", result)
    
    def select_image_files(self):
        """Show image file selection dialog."""
        result = tkface.pathchooser.askpath(
            select="file",
            multiple=True,
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg")
            ],
            parent=self.root,
            x=None,  # Center horizontally
            y=None,  # Center vertically
            unround=True  # Enable unround for Windows
        )
        self.display_result("Image File Selection", result)
    
    def save_text_file(self):
        """Show text file save dialog and actually save a file."""
        result = tkface.pathchooser.asksavefile(
            title="Save Text File",
            initialfile="document.txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Python files", "*.py")
            ],
            parent=self.root,
            x=None,  # Center horizontally
            y=None,  # Center vertically
            unround=True  # Enable unround for Windows
        )
        
        if result:
            file_path = result[0]
            try:
                # Create sample text content
                content = f"""# Sample Text File
# Created by tkface pathchooser demo
# Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Hello, World!

This is a sample text file created using tkface pathchooser demo.
The file was saved to: {file_path}

Features:
- Multi-line text support
- Unicode characters: こんにちは, 你好, Привет
- Special characters: © ® ™ € £ ¥
- Numbers: 1234567890

This demonstrates the save functionality of tkface pathchooser.
"""
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Show success message
                tkface.messagebox.showinfo(
                    title="Save Successful",
                    message=f"Text file saved successfully!\n\nPath: {file_path}\nSize: {len(content)} characters",
                    master=self.root
                )
                
                self.display_result("Save Text File", [f"✅ Saved: {file_path}"])
                
            except Exception as e:
                error_msg = f"Failed to save file: {e}"
                tkface.messagebox.showerror(
                    title="Save Error",
                    message=error_msg,
                    master=self.root
                )
                self.display_result("Save Text File Error", [f"❌ {error_msg}"])
        else:
            self.display_result("Save Text File", ["Cancelled"])
    

    
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


def main():
    """Main function to run the demo."""
    root = tk.Tk()
    root.title("tkface Path Chooser Demo")
    # Enable DPI-aware geometry (automatically adjusts window size)
    tkface.win.dpi(root)
    # Set window size (will be automatically adjusted for DPI if enabled)
    root.geometry("600x500")
    root.resizable(True, True)
    
    app = FileDialogDemo(root)
    
    root.mainloop()


if __name__ == "__main__":
    main()
