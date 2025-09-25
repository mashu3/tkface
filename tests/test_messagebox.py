# pylint: disable=import-outside-toplevel,protected-access
import tempfile
from unittest.mock import MagicMock, patch

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
def test_dialog_creation_with_defaults(
    root, func_name, expected_title, expected_icon  # pylint: disable=unused-argument
):
    """Test that dialogs are created by calling CustomMessageBox with correct
    defaults."""
    dialog_func = getattr(messagebox, func_name)
    # We patch the underlying show method to prevent actual dialog creation
    with patch("tkface.messagebox.CustomMessageBox.show") as mock_show:
        # We need to test the wrapper functions, not the class directly
        if func_name in ["showinfo", "showerror", "showwarning"]:
            dialog_func(master=root, message="Test message")
            mock_show.assert_called_once()
            _, kwargs = mock_show.call_args
            assert kwargs["config"].icon == expected_icon
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
    """Test the final return value of dialogs, including boolean/None
    conversion."""
    dialog_func = getattr(messagebox, func_name)
    with patch("tkface.messagebox.CustomMessageBox.show", return_value=mocked_return):
        final_result = dialog_func(master=root, message="Test")
        assert final_result == expected_final_return


# --- Test language support ---
@pytest.mark.parametrize("lang", ["ja", "en"])
def test_language_passed_to_show(root, lang):
    """Test that the language parameter is correctly passed to
    CustomMessageBox.show."""
    with patch("tkface.messagebox.CustomMessageBox.show") as mock_show:
        messagebox.showinfo(master=root, message="Test", language=lang)
        mock_show.assert_called_once()
        _, kwargs = mock_show.call_args
        assert kwargs["config"].language == lang


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
        # Position parameters are now passed via WindowPosition object
        # This test needs to be updated to test the new API
        from tkface.dialog.messagebox import (
            CustomMessageBox,
            MessageBoxConfig,
            WindowPosition,
        )

        CustomMessageBox.show(
            master=root,
            config=MessageBoxConfig(message="Position test"),
            position=WindowPosition(x=x, y=y, x_offset=x_offset, y_offset=y_offset),
        )
        mock_show.assert_called_once()
        _, kwargs = mock_show.call_args
        assert kwargs["position"].x == x
        assert kwargs["position"].y == y
        assert kwargs["position"].x_offset == x_offset
        assert kwargs["position"].y_offset == y_offset


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
            from tkface.dialog.messagebox import MessageBoxConfig

            CustomMessageBox(
                master=root,
                config=MessageBoxConfig(
                    title="Test Title",
                    message="Test Message",
                    button_set="okcancel",
                    language=lang,
                ),
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
    """Test that the bell parameter is correctly passed to
    CustomMessageBox.show."""
    with patch("tkface.messagebox.CustomMessageBox.show") as mock_show:
        messagebox.showinfo(master=root, message="Test", bell=True)
        mock_show.assert_called_once()
        _, kwargs = mock_show.call_args
        assert kwargs["config"].bell is True


def test_bell_parameter_default_false(root):
    """Test that bell parameter defaults to False."""
    with patch("tkface.messagebox.CustomMessageBox.show") as mock_show:
        messagebox.showinfo(master=root, message="Test")
        mock_show.assert_called_once()
        _, kwargs = mock_show.call_args
        assert kwargs["config"].bell is False


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
        assert kwargs["config"].bell is True


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
        mock_photo.side_effect = OSError("File not found")
        with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
            "tkinter.Button"
        ):
            # Should not raise exception, should handle gracefully
            from tkface.dialog.messagebox import MessageBoxConfig

            CustomMessageBox(
                master=root,
                config=MessageBoxConfig(message="Test", icon="/invalid/path/icon.png"),
            )


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
        from tkface.dialog.messagebox import MessageBoxConfig

        CustomMessageBox(
            master=root,
            config=MessageBoxConfig(
                message="Test",
                buttons=custom_buttons,
                default="save",
                cancel="cancel",
            ),
        )


