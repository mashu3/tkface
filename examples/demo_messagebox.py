import tkinter as tk
from tkinter import messagebox as tk_messagebox
import tkface
from tkface import messagebox as tkface_messagebox
# Note: tkface.Button provides Windows-specific flat styling
# On Windows: flat appearance (no shadow)
# On non-Windows: standard button styling

def main():
    root = tk.Tk()
    root.title("tkface messagebox demo")
    # Enable DPI-aware geometry (automatically adjusts window size)
    tkface.win.dpi(root)
    # Get scaling factor for custom positioning
    scaling = tkface.win.get_scaling_factor(root)
    # Set window size (will be automatically adjusted for DPI if enabled)
    root.geometry("650x500")
    root.resizable(False, False)
    # Main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    # Button frame (3-column layout)
    button_frame = tk.Frame(main_frame)
    button_frame.pack(fill=tk.BOTH, expand=True)
    # Left column: pure tkinter
    left_frame = tk.Frame(button_frame)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
    tk.Label(
        left_frame,
        text="tkinter.messagebox\n(System Default)",
        font=("Arial", 12, "bold"),
    ).pack(pady=(0, 10))
    # Functions for pure tkinter
    def tk_showerror():
        print("=== tkinter.messagebox.showerror ===")
        result = tk_messagebox.showerror(
            "Error", "An error has occurred.", parent=root
        )
        print(f"Result: {result}")
    def tk_showinfo():
        print("=== tkinter.messagebox.showinfo ===")
        result = tk_messagebox.showinfo(
            "Info", "Operation completed successfully.", parent=root
        )
        print(f"Result: {result}")
    def tk_showwarning():
        print("=== tkinter.messagebox.showwarning ===")
        result = tk_messagebox.showwarning(
            "Warning", "This is a warning message.", parent=root
        )
        print(f"Result: {result}")
    def tk_askquestion():
        print("=== tkinter.messagebox.askquestion ===")
        result = tk_messagebox.askquestion(
            "Question", "Do you want to proceed?", parent=root
        )
        print(f"Result: {result}")
    def tk_askyesno():
        print("=== tkinter.messagebox.askyesno ===")
        result = tk_messagebox.askyesno(
            "Question", "Do you want to proceed?", parent=root
        )
        print(f"Result: {result}")
    def tk_askokcancel():
        print("=== tkinter.messagebox.askokcancel ===")
        result = tk_messagebox.askokcancel(
            "Confirm", "Do you want to save?", parent=root
        )
        print(f"Result: {result}")
    def tk_askyesnocancel():
        print("=== tkinter.messagebox.askyesnocancel ===")
        result = tk_messagebox.askyesnocancel(
            "Question", "Do you want to save before closing?", parent=root
        )
        print(f"Result: {result}")
    def tk_askretrycancel():
        print("=== tkinter.messagebox.askretrycancel ===")
        result = tk_messagebox.askretrycancel(
            "Retry", "Failed to save. Retry?", parent=root
        )
        print(f"Result: {result}")
    tkface.Button(left_frame, text="showerror", command=tk_showerror).pack(
        pady=3, fill=tk.X
    )
    tkface.Button(left_frame, text="showinfo", command=tk_showinfo).pack(
        pady=3, fill=tk.X
    )
    tkface.Button(left_frame, text="showwarning", command=tk_showwarning).pack(
        pady=3, fill=tk.X
    )
    tkface.Button(left_frame, text="askquestion", command=tk_askquestion).pack(
        pady=3, fill=tk.X
    )
    tkface.Button(left_frame, text="askyesno", command=tk_askyesno).pack(
        pady=3, fill=tk.X
    )
    tkface.Button(left_frame, text="askokcancel", command=tk_askokcancel).pack(
        pady=3, fill=tk.X
    )
    tkface.Button(
        left_frame, text="askyesnocancel", command=tk_askyesnocancel
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        left_frame, text="askretrycancel", command=tk_askretrycancel
    ).pack(pady=3, fill=tk.X)
    # Center column: tkface English
    center_frame = tk.Frame(button_frame)
    center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
    tk.Label(
        center_frame,
        text="tkface.messagebox\n(English)",
        font=("Arial", 12, "bold"),
    ).pack(pady=(0, 10))
    # Functions for tkface English
    def tkface_showerror_en():
        print("=== tkface.messagebox.showerror (English) ===")
        result = tkface_messagebox.showerror(
            message="An error has occurred.", language="en", bell=True
        )
        print(f"Result: {result}")
    def tkface_showinfo_en():
        print("=== tkface.messagebox.showinfo (English) ===")
        result = tkface_messagebox.showinfo(
            message="Operation completed successfully.",
            language="en",
            bell=True,
        )
        print(f"Result: {result}")
    def tkface_showwarning_en():
        print("=== tkface.messagebox.showwarning (English) ===")
        result = tkface_messagebox.showwarning(
            message="This is a warning message.", language="en", bell=True
        )
        print(f"Result: {result}")
    def tkface_askquestion_en():
        print("=== tkface.messagebox.askquestion (English) ===")
        result = tkface_messagebox.askquestion(
            message="Do you want to proceed?", language="en", bell=True
        )
        print(f"Result: {result}")
    def tkface_askyesno_en():
        print("=== tkface.messagebox.askyesno (English) ===")
        result = tkface_messagebox.askyesno(
            message="Do you want to proceed?", language="en"
        )
        print(f"Result: {result}")
    def tkface_askokcancel_en():
        print("=== tkface.messagebox.askokcancel (English) ===")
        result = tkface_messagebox.askokcancel(
            message="Do you want to save?", language="en"
        )
        print(f"Result: {result}")
    def tkface_askyesnocancel_en():
        print("=== tkface.messagebox.askyesnocancel (English) ===")
        result = tkface_messagebox.askyesnocancel(
            message="Do you want to save before closing?", language="en"
        )
        print(f"Result: {result}")
    def tkface_askretrycancel_en():
        print("=== tkface.messagebox.askretrycancel (English) ===")
        result = tkface_messagebox.askretrycancel(
            message="Failed to save. Retry?", language="en"
        )
        print(f"Result: {result}")
    def tkface_custom_position_en():
        print("=== tkface.messagebox.showinfo (custom position) ===")
        x = int(100 * scaling)
        y = int(100 * scaling)
        result = tkface_messagebox.showinfo(
            message="This box appears at a custom position.",
            x=x,
            y=y,
            language="en",
        )
        print(f"Result: {result}")
    def tkface_custom_offset_en():
        print("=== tkface.messagebox.showinfo (custom offset) ===")
        x_offset = int(500 * scaling)
        y_offset = int(-300 * scaling)
        result = tkface_messagebox.showinfo(
            message="This box appears with an offset from the parent window.",
            x_offset=x_offset,
            y_offset=y_offset,
            language="en",
        )
        print(f"Result: {result}")
    tkface.Button(
        center_frame, text="showerror (EN)", command=tkface_showerror_en
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        center_frame, text="showinfo (EN)", command=tkface_showinfo_en
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        center_frame, text="showwarning (EN)", command=tkface_showwarning_en
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        center_frame, text="askquestion (EN)", command=tkface_askquestion_en
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        center_frame, text="askyesno (EN)", command=tkface_askyesno_en
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        center_frame, text="askokcancel (EN)", command=tkface_askokcancel_en
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        center_frame,
        text="askyesnocancel (EN)",
        command=tkface_askyesnocancel_en,
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        center_frame,
        text="askretrycancel (EN)",
        command=tkface_askretrycancel_en,
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        center_frame,
        text="custom position (EN)",
        command=tkface_custom_position_en,
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        center_frame,
        text="custom offset (EN)",
        command=tkface_custom_offset_en,
    ).pack(pady=3, fill=tk.X)
    # Right column: tkface Japanese
    right_frame = tk.Frame(button_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
    tk.Label(
        right_frame,
        text="tkface.messagebox\n(Japanese)",
        font=("Arial", 12, "bold"),
    ).pack(pady=(0, 10))
    # Functions for tkface Japanese
    def tkface_showerror_ja():
        print("=== tkface.messagebox.showerror (Japanese) ===")
        result = tkface_messagebox.showerror(
            message="An error has occurred.", language="ja", bell=True
        )
        print(f"Result: {result}")
    def tkface_showinfo_ja():
        print("=== tkface.messagebox.showinfo (Japanese) ===")
        result = tkface_messagebox.showinfo(
            message="Operation completed successfully.",
            language="ja",
            bell=True,
        )
        print(f"Result: {result}")
    def tkface_showwarning_ja():
        print("=== tkface.messagebox.showwarning (Japanese) ===")
        result = tkface_messagebox.showwarning(
            message="This is a warning message.", language="ja", bell=True
        )
        print(f"Result: {result}")
    def tkface_askquestion_ja():
        print("=== tkface.messagebox.askquestion (Japanese) ===")
        result = tkface_messagebox.askquestion(
            message="Do you want to proceed?", language="ja", bell=True
        )
        print(f"Result: {result}")
    def tkface_askyesno_ja():
        print("=== tkface.messagebox.askyesno (Japanese) ===")
        result = tkface_messagebox.askyesno(
            message="Do you want to proceed?", language="ja"
        )
        print(f"Result: {result}")
    def tkface_askokcancel_ja():
        print("=== tkface.messagebox.askokcancel (Japanese) ===")
        result = tkface_messagebox.askokcancel(
            message="Do you want to save?", language="ja"
        )
        print(f"Result: {result}")
    def tkface_askyesnocancel_ja():
        print("=== tkface.messagebox.askyesnocancel (Japanese) ===")
        result = tkface_messagebox.askyesnocancel(
            message="Do you want to save before closing?", language="ja"
        )
        print(f"Result: {result}")
    def tkface_askretrycancel_ja():
        print("=== tkface.messagebox.askretrycancel (Japanese) ===")
        result = tkface_messagebox.askretrycancel(
            message="Failed to save. Retry?", language="ja"
        )
        print(f"Result: {result}")
    def tkface_custom_position_ja():
        print("=== tkface.messagebox.showinfo (custom position) ===")
        x = int(100 * scaling)
        y = int(100 * scaling)
        result = tkface_messagebox.showinfo(
            message="This box appears at a custom position.",
            x=x,
            y=y,
            language="ja",
        )
        print(f"Result: {result}")
    def tkface_custom_offset_ja():
        print("=== tkface.messagebox.showinfo (custom offset) ===")
        x_offset = int(500 * scaling)
        y_offset = int(-300 * scaling)
        result = tkface_messagebox.showinfo(
            message="This box appears with an offset from the parent window.",
            x_offset=x_offset,
            y_offset=y_offset,
            language="ja",
        )
        print(f"Result: {result}")
    tkface.Button(
        right_frame, text="showerror (JA)", command=tkface_showerror_ja
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        right_frame, text="showinfo (JA)", command=tkface_showinfo_ja
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        right_frame, text="showwarning (JA)", command=tkface_showwarning_ja
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        right_frame, text="askquestion (JA)", command=tkface_askquestion_ja
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        right_frame, text="askyesno (JA)", command=tkface_askyesno_ja
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        right_frame, text="askokcancel (JA)", command=tkface_askokcancel_ja
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        right_frame,
        text="askyesnocancel (JA)",
        command=tkface_askyesnocancel_ja,
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        right_frame,
        text="askretrycancel (JA)",
        command=tkface_askretrycancel_ja,
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        right_frame,
        text="custom position (JA)",
        command=tkface_custom_position_ja,
    ).pack(pady=3, fill=tk.X)
    tkface.Button(
        right_frame,
        text="custom offset (JA)",
        command=tkface_custom_offset_ja,
    ).pack(pady=3, fill=tk.X)
    # Footer
    footer_frame = tk.Frame(main_frame)
    footer_frame.pack(fill=tk.X, pady=(20, 0))
    footer_text = (
        "Click buttons to test message boxes. Check console for results."
    )
    tk.Label(
        footer_frame, text=footer_text, font=("Arial", 9), fg="#666666"
    ).pack()
    root.mainloop()
if __name__ == "__main__":
    main()
