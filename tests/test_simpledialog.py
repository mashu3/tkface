# pylint: disable=import-outside-toplevel,protected-access
from unittest.mock import MagicMock, patch

import pytest

from tkface import simpledialog


@pytest.mark.parametrize(
    "mocked_return, expected",
    [
        ("hello", "hello"),
        (None, None),
    ],
)
def test_askstring_return_value(mocked_return, expected):
    with patch(
        "tkface.simpledialog.CustomSimpleDialog.show",
        return_value=mocked_return,
    ) as mock_show:
        result = simpledialog.askstring(message="Enter text:")
        assert result == expected
        mock_show.assert_called_once()


@pytest.mark.parametrize(
    "mocked_return, expected",
    [
        ("42", 42),
        (None, None),
    ],
)
def test_askinteger_return_value(mocked_return, expected):
    with patch(
        "tkface.simpledialog.CustomSimpleDialog.show",
        return_value=mocked_return,
    ) as mock_show:
        result = simpledialog.askinteger(message="Enter int:")
        assert result == expected
        mock_show.assert_called_once()


@pytest.mark.parametrize(
    "mocked_return, expected",
    [
        ("3.14", 3.14),
        (None, None),
    ],
)
def test_askfloat_return_value(mocked_return, expected):
    with patch(
        "tkface.simpledialog.CustomSimpleDialog.show",
        return_value=mocked_return,
    ) as mock_show:
        result = simpledialog.askfloat(message="Enter float:")
        assert result == expected
        mock_show.assert_called_once()


@pytest.mark.parametrize(
    "func, value, minv, maxv, valid",
    [
        (simpledialog.askinteger, "5", 1, 10, 5),
        (simpledialog.askinteger, "0", 1, 10, None),
        (simpledialog.askinteger, "11", 1, 10, None),
        (simpledialog.askfloat, "2.5", 1.0, 3.0, 2.5),
        (simpledialog.askfloat, "0.5", 1.0, 3.0, None),
        (simpledialog.askfloat, "3.5", 1.0, 3.0, None),
    ],
)
def test_range_validation(func, value, minv, maxv, valid):
    # Control whether validation passes or fails using a mock
    with patch(
        "tkface.simpledialog.CustomSimpleDialog.show",
        return_value=value if valid is not None else None,
    ):
        result = func(message="test", minvalue=minv, maxvalue=maxv)
        assert result == valid


@pytest.mark.parametrize("lang", ["ja", "en"])
def test_language_passed_to_show(lang):
    with patch("tkface.simpledialog.CustomSimpleDialog.show") as mock_show:
        simpledialog.askstring(message="Test", language=lang)
        mock_show.assert_called_once()
        _, kwargs = mock_show.call_args
        assert kwargs["config"].language == lang


@pytest.mark.parametrize(
    "x, y, x_offset, y_offset",
    [
        (100, 200, 0, 0),
        (None, None, 50, -30),
    ],
)
def test_dialog_positioning_kwargs_passed(x, y, x_offset, y_offset):
    with patch("tkface.simpledialog.CustomSimpleDialog.show") as mock_show:
        simpledialog.askstring(
            message="Position test",
            x=x,
            y=y,
            x_offset=x_offset,
            y_offset=y_offset,
        )
        mock_show.assert_called_once()
        _, kwargs = mock_show.call_args
        assert kwargs["position"].x == x
        assert kwargs["position"].y == y
        assert kwargs["position"].x_offset == x_offset
        assert kwargs["position"].y_offset == y_offset


@pytest.mark.parametrize("lang", ["ja", "en"])
def test_simpledialog_translation_calls(root, lang):
    """Test that lang.get is called for title, message, and buttons."""
    with patch("tkface.lang.get") as mock_lang_get:
        mock_lang_get.side_effect = lambda key, *a, **kw: f"{key}_{lang}"
        from tkface.dialog.simpledialog import CustomSimpleDialog

        with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
            "tkinter.Button"
        ), patch("tkinter.Entry"):
            from tkface.dialog.simpledialog import SimpleDialogConfig

            CustomSimpleDialog(
                master=root,
                config=SimpleDialogConfig(
                    title="Test Title",
                    message="Test Message",
                    language=lang,
                ),
            )
    calls = mock_lang_get.call_args_list
    assert any(c.args[0] == "Test Title" for c in calls)
    assert any(c.args[0] == "ok" for c in calls)
    assert any(c.args[0] == "cancel" for c in calls)
    assert all(
        c.kwargs["language"] == lang
        for c in calls
        if c.args[0] in ["ok", "cancel", "Test Title"]
    )


