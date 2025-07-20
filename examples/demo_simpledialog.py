import tkinter as tk
from tkinter import simpledialog as tk_simpledialog
from tkface import simpledialog as tkface_simpledialog
import platform
from tkface import win

# Enable DPI awareness only on Windows
if platform.system() == "Windows":
    win.dpi()

def main():
    root = tk.Tk()
    root.title("tkface simpledialog demo")
    width, height = 600, 500
    # If DPI awareness is enabled on Windows, enlarge window size by scaling factor
    if platform.system() == "Windows":
        scaling = root.tk.call('tk', 'scaling')
        width = int(width * scaling)
        height = int(height * scaling)
    root.geometry(f"{width}x{height}")
    root.resizable(False, False)

    # Main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Button frame (2-column layout)
    button_frame = tk.Frame(main_frame)
    button_frame.pack(fill=tk.BOTH, expand=True)

    # Left column: pure tkinter
    left_frame = tk.Frame(button_frame)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

    tk.Label(left_frame, text="tkinter.simpledialog", font=("Arial", 12, "bold")).pack(pady=(0, 10))

    # Functions for pure tkinter
    def tk_askstring():
        print("=== tkinter.simpledialog.askstring ===")
        result = tk_simpledialog.askstring("Input", "Enter your name:", parent=root)
        print(f"Result: {result}")

    def tk_askinteger():
        print("=== tkinter.simpledialog.askinteger ===")
        result = tk_simpledialog.askinteger("Input", "Enter your age (0-120):", parent=root, minvalue=0, maxvalue=120)
        print(f"Result: {result}")

    def tk_askfloat():
        print("=== tkinter.simpledialog.askfloat ===")
        result = tk_simpledialog.askfloat("Input", "Enter your height (m):", parent=root, minvalue=0.0, maxvalue=3.0)
        print(f"Result: {result}")

    tk.Button(left_frame, text="askstring", command=tk_askstring).pack(pady=3, fill=tk.X)
    tk.Button(left_frame, text="askinteger", command=tk_askinteger).pack(pady=3, fill=tk.X)
    tk.Button(left_frame, text="askfloat", command=tk_askfloat).pack(pady=3, fill=tk.X)

    # Right column: tkface
    right_frame = tk.Frame(button_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

    tk.Label(right_frame, text="tkface.simpledialog", font=("Arial", 12, "bold")).pack(pady=(0, 10))

    # Functions for tkface
    def tkface_askstring_en():
        print("=== tkface.simpledialog.askstring (English) ===")
        result = tkface_simpledialog.askstring(message="Enter your name:", title="Input", language="en")
        print(f"Result: {result}")

    def tkface_askstring_ja():
        print("=== tkface.simpledialog.askstring (Japanese) ===")
        result = tkface_simpledialog.askstring(message="お名前を入力してください：", title="入力", language="ja")
        print(f"Result: {result}")

    def tkface_askinteger_en():
        print("=== tkface.simpledialog.askinteger (English) ===")
        result = tkface_simpledialog.askinteger(message="Enter your age:", title="Input", minvalue=0, maxvalue=120, language="en")
        print(f"Result: {result}")

    def tkface_askinteger_ja():
        print("=== tkface.simpledialog.askinteger (Japanese) ===")
        result = tkface_simpledialog.askinteger(message="年齢を入力してください：", title="入力", minvalue=0, maxvalue=120, language="ja")
        print(f"Result: {result}")

    def tkface_askfloat_en():
        print("=== tkface.simpledialog.askfloat (English) ===")
        result = tkface_simpledialog.askfloat(message="Enter your height (m):", title="Input", minvalue=0.0, maxvalue=3.0, language="en")
        print(f"Result: {result}")

    def tkface_askfloat_ja():
        print("=== tkface.simpledialog.askfloat (Japanese) ===")
        result = tkface_simpledialog.askfloat(message="身長を入力してください（m）：", title="入力", minvalue=0.0, maxvalue=3.0, language="ja")
        print(f"Result: {result}")

    def tkface_custom_position():
        print("=== tkface.simpledialog.askstring (custom position) ===")
        result = tkface_simpledialog.askstring(
            message="This dialog appears at a custom position",
            title="Custom Position",
            x=100,
            y=100,
            language="en"
        )
        print(f"Result: {result}")

    def tkface_custom_translations():
        print("=== tkface.simpledialog.askstring (custom translations) ===")
        custom_dict = {
            "ja": {
                "ok": "決定",
                "cancel": "中止",
                "Invalid input.": "入力が正しくありません。"
            }
        }
        result = tkface_simpledialog.askstring(
            message="カスタム辞書を使用したダイアログ",
            title="カスタム翻訳",
            language="ja",
            custom_translations=custom_dict
        )
        print(f"Result: {result}")

    # Basic functions section
    basic_frame = tk.Frame(right_frame)
    basic_frame.pack(fill=tk.BOTH, expand=True)
    
    tk.Label(basic_frame, text="Basic Functions", font=("Arial", 10, "bold")).pack(pady=(0, 5))
    
    tk.Button(basic_frame, text="askstring (EN)", command=tkface_askstring_en).pack(pady=2, fill=tk.X)
    tk.Button(basic_frame, text="askstring (JA)", command=tkface_askstring_ja).pack(pady=2, fill=tk.X)
    tk.Button(basic_frame, text="askinteger (EN)", command=tkface_askinteger_en).pack(pady=2, fill=tk.X)
    tk.Button(basic_frame, text="askinteger (JA)", command=tkface_askinteger_ja).pack(pady=2, fill=tk.X)
    tk.Button(basic_frame, text="askfloat (EN)", command=tkface_askfloat_en).pack(pady=2, fill=tk.X)
    tk.Button(basic_frame, text="askfloat (JA)", command=tkface_askfloat_ja).pack(pady=2, fill=tk.X)
    
    # Extensions section
    tk.Label(basic_frame, text="Extensions", font=("Arial", 10, "bold")).pack(pady=(10, 5))
    
    tk.Button(basic_frame, text="custom position", command=tkface_custom_position).pack(pady=2, fill=tk.X)
    tk.Button(basic_frame, text="custom translations", command=tkface_custom_translations).pack(pady=2, fill=tk.X)

    # Footer
    footer_frame = tk.Frame(main_frame)
    footer_frame.pack(fill=tk.X, pady=(20, 0))
    
    footer_text = "Click buttons to test dialogs. Check console for results."
    tk.Label(footer_frame, text=footer_text, font=("Arial", 9), fg="#666666").pack()

    root.mainloop()

if __name__ == "__main__":
    main() 