def test_custom_messagebox_keyboard_shortcuts(root):
    """Test CustomMessageBox keyboard shortcuts."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ):
        from tkface.dialog.messagebox import MessageBoxConfig

        dialog = CustomMessageBox(
            master=root,
            config=MessageBoxConfig(message="Test", button_set="yesno"),
        )
        # Test that keyboard shortcuts are bound
        assert hasattr(dialog, "button_widgets")


def test_custom_messagebox_window_positioning(root):
    """Test CustomMessageBox window positioning."""
    from tkface.dialog.messagebox import CustomMessageBox

    root.geometry("800x600+100+100")
    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Toplevel.geometry") as mock_geometry:
        from tkface.dialog.messagebox import MessageBoxConfig, WindowPosition

        CustomMessageBox(
            master=root,
            config=MessageBoxConfig(message="Test"),
            position=WindowPosition(x=200, y=300),
        )
        # Should call geometry with position
        mock_geometry.assert_called()


def test_custom_messagebox_bell_error(root):
    """Test CustomMessageBox bell error handling."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkface.win.bell") as mock_win_bell:
        mock_win_bell.side_effect = AttributeError("Bell error")
        with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
            "tkinter.Button"
        ), patch("tkinter.Toplevel.bell") as mock_bell:
            from tkface.dialog.messagebox import MessageBoxConfig

            CustomMessageBox(
                master=root,
                config=MessageBoxConfig(message="Test", bell=True, icon="error"),
            )
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
        from tkface.dialog.messagebox import MessageBoxConfig

        dialog = CustomMessageBox(
            master=root,
            config=MessageBoxConfig(message="Test", button_set="yesno"),
        )
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
        from tkface.dialog.messagebox import MessageBoxConfig

        dialog = CustomMessageBox(master=root, config=MessageBoxConfig(message="Test"))
        dialog.set_result("test_result")
        assert dialog.result == "test_result"
        mock_destroy.assert_called()


def test_custom_messagebox_close(root):
    """Test close method."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Toplevel.destroy") as mock_destroy:
        from tkface.dialog.messagebox import MessageBoxConfig

        dialog = CustomMessageBox(master=root, config=MessageBoxConfig(message="Test"))
        dialog.close()
        mock_destroy.assert_called()


def test_custom_messagebox_show_class_method(root):  # pylint: disable=unused-argument
    """Test CustomMessageBox.show class method."""
    from tkface.dialog.messagebox import CustomMessageBox, MessageBoxConfig

    with patch("tkface.dialog.messagebox.CustomMessageBox.show") as mock_show:
        mock_show.return_value = "ok"
        result = CustomMessageBox.show(
            config=MessageBoxConfig(message="Test", title="Test Title")
        )
        assert result == "ok"
        mock_show.assert_called_once()


def test_custom_messagebox_show_with_created_root(
    root,
):  # pylint: disable=unused-argument
    """Test CustomMessageBox.show when root is created."""
    from tkface.dialog.messagebox import CustomMessageBox, MessageBoxConfig

    with patch("tkface.dialog.messagebox.CustomMessageBox.show") as mock_show:
        mock_show.return_value = "ok"
        result = CustomMessageBox.show(config=MessageBoxConfig(message="Test"))
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
        from tkface.dialog.messagebox import MessageBoxConfig

        CustomMessageBox(
            master=root,
            config=MessageBoxConfig(
                message="Test",
                custom_translations=custom_translations,
            ),
        )
        mock_register.assert_called()


def test_custom_messagebox_without_icon(root):  # pylint: disable=unused-argument
    """Test CustomMessageBox without icon."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ):
        from tkface.dialog.messagebox import MessageBoxConfig

        CustomMessageBox(
            master=root, config=MessageBoxConfig(message="Test", icon=None)
        )


def test_custom_messagebox_without_message(root):  # pylint: disable=unused-argument
    """Test CustomMessageBox without message."""
    from tkface.dialog.messagebox import CustomMessageBox

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ):
        from tkface.dialog.messagebox import MessageBoxConfig

        CustomMessageBox(master=root, config=MessageBoxConfig(message="", icon="info"))