def test_bell_parameter_not_supported_in_simpledialog(root):
    """Test that bell parameter is not supported in simpledialog."""
    with patch("tkface.simpledialog.CustomSimpleDialog.show") as mock_show:
        simpledialog.askstring(master=root, message="Test")
        mock_show.assert_called_once()
        _, kwargs = mock_show.call_args
        # Bell parameter should not be passed
        assert not hasattr(kwargs["config"], "bell")


def test_askfromlistbox_single_selection():
    """Test askfromlistbox with single selection."""
    choices = ["Red", "Green", "Blue"]
    with patch(
        "tkface.simpledialog.CustomSimpleDialog.show", return_value="Green"
    ) as mock_show:
        result = simpledialog.askfromlistbox(message="Choose color:", choices=choices)
        assert result == "Green"
        mock_show.assert_called_once()


def test_askfromlistbox_multiple_selection():
    """Test askfromlistbox with multiple selection."""
    choices = ["Red", "Green", "Blue"]
    with patch(
        "tkface.simpledialog.CustomSimpleDialog.show",
        return_value=["Red", "Blue"],
    ) as mock_show:
        result = simpledialog.askfromlistbox(
            message="Choose colors:", choices=choices, multiple=True
        )
        assert result == ["Red", "Blue"]
        mock_show.assert_called_once()


def test_askfromlistbox_no_choices():
    """Test askfromlistbox with no choices raises ValueError."""
    with pytest.raises(ValueError, match="choices parameter is required"):
        simpledialog.askfromlistbox(message="Test", choices=[])


def test_askfromlistbox_empty_choices():
    """Test askfromlistbox with empty choices raises ValueError."""
    with pytest.raises(ValueError, match="choices parameter is required"):
        simpledialog.askfromlistbox(message="Test", choices=None)


def test_custom_simpledialog_with_choices(root):
    """Test CustomSimpleDialog with choices parameter."""
    from tkface.dialog.simpledialog import CustomSimpleDialog

    choices = ["Option 1", "Option 2", "Option 3"]
    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Listbox"):
        from tkface.dialog.simpledialog import SimpleDialogConfig

        dialog = CustomSimpleDialog(
            master=root,
            config=SimpleDialogConfig(
                title="Test",
                message="Choose an option:",
                choices=choices,
            ),
        )
        assert dialog.choices == choices
        assert dialog.multiple is False


def test_custom_simpledialog_with_multiple_selection(root):
    """Test CustomSimpleDialog with multiple selection."""
    from tkface.dialog.simpledialog import CustomSimpleDialog

    choices = ["Option 1", "Option 2", "Option 3"]
    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Listbox"):
        from tkface.dialog.simpledialog import SimpleDialogConfig

        dialog = CustomSimpleDialog(
            master=root,
            config=SimpleDialogConfig(
                title="Test",
                message="Choose options:",
                choices=choices,
                multiple=True,
            ),
        )
        assert dialog.choices == choices
        assert dialog.multiple is True


def test_custom_simpledialog_with_initial_selection(root):
    """Test CustomSimpleDialog with initial selection."""
    from tkface.dialog.simpledialog import CustomSimpleDialog

    choices = ["Option 1", "Option 2", "Option 3"]
    initial_selection = [0, 2]  # Select first and third items
    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Listbox"):
        from tkface.dialog.simpledialog import SimpleDialogConfig

        dialog = CustomSimpleDialog(
            master=root,
            config=SimpleDialogConfig(
                title="Test",
                message="Choose options:",
                choices=choices,
                multiple=True,
                initial_selection=initial_selection,
            ),
        )
        assert dialog.initial_selection == initial_selection


def test_custom_simpledialog_with_validation(root):
    """Test CustomSimpleDialog with validation function."""
    from tkface.dialog.simpledialog import CustomSimpleDialog

    def validate_func(value):
        return len(value) > 0

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Entry"):
        from tkface.dialog.simpledialog import SimpleDialogConfig

        dialog = CustomSimpleDialog(
            master=root,
            config=SimpleDialogConfig(
                title="Test",
                message="Enter text:",
                validate_func=validate_func,
            ),
        )
        assert dialog.validate_func is validate_func


