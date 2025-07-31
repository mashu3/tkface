import tkinter as tk
from tkinter import simpledialog as tk_simpledialog
import tkface
from tkface import simpledialog as tkface_simpledialog

# Enable DPI awareness only on Windows
try:
    tkface.win.dpi()
except Exception:
    pass

# Note: tkface.Button provides Windows-specific flat styling
# On Windows: flat appearance (no shadow)
# On non-Windows: standard button styling

def main():
    root = tk.Tk()
    root.title("tkface simpledialog demo")
    width, height = 650, 500
    # If DPI awareness is enabled on Windows, adjust window size by scaling factor
    scaling = tkface.win.get_scaling_factor(root)
    if scaling > 1.0:
        # Adjust window size for Windows DPI scaling
        width = int(width * scaling * 0.75)
        height = int(height * scaling * 0.75)
    root.geometry(f"{width}x{height}")
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

    tk.Label(left_frame, text="tkinter.simpledialog\n(System Default)", font=("Arial", 12, "bold")).pack(pady=(0, 10))

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

    tkface.Button(left_frame, text="askstring", command=tk_askstring).pack(pady=3, fill=tk.X)
    tkface.Button(left_frame, text="askinteger", command=tk_askinteger).pack(pady=3, fill=tk.X)
    tkface.Button(left_frame, text="askfloat", command=tk_askfloat).pack(pady=3, fill=tk.X)

    # Center column: tkface English
    center_frame = tk.Frame(button_frame)
    center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

    tk.Label(center_frame, text="tkface.simpledialog\n(English)", font=("Arial", 12, "bold")).pack(pady=(0, 10))

    # Right column: tkface Japanese
    right_frame = tk.Frame(button_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

    tk.Label(right_frame, text="tkface.simpledialog\n(Japanese)", font=("Arial", 12, "bold")).pack(pady=(0, 10))

    # Functions for tkface English
    def tkface_askstring_en():
        print("=== tkface.simpledialog.askstring (English) ===")
        result = tkface_simpledialog.askstring(message="Enter your name:", title="Input", language="en")
        print(f"Result: {result}")

    def tkface_askinteger_en():
        print("=== tkface.simpledialog.askinteger (English) ===")
        result = tkface_simpledialog.askinteger(message="Enter your age:", title="Input", minvalue=0, maxvalue=120, language="en")
        print(f"Result: {result}")

    def tkface_askfloat_en():
        print("=== tkface.simpledialog.askfloat (English) ===")
        result = tkface_simpledialog.askfloat(message="Enter your height (m):", title="Input", minvalue=0.0, maxvalue=3.0, language="en")
        print(f"Result: {result}")

    def tkface_askfromlistbox_single_en():
        print("=== tkface.simpledialog.askfromlistbox (single selection) ===")
        result = tkface_simpledialog.askfromlistbox(
            message="Choose your favorite color:",
            choices=["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Pink"],
            language="en"
        )
        print(f"Result: {result}")

    def tkface_askfromlistbox_multiple_en():
        print("=== tkface.simpledialog.askfromlistbox (multiple selection) ===")
        result = tkface_simpledialog.askfromlistbox(
            message="Choose your favorite colors (multiple):",
            choices=["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Pink"],
            multiple=True,
            initial_selection=[0, 2],  # Pre-select Red and Green
            language="en"
        )
        print(f"Result: {result}")

    def tkface_custom_position_en():
        print("=== tkface.simpledialog.askstring (custom position) ===")
        x = int(100 * scaling)
        y = int(100 * scaling)
        result = tkface_simpledialog.askstring(
            message="This dialog appears at a custom position",
            title="Custom Position",
            x=x,
            y=y,
            language="en"
        )
        print(f"Result: {result}")

    def tkface_custom_offset_en():
        print("=== tkface.simpledialog.askstring (custom offset) ===")
        x_offset = int(500 * scaling)
        y_offset = int(-300 * scaling)
        result = tkface_simpledialog.askstring(
            message="This dialog appears with an offset from the parent window.",
            title="Custom Offset",
            x_offset=x_offset,
            y_offset=y_offset,
            language="en"
        )
        print(f"Result: {result}")

    # Functions for tkface Japanese
    def tkface_askstring_ja():
        print("=== tkface.simpledialog.askstring (Japanese) ===")
        result = tkface_simpledialog.askstring(message="お名前を入力してください：", title="入力", language="ja")
        print(f"Result: {result}")

    def tkface_askinteger_ja():
        print("=== tkface.simpledialog.askinteger (Japanese) ===")
        result = tkface_simpledialog.askinteger(message="年齢を入力してください：", title="入力", minvalue=0, maxvalue=120, language="ja")
        print(f"Result: {result}")

    def tkface_askfloat_ja():
        print("=== tkface.simpledialog.askfloat (Japanese) ===")
        result = tkface_simpledialog.askfloat(message="身長を入力してください（m）：", title="入力", minvalue=0.0, maxvalue=3.0, language="ja")
        print(f"Result: {result}")

    def tkface_askfromlistbox_single_ja():
        print("=== tkface.simpledialog.askfromlistbox (single selection) ===")
        result = tkface_simpledialog.askfromlistbox(
            message="好きな色を選んでください:",
            choices=["赤", "青", "緑", "黄", "紫", "オレンジ", "ピンク"],
            language="ja"
        )
        print(f"Result: {result}")

    def tkface_askfromlistbox_multiple_ja():
        print("=== tkface.simpledialog.askfromlistbox (multiple selection) ===")
        result = tkface_simpledialog.askfromlistbox(
            message="好きな色を複数選んでください:",
            choices=["赤", "青", "緑", "黄", "紫", "オレンジ", "ピンク"],
            multiple=True,
            initial_selection=[0, 2],  # 最初に「赤」と「緑」を選択
            language="ja"
        )
        print(f"Result: {result}")

    def tkface_custom_position_ja():
        print("=== tkface.simpledialog.askstring (custom position) ===")
        x = int(100 * scaling)
        y = int(100 * scaling)
        result = tkface_simpledialog.askstring(
            message="このダイアログはカスタム位置に表示されます",
            title="カスタム位置",
            x=x,
            y=y,
            language="ja"
        )
        print(f"Result: {result}")

    def tkface_custom_offset_ja():
        print("=== tkface.simpledialog.askstring (custom offset) ===")
        x_offset = int(500 * scaling)
        y_offset = int(-300 * scaling)
        result = tkface_simpledialog.askstring(
            message="このダイアログは親ウィンドウからのオフセットで表示されます",
            title="カスタムオフセット",
            x_offset=x_offset,
            y_offset=y_offset,
            language="ja"
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

    # Center column buttons (English)
    tkface.Button(center_frame, text="askstring (EN)", command=tkface_askstring_en).pack(pady=3, fill=tk.X)
    tkface.Button(center_frame, text="askinteger (EN)", command=tkface_askinteger_en).pack(pady=3, fill=tk.X)
    tkface.Button(center_frame, text="askfloat (EN)", command=tkface_askfloat_en).pack(pady=3, fill=tk.X)
    tkface.Button(center_frame, text="askfromlistbox single (EN)", command=tkface_askfromlistbox_single_en).pack(pady=3, fill=tk.X)
    tkface.Button(center_frame, text="askfromlistbox multiple (EN)", command=tkface_askfromlistbox_multiple_en).pack(pady=3, fill=tk.X)
    tkface.Button(center_frame, text="custom position (EN)", command=tkface_custom_position_en).pack(pady=3, fill=tk.X)
    tkface.Button(center_frame, text="custom offset (EN)", command=tkface_custom_offset_en).pack(pady=3, fill=tk.X)

    # Right column buttons (Japanese)
    tkface.Button(right_frame, text="askstring (JA)", command=tkface_askstring_ja).pack(pady=3, fill=tk.X)
    tkface.Button(right_frame, text="askinteger (JA)", command=tkface_askinteger_ja).pack(pady=3, fill=tk.X)
    tkface.Button(right_frame, text="askfloat (JA)", command=tkface_askfloat_ja).pack(pady=3, fill=tk.X)
    tkface.Button(right_frame, text="askfromlistbox single (JA)", command=tkface_askfromlistbox_single_ja).pack(pady=3, fill=tk.X)
    tkface.Button(right_frame, text="askfromlistbox multiple (JA)", command=tkface_askfromlistbox_multiple_ja).pack(pady=3, fill=tk.X)
    tkface.Button(right_frame, text="custom position (JA)", command=tkface_custom_position_ja).pack(pady=3, fill=tk.X)
    tkface.Button(right_frame, text="custom offset (JA)", command=tkface_custom_offset_ja).pack(pady=3, fill=tk.X)
    tkface.Button(right_frame, text="custom translations", command=tkface_custom_translations).pack(pady=3, fill=tk.X)

    # Footer
    footer_frame = tk.Frame(main_frame)
    footer_frame.pack(fill=tk.X, pady=(20, 0))
    
    footer_text = "Click buttons to test dialogs. Check console for results."
    tk.Label(footer_frame, text=footer_text, font=("Arial", 9), fg="#666666").pack()

    root.mainloop()

if __name__ == "__main__":
    main() 