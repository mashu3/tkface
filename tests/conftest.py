import pytest
import tkinter as tk
import os
import time
import threading
import sys
import gc

# グローバルなTkinterインスタンス管理
_tk_root = None
_tk_lock = threading.Lock()
_tk_initialized = False

def _cleanup_tkinter():
    """Clean up Tkinter resources safely."""
    global _tk_root, _tk_initialized
    
    if _tk_root is not None:
        try:
            # すべての子ウィンドウを破棄
            for widget in _tk_root.winfo_children():
                try:
                    widget.destroy()
                except (tk.TclError, AttributeError):
                    pass
            
            # メインウィンドウを破棄
            _tk_root.destroy()
        except tk.TclError:
            pass
        except Exception:
            pass
        finally:
            _tk_root = None
            _tk_initialized = False
    
    # ガベージコレクションを強制実行
    gc.collect()
    
    # リソース解放のための短い待機
    time.sleep(0.1)

@pytest.fixture(scope="session")
def root():
    """Create a root window for the tests with session scope for better parallel execution."""
    global _tk_root, _tk_initialized
    
    with _tk_lock:
        try:
            # 環境変数の設定
            os.environ['TK_SILENCE_DEPRECATION'] = '1'
            os.environ['PYTHONUNBUFFERED'] = '1'
            
            # 既存のインスタンスをクリーンアップ
            if _tk_initialized:
                _cleanup_tkinter()
            
            # 新しいルートウィンドウを作成
            _tk_root = tk.Tk()
            _tk_root.withdraw()  # Hide the main window
            
            # ウィンドウの更新を強制
            _tk_root.update()
            _tk_root.update_idletasks()
            
            _tk_initialized = True
            
            yield _tk_root
            
        except tk.TclError as e:
            error_str = str(e)
            if any(pattern in error_str for pattern in [
                "Can't find a usable tk.tcl",
                "invalid command name",
                "Can't find a usable init.tcl",
                "vistaTheme.tcl",
                "init.tcl",
                "No error",
                "fonts.tcl",
                "icons.tcl",
                "tk.tcl"
            ]):
                pytest.skip(f"Tkinter not properly installed or Tcl/Tk files missing: {error_str}")
            else:
                raise
        except Exception as e:
            # 予期しないエラーの場合はクリーンアップを試行
            _cleanup_tkinter()
            raise

@pytest.fixture(scope="session", autouse=True)
def cleanup_session():
    """Clean up Tkinter resources after all tests complete."""
    yield
    with _tk_lock:
        _cleanup_tkinter()

@pytest.fixture(scope="function")
def root_function():
    """Create a temporary root window for individual function tests."""
    try:
        # 環境変数の設定
        os.environ['TK_SILENCE_DEPRECATION'] = '1'
        
        # 新しいルートウィンドウを作成
        temp_root = tk.Tk()
        temp_root.withdraw()
        temp_root.update()
        
        yield temp_root
        
        # クリーンアップ
        try:
            temp_root.destroy()
        except tk.TclError:
            pass
        
    except tk.TclError as e:
        error_str = str(e)
        if any(pattern in error_str for pattern in [
            "Can't find a usable tk.tcl",
            "invalid command name",
            "Can't find a usable init.tcl",
            "vistaTheme.tcl",
            "init.tcl",
            "No error",
            "fonts.tcl",
            "icons.tcl",
            "tk.tcl"
        ]):
            pytest.skip(f"Tkinter not properly installed or Tcl/Tk files missing: {error_str}")
        else:
            raise

# 並列テスト用の設定
def pytest_configure(config):
    """Configure pytest for parallel execution."""
    # 並列実行時の警告を抑制
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "gui: marks tests as GUI tests"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection for better parallel execution."""
    for item in items:
        # GUIテストにはguiマーカーを追加
        if "messagebox" in item.nodeid or "calendar" in item.nodeid:
            item.add_marker(pytest.mark.gui) 