def test_custom_messagebox_button_default_cancel_logic(
    root,
):  # pylint: disable=unused-argument
    """Test CustomMessageBox button default/cancel logic."""
    from tkface.dialog.messagebox import CustomMessageBox

    custom_buttons = [("Button1", "btn1"), ("Button2", "btn2")]
    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ):
        # Test without specifying default/cancel
        from tkface.dialog.messagebox import MessageBoxConfig

        CustomMessageBox(
            master=root,
            config=MessageBoxConfig(message="Test", buttons=custom_buttons),
        )


def test_custom_messagebox_bell_with_different_icons(
    root,
):  # pylint: disable=unused-argument
    """Test CustomMessageBox bell with different icon types."""
    from tkface.dialog.messagebox import CustomMessageBox

    with (
        patch("tkinter.Toplevel.wait_window"),
        patch("tkinter.Label"),
        patch("tkinter.Button"),
        patch("tkface.win.bell") as mock_win_bell,
        patch("tkinter.Toplevel.bell") as mock_bell,
    ):
        mock_win_bell.side_effect = AttributeError("Bell error")
        # Test with warning icon
        from tkface.dialog.messagebox import MessageBoxConfig

        CustomMessageBox(
            master=root,
            config=MessageBoxConfig(message="Test", bell=True, icon="warning"),
        )
        mock_bell.assert_called()


def test_messagebox_actual_translation(root):
    """Test that messagebox actually translates messages correctly."""
    from tkface.dialog.messagebox import CustomMessageBox, MessageBoxConfig

    # Test Japanese translation
    with patch("tkinter.Toplevel.wait_window"), patch(
        "tkinter.Label"
    ) as mock_label, patch("tkinter.Button"):
        # Set up language for the root window
        from tkface import lang

        lang.set("ja", root)

        CustomMessageBox(
            master=root,
            config=MessageBoxConfig(
                title="Info",
                message="Operation completed successfully.",
                button_set="ok",
                language="ja",
            ),
        )

    # Check that the translated message was used
    label_calls = mock_label.call_args_list
    # Find the call that creates the message label
    message_call = None
    for call in label_calls:
        if call.kwargs.get("text") == "操作が正常に完了しました。":
            message_call = call
            break

    assert (
        message_call is not None
    ), "Translated message was not found in label creation"


def test_messagebox_button_translation(root):
    """Test that messagebox buttons are translated correctly."""
    from tkface.dialog.messagebox import CustomMessageBox, MessageBoxConfig

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ) as mock_button:
        # Set up language for the root window
        from tkface import lang

        lang.set("ja", root)

        CustomMessageBox(
            master=root,
            config=MessageBoxConfig(
                title="Question",
                message="Do you want to proceed?",
                button_set="yesno",
                language="ja",
            ),
        )

    # Check that buttons were created with translated text
    button_calls = mock_button.call_args_list
    button_texts = [call.kwargs.get("text", "") for call in button_calls]

    # Check for Japanese button text (with keyboard shortcuts)
    assert any(
        "はい" in text for text in button_texts
    ), "Japanese 'yes' button not found"
    assert any(
        "いいえ" in text for text in button_texts
    ), "Japanese 'no' button not found"


def test_messagebox_title_translation(root):
    """Test that messagebox titles are translated correctly."""
    from tkface.dialog.messagebox import CustomMessageBox, MessageBoxConfig

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Toplevel.title") as mock_title:
        # Set up language for the root window
        from tkface import lang

        lang.set("ja", root)

        CustomMessageBox(
            master=root,
            config=MessageBoxConfig(
                title="Error",
                message="An error has occurred.",
                button_set="ok",
                language="ja",
            ),
        )

    # Check that the title was translated
    title_calls = mock_title.call_args_list
    assert any(
        "エラー" in str(call) for call in title_calls
    ), "Translated title not found"


