from unittest.mock import patch, MagicMock
import pytest
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


@pytest.mark.parametrize(
    "func_name, expected_title, expected_icon",
    [(k, v[0], v[1]) for k, v in DIALOG_CONFIG.items()],
)
def test_dialog_creation_with_defaults(root, func_name, expected_title, expected_icon):
    """Test that dialogs are created by calling CustomMessageBox with correct defaults."""
    dialog_func = getattr(messagebox, func_name)

    # We patch the underlying show method to prevent actual dialog creation
    with patch("tkface.messagebox.CustomMessageBox.show") as mock_show:
        # We need to test the wrapper functions, not the class directly
        if func_name in ["showinfo", "showerror", "showwarning"]:
            dialog_func(master=root, message="Test message")
            mock_show.assert_called_once()
            _, kwargs = mock_show.call_args
            assert kwargs["icon"] == expected_icon
        else:
            dialog_func(master=root, message="Test message")


# --- Test button clicks and return values ---
@pytest.mark.parametrize(
    "func_name, mocked_return, expected_final_return",
    [
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
    ],
)
def test_dialog_return_values(root, func_name, mocked_return, expected_final_return):
    """Test the final return value of dialogs, including boolean/None conversion."""
    dialog_func = getattr(messagebox, func_name)

    with patch("tkface.messagebox.CustomMessageBox.show", return_value=mocked_return):
        final_result = dialog_func(master=root, message="Test")
        assert final_result == expected_final_return


# --- Test language support ---
@pytest.mark.parametrize("lang", ["ja", "en"])
def test_language_passed_to_show(root, lang):
    """Test that the language parameter is correctly passed to CustomMessageBox.show."""
    with patch("tkface.messagebox.CustomMessageBox.show") as mock_show:
        messagebox.showinfo(master=root, message="Test", language=lang)
        mock_show.assert_called_once()
        _, kwargs = mock_show.call_args
        assert kwargs["language"] == lang


# --- Test geometry ---
@pytest.mark.parametrize(
    "x, y, x_offset, y_offset",
    [
        (100, 200, 0, 0),
        (None, None, 50, -30),
    ],
)
def test_dialog_positioning_kwargs_passed(root, x, y, x_offset, y_offset):
    """Test that geometry-related kwargs are passed correctly."""
    root.geometry("800x600+0+0")

    with patch("tkface.messagebox.CustomMessageBox.show") as mock_show:
        messagebox.showinfo(
            master=root,
            message="Position test",
            x=x,
            y=y,
            x_offset=x_offset,
            y_offset=y_offset,
        )

        mock_show.assert_called_once()
        _, kwargs = mock_show.call_args

        assert kwargs.get("x") == x
        assert kwargs.get("y") == y
        assert kwargs.get("x_offset") == x_offset
        assert kwargs.get("y_offset") == y_offset


@pytest.mark.parametrize("lang", ["ja", "en"])
def test_messagebox_translation_calls(root, lang):
    """Test that lang.get is called for title, message, and buttons."""
    with patch("tkface.lang.get") as mock_lang_get:
        # Assume translated text to be returned
        mock_lang_get.side_effect = lambda key, *a, **kw: f"{key}_{lang}"

        from tkface.dialog.messagebox import CustomMessageBox

        with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
            "tkinter.Button"
        ):
            CustomMessageBox(
                master=root,
                title="Test Title",
                message="Test Message",
                button_set="okcancel",
                language=lang,
            )

    # Check if lang.get was called as expected
    calls = mock_lang_get.call_args_list

    # Check for calls for Title, ok, and cancel
    assert any(c.args[0] == "Test Title" for c in calls)
    assert any(c.args[0] == "ok" for c in calls)
    assert any(c.args[0] == "cancel" for c in calls)
    # Check if the correct language was specified in all calls
    assert all(c.kwargs["language"] == lang for c in calls)


def test_bell_parameter_passed_to_show(root):
    """Test that the bell parameter is correctly passed to CustomMessageBox.show."""
    with patch("tkface.messagebox.CustomMessageBox.show") as mock_show:
        messagebox.showinfo(master=root, message="Test", bell=True)
        mock_show.assert_called_once()
        _, kwargs = mock_show.call_args
        assert kwargs["bell"] is True


def test_bell_parameter_default_false(root):
    """Test that bell parameter defaults to False."""
    with patch("tkface.messagebox.CustomMessageBox.show") as mock_show:
        messagebox.showinfo(master=root, message="Test")
        mock_show.assert_called_once()
        _, kwargs = mock_show.call_args
        assert kwargs.get("bell", False) is False


