# Tkface

**Restore the "face" to your Tkinter!**

A modern, multilingual GUI extension library for Tkinter (tkinter)-bringing back the "face" (interface) that Tkinter left behind.

---

## 📖 Overview

Tkface is a Python library designed to restore and enhance the "face" (user interface) of Tkinter. While Tkinter is a powerful toolkit, its dialogs and user-facing components are minimal and lack modern, friendly interfaces. Tkface fills this gap with beautiful, multilingual dialogs, advanced message boxes, and Windows-specific features.

- **Restore the Face**: "Tkinter" stands for "Tk interface", but ironically, its "face" (user interface) is often lacking. Tkface restores and enhances this missing "face" with beautiful, multilingual dialogs and user-centric design.
- **Vibe Coding**: Developed with a "Vibe Coding" approach-prioritizing developer joy, rapid prototyping, and a sense of fun. The codebase is hackable, readable, and easy to extend.

---

## 🔧 Requirements

- Python 3.7+
- Tkinter (included with Python)
- No additional dependencies

---

## 📦 Installation

Install the latest version from PyPI:

```bash
pip install tkface
```

Or install from the GitHub repository for the latest changes:

```bash
pip install git+https://github.com/mashu3/tkface.git
```

---

## 🚀 Usage

### Message Boxes

```python
from tkface import messagebox

# Simple information dialog
messagebox.showinfo("Success", "Operation completed successfully!")

# Multilingual support
messagebox.showerror("Error", "An error has occurred!", language="ja")

# Confirmation dialog
if messagebox.askyesno("Confirm", "Do you want to save?"):
    save_file()
```

### Input Dialogs

```python
from tkface import simpledialog

# String input
name = simpledialog.askstring("Name", "Enter your name:")

# Integer input with validation
age = simpledialog.askinteger("Age", "Enter your age:", minvalue=0, maxvalue=120)
```

### Windows-Specific Features

```python
import tkinter as tk
from tkface import win

root = tk.Tk()
win.dpi()         # Enable DPI awareness (Windows only)
win.unround(root) # Disable corner rounding (Windows 11 only)
root.mainloop()
```

### Language Management

```python
from tkface import lang
import tkinter as tk

root = tk.Tk()
lang.set("ja", root)  # Set language manually
lang.set("auto", root)  # Auto-detect system language

# Register custom translations
custom_translations = {
    "ja": {
        "Custom Message": "カスタムメッセージ",
        "Custom Button": "カスタムボタン"
    }
}
from tkface import messagebox
messagebox.showinfo(
    "Custom Message",
    "This will be translated",
    custom_translations=custom_translations,
    language="ja"
)
```

---

## 🧩 Features

- **Multilingual Support**: Automatic language detection, English/Japanese built-in, custom dictionaries
- **Enhanced Message Boxes**: All standard and advanced dialogs, custom positioning, keyboard shortcuts, tab navigation
- **Enhanced Input Dialogs**: String/integer/float input, validation, password input, custom positioning
- **Windows Features**: DPI awareness, Windows 11 corner rounding control (no-ops on other OS)

---

## 📁 Examples

See the `examples/` directory for complete working examples:

- `demo_messagebox.py` - Message box demonstrations
- `demo_simpledialog.py` - Input dialog demonstrations

> **Note**: Test files are not included in the public release. For testing, see the development repository.

---

## 🌐 Supported Languages

- **English (en)**: Default, comprehensive translations
- **Japanese (ja)**: Complete Japanese translations

You can add support for any language by providing translation dictionaries:

```python
custom_translations = {
    "fr": {
        "ok": "OK",
        "cancel": "Annuler",
        "yes": "Oui",
        "no": "Non",
        "Error": "Erreur",
        "Warning": "Avertissement"
    }
}
```

---

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 👤 Author

[mashu3](https://github.com/mashu3)

--- 