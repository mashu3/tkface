import pytest
from unittest.mock import patch
from tkface import messagebox

# A mapping of dialog function names to their expected default titles and icons
DIALOG_CONFIG = {
    "showinfo": ("Info", messagebox.INFO),
    "showwarning": ("Warning", messagebox.WARNING),
    "showerror": ("Error", messagebox.ERROR),
    "askquestion": ("Question", messagebox.QUESTION),
    "askyesno": ("Question", messagebox.QUESTION),
    "askokcancel": ("Confirm", messagebox.QUESTION),
    "askretrycancel": ("Retry", messagebox.WARNING),
    "askyesnocancel": ("Question", messagebox.QUESTION),
}

@pytest.mark.parametrize("func_name, expected_title, expected_icon", [
    (k, v[0], v[1]) for k, v in DIALOG_CONFIG.items()
])
def test_dialog_creation_with_defaults(root, func_name, expected_title, expected_icon):
    """Test that dialogs are created by calling CustomMessageBox with correct defaults."""
    dialog_func = getattr(messagebox, func_name)
    
    # We patch the underlying show method to prevent actual dialog creation
    with patch('tkface.messagebox.CustomMessageBox.show') as mock_show:
        # We need to test the wrapper functions, not the class directly
        if func_name in ['showinfo', 'showerror', 'showwarning']:
             dialog_func(master=root, message="Test message")
             mock_show.assert_called_once()
             args, kwargs = mock_show.call_args
             assert kwargs['icon'] == expected_icon
        else:
             dialog_func(master=root, message="Test message")
    
# --- Test button clicks and return values ---
@pytest.mark.parametrize("func_name, mocked_return, expected_final_return", [
    ("showinfo", "ok", "ok"),
    ("askquestion", "yes", "yes"),
    ("askyesno", "yes", True),
    ("askyesno", "no", False),
    ("askokcancel", "ok", True),
    ("askokcancel", "cancel", False),
    ("askretrycancel", "retry", True),
    ("askretrycancel", "cancel", False),
    ("askyesnocancel", "yes", True),
    ("askyesnocancel", "no", False),
    ("askyesnocancel", "cancel", None),
])
def test_dialog_return_values(root, func_name, mocked_return, expected_final_return):
    """Test the final return value of dialogs, including boolean/None conversion."""
    dialog_func = getattr(messagebox, func_name)

    with patch('tkface.messagebox.CustomMessageBox.show', return_value=mocked_return) as mock_show:
        final_result = dialog_func(master=root, message="Test")
        assert final_result == expected_final_return

# --- Test language support ---
@pytest.mark.parametrize("lang", ["ja", "en"])
def test_language_passed_to_show(root, lang):
    """Test that the language parameter is correctly passed to CustomMessageBox.show."""
    with patch('tkface.messagebox.CustomMessageBox.show') as mock_show:
        messagebox.showinfo(master=root, message="Test", language=lang)
        mock_show.assert_called_once()
        args, kwargs = mock_show.call_args
        assert kwargs['language'] == lang

# --- Test geometry ---
@pytest.mark.parametrize("x, y, x_offset, y_offset", [
    (100, 200, 0, 0),
    (None, None, 50, -30),
])
def test_dialog_positioning_kwargs_passed(root, x, y, x_offset, y_offset):
    """Test that geometry-related kwargs are passed correctly."""
    root.geometry("800x600+0+0")
    
    with patch('tkface.messagebox.CustomMessageBox.show') as mock_show:
        messagebox.showinfo(
            master=root, 
            message="Position test", 
            x=x, y=y, 
            x_offset=x_offset, y_offset=y_offset
        )
        
        mock_show.assert_called_once()
        args, kwargs = mock_show.call_args
        
        assert kwargs.get('x') == x
        assert kwargs.get('y') == y
        assert kwargs.get('x_offset') == x_offset
        assert kwargs.get('y_offset') == y_offset 

@pytest.mark.parametrize("lang", ["ja", "en"])
def test_messagebox_translation_calls(root, lang):
    """Test that lang.get is called for title, message, and buttons."""
    with patch('tkface.lang.get') as mock_lang_get:
        # Assume translated text to be returned
        mock_lang_get.side_effect = lambda key, *a, **kw: f"{key}_{lang}"

        from tkface.messagebox import CustomMessageBox
        with patch('tkinter.Toplevel.wait_window'), \
             patch('tkinter.Label'), \
             patch('tkinter.Button'):
            CustomMessageBox(
                master=root,
                title="Test Title",
                message="Test Message",
                button_set="okcancel",
                language=lang
            )

    # Check if lang.get was called as expected
    calls = mock_lang_get.call_args_list
    
    # Check for calls for Title, ok, and cancel
    assert any(c.args[0] == 'Test Title' for c in calls)
    assert any(c.args[0] == 'ok' for c in calls)
    assert any(c.args[0] == 'cancel' for c in calls)
    # Check if the correct language was specified in all calls
    assert all(c.kwargs['language'] == lang for c in calls) 