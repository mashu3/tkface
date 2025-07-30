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
    "askfromlistbox": ("Select", messagebox.QUESTION),
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
        elif func_name == 'askfromlistbox':
            # askfromlistbox requires choices parameter
            dialog_func(master=root, message="Test message", choices=["A", "B", "C"])
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
    ("askfromlistbox", "Red", "Red"),
    ("askfromlistbox", None, None),
])
def test_dialog_return_values(root, func_name, mocked_return, expected_final_return):
    """Test the final return value of dialogs, including boolean/None conversion."""
    dialog_func = getattr(messagebox, func_name)

    with patch('tkface.messagebox.CustomMessageBox.show', return_value=mocked_return) as mock_show:
        if func_name == 'askfromlistbox':
            # askfromlistbox requires choices parameter
            final_result = dialog_func(master=root, message="Test", choices=["A", "B", "C"])
        else:
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

# --- Test askfromlistbox function ---
def test_askfromlistbox_requires_choices(root):
    """Test that askfromlistbox raises ValueError when choices is not provided."""
    with pytest.raises(ValueError, match="choices parameter is required"):
        messagebox.askfromlistbox(master=root, message="Test")

def test_askfromlistbox_single_selection(root):
    """Test askfromlistbox with single selection mode."""
    choices = ["Red", "Green", "Blue"]
    
    with patch('tkface.messagebox.CustomMessageBox.show', return_value="Red") as mock_show:
        result = messagebox.askfromlistbox(
            master=root,
            message="Choose a color:",
            choices=choices
        )
        
        mock_show.assert_called_once()
        args, kwargs = mock_show.call_args
        
        assert kwargs['message'] == "Choose a color:"
        assert kwargs['choices'] == choices
        assert kwargs['multiple'] is False
        assert kwargs['title'] == "Select"
        assert kwargs['icon'] == messagebox.QUESTION
        assert kwargs['button_set'] == "okcancel"
        assert result == "Red"

def test_askfromlistbox_multiple_selection(root):
    """Test askfromlistbox with multiple selection mode."""
    choices = ["Red", "Green", "Blue"]
    initial_selection = [0, 2]
    
    with patch('tkface.messagebox.CustomMessageBox.show', return_value=["Red", "Blue"]) as mock_show:
        result = messagebox.askfromlistbox(
            master=root,
            message="Choose colors:",
            choices=choices,
            multiple=True,
            initial_selection=initial_selection
        )
        
        mock_show.assert_called_once()
        args, kwargs = mock_show.call_args
        
        assert kwargs['message'] == "Choose colors:"
        assert kwargs['choices'] == choices
        assert kwargs['multiple'] is True
        assert kwargs['initial_selection'] == initial_selection
        assert result == ["Red", "Blue"]

def test_askfromlistbox_cancel_returns_none(root):
    """Test that askfromlistbox returns None when cancelled."""
    choices = ["Red", "Green", "Blue"]
    
    with patch('tkface.messagebox.CustomMessageBox.show', return_value=None) as mock_show:
        result = messagebox.askfromlistbox(
            master=root,
            message="Choose a color:",
            choices=choices
        )
        
        assert result is None

def test_askfromlistbox_with_custom_title(root):
    """Test askfromlistbox with custom title."""
    choices = ["Red", "Green", "Blue"]
    
    with patch('tkface.messagebox.CustomMessageBox.show') as mock_show:
        messagebox.askfromlistbox(
            master=root,
            message="Choose a color:",
            title="Custom Title",
            choices=choices
        )
        
        mock_show.assert_called_once()
        args, kwargs = mock_show.call_args
        assert kwargs['title'] == "Custom Title"

def test_askfromlistbox_language_support(root):
    """Test that askfromlistbox passes language parameter correctly."""
    choices = ["Red", "Green", "Blue"]
    
    with patch('tkface.messagebox.CustomMessageBox.show') as mock_show:
        messagebox.askfromlistbox(
            master=root,
            message="Choose a color:",
            choices=choices,
            language="ja"
        )
        
        mock_show.assert_called_once()
        args, kwargs = mock_show.call_args
        assert kwargs['language'] == "ja"

# --- Test CustomMessageBox selection functionality ---
def test_custom_messagebox_selection_single(root):
    """Test CustomMessageBox with single selection."""
    from tkface.messagebox import CustomMessageBox
    
    with patch('tkinter.Toplevel.wait_window'), \
         patch('tkinter.Listbox'), \
         patch('tkinter.Button'):
        
        dialog = CustomMessageBox(
            master=root,
            title="Test",
            message="Choose:",
            choices=["A", "B", "C"],
            multiple=False
        )
        
        assert dialog.choices == ["A", "B", "C"]
        assert dialog.multiple is False
        assert dialog.initial_selection == []

def test_custom_messagebox_selection_multiple(root):
    """Test CustomMessageBox with multiple selection."""
    from tkface.messagebox import CustomMessageBox
    
    with patch('tkinter.Toplevel.wait_window'), \
         patch('tkinter.Listbox'), \
         patch('tkinter.Button'):
        
        dialog = CustomMessageBox(
            master=root,
            title="Test",
            message="Choose:",
            choices=["A", "B", "C"],
            multiple=True,
            initial_selection=[0, 2]
        )
        
        assert dialog.choices == ["A", "B", "C"]
        assert dialog.multiple is True
        assert dialog.initial_selection == [0, 2]