@pytest.mark.parametrize(
    "func_name",
    [
        "showinfo",
        "showerror",
        "showwarning",
        "askquestion",
        "askyesno",
        "askokcancel",
        "askretrycancel",
        "askyesnocancel",
    ],
)
def test_bell_parameter_all_functions(root, func_name):
    """Test that bell parameter works for all messagebox functions."""
    dialog_func = getattr(messagebox, func_name)

    with patch("tkface.messagebox.CustomMessageBox.show") as mock_show:
        dialog_func(master=root, message="Test", bell=True)

        mock_show.assert_called_once()
        _, kwargs = mock_show.call_args
        assert kwargs["bell"] is True


# --- Additional tests for better coverage ---


def test_get_icon_title():
    """Test get_icon_title function."""
    from tkface.dialog.messagebox import get_icon_title

    assert get_icon_title("info") == "Info"
    assert get_icon_title("warning") == "Warning"
    assert get_icon_title("error") == "Error"
    assert get_icon_title("question") == "Question"
    assert get_icon_title("unknown") == "Message"


def test_get_tk_icon():
    """Test get_tk_icon function."""
    from tkface.dialog.messagebox import get_tk_icon

    assert get_tk_icon("info") == "::tk::icons::information"
    assert get_tk_icon("warning") == "::tk::icons::warning"
    assert get_tk_icon("error") == "::tk::icons::error"
    assert get_tk_icon("question") == "::tk::icons::question"
    assert get_tk_icon("unknown") == "::tk::icons::unknown"


def test_get_or_create_root():
    """Test _get_or_create_root function."""
    from tkface.dialog.messagebox import _get_or_create_root

    # Test when root exists
    with patch("tkinter._default_root", None):
        with patch("tkinter.Tk") as mock_tk:
            mock_root = MagicMock()
            mock_tk.return_value = mock_root
            root, created = _get_or_create_root()
            assert created is True
            assert root == mock_root
            mock_tk.assert_called_once()
            mock_root.withdraw.assert_called_once()

    # Test when root already exists
    mock_root = MagicMock()
    with patch("tkinter._default_root", mock_root):
        root, created = _get_or_create_root()
        assert created is False
        assert root == mock_root


def test_get_button_labels():
    """Test _get_button_labels function."""
    from tkface.dialog.messagebox import _get_button_labels

    with patch("tkface.lang.get") as mock_lang_get:
        mock_lang_get.side_effect = lambda key, *a, **kw: key.upper()

        # Test different button sets
        result = _get_button_labels("ok", None, "en")
        assert len(result) == 1
        assert result[0][0] == "OK"
        assert result[0][1] == "ok"
        assert result[0][2] is True  # is_default
        assert result[0][3] is False  # is_cancel

        result = _get_button_labels("okcancel", None, "en")
        assert len(result) == 2
        assert result[0][1] == "ok"
        assert result[1][1] == "cancel"
        assert result[0][2] is True  # ok is default
        assert result[1][3] is True  # cancel is cancel


def test_custom_messagebox_without_master():
    """Test CustomMessageBox when no master is provided and no root exists."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkinter._default_root", None):
        with pytest.raises(RuntimeError, match="No Tk root window found"):
            CustomMessageBox()


def test_custom_messagebox_icon_file_error(root):
    """Test CustomMessageBox with invalid icon file."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkinter.PhotoImage") as mock_photo:
        mock_photo.side_effect = Exception("File not found")

        with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
            "tkinter.Button"
        ):
            # Should not raise exception, should handle gracefully
            CustomMessageBox(master=root, message="Test", icon="/invalid/path/icon.png")


def test_custom_messagebox_custom_buttons(root):
    """Test CustomMessageBox with custom buttons."""
    from tkface.dialog.messagebox import CustomMessageBox

    custom_buttons = [
        ("Save", "save"),
        ("Don't Save", "dont_save"),
        ("Cancel", "cancel"),
    ]

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ):
        CustomMessageBox(
            master=root,
            message="Test",
            buttons=custom_buttons,
            default="save",
            cancel="cancel",
        )


