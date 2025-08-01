# Tkface
[![License: MIT](https://img.shields.io/pypi/l/tkface)](https://opensource.org/licenses/MIT)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tkface)](https://pypi.org/project/tkface)
[![GitHub Release](https://img.shields.io/github/release/mashu3/tkface?color=orange)](https://github.com/mashu3/tkface/releases)
[![PyPi Version](https://img.shields.io/pypi/v/tkface?color=yellow)](https://pypi.org/project/tkface/)
[![Downloads](https://static.pepy.tech/badge/tkface)](https://pepy.tech/project/tkface)

**Restore the "face" to your Tkinter!**

A multilingual GUI extension library for Tkinter (tkinter) - bringing back the "face" (interface) that Tkinter left behind.

---

## 📖 Overview

Tkface is a Python library designed to restore and enhance the "face" (user interface) of Tkinter. While Tkinter is a powerful toolkit, its dialogs and user-facing components are minimal and lack friendly interfaces. Tkface fills this gap with multilingual dialogs, advanced message boxes, and Windows-specific features.

- **Completing the Interface**: Tkinter stands for "Tk **inter**face," providing a powerful core for building GUIs. Tk**face** is designed to complement it by providing the user-facing components—the "**face**"—that are essential for a polished user experience but not built into the standard library. It extends Tkinter with ready-to-use, multilingual dialogs and widgets, letting you build sophisticated, user-friendly applications with less effort.
- **Vibe Coding**: Developed with a "Vibe Coding" approach-prioritizing developer joy, rapid prototyping, and a sense of fun. The codebase is hackable, readable, and easy to extend—and so is this document.

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
import tkface

# Simple information dialog
tkface.messagebox.showinfo("Success", "Operation completed successfully!")

# Multilingual support
tkface.messagebox.showerror("Error", "An error has occurred!", language="ja")

# With system sound (Windows only)
tkface.messagebox.showerror("Error", "An error has occurred!", bell=True)

# Confirmation dialog
if tkface.messagebox.askyesno("Confirm", "Do you want to save?"):
    save_file()
```

### Screenshots

| Dialog Type | Windows | macOS |
|-------------|---------|-------|
| **Warning** | <img src="https://raw.githubusercontent.com/mashu3/tkface/main/examples/images/tkface_messagebox_warning_windows.png" width="200px" alt="Warning Dialog"> | <img src="https://raw.githubusercontent.com/mashu3/tkface/main/examples/images/tkface_messagebox_warning_mac.png" width="200px" alt="Warning Dialog"> |
| **Error** | <img src="https://raw.githubusercontent.com/mashu3/tkface/main/examples/images/tkface_messagebox_error_windows.png" width="200px" alt="Error Dialog"> | <img src="https://raw.githubusercontent.com/mashu3/tkface/main/examples/images/tkface_messagebox_error_mac.png" width="200px" alt="Error Dialog"> |
| **Information** | <img src="https://raw.githubusercontent.com/mashu3/tkface/main/examples/images/tkface_messagebox_info_windows.png" width="200px" alt="Info Dialog"> | <img src="https://raw.githubusercontent.com/mashu3/tkface/main/examples/images/tkface_messagebox_info_mac.png" width="200px" alt="Info Dialog"> |
| **Question** | <img src="https://raw.githubusercontent.com/mashu3/tkface/main/examples/images/tkface_messagebox_question_windows.png" width="200px" alt="Question Dialog"> | <img src="https://raw.githubusercontent.com/mashu3/tkface/main/examples/images/tkface_messagebox_question_mac.png" width="200px" alt="Question Dialog"> |

### Input Dialogs

```python
import tkface

# String input
name = tkface.simpledialog.askstring("Name", "Enter your name:")

# Integer input with validation
age = tkface.simpledialog.askinteger("Age", "Enter your age:", minvalue=0, maxvalue=120)

# List selection dialog
color = tkface.simpledialog.askfromlistbox("Choose a color:", choices=["Red", "Green", "Blue"])

# Multiple selection dialog
colors = tkface.simpledialog.askfromlistbox("Choose colors:", choices=["Red", "Green", "Blue"], multiple=True)
```

### Calendar Widget

#### Screenshots

| Widget Type | Windows | macOS |
|-------------|---------|-------|
| **DateEntry** | <img src="https://raw.githubusercontent.com/mashu3/tkface/main/examples/images/tkface_calendar_dateentry_windows.png" width="200px" alt="DateEntry Widget"> | <img src="https://raw.githubusercontent.com/mashu3/tkface/main/examples/images/tkface_calendar_dateentry_mac.png" width="200px" alt="DateEntry Widget"> |

#### Usage Examples

```python
import tkinter as tk
import tkface

root = tk.Tk()
root.title("Calendar Demo")

# Basic calendar
calendar = tkface.calendar.Calendar(root, year=2024, month=1)
calendar.pack(padx=10, pady=10)

# Advanced calendar with multiple months and features
calendar = tkface.calendar.Calendar(
    root,
    year=2024,
    month=1,
    months=3,                    # Display 3 months horizontally
    show_week_numbers=True,      # Show week numbers
    week_start="Monday",         # Start week on Monday
    day_colors={                 # Color weekends
        "Sunday": "lightcoral",
        "Saturday": "lightblue"
    },
    holidays={                   # Highlight holidays
        "2024-01-01": "red",     # New Year's Day
        "2024-01-15": "blue"     # Custom holiday
    }
)
calendar.pack(padx=10, pady=10)

# Change language
tkface.lang.set("ja", root)  # Japanese
calendar._update_display()   # Refresh display

root.mainloop()
```

### Windows-Specific Features

#### DPI Awareness and Scaling

```python
import tkinter as tk
import tkface

root = tk.Tk()

# Enable DPI awareness and automatic scaling
tkface.dpi(root)  # Short alias for tkface.win.dpi()

# Or use the full function name
# tkface.win.dpi(root)

# Window geometry is automatically adjusted for DPI
root.geometry("600x400")  # Will be scaled appropriately

# UI elements are automatically scaled
button = tkface.Button(root, text="Scaled Button")
button.pack()

root.mainloop()
```

#### Other Windows Features

```python
import tkinter as tk
import tkface

root = tk.Tk()
tkface.win.dpi(root)         # Enable DPI awareness (Windows only)
tkface.win.unround(root)     # Disable corner rounding (Windows 11 only)
tkface.win.bell("error")     # Play Windows system sound (Windows only)

# Windows-specific flat button styling
button = tkface.Button(root, text="Flat Button", command=callback)  # No shadow on Windows
root.mainloop()
```

> **Note**: All Windows-specific features gracefully degrade on non-Windows platforms.

### Language Management

```python
import tkface
import tkinter as tk

root = tk.Tk()
tkface.lang.set("ja", root)  # Set language manually
tkface.lang.set("auto", root)  # Auto-detect system language

# Register custom translations
custom_translations = {
    "ja": {
        "Custom Message": "カスタムメッセージ",
        "Custom Button": "カスタムボタン"
    }
}
tkface.simpledialog.askfromlistbox(
    "Choose an option:",
    choices=["Option 1", "Option 2", "Option 3"],
    custom_translations=custom_translations,
    language="ja"
)
```

---

## 🧩 Features

- **Multilingual Support**: Automatic language detection, English/Japanese built-in, custom dictionaries
- **Enhanced Message Boxes**: All standard and advanced dialogs, custom positioning, keyboard shortcuts, tab navigation
- **Enhanced Input Dialogs**: String/integer/float input, validation, password input, list selection, custom positioning
- **Calendar Widget**: Multi-month display, week numbers, holiday highlighting, customizable colors, language support
- **Windows Features**: 
  - **DPI Awareness**: Automatic scaling for high-resolution displays
  - **Windows 11 Corner Rounding Control**: Modern UI appearance
  - **Windows System Sounds**: Platform-specific audio feedback
  - **Flat Button Styling**: Modern appearance without shadows
  - All features gracefully degrade on other OS

---

## 📁 Examples

See the `examples/` directory for complete working examples:

- `demo_messagebox.py` - Message box demonstrations
- `demo_simpledialog.py` - Input dialog demonstrations
- `demo_calendar.py` - Calendar widget demonstrations

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

## 👨‍💻 Author
[mashu3](https://github.com/mashu3)

[![Authors](https://contrib.rocks/image?repo=mashu3/tkface)](https://github.com/mashu3/tkface/graphs/contributors)