def test_custom_messagebox_set_result_with_selection(root):
    """Test CustomMessageBox set_result with selection dialog."""
    from tkface.messagebox import CustomMessageBox
    
    with patch('tkinter.Toplevel.wait_window'), \
         patch('tkinter.Listbox') as mock_listbox, \
         patch('tkinter.Button'):
        
        # Mock listbox selection
        mock_listbox_instance = mock_listbox.return_value
        mock_listbox_instance.curselection.return_value = [1]  # Select second item
        
        dialog = CustomMessageBox(
            master=root,
            title="Test",
            message="Choose:",
            choices=["A", "B", "C"],
            multiple=False
        )
        
        # Test set_result with "ok" (should get selection)
        dialog.set_result("ok")
        assert dialog.result == "B"  # Second item (index 1)
        
        # Test set_result with "cancel" (should return None)
        dialog.set_result("cancel")
        assert dialog.result is None

def test_custom_messagebox_set_result_multiple_selection(root):
    """Test CustomMessageBox set_result with multiple selection."""
    from tkface.messagebox import CustomMessageBox
    
    with patch('tkinter.Toplevel.wait_window'), \
         patch('tkinter.Listbox') as mock_listbox, \
         patch('tkinter.Button'):
        
        # Mock listbox selection for multiple items
        mock_listbox_instance = mock_listbox.return_value
        mock_listbox_instance.curselection.return_value = [0, 2]  # Select first and third items
        
        dialog = CustomMessageBox(
            master=root,
            title="Test",
            message="Choose:",
            choices=["A", "B", "C"],
            multiple=True
        )
        
        # Test set_result with "ok" (should get selection)
        dialog.set_result("ok")
        assert dialog.result == ["A", "C"]  # First and third items 

def test_bell_parameter_passed_to_show(root):
    """Test that the bell parameter is correctly passed to CustomMessageBox.show."""
    with patch('tkface.messagebox.CustomMessageBox.show') as mock_show:
        messagebox.showinfo(master=root, message="Test", bell=True)
        mock_show.assert_called_once()
        args, kwargs = mock_show.call_args
        assert kwargs['bell'] is True

def test_bell_parameter_default_false(root):
    """Test that bell parameter defaults to False."""
    with patch('tkface.messagebox.CustomMessageBox.show') as mock_show:
        messagebox.showinfo(master=root, message="Test")
        mock_show.assert_called_once()
        args, kwargs = mock_show.call_args
        assert kwargs.get('bell', False) is False

@pytest.mark.parametrize("func_name", [
    "showinfo", "showerror", "showwarning", "askquestion", 
    "askyesno", "askokcancel", "askretrycancel", "askyesnocancel"
])
def test_bell_parameter_all_functions(root, func_name):
    """Test that bell parameter works for all messagebox functions."""
    dialog_func = getattr(messagebox, func_name)
    
    with patch('tkface.messagebox.CustomMessageBox.show') as mock_show:
        if func_name == 'askfromlistbox':
            dialog_func(master=root, message="Test", choices=["A", "B"], bell=True)
        else:
            dialog_func(master=root, message="Test", bell=True)
        
        mock_show.assert_called_once()
        args, kwargs = mock_show.call_args
        assert kwargs['bell'] is True 

def test_askfromlistbox_with_empty_choices(root):
    """Test askfromlistbox with empty choices list raises ValueError."""
    with pytest.raises(ValueError, match="choices parameter is required"):
        messagebox.askfromlistbox(master=root, message="Test", choices=[])

def test_askfromlistbox_with_initial_selection_single(root):
    """Test askfromlistbox with initial selection for single mode."""
    with patch('tkface.messagebox.CustomMessageBox.show') as mock_show:
        messagebox.askfromlistbox(
            master=root, 
            message="Test", 
            choices=["A", "B", "C"],
            initial_selection=1
        )
        mock_show.assert_called_once()
        args, kwargs = mock_show.call_args
        assert kwargs['initial_selection'] == 1

def test_askfromlistbox_with_initial_selection_multiple(root):
    """Test askfromlistbox with initial selection for multiple mode."""
    with patch('tkface.messagebox.CustomMessageBox.show') as mock_show:
        messagebox.askfromlistbox(
            master=root, 
            message="Test", 
            choices=["A", "B", "C"],
            multiple=True,
            initial_selection=[0, 2]
        )
        mock_show.assert_called_once()
        args, kwargs = mock_show.call_args
        assert kwargs['multiple'] is True
        assert kwargs['initial_selection'] == [0, 2]

def test_askfromlistbox_multiple_selection_return_type(root):
    """Test that multiple selection returns list."""
    with patch('tkface.messagebox.CustomMessageBox.show', return_value=["A", "C"]) as mock_show:
        result = messagebox.askfromlistbox(
            master=root, 
            message="Test", 
            choices=["A", "B", "C"],
            multiple=True
        )
        assert isinstance(result, list)
        assert result == ["A", "C"]

def test_askfromlistbox_single_selection_return_type(root):
    """Test that single selection returns string or None."""
    with patch('tkface.messagebox.CustomMessageBox.show', return_value="B") as mock_show:
        result = messagebox.askfromlistbox(
            master=root, 
            message="Test", 
            choices=["A", "B", "C"]
        )
        assert isinstance(result, str)
        assert result == "B"

def test_askfromlistbox_cancel_multiple_selection(root):
    """Test that cancel in multiple selection returns None."""
    with patch('tkface.messagebox.CustomMessageBox.show', return_value=None) as mock_show:
        result = messagebox.askfromlistbox(
            master=root, 
            message="Test", 
            choices=["A", "B", "C"],
            multiple=True
        )
        assert result is None 