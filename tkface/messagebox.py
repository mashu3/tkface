import tkinter as tk
from tkface import lang
from typing import Optional

def _get_or_create_root():
    """
    Get the existing Tk root window or create a new one.
    
    Returns:
        tuple: (root_window, created_flag) where created_flag indicates if a new root was created
    """
    root = getattr(tk, '_default_root', None)
    created = False
    if root is None:
        root = tk.Tk()
        root.withdraw()
        created = True
    return root, created

def _get_button_labels(button_set="ok", root=None, language=None):
    """
    Get button labels for the specified button set with proper translations.
    
    Args:
        button_set (str): The type of button set ("ok", "okcancel", "retrycancel", etc.)
        root: Tkinter root window
        language (str): Language code for translations
        
    Returns:
        list: List of tuples (translated_text, button_value, is_default, is_cancel)
    """
    button_sets = {
        "ok": ["ok"],
        "okcancel": ["ok", "cancel"],
        "retrycancel": ["retry", "cancel"],
        "yesno": ["yes", "no"],
        "yesnocancel": ["yes", "no", "cancel"],
        "abortretryignore": ["abort", "retry", "ignore"]
    }
    keys = button_sets.get(button_set, ["ok"])
    # Return which is default/cancel button
    default_map = {
        "ok": "ok",
        "okcancel": "ok",
        "retrycancel": "retry",
        "yesno": "yes",
        "yesnocancel": "yes",
        "abortretryignore": "abort"
    }
    cancel_map = {
        "okcancel": "cancel",
        "retrycancel": "cancel",
        "yesnocancel": "cancel",
        "abortretryignore": "cancel"
    }
    default_key = default_map.get(button_set, keys[0])
    cancel_key = cancel_map.get(button_set)
    return [(lang.get(key.lower(), root, language=language), key, key == default_key, key == cancel_key) for key in keys]