def test_custom_simpledialog_validation_failure(root):
    """Test CustomSimpleDialog validation failure."""
    from tkface.dialog.simpledialog import CustomSimpleDialog

    def validate_func(value):  # pylint: disable=unused-argument
        return False  # Always fail validation

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Entry"), patch("tkface.messagebox.showwarning") as mock_warning:
        from tkface.dialog.simpledialog import SimpleDialogConfig

        dialog = CustomSimpleDialog(
            master=root,
            config=SimpleDialogConfig(
                title="Test",
                message="Enter text:",
                validate_func=validate_func,
            ),
        )
        # Test validation failure
        dialog.entry_var = type("MockVar", (), {"get": lambda self: "test"})()
        dialog._on_ok()
        # Should show warning and not close dialog
        mock_warning.assert_called_once()


def test_custom_simpledialog_get_selection_result_single(root):
    """Test _get_selection_result with single selection."""
    from tkface.dialog.simpledialog import CustomSimpleDialog

    choices = ["Option 1", "Option 2", "Option 3"]
    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Listbox"):
        from tkface.dialog.simpledialog import SimpleDialogConfig

        dialog = CustomSimpleDialog(
            master=root,
            config=SimpleDialogConfig(
                title="Test",
                message="Choose an option:",
                choices=choices,
            ),
        )
        # Mock listbox with single selection
        mock_listbox_instance = MagicMock()
        mock_listbox_instance.curselection.return_value = [1]  # Select second item
        dialog.listbox = mock_listbox_instance
        result = dialog._get_selection_result()
        assert result == "Option 2"


def test_custom_simpledialog_get_selection_result_multiple(root):
    """Test _get_selection_result with multiple selection."""
    from tkface.dialog.simpledialog import CustomSimpleDialog

    choices = ["Option 1", "Option 2", "Option 3"]
    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Listbox"):
        from tkface.dialog.simpledialog import SimpleDialogConfig

        dialog = CustomSimpleDialog(
            master=root,
            config=SimpleDialogConfig(
                title="Test",
                message="Choose options:",
                choices=choices,
                multiple=True,
            ),
        )
        # Mock listbox with multiple selection
        mock_listbox_instance = MagicMock()
        mock_listbox_instance.curselection.return_value = [
            0,
            2,
        ]  # Select first and third items
        dialog.listbox = mock_listbox_instance
        result = dialog._get_selection_result()
        assert result == ["Option 1", "Option 3"]


def test_custom_simpledialog_get_selection_result_no_selection(root):
    """Test _get_selection_result with no selection."""
    from tkface.dialog.simpledialog import CustomSimpleDialog

    choices = ["Option 1", "Option 2", "Option 3"]
    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Listbox"):
        from tkface.dialog.simpledialog import SimpleDialogConfig

        dialog = CustomSimpleDialog(
            master=root,
            config=SimpleDialogConfig(
                title="Test",
                message="Choose an option:",
                choices=choices,
            ),
        )
        # Mock listbox with no selection
        mock_listbox_instance = MagicMock()
        mock_listbox_instance.curselection.return_value = []
        dialog.listbox = mock_listbox_instance
        result = dialog._get_selection_result()
        assert result is None


def test_custom_simpledialog_double_click(root):
    """Test _on_double_click method."""
    from tkface.dialog.simpledialog import CustomSimpleDialog

    choices = ["Option 1", "Option 2", "Option 3"]
    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Listbox"):
        from tkface.dialog.simpledialog import SimpleDialogConfig

        dialog = CustomSimpleDialog(
            master=root,
            config=SimpleDialogConfig(
                title="Test",
                message="Choose an option:",
                choices=choices,
            ),
        )
        # Mock listbox with selection
        mock_listbox_instance = MagicMock()
        mock_listbox_instance.curselection.return_value = [1]
        dialog.listbox = mock_listbox_instance
        # Mock event
        mock_event = MagicMock()
        with patch.object(dialog, "set_result") as mock_set_result:
            dialog._on_double_click(mock_event)
            mock_set_result.assert_called_once_with("Option 2")


