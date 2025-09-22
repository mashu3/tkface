import tkinter as tk
from unittest.mock import Mock, patch

import pytest

# Note: We test internal helpers in tkface.dialog.__init__
# - _get_or_create_root
# - _get_button_labels
# - _position_window
# - _setup_dialog_base


def test_get_or_create_root_creates_when_missing(monkeypatch):
    import tkface.dialog.__init__ as dialog_init

    # Ensure no default root exists
    monkeypatch.setattr(tk, "_default_root", None, raising=False)

    with patch.object(tk, "Tk") as mock_tk:
        mock_root = Mock()
        mock_root.withdraw = Mock()
        mock_tk.return_value = mock_root

        root, created = dialog_init._get_or_create_root()  # pylint: disable=protected-access
        assert root is mock_root
        assert created is True
        mock_root.withdraw.assert_called_once()
        mock_tk.assert_called_once()


def test_get_or_create_root_reuses_existing(monkeypatch):
    import tkface.dialog.__init__ as dialog_init

    existing_root = Mock()
    monkeypatch.setattr(tk, "_default_root", existing_root, raising=False)

    root, created = dialog_init._get_or_create_root()  # pylint: disable=protected-access
    assert root is existing_root
    assert created is False


def test_get_button_labels_sets_language_when_provided(monkeypatch):
    import tkface.dialog.__init__ as dialog_init

    mock_root = Mock()
    with patch("tkface.lang.lang.set") as mock_lang_set:
        # language と root がある時に set が呼ばれる
        res = dialog_init._get_button_labels(  # pylint: disable=protected-access
            button_set="ok", root=mock_root, language="ja"
        )
        assert res == []  # __init__ 側の実装は placeholder
        mock_lang_set.assert_called_once_with("ja", mock_root)


def test_position_window_center_and_offset():
    import tkface.dialog.__init__ as dialog_init

    window = Mock()
    window.update_idletasks = Mock()
    window.winfo_reqwidth.return_value = 200
    window.winfo_reqheight.return_value = 100
    window.geometry = Mock()

    master = Mock()
    master.winfo_rootx.return_value = 100
    master.winfo_rooty.return_value = 50
    master.winfo_width.return_value = 400
    master.winfo_height.return_value = 300

    # x, y を None にしてセンタリング + オフセット
    dialog_init._position_window(  # pylint: disable=protected-access
        window, master, x=None, y=None, x_offset=10, y_offset=20
    )

    # センタリング: 親中心(100+ (400-200)//2, 50 + (300-100)//2) = (200, 150)
    # オフセット加算後: (210, 170)
    window.update_idletasks.assert_called_once()
    window.geometry.assert_called_once_with("200x100+210+170")


def test_position_window_explicit_coordinates():
    import tkface.dialog.__init__ as dialog_init

    window = Mock()
    window.update_idletasks = Mock()
    window.winfo_reqwidth.return_value = 200
    window.winfo_reqheight.return_value = 100
    window.geometry = Mock()

    master = Mock()

    dialog_init._position_window(  # pylint: disable=protected-access
        window, master, x=300, y=400, x_offset=-5, y_offset=5
    )

    window.update_idletasks.assert_called_once()
    window.geometry.assert_called_once_with("200x100+295+405")


def test_setup_dialog_base_with_master_pass_through():
    import tkface.dialog.__init__ as dialog_init

    master = Mock()
    root, created, language = dialog_init._setup_dialog_base(  # pylint: disable=protected-access
        master, "ja"
    )
    assert root is master
    assert created is False
    assert language == "ja"


def test_setup_dialog_base_without_master_raises():
    import tkface.dialog.__init__ as dialog_init

    # master is None and tk._default_root is None -> RuntimeError
    with patch.object(tk, "_default_root", None, create=True):
        with pytest.raises(RuntimeError):
            dialog_init._setup_dialog_base(None, "en")  # pylint: disable=protected-access


def test_setup_dialog_base_uses_default_root(monkeypatch):
    import tkface.dialog.__init__ as dialog_init

    default_root = Mock()
    # __init__ 実装では master が None なら _default_root を見て、None なら例外
    # ここでは _default_root が存在するケースを検証
    monkeypatch.setattr(tk, "_default_root", default_root, raising=False)

    root, created, language = dialog_init._setup_dialog_base(  # pylint: disable=protected-access
        None, "auto"
    )
    assert root is default_root
    assert created is False
    assert language == "auto"