class CustomMessageBox:
    """
    A custom message box dialog with multilingual support and enhanced features.
    
    This class provides a fully customizable message box that supports multiple
    languages, custom positioning, and various button configurations.
    
    Attributes:
        window: The Toplevel window instance
        result: The result value returned when the dialog is closed
        language: The language code used for translations
    """
    
    def __init__(self, master=None, title: Optional[str] = "Message", message="", icon=None, button_set: Optional[str] = "ok", buttons=None, default=None, cancel=None, x=None, y=None, x_offset=0, y_offset=0, language=None, custom_translations=None):
        """
        Initialize a custom message box.
        
        Args:
            master: Parent window (defaults to tk._default_root)
            title (str): Window title (will be translated if language is set)
            message (str): Message text to display (will be translated if language is set)
            icon (str): Icon to display ("error", "info", "warning", "question", or file path)
            button_set (str): Predefined button set ("ok", "okcancel", "retrycancel", etc.)
            buttons (list): Custom button list as [(label, value), ...]
            default: Default button value
            cancel: Cancel button value
            x (int): X coordinate for window position
            y (int): Y coordinate for window position
            x_offset (int): X offset from calculated position
            y_offset (int): Y offset from calculated position
            language (str): Language code for translations
            custom_translations (dict): Custom translation dictionary
        """
        if master is None:
            master = getattr(tk, '_default_root', None)
            if master is None:
                raise RuntimeError("No Tk root window found. Please create a Tk instance or pass master explicitly.")
        self.language = language
        self.window = tk.Toplevel(master)
        self.window.title(lang.get(title, self.window, language=language))
        self.window.transient(master)
        self.window.grab_set()
        if custom_translations:
            for lang_code, dictionary in custom_translations.items():
                lang.register(lang_code, dictionary, self.window)
        self._create_content(message, icon)
        self.result = None
        self._create_buttons(button_set, buttons, default, cancel)
        self._set_window_position(master, x, y, x_offset, y_offset)
        self.window.lift()
        self.window.focus_set()
        self.window.wait_window()

    def _create_content(self, message, icon):
        """
        Create the main content area with message and icon.
        
        Args:
            message (str): Message text to display
            icon (str): Icon identifier or file path
        """
        frame = tk.Frame(self.window, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        icon_frame = tk.Frame(frame)
        icon_frame.pack(side="left", padx=(0, 10))

        if icon:
            icon_label = self._get_icon_label(icon, icon_frame)
            if icon_label:
                icon_label.pack(side="left")

        message_label = tk.Label(frame, text=message, wraplength=300, justify="left")
        message_label.pack(side="left", fill="both", expand=True)

    def _get_icon_label(self, icon, parent):
        """
        Create an icon label widget.
        
        Args:
            icon (str): Icon identifier or file path
            parent: Parent widget
            
        Returns:
            tk.Label: Icon label widget or None if icon cannot be loaded
        """
        icons = {
            "error": "::tk::icons::error",
            "info": "::tk::icons::information",
            "warning": "::tk::icons::warning",
            "question": "::tk::icons::question"
        }
        if icon in icons:
            return tk.Label(parent, image=icons[icon])
        try:
            icon_image = tk.PhotoImage(file=icon)
            return tk.Label(parent, image=icon_image)
        except Exception:
            return None

    def _create_buttons(self, button_set, buttons, default, cancel):
        """
        Create and configure button widgets.
        
        Args:
            button_set (str): Predefined button set
            buttons (list): Custom button list
            default: Default button value
            cancel: Cancel button value
        """
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=(0, 10))
        self.button_widgets = []
        default_btn = None
        cancel_btn = None
        if buttons:
            for label, value in buttons:
                btn = tk.Button(button_frame, text=label, width=10, command=lambda v=value: self.set_result(v))
                btn.pack(side="left", padx=5)
                self.button_widgets.append((btn, value))
                if value == default:
                    default_btn = btn
                if value == cancel:
                    cancel_btn = btn
            # If default/cancel not specified, use first/last
            if not default_btn and self.button_widgets:
                default_btn = self.button_widgets[0][0]
            if not cancel_btn and self.button_widgets:
                cancel_btn = self.button_widgets[-1][0]
        else:
            for text, value, is_default, is_cancel in _get_button_labels(button_set, self.window, language=self.language):
                btn = tk.Button(button_frame, text=text, width=10, command=lambda v=value: self.set_result(v))
                btn.pack(side="left", padx=5)
                self.button_widgets.append((btn, value))
                if is_default:
                    default_btn = btn
                    # Set as default button (this gives the blue appearance on most systems)
                    btn.configure(default=tk.ACTIVE)
                if is_cancel:
                    cancel_btn = btn
        # Focus only on default button
        if default_btn:
            default_btn.focus_set()
        # Enter triggers default button
        if default_btn:
            self.window.bind("<Return>", lambda e: default_btn.invoke())
        # Esc triggers cancel button
        if cancel_btn:
            self.window.bind("<Escape>", lambda e: cancel_btn.invoke())
        # Tab navigation
        for i, (btn, _) in enumerate(self.button_widgets):
            btn.bind("<Tab>", lambda e, idx=i: self._focus_next(idx))

    def _focus_next(self, idx):
        """
        Move focus to the next button in the tab order.
        
        Args:
            idx (int): Current button index
        """
        next_idx = (idx + 1) % len(self.button_widgets)
        self.button_widgets[next_idx][0].focus_set()

    def _set_window_position(self, master, x=None, y=None, x_offset=0, y_offset=0):
        """
        Set the window position relative to the master window.
        
        Args:
            master: Parent window
            x (int): X coordinate (None for center)
            y (int): Y coordinate (None for center)
            x_offset (int): X offset from calculated position
            y_offset (int): Y offset from calculated position
        """
        self.window.update_idletasks()
        width = self.window.winfo_reqwidth()
        height = self.window.winfo_reqheight()
        if x is None or y is None:
            parent_x = master.winfo_rootx()
            parent_y = master.winfo_rooty()
            parent_width = master.winfo_width()
            parent_height = master.winfo_height()
            x = parent_x + (parent_width - width) // 2
            y = parent_y + (parent_height - height) // 2
        x += x_offset
        y += y_offset
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def set_result(self, value):
        """
        Set the dialog result and close the window.
        
        Args:
            value: The result value to return
        """
        self.result = value
        self.close()

    def close(self):
        """Close the dialog window."""
        self.window.destroy()

    @classmethod
    def show(cls, master=None, message="", title=None, icon=None, button_set=None, buttons=None, default=None, cancel=None, language=None, custom_translations=None, x=None, y=None, x_offset=0, y_offset=0):
        """
        Show a message box dialog and return the result.
        
        This is the main class method for displaying message boxes. It handles
        root window creation/destruction and returns the user's choice.
        
        Args:
            master: Parent window
            message (str): Message text to display
            title (str): Window title
            icon (str): Icon identifier or file path
            button_set (str): Predefined button set
            buttons (list): Custom button list
            default: Default button value
            cancel: Cancel button value
            language (str): Language code for translations
            custom_translations (dict): Custom translation dictionary
            x (int): X coordinate for window position
            y (int): Y coordinate for window position
            x_offset (int): X offset from calculated position
            y_offset (int): Y offset from calculated position
            
        Returns:
            The value corresponding to the button that was clicked
        """
        root, created = _get_or_create_root() if master is None else (master, False)
        lang.set(language or "auto", root)
        result = cls(
            master=root,
            title=lang.get(title, root, language=language) if title else None,
            message=lang.get(message, root, language=language),
            icon=icon,
            button_set=button_set,
            buttons=buttons,
            default=default,
            cancel=cancel,
            language=language,
            custom_translations=custom_translations,
            x=x,
            y=y,
            x_offset=x_offset,
            y_offset=y_offset
        ).result
        if created:
            root.destroy()
        return result