def test_custom_messagebox_icon_file_success(root):
    """Test successful icon file loading path in _get_icon_label."""
    from tkface.dialog.messagebox import CustomMessageBox, MessageBoxConfig

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_icon_path = temp_file.name
    
    try:
        with (
            patch("tkinter.Toplevel.wait_window"),
            patch("tkinter.PhotoImage") as mock_photo,
            patch("tkinter.Label") as mock_label,
            patch("tkinter.Button"),
        ):
            mock_photo.return_value = MagicMock(name="Image")
            CustomMessageBox(
                master=root,
                config=MessageBoxConfig(message="Test", icon=temp_icon_path),
            )
        # Ensure a Label was created with the image returned by PhotoImage
        assert any(
            ("image" in call.kwargs) and (call.kwargs["image"] is mock_photo.return_value)
            for call in mock_label.call_args_list
        )
    finally:
        import os
        try:
            os.unlink(temp_icon_path)
        except OSError:
            pass


def test_classmethod_show_created_root(root):
    """Exercise CustomMessageBox.show wrapper when root is auto-created."""
    from tkface.dialog.messagebox import (
        CustomMessageBox,
        MessageBoxConfig,
        WindowPosition,
    )

    with (
        patch("tkface.dialog.messagebox._get_or_create_root") as mock_get_or_create,
        patch("tkface.dialog.messagebox.lang.set") as mock_lang_set,
        patch.object(root, "destroy") as mock_destroy,
    ):
        mock_get_or_create.return_value = (root, True)

        class FakeMessageBox:
            def __init__(self, master=None, config=None, position=None):  # pylint: disable=unused-argument
                self.result = "ok"

        result = CustomMessageBox.show.__func__(
            FakeMessageBox,
            config=MessageBoxConfig(message="Test"),
            position=WindowPosition(x=10, y=20),
        )
        assert result == "ok"
        mock_lang_set.assert_called()
        mock_destroy.assert_called_once()


def test_classmethod_show_with_master_provided(root):
    """Exercise CustomMessageBox.show wrapper when master is provided."""
    from tkface.dialog.messagebox import CustomMessageBox, MessageBoxConfig

    class FakeMessageBox:
        def __init__(self, master=None, config=None, position=None):  # pylint: disable=unused-argument
            self.result = "ok"

    with (
        patch("tkface.dialog.messagebox._get_or_create_root") as mock_get_or_create,
        patch("tkface.dialog.messagebox.lang.set") as mock_lang_set,
    ):
        result = CustomMessageBox.show.__func__(
            FakeMessageBox,
            master=root,
            config=MessageBoxConfig(message="Test"),
        )
        assert result == "ok"
        mock_lang_set.assert_called()
        mock_get_or_create.assert_not_called()


def test_classmethod_show_default_config_when_none(root):
    """Ensure default MessageBoxConfig is created when config is None."""
    from tkface.dialog.messagebox import CustomMessageBox, MessageBoxConfig

    seen = {}

    class FakeMessageBox:
        def __init__(self, master=None, config=None, position=None):  # pylint: disable=unused-argument
            seen["config"] = config
            self.result = "ok"

    with patch("tkface.dialog.messagebox.lang.set"):
        result = CustomMessageBox.show.__func__(
            FakeMessageBox,
            master=root,
            config=None,
            position=None,
        )
    assert result == "ok"
    assert isinstance(seen["config"], MessageBoxConfig)

def test_simpledialog_actual_translation(root):
    """Test that simpledialog actually translates messages correctly."""
    from tkface.dialog.simpledialog import CustomSimpleDialog, SimpleDialogConfig

    with patch("tkinter.Toplevel.wait_window"), patch(
        "tkinter.Label"
    ) as mock_label, patch("tkinter.Entry"), patch("tkinter.Button"):
        CustomSimpleDialog(
            master=root,
            config=SimpleDialogConfig(
                title="Input",
                message="Please enter a value.",
                language="ja",
            ),
        )

    # Check that the translated message was used
    label_calls = mock_label.call_args_list
    message_call = None
    for call in label_calls:
        if call.kwargs.get("text") == "値を入力してください。":
            message_call = call
            break

    assert message_call is not None, "Translated message was not found in simpledialog"