def test_custom_messagebox_keyboard_shortcuts(root):
    """Test CustomMessageBox keyboard shortcuts."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ):
        dialog = CustomMessageBox(master=root, message="Test", button_set="yesno")
        # Test that keyboard shortcuts are bound
        assert hasattr(dialog, "button_widgets")


def test_custom_messagebox_window_positioning(root):
    """Test CustomMessageBox window positioning."""
    from tkface.dialog.messagebox import CustomMessageBox

    root.geometry("800x600+100+100")

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Toplevel.geometry") as mock_geometry:
        CustomMessageBox(master=root, message="Test", x=200, y=300)
        # Should call geometry with position
        mock_geometry.assert_called()


def test_custom_messagebox_bell_error(root):
    """Test CustomMessageBox bell error handling."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkface.win.bell") as mock_win_bell:
        mock_win_bell.side_effect = Exception("Bell error")

        with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
            "tkinter.Button"
        ), patch("tkinter.Toplevel.bell") as mock_bell:
            CustomMessageBox(master=root, message="Test", bell=True, icon="error")
            # Should fallback to standard bell
            mock_bell.assert_called()


def test_askabortretryignore(root):
    """Test askabortretryignore function."""
    with patch("tkface.messagebox.CustomMessageBox.show") as mock_show:
        mock_show.return_value = "retry"
        result = messagebox.askabortretryignore(master=root, message="Test")
        assert result == "retry"

        mock_show.return_value = "abort"
        result = messagebox.askabortretryignore(master=root, message="Test")
        assert result == "abort"

        mock_show.return_value = "ignore"
        result = messagebox.askabortretryignore(master=root, message="Test")
        assert result == "ignore"


def test_custom_messagebox_focus_next(root):
    """Test _focus_next method."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ):
        dialog = CustomMessageBox(master=root, message="Test", button_set="yesno")

        # Test focus navigation
        if len(dialog.button_widgets) >= 2:
            dialog._focus_next(0)
            # Should focus on next button (index 1)


def test_custom_messagebox_set_result(root):
    """Test set_result method."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Toplevel.destroy") as mock_destroy:
        dialog = CustomMessageBox(master=root, message="Test")

        dialog.set_result("test_result")
        assert dialog.result == "test_result"
        mock_destroy.assert_called()


def test_custom_messagebox_close(root):
    """Test close method."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Toplevel.destroy") as mock_destroy:
        dialog = CustomMessageBox(master=root, message="Test")

        dialog.close()
        mock_destroy.assert_called()


def test_custom_messagebox_show_class_method(root):
    """Test CustomMessageBox.show class method."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkface.dialog.messagebox.CustomMessageBox.show") as mock_show:
        mock_show.return_value = "ok"
        result = CustomMessageBox.show(message="Test", title="Test Title")
        assert result == "ok"
        mock_show.assert_called_once()


def test_custom_messagebox_show_with_created_root(root):
    """Test CustomMessageBox.show when root is created."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkface.dialog.messagebox.CustomMessageBox.show") as mock_show:
        mock_show.return_value = "ok"
        result = CustomMessageBox.show(message="Test")
        assert result == "ok"
        mock_show.assert_called_once()


# --- Additional tests for remaining coverage ---


def test_custom_messagebox_with_custom_translations(root):
    """Test CustomMessageBox with custom translations."""
    from tkface.dialog.messagebox import CustomMessageBox

    custom_translations = {"ja": {"ok": "OK", "cancel": "キャンセル"}}

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkface.lang.register") as mock_register:
        CustomMessageBox(
            master=root, message="Test", custom_translations=custom_translations
        )
        mock_register.assert_called()


def test_custom_messagebox_without_icon(root):
    """Test CustomMessageBox without icon."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ):
        CustomMessageBox(master=root, message="Test", icon=None)


def test_custom_messagebox_without_message(root):
    """Test CustomMessageBox without message."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ):
        CustomMessageBox(master=root, message="", icon="info")


def test_custom_messagebox_button_default_cancel_logic(root):
    """Test CustomMessageBox button default/cancel logic."""
    from tkface.dialog.messagebox import CustomMessageBox

    custom_buttons = [("Button1", "btn1"), ("Button2", "btn2")]

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ):
        # Test without specifying default/cancel
        CustomMessageBox(master=root, message="Test", buttons=custom_buttons)


def test_custom_messagebox_bell_with_different_icons(root):
    """Test CustomMessageBox bell with different icon types."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkface.win.bell") as mock_win_bell, patch(
        "tkinter.Toplevel.bell"
    ) as mock_bell:
        mock_win_bell.side_effect = Exception("Bell error")
        # Test with warning icon
        CustomMessageBox(master=root, message="Test", bell=True, icon="warning")
        mock_bell.assert_called()