def showinfo(master=None, message="", title=None, language=None, **kwargs):
    """
    Show an information message box.
    
    Args:
        master: Parent window
        message (str): Information message to display
        title (str): Window title (defaults to "Info")
        language (str): Language code for translations
        **kwargs: Additional arguments passed to CustomMessageBox.show
        
    Returns:
        The button value that was clicked (usually "ok")
        
    Example:
        >>> showinfo("Operation completed successfully!", language="ja")
    """
    return CustomMessageBox.show(
        master=master,
        message=message,
        title=title or "Info",
        icon="info",
        button_set="ok",
        language=language,
        **kwargs
    )

def showerror(master=None, message="", title=None, language=None, **kwargs):
    """
    Show an error message box.
    
    Args:
        master: Parent window
        message (str): Error message to display
        title (str): Window title (defaults to "Error")
        language (str): Language code for translations
        **kwargs: Additional arguments passed to CustomMessageBox.show
        
    Returns:
        The button value that was clicked (usually "ok")
        
    Example:
        >>> showerror("An error has occurred!", language="ja")
    """
    return CustomMessageBox.show(
        master=master,
        message=message,
        title=title or "Error",
        icon="error",
        button_set="ok",
        language=language,
        **kwargs
    )

def showwarning(master=None, message="", title=None, language=None, **kwargs):
    """
    Show a warning message box.
    
    Args:
        master: Parent window
        message (str): Warning message to display
        title (str): Window title (defaults to "Warning")
        language (str): Language code for translations
        **kwargs: Additional arguments passed to CustomMessageBox.show
        
    Returns:
        The button value that was clicked (usually "ok")
        
    Example:
        >>> showwarning("This is a warning message!", language="ja")
    """
    return CustomMessageBox.show(
        master=master,
        message=message,
        title=title or "Warning",
        icon="warning",
        button_set="ok",
        language=language,
        **kwargs
    )

def askquestion(master=None, message="", title=None, language=None, **kwargs):
    """
    Show a question dialog with Yes/No buttons.
    
    Args:
        master: Parent window
        message (str): Question message to display
        title (str): Window title (defaults to "Question")
        language (str): Language code for translations
        **kwargs: Additional arguments passed to CustomMessageBox.show
        
    Returns:
        "yes" or "no" depending on which button was clicked
        
    Example:
        >>> result = askquestion("Do you want to proceed?", language="ja")
        >>> if result == "yes":
        ...     print("User chose yes")
    """
    return CustomMessageBox.show(
        master=master,
        message=message,
        title=title or "Question",
        icon="question",
        button_set="yesno",
        language=language,
        **kwargs
    )

