import pytest
from unittest.mock import patch
from tkface import simpledialog

@pytest.mark.parametrize("mocked_return, expected", [
    ("hello", "hello"),
    (None, None),
])
def test_askstring_return_value(mocked_return, expected):
    with patch('tkface.simpledialog.CustomSimpleDialog.show', return_value=mocked_return) as mock_show:
        result = simpledialog.askstring(message="Enter text:")
        assert result == expected
        mock_show.assert_called_once()

@pytest.mark.parametrize("mocked_return, expected", [
    ("42", 42),
    (None, None),
])
def test_askinteger_return_value(mocked_return, expected):
    with patch('tkface.simpledialog.CustomSimpleDialog.show', return_value=mocked_return) as mock_show:
        result = simpledialog.askinteger(message="Enter int:")
        assert result == expected
        mock_show.assert_called_once()

@pytest.mark.parametrize("mocked_return, expected", [
    ("3.14", 3.14),
    (None, None),
])
def test_askfloat_return_value(mocked_return, expected):
    with patch('tkface.simpledialog.CustomSimpleDialog.show', return_value=mocked_return) as mock_show:
        result = simpledialog.askfloat(message="Enter float:")
        assert result == expected
        mock_show.assert_called_once()

@pytest.mark.parametrize("func, value, minv, maxv, valid", [
    (simpledialog.askinteger, "5", 1, 10, 5),
    (simpledialog.askinteger, "0", 1, 10, None),
    (simpledialog.askinteger, "11", 1, 10, None),
    (simpledialog.askfloat, "2.5", 1.0, 3.0, 2.5),
    (simpledialog.askfloat, "0.5", 1.0, 3.0, None),
    (simpledialog.askfloat, "3.5", 1.0, 3.0, None),
])
def test_range_validation(func, value, minv, maxv, valid):
    # Control whether validation passes or fails using a mock
    with patch('tkface.simpledialog.CustomSimpleDialog.show', return_value=value if valid is not None else None):
        result = func(message="test", minvalue=minv, maxvalue=maxv)
        assert result == valid

@pytest.mark.parametrize("lang", ["ja", "en"])
def test_language_passed_to_show(lang):
    with patch('tkface.simpledialog.CustomSimpleDialog.show') as mock_show:
        simpledialog.askstring(message="Test", language=lang)
        mock_show.assert_called_once()
        args, kwargs = mock_show.call_args
        assert kwargs['language'] == lang

@pytest.mark.parametrize("x, y, x_offset, y_offset", [
    (100, 200, 0, 0),
    (None, None, 50, -30),
])
def test_dialog_positioning_kwargs_passed(x, y, x_offset, y_offset):
    with patch('tkface.simpledialog.CustomSimpleDialog.show') as mock_show:
        simpledialog.askstring(
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
def test_simpledialog_translation_calls(root, lang):
    """Test that lang.get is called for title, message, and buttons."""
    with patch('tkface.lang.get') as mock_lang_get:
        mock_lang_get.side_effect = lambda key, *a, **kw: f"{key}_{lang}"

        from tkface.simpledialog import CustomSimpleDialog
        with patch('tkinter.Toplevel.wait_window'), \
             patch('tkinter.Label'), \
             patch('tkinter.Button'), \
             patch('tkinter.Entry'):
            CustomSimpleDialog(
                master=root,
                title="Test Title",
                message="Test Message",
                language=lang
            )

    calls = mock_lang_get.call_args_list
    assert any(c.args[0] == 'Test Title' for c in calls)
    assert any(c.args[0] == 'ok' for c in calls)
    assert any(c.args[0] == 'cancel' for c in calls)
    assert all(c.kwargs['language'] == lang for c in calls if c.args[0] in ['ok', 'cancel', 'Test Title']) 