def test_custom_simpledialog_double_click_no_selection(root):
    """Test _on_double_click method with no selection."""
    from tkface.dialog.simpledialog import CustomSimpleDialog

    choices = ["Option 1", "Option 2", "Option 3"]
    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Listbox"):
        from tkface.dialog.simpledialog import SimpleDialogConfig

        dialog = CustomSimpleDialog(
            master=root,
            config=SimpleDialogConfig(
                title="Test",
                message="Choose an option:",
                choices=choices,
            ),
        )
        # Mock listbox with no selection
        mock_listbox_instance = MagicMock()
        mock_listbox_instance.curselection.return_value = []
        dialog.listbox = mock_listbox_instance
        # Mock event
        mock_event = MagicMock()
        with patch.object(dialog, "set_result") as mock_set_result:
            dialog._on_double_click(mock_event)
            mock_set_result.assert_not_called()


def test_custom_simpledialog_without_master():
    """Test CustomSimpleDialog when no master is provided
    and no root exists."""
    from tkface.dialog.simpledialog import CustomSimpleDialog

    with patch("tkinter._default_root", None):
        with pytest.raises(RuntimeError, match="No Tk root window found"):
            CustomSimpleDialog()


def test_custom_simpledialog_show_class_method():
    """Test CustomSimpleDialog.show class method."""
    from tkface.dialog.simpledialog import CustomSimpleDialog, SimpleDialogConfig

    with patch("tkface.dialog.simpledialog.CustomSimpleDialog.show") as mock_show:
        mock_show.return_value = "test_result"
        result = CustomSimpleDialog.show(
            config=SimpleDialogConfig(message="Test", title="Test Title")
        )
        assert result == "test_result"
        mock_show.assert_called_once()


def test_custom_simpledialog_show_with_created_root():
    """Test CustomSimpleDialog.show when root is created."""
    from tkface.dialog.simpledialog import CustomSimpleDialog, SimpleDialogConfig

    with patch("tkface.dialog.simpledialog.CustomSimpleDialog.show") as mock_show:
        mock_show.return_value = "test_result"
        result = CustomSimpleDialog.show(config=SimpleDialogConfig(message="Test"))
        assert result == "test_result"
        mock_show.assert_called_once()


def test_custom_simpledialog_close(root):
    """Test close method."""
    from tkface.dialog.simpledialog import CustomSimpleDialog

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Entry"), patch("tkinter.Toplevel.destroy") as mock_destroy:
        from tkface.dialog.simpledialog import SimpleDialogConfig

        dialog = CustomSimpleDialog(
            master=root,
            config=SimpleDialogConfig(title="Test", message="Test Message"),
        )
        dialog.close()
        mock_destroy.assert_called()


def test_custom_simpledialog_on_cancel(root):
    """Test _on_cancel method."""
    from tkface.dialog.simpledialog import CustomSimpleDialog

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Button"
    ), patch("tkinter.Entry"), patch("tkinter.Toplevel.destroy") as mock_destroy:
        from tkface.dialog.simpledialog import SimpleDialogConfig

        dialog = CustomSimpleDialog(
            master=root,
            config=SimpleDialogConfig(title="Test", message="Test Message"),
        )
        dialog._on_cancel()
        assert dialog.result is None
        mock_destroy.assert_called()


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


def test_simpledialog_error_message_translation(root):
    """Test that simpledialog error messages are translated correctly."""
    from tkface.dialog.simpledialog import CustomSimpleDialog, SimpleDialogConfig

    def validate_false(val):  # pylint: disable=unused-argument
        return False

    with patch("tkinter.Toplevel.wait_window"), patch("tkinter.Label"), patch(
        "tkinter.Entry"
    ), patch("tkinter.Button"), patch(
        "tkface.dialog.messagebox.showwarning"
    ) as mock_warning:
        dialog = CustomSimpleDialog(
            master=root,
            config=SimpleDialogConfig(
                title="Input",
                message="Test message",
                validate_func=validate_false,
                language="ja",
            ),
        )
        # Trigger validation by calling _on_ok
        dialog._on_ok()

    # Check that the error message was translated
    warning_calls = mock_warning.call_args_list
    assert len(warning_calls) > 0, "Error message should be shown"

    # Check that the error message contains translated text
    call_args = warning_calls[0]
    message = call_args.kwargs.get("message", "")
    assert "入力が無効です。" in message, "Translated error message not found"
    assert "もう一度お試しください。" in message, "Translated retry message not found"