def askyesno(master=None, message="", title=None, language=None, **kwargs):
    """
    Show a question dialog with Yes/No buttons.
    
    This function is identical to askquestion() but returns boolean values
    instead of strings for better integration with conditional statements.
    
    Args:
        master: Parent window
        message (str): Question message to display
        title (str): Window title (defaults to "Question")
        language (str): Language code for translations
        **kwargs: Additional arguments passed to CustomMessageBox.show
        
    Returns:
        True for "yes", False for "no"
        
    Example:
        >>> if askyesno("Do you want to save?", language="ja"):
        ...     save_file()
    """
    return CustomMessageBox.show(
        master=master,
        message=message,
        title=title or "Question",
        icon="question",
        button_set="yesno",
        language=language,
        **kwargs
    )

def askokcancel(master=None, message="", title=None, language=None, **kwargs):
    """
    Show a confirmation dialog with OK/Cancel buttons.
    
    Args:
        master: Parent window
        message (str): Confirmation message to display
        title (str): Window title (defaults to "Confirm")
        language (str): Language code for translations
        **kwargs: Additional arguments passed to CustomMessageBox.show
        
    Returns:
        True for "ok", False for "cancel"
        
    Example:
        >>> if askokcancel("Do you want to save?", language="ja"):
        ...     save_file()
    """
    return CustomMessageBox.show(
        master=master,
        message=message,
        title=title or "Confirm",
        icon="question",
        button_set="okcancel",
        language=language,
        **kwargs
    )

def askretrycancel(master=None, message="", title=None, language=None, **kwargs):
    """
    Show a retry dialog with Retry/Cancel buttons.
    
    Args:
        master: Parent window
        message (str): Retry message to display
        title (str): Window title (defaults to "Retry")
        language (str): Language code for translations
        **kwargs: Additional arguments passed to CustomMessageBox.show
        
    Returns:
        "retry" or "cancel" depending on which button was clicked
        
    Example:
        >>> result = askretrycancel("Connection failed. Retry?", language="ja")
        >>> if result == "retry":
        ...     retry_connection()
    """
    return CustomMessageBox.show(
        master=master,
        message=message,
        title=title or "Retry",
        icon="warning",
        button_set="retrycancel",
        language=language,
        **kwargs
    )

def askyesnocancel(master=None, message="", title=None, language=None, **kwargs):
    """
    Show a question dialog with Yes/No/Cancel buttons.
    
    Args:
        master: Parent window
        message (str): Question message to display
        title (str): Window title (defaults to "Question")
        language (str): Language code for translations
        **kwargs: Additional arguments passed to CustomMessageBox.show
        
    Returns:
        "yes", "no", or "cancel" depending on which button was clicked
        
    Example:
        >>> result = askyesnocancel("Save changes?", language="ja")
        >>> if result == "yes":
        ...     save_file()
        >>> elif result == "no":
        ...     discard_changes()
        >>> # else: cancel - do nothing
    """
    return CustomMessageBox.show(
        master=master,
        message=message,
        title=title or "Question",
        icon="question",
        button_set="yesnocancel",
        language=language,
        **kwargs
    )

def askabortretryignore(master=None, message="", title=None, language=None, **kwargs):
    """
    Show a dialog with Abort/Retry/Ignore buttons.
    
    This is typically used for error handling scenarios where the user can
    choose to abort the operation, retry it, or ignore the error.
    
    Args:
        master: Parent window
        message (str): Error message to display
        title (str): Window title (defaults to "Abort")
        language (str): Language code for translations
        **kwargs: Additional arguments passed to CustomMessageBox.show
        
    Returns:
        "abort", "retry", or "ignore" depending on which button was clicked
        
    Example:
        >>> result = askabortretryignore("File access error", language="ja")
        >>> if result == "abort":
        ...     exit_program()
        >>> elif result == "retry":
        ...     retry_file_access()
        >>> # else: ignore - continue with default behavior
    """
    return CustomMessageBox.show(
        master=master,
        message=message,
        title=title or "Abort",
        icon="error",
        button_set="abortretryignore",
        language=language,
        **kwargs
    ) 