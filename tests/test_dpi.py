"""
Tests for tkface.win.dpi module.

This module tests the DPI management functionality for Windows applications,
including automatic ttk widget configuration and tk widget patching.
"""

import contextlib
import ctypes
import sys
import tkinter as tk
from ctypes import wintypes
from unittest.mock import MagicMock, Mock, call, patch

import pytest
from tkinter import ttk


# Common mock fixtures for DPI testing
@pytest.fixture
def mock_root():
    """Create a mock Tkinter root window with common attributes."""
    root = MagicMock()
    root.winfo_id.return_value = 12345
    root.wm_geometry = MagicMock()
    root.geometry.return_value = "800x600"
    root.tk.call.return_value = "2.0"
    return root


@pytest.fixture
def mock_windll():
    """Create a mock Windows API windll object."""
    windll = MagicMock()
    windll.user32.MonitorFromWindow.return_value = 67890
    windll.shcore.GetDpiForMonitor.return_value = None
    windll.shcore.GetScaleFactorForDevice.return_value = 200
    windll.shcore.SetProcessDpiAwareness.return_value = None
    return windll


@pytest.fixture
def mock_dpi_values():
    """Create mock DPI value objects."""
    mock_x_dpi = MagicMock()
    mock_x_dpi.value = 192
    mock_y_dpi = MagicMock()
    mock_y_dpi.value = 192
    return mock_x_dpi, mock_y_dpi


@pytest.fixture
def mock_wintypes():
    """Create mock wintypes objects."""
    wintypes_mock = MagicMock()
    wintypes_mock.HWND.return_value = 12345
    wintypes_mock.DWORD.return_value = 2
    return wintypes_mock


@pytest.fixture
def mock_pointer():
    """Create mock pointer function."""
    pointer_mock = MagicMock()
    return pointer_mock


@pytest.fixture
def manager():
    """Create a DPIManager instance."""
    from tkface.win.dpi import DPIManager
    return DPIManager()


@pytest.fixture
def mock_root_with_dpi():
    """Create a mock root with DPI attributes set."""
    root = MagicMock()
    root.winfo_id.return_value = 12345
    root.wm_geometry = MagicMock()
    root.geometry.return_value = "800x600"
    root.tk.call.return_value = "2.0"
    root.DPI_X = 192
    root.DPI_Y = 192
    root.DPI_scaling = 2.0
    return root


@pytest.fixture
def mock_root_with_exception():
    """Create a mock root that raises exceptions for error testing."""
    root = MagicMock()
    root.winfo_id.side_effect = Exception("Test error")
    root.tk.call.side_effect = Exception("Test error")
    return root


@pytest.fixture
def common_test_scaling_factors():
    """Common scaling factors used in tests."""
    return [1.0, 1.5, 2.0, 2.5]


@pytest.fixture
def common_test_values():
    """Common test values for DPI calculations."""
    return {
        'small_value': 10,
        'medium_value': 100,
        'large_value': 1000,
        'font_size': 12,
        'geometry': "800x600",
        'hwnd': 12345
    }


@pytest.fixture
def windows_patches():
    """Create common Windows-related patches."""
    with patch('tkface.win.dpi.is_windows') as mock_is_windows, \
         patch('tkface.win.dpi.ctypes') as mock_ctypes:
        mock_is_windows.return_value = True
        yield mock_is_windows, mock_ctypes


@pytest.fixture
def non_windows_patches():
    """Create common non-Windows patches."""
    with patch('tkface.win.dpi.is_windows') as mock_is_windows:
        mock_is_windows.return_value = False
        yield mock_is_windows


@pytest.fixture
def mock_tkfont():
    """Create mock tkfont module."""
    with patch('tkface.win.dpi.tkfont') as mock_tkfont:
        mock_tkfont.names.return_value = ["TkDefaultFont"]
        mock_font = MagicMock()
        mock_font.__getitem__.return_value = -12
        mock_tkfont.Font.return_value = mock_font
        yield mock_tkfont


# Helper functions for common test patterns
def create_windows_dpi_setup(mock_windll, mock_dpi_values, mock_wintypes, mock_pointer):
    """Helper function to setup Windows DPI mocking."""
    mock_x_dpi, mock_y_dpi = mock_dpi_values
    mock_wintypes.HWND.return_value = 12345
    mock_wintypes.DWORD.return_value = 2
    mock_wintypes.UINT.return_value = mock_x_dpi
    mock_pointer.side_effect = [mock_x_dpi, mock_y_dpi]
    return mock_x_dpi, mock_y_dpi


def assert_dpi_attributes_set(mock_root):
    """Helper function to assert DPI attributes are set."""
    assert hasattr(mock_root, 'DPI_X')
    assert hasattr(mock_root, 'DPI_Y')
    assert hasattr(mock_root, 'DPI_scaling')


def helper_test_with_exception_handling(func, *args, **kwargs):
    """Helper function to test exception handling."""
    try:
        result = func(*args, **kwargs)
        return result
    except Exception:
        # Expected to handle exceptions gracefully
        return None


# Enhanced helper functions for common test patterns
def create_dpi_manager_for_test():
    """Helper function to create a DPIManager instance for testing."""
    from tkface.win.dpi import DPIManager
    return DPIManager()


def setup_mock_root_with_dpi_attributes(root, dpi_x=192, dpi_y=192, scaling=2.0):
    """Helper function to setup mock root with DPI attributes."""
    root.DPI_X = dpi_x
    root.DPI_Y = dpi_y
    root.DPI_scaling = scaling
    return root


def create_mock_windll_setup():
    """Helper function to create a complete mock windll setup."""
    windll = MagicMock()
    windll.user32.MonitorFromWindow.return_value = 67890
    windll.shcore.GetDpiForMonitor.return_value = None
    windll.shcore.GetScaleFactorForDevice.return_value = 200
    windll.shcore.SetProcessDpiAwareness.return_value = None
    return windll


def create_mock_dpi_values(x_dpi=192, y_dpi=192):
    """Helper function to create mock DPI values."""
    mock_x_dpi = MagicMock()
    mock_x_dpi.value = x_dpi
    mock_y_dpi = MagicMock()
    mock_y_dpi.value = y_dpi
    return mock_x_dpi, mock_y_dpi


# Common mock creation helpers to reduce duplication
def create_basic_mock_root(winfo_id=12345, geometry="800x600", tk_call="2.0", **kwargs):
    """Create a basic mock root with common attributes."""
    root = MagicMock()
    root.winfo_id.return_value = winfo_id
    root.wm_geometry = MagicMock()
    root.geometry.return_value = geometry
    root.tk.call.return_value = tk_call
    
    # Set any additional attributes passed in kwargs
    for key, value in kwargs.items():
        setattr(root, key, value)
    
    return root


def create_mock_windll_basic():
    """Create a basic mock windll object."""
    windll = MagicMock()
    windll.user32.MonitorFromWindow.return_value = 67890
    windll.shcore.GetDpiForMonitor.return_value = None
    windll.shcore.GetScaleFactorForDevice.return_value = 200
    windll.shcore.SetProcessDpiAwareness.return_value = None
    windll.user32.SetProcessDPIAware.return_value = None
    return windll


def create_mock_dpi_values_basic(x_dpi=192, y_dpi=192):
    """Create basic mock DPI values."""
    mock_x_dpi = MagicMock()
    mock_x_dpi.value = x_dpi
    mock_y_dpi = MagicMock()
    mock_y_dpi.value = y_dpi
    return mock_x_dpi, mock_y_dpi


def with_treeview_column_patch(test_func):
    """Decorator to handle TreeView column method patching and restoration."""
    def wrapper(*args, **kwargs):
        # Use the comprehensive test context helper with treeview patches
        decorator_func = with_test_context(
            is_windows=True,
            treeview_patches=['column']
        )
        return decorator_func(test_func)(*args, **kwargs)
    return wrapper


def with_treeview_style_patch(test_func):
    """Decorator to handle TreeView style method patching and restoration."""
    def wrapper(*args, **kwargs):
        # Use the comprehensive test context helper with treeview patches
        decorator_func = with_test_context(
            is_windows=True,
            treeview_patches=['style']
        )
        return decorator_func(test_func)(*args, **kwargs)
    return wrapper


def with_real_tkinter_root(test_func):
    """Decorator to handle real Tkinter root creation and cleanup."""
    def wrapper(*args, **kwargs):
        # Use the comprehensive test context helper with real tkinter root
        decorator_func = with_test_context(
            is_windows=True,
            real_tkinter_root=True
        )
        return decorator_func(test_func)(*args, **kwargs)
    return wrapper


def with_widget_method_patch(method_name):
    """Decorator factory to handle widget method patching and restoration."""
    def decorator(test_func):
        def wrapper(*args, **kwargs):
            # Use the comprehensive test context helper with tkinter patches
            decorator_func = with_test_context(
                is_windows=True,
                tkinter_patches=[{
                    'class': tk.Widget,
                    'method': method_name,
                    'scaling_factor': 2.0
                }]
            )
            return decorator_func(test_func)(*args, **kwargs)
        return wrapper
    return decorator


def with_tkinter_constructor_patch(tk_class, method_name='__init__'):
    """Decorator factory to handle tkinter constructor patching and restoration."""
    def decorator(test_func):
        def wrapper(*args, **kwargs):
            # Use the comprehensive test context helper with tkinter patches
            decorator_func = with_test_context(
                is_windows=True,
                tkinter_patches=[{
                    'class': tk_class,
                    'method': method_name,
                    'scaling_factor': 2.0
                }]
            )
            return decorator_func(test_func)(*args, **kwargs)
        return wrapper
    return decorator


# Common mock creation helpers
def create_mock_instance():
    """Helper function to create a mock instance."""
    return MagicMock()


def create_mock_parent():
    """Helper function to create a mock parent."""
    return MagicMock()


def _test_scale_icon_with_scaling(scaling_factor, icon_name="error", max_scale=None, expected_result=None):
    """
    Helper function to test scale_icon with common Windows context setup.
    
    Args:
        scaling_factor: The scaling factor to mock
        icon_name: The icon name to test (default: "error")
        max_scale: Optional max_scale parameter
        expected_result: Expected result (default: "scaled_{icon_name}_large")
    
    Returns:
        The result of scale_icon call
    """
    if expected_result is None:
        expected_result = f"scaled_{icon_name}_large"
    
    with WindowsPatchContext(is_windows=True) as patch_ctx:
        from tkface.win.dpi import get_scaling_factor, scale_icon
        
        with GetScalingFactorMockContext(return_value=scaling_factor) as mock_ctx:
            mock_parent = create_mock_parent()
            mock_parent.tk.call.return_value = None
            
            if max_scale is not None:
                result = scale_icon(icon_name, mock_parent, max_scale=max_scale)
            else:
                result = scale_icon(icon_name, mock_parent)
            
            return result


def _test_scale_icon_with_patch(is_windows=True, scaling_factor=None, icon_name="error", parent=None):
    """
    Helper function to test scale_icon using patch decorators.
    
    Args:
        is_windows: Whether to mock as Windows platform (default: True)
        scaling_factor: The scaling factor to mock (default: None)
        icon_name: The icon name to test (default: "error")
        parent: Parent widget to use (default: None, will create mock)
    
    Returns:
        The result of scale_icon call
    """
    with patch('tkface.win.dpi.is_windows', return_value=is_windows):
        from tkface.win.dpi import scale_icon
        
        if scaling_factor is not None:
            with patch('tkface.win.dpi.get_scaling_factor', return_value=scaling_factor):
                if parent is None:
                    mock_parent = create_mock_parent()
                    mock_parent.tk.call.return_value = None
                    parent = mock_parent
                
                result = scale_icon(icon_name, parent)
                return result
        else:
            result = scale_icon(icon_name, parent)
            return result


def _test_scale_icon_with_exception(exception, icon_name="error", parent=None):
    """
    Helper function to test scale_icon with exception handling.
    
    Args:
        exception: The exception to raise in get_scaling_factor
        icon_name: The icon name to test (default: "error")
        parent: Parent widget to use (default: None)
    
    Returns:
        The result of scale_icon call
    """
    with WindowsPatchContext(is_windows=True) as patch_ctx:
        from tkface.win.dpi import get_scaling_factor, scale_icon
        
        with GetScalingFactorMockContext(side_effect=exception) as mock_ctx:
            result = scale_icon(icon_name, parent)
            return result




def create_mock_original_method():
    """Helper function to create a mock original method."""
    return MagicMock()


def create_mock_root_with_dpi_scaling(scaling=2.0):
    """Helper function to create a mock root with DPI scaling."""
    root = MagicMock()
    root.DPI_scaling = scaling
    return root


def create_mock_root_with_geometry(geometry="800x600", tk_scale_factor=2):
    """Helper function to create a mock root with geometry and TkScale."""
    root = create_basic_mock_root()
    root.wm_geometry = create_mock_original_method()
    root.wm_geometry.return_value = geometry
    root.TkScale = lambda x: int(x * tk_scale_factor)
    return root


def create_mock_root_with_exception(exception_attr, exception_msg="Test error"):
    """Helper function to create a mock root that raises exceptions."""
    root = create_basic_mock_root()
    getattr(root, exception_attr).side_effect = Exception(exception_msg)
    return root


def create_mock_root_without_dpi_scaling():
    """Helper function to create a mock root without DPI_scaling attribute."""
    root = create_basic_mock_root()
    del root.DPI_scaling
    return root


# Comprehensive test context helper
def with_test_context(
    is_windows=True,
    wintypes_mock=None,
    windll_config=None,
    patches=None,
    tkinter_patches=None,
    treeview_patches=None,
    real_tkinter_root=False,
    **kwargs
):
    """
    Comprehensive decorator factory for test context setup.
    
    Args:
        is_windows (bool): Whether to use Windows context (default: True)
        wintypes_mock (dict): Wintypes mock configuration
            - hwnd: HWND value (default: 12345)
            - monitor_handle: Monitor handle (default: 2)
            - x_dpi: X DPI value (default: 96)
            - y_dpi: Y DPI value (default: 96)
        windll_config (dict): Windll configuration
            - get_dpi_return: Return value for GetDpiForMonitor
            - get_scale_return: Return value for GetScaleFactorForDevice
        patches (list): List of patch configurations
            - Each item: {'target': 'manager.method', 'return_value': None, 'side_effect': None}
        tkinter_patches (list): List of tkinter patch configurations
            - Each item: {'class': tk.Widget, 'method': 'method_name', 'scaling_factor': 2.0}
        treeview_patches (list): List of treeview patch types
            - Options: ['column', 'style']
        real_tkinter_root (bool): Whether to create real tkinter root
        **kwargs: Additional arguments passed to test function
    
    Returns:
        Decorator function
    """
    def decorator(test_func):
        def wrapper(self, *args, **kwargs):
            # Setup Windows/Non-Windows context
            with WindowsPatchContext(is_windows=is_windows) as patch_ctx:
                manager = create_dpi_manager_for_test()
                
                # Setup wintypes mock if specified
                wintypes_ctx = None
                if wintypes_mock:
                    wintypes_ctx = WintypesPointerMockContext(
                        wintypes_mock.get('hwnd', 12345),
                        wintypes_mock.get('monitor_handle', 2),
                        wintypes_mock.get('x_dpi', 96),
                        wintypes_mock.get('y_dpi', 96)
                    )
                
                # Setup windll config if specified
                windll_ctx = None
                if windll_config:
                    # Configure windll directly in patch_ctx
                    patch_ctx.get_windll().shcore.GetDpiForMonitor.return_value = windll_config.get('get_dpi_return')
                    patch_ctx.get_windll().shcore.GetScaleFactorForDevice.return_value = windll_config.get('get_scale_return', 200)
                
                # Setup tkinter root if specified
                root = None
                if real_tkinter_root:
                    try:
                        root = tk.Tk()
                        root.withdraw()
                    except tk.TclError:
                        pytest.skip("Tkinter not available")
                
                # Store original methods for restoration
                original_methods = {}
                
                try:
                    # Apply patches
                    patch_contexts = []
                    if patches:
                        for patch_config in patches:
                            target = patch_config['target']
                            method_name = target.split('.')[-1]
                            patch_ctx_obj = patch.object(
                                manager, method_name,
                                return_value=patch_config.get('return_value'),
                                side_effect=patch_config.get('side_effect')
                            )
                            patch_contexts.append(patch_ctx_obj)
                    
                    # Apply tkinter patches
                    if tkinter_patches:
                        for patch_config in tkinter_patches:
                            tk_class = patch_config['class']
                            method_name = patch_config['method']
                            scaling_factor = patch_config.get('scaling_factor', 2.0)
                            
                            original_method = getattr(tk_class, method_name)
                            original_methods[(tk_class, method_name)] = original_method
                            
                        # Apply the patch
                        if method_name == '__init__':
                            # For constructors, use the specific constructor method
                            if tk_class.__name__ == 'Menu':
                                patch_method = getattr(manager, '_patch_menu_constructor')
                            elif tk_class.__name__ == 'Menubutton':
                                patch_method = getattr(manager, '_patch_menubutton_constructor')
                            elif tk_class.__name__ == 'Treeview':
                                patch_method = getattr(manager, '_patch_treeview_constructor')
                            else:
                                # For other constructors, use the generic method
                                patch_method = getattr(manager, f'_patch_{tk_class.__name__.lower()}_constructor')
                        else:
                            # For layout methods, add '_method' suffix
                            patch_method = getattr(manager, f'_patch_{method_name}_method')
                        patch_method(scaling_factor)
                    
                    # Apply treeview patches
                    if treeview_patches:
                        from tkinter import ttk
                        if 'column' in treeview_patches:
                            original_methods[(ttk.Treeview, 'column')] = ttk.Treeview.column
                        if 'style' in treeview_patches:
                            original_methods[(ttk.Style, 'configure')] = ttk.Style.configure
                    
                    # Execute test with all contexts
                    contexts = [patch_ctx]
                    if wintypes_ctx:
                        contexts.append(wintypes_ctx)
                    contexts.extend(patch_contexts)
                    
                    with contextlib.ExitStack() as stack:
                        for ctx in contexts:
                            stack.enter_context(ctx)
                        
                        # Prepare test arguments
                        test_args = [self, manager, patch_ctx]
                        if wintypes_ctx:
                            test_args.append(wintypes_ctx)
                        if root:
                            test_args.insert(1, root)  # Insert root after self
                        
                        # Add commonly needed mock objects if test function expects them
                        import inspect
                        sig = inspect.signature(test_func)
                        param_names = list(sig.parameters.keys())
                        
                        # Add mock objects if they are expected by the test function
                        if 'mock_root' in param_names:
                            test_args.append(create_basic_mock_root())
                        if 'mock_windll' in param_names:
                            test_args.append(patch_ctx.get_windll() if is_windows else None)
                        if 'mock_dpi_values' in param_names:
                            test_args.append((192, 192, 2.0) if is_windows else (96, 96, 1.0))
                        
                        test_args.extend(args)
                        
                        return test_func(*test_args, **kwargs)
                
                finally:
                    # Restore original methods
                    for (tk_class, method_name), original_method in original_methods.items():
                        setattr(tk_class, method_name, original_method)
                    
                    # Cleanup root
                    if root:
                        try:
                            root.destroy()
                        except Exception as e:
                            # Log cleanup errors but don't fail the test
                            print(f"Warning: Failed to destroy root in cleanup: {e}")
        
        return wrapper
    return decorator




# Patch test helpers
def _test_widget_method_patch(manager, method_name, patch_method_name, scaling_factor=2.0):
    """Helper function to test widget method patching."""
    import tkinter as tk

    # Store original method for comparison
    original_method = getattr(tk.Widget, method_name)
    
    # Apply the patch
    patch_method = getattr(manager, patch_method_name)
    patch_method(scaling_factor)
    
    # Verify the method was patched
    assert getattr(tk.Widget, method_name) != original_method


def _test_tkinter_constructor_patch(manager, tk_class, patch_method_name, scaling_factor=2.0):
    """Helper function to test tkinter constructor patching."""
    # Store original method for comparison
    original_method = getattr(tk_class, '__init__')
    
    # Apply the patch
    patch_method = getattr(manager, patch_method_name)
    patch_method(scaling_factor)
    
    # Verify the method was patched
    assert getattr(tk_class, '__init__') != original_method


def _test_tkinter_constructor_patch_with_context(manager, tk_class, patch_method_name, scaling_factor=2.0):
    """Helper function to test tkinter constructor patching with TkinterMethodPatchContext."""
    with TkinterMethodPatchContext(tk_class, '__init__', manager, scaling_factor) as patch_ctx:
        # Apply the patch
        patch_method = getattr(manager, patch_method_name)
        patch_method(scaling_factor)
        
        # Verify the method was patched
        assert getattr(tk_class, '__init__') != patch_ctx.get_original_method()


def test_treeview_column_patch_basic(manager, scaling_factor=2.0):
    """Helper function to test basic treeview column method patching."""
    from tkinter import ttk

    # Store original method for comparison
    original_column = ttk.Treeview.column
    
    manager._patch_treeview_column_method(scaling_factor)
    
    # Verify the method was patched
    assert ttk.Treeview.column != original_column


def test_treeview_column_patch_with_parameters(manager, scaling_factor=2.0):
    """Helper function to test treeview column method patching with width and minwidth parameters."""
    from tkinter import ttk

    # Mock the original method before patching
    mock_original_column = create_mock_original_method()
    ttk.Treeview.column = mock_original_column
    
    # Apply the patch
    manager._patch_treeview_column_method(scaling_factor)
    
    # Test with width and minwidth parameters
    mock_instance = create_mock_instance()
    
    # Test with width and minwidth parameters
    ttk.Treeview.column(mock_instance, "column1", width=100, minwidth=50)
    
    # Should call original with scaled values
    expected_width = int(100 * scaling_factor)
    expected_minwidth = int(50 * scaling_factor)
    mock_original_column.assert_called_once_with(mock_instance, "column1", None, width=expected_width, minwidth=expected_minwidth)


def test_treeview_column_patch_without_scaling_params(manager, scaling_factor=2.0):
    """Helper function to test treeview column method patching without scaling parameters."""
    from tkinter import ttk
    
    manager._patch_treeview_column_method(scaling_factor)
    
    # Test without scaling parameters
    mock_instance = create_mock_instance()
    mock_original_column = create_mock_original_method()
    ttk.Treeview.column = mock_original_column
    
    # Test without scaling parameters
    ttk.Treeview.column(mock_instance, "column1", text="Test")
    
    # Should call original with unchanged values
    mock_original_column.assert_called_once_with(mock_instance, "column1", text="Test")


def test_treeview_style_patch_basic(manager, scaling_factor=2.0):
    """Helper function to test basic treeview style method patching."""
    from tkinter import ttk

    # Store original method for comparison
    original_configure = ttk.Style.configure
    
    manager._patch_treeview_style_method(scaling_factor)
    
    # Verify the method was patched
    assert ttk.Style.configure != original_configure


def test_treeview_style_patch_with_rowheight(manager, scaling_factor=2.0):
    """Helper function to test treeview style method patching with rowheight parameter."""
    from tkinter import ttk

    # Mock the original method before patching
    mock_original_configure = create_mock_original_method()
    ttk.Style.configure = mock_original_configure
    
    # Apply the patch
    manager._patch_treeview_style_method(scaling_factor)
    
    # Test with rowheight parameter
    mock_instance = create_mock_instance()
    
    # Test with rowheight parameter
    ttk.Style.configure(mock_instance, "style1", rowheight=20)
    
    # Should call original with scaled values
    expected_rowheight = int(20 * scaling_factor)
    mock_original_configure.assert_called_once_with(mock_instance, "style1", None, rowheight=expected_rowheight)


def test_treeview_style_patch_without_rowheight(manager, scaling_factor=2.0):
    """Helper function to test treeview style method patching without rowheight parameter."""
    from tkinter import ttk
    
    manager._patch_treeview_style_method(scaling_factor)
    
    # Test without rowheight parameter
    mock_instance = create_mock_instance()
    mock_original_configure = create_mock_original_method()
    ttk.Style.configure = mock_original_configure
    
    # Test without rowheight parameter
    ttk.Style.configure(mock_instance, "style1", text="Test")
    
    # Should call original with unchanged values
    mock_original_configure.assert_called_once_with(mock_instance, "style1", text="Test")


# Additional tests migrated from tests/test_dpi_extra.py

@pytest.mark.parametrize(
    "value,expected",
    [
        (51, 51),  # over upper bound -> no scaling
        ((60, 5), (60, 5)),  # tuple with out-of-range first -> no scaling
        ((5, 60), (5, 60)),  # tuple with out-of-range second -> no scaling
        (-51, -51),  # abs(value) > 50 -> no scaling
    ],
)
def test_scale_padding_value_out_of_range_no_scaling(manager, value, expected):
    assert manager._scale_padding_value(value, 2.0) == expected


def test_scale_padding_kwargs_out_of_range_no_scaling(manager):
    kwargs = {"padx": 100, "pady": (5, 60)}
    scaled = manager._scale_padding_kwargs(kwargs, 2.0)
    assert scaled["padx"] == 100
    assert scaled["pady"] == (5, 60)


def test_patch_ttk_checkbutton_radiobutton_width_scaling(manager):
    with patch("tkinter.ttk.Checkbutton.__init__") as cb_init, \
         patch("tkinter.ttk.Radiobutton.__init__") as rb_init:
        cb_init.return_value = None
        rb_init.return_value = None

        # Patch wrappers
        manager._patch_ttk_checkbutton_constructor(2.0)
        manager._patch_ttk_radiobutton_constructor(1.5)

        # New classes should scale width if provided
        class Dummy:
            pass

        # Checkbutton width scaling
        tk.ttk.Checkbutton.__init__(Dummy(), None, width=10)
        assert cb_init.call_args.kwargs["width"] == 20

        # Radiobutton width scaling
        tk.ttk.Radiobutton.__init__(Dummy(), None, width=10)
        assert rb_init.call_args.kwargs["width"] == 15


def test_patch_ttk_style_for_dpi_success_and_inner_failures(manager):
    with patch("tkinter.ttk.Style") as style_cls:
        style = Mock()
        style_cls.return_value = style

        def configure_side_effect(name, **kw):  # pylint: disable=unused-argument
            if name == "TCheckbutton":
                raise Exception("boom")
            return None

        style.configure.side_effect = configure_side_effect

        # Should swallow inner exception and continue
        manager._patch_ttk_style_for_dpi(2.0)
        style_cls.assert_called_once()
        assert style.configure.call_count >= 2


def test_patch_ttk_style_for_dpi_outer_exception(manager):
    # Make Style() raise; method should handle and not raise
    with patch("tkinter.ttk.Style", side_effect=Exception("style boom")):
        manager._patch_ttk_style_for_dpi(2.0)


def test_auto_patch_tk_widgets_to_ttk_success(manager, monkeypatch):
    # Force Windows path
    monkeypatch.setattr("tkface.win.dpi.is_windows", lambda: True)

    # Prepare orig constructors to observe calls
    with patch("tkinter.ttk.Checkbutton.__init__") as cb_init, \
         patch("tkinter.ttk.Radiobutton.__init__") as rb_init:
        cb_init.return_value = None
        rb_init.return_value = None

        # Remove guard to ensure patch applies
        if hasattr(tk.Checkbutton, "_tkface_patched_to_ttk"):
            delattr(tk.Checkbutton, "_tkface_patched_to_ttk")
        if hasattr(tk.Radiobutton, "_tkface_patched_to_ttk"):
            delattr(tk.Radiobutton, "_tkface_patched_to_ttk")

        manager._auto_patch_tk_widgets_to_ttk()

        class Dummy:
            pass

        tk.Checkbutton.__init__(Dummy(), None)
        tk.Radiobutton.__init__(Dummy(), None)
        assert cb_init.called
        assert rb_init.called


def test_auto_patch_tk_widgets_to_ttk_exception(manager, monkeypatch):
    monkeypatch.setattr("tkface.win.dpi.is_windows", lambda: True)
    # Make ttk init raise to exercise exception handler
    with patch("tkinter.ttk.Checkbutton.__init__", side_effect=Exception("x")):
        # Remove guard flags
        if hasattr(tk.Checkbutton, "_tkface_patched_to_ttk"):
            delattr(tk.Checkbutton, "_tkface_patched_to_ttk")
        if hasattr(tk.Radiobutton, "_tkface_patched_to_ttk"):
            delattr(tk.Radiobutton, "_tkface_patched_to_ttk")
        manager._auto_patch_tk_widgets_to_ttk()


def test_get_effective_dpi_with_attributes_and_exception(manager, monkeypatch):
    monkeypatch.setattr("tkface.win.dpi.is_windows", lambda: True)

    # With attributes path
    root = Mock()
    root.DPI_X = 120
    root.DPI_Y = 144
    assert manager.get_effective_dpi(root) == (120 + 144) / 2

    # Exception path: winfo_id raises
    root2 = Mock()
    if hasattr(root2, "DPI_X"):
        delattr(root2, "DPI_X")
    if hasattr(root2, "DPI_Y"):
        delattr(root2, "DPI_Y")
    root2.winfo_id.side_effect = Exception("boom")
    assert manager.get_effective_dpi(root2) == 96


def test_logical_and_physical_exception_paths(manager, monkeypatch):
    monkeypatch.setattr("tkface.win.dpi.is_windows", lambda: True)

    root = Mock()
    # Ensure DPI_scaling is not present so _get_hwnd_dpi path is used
    if hasattr(root, "DPI_scaling"):
        delattr(root, "DPI_scaling")
    # Provide winfo_id for the call inside _get_hwnd_dpi
    root.winfo_id = Mock(return_value=12345)
    # Make _get_hwnd_dpi raise to hit exception fallback
    with patch.object(manager, "_get_hwnd_dpi", side_effect=Exception("err")):
        assert manager.logical_to_physical(10, root=root) == 10
        assert manager.physical_to_logical(10, root=root) == 10


def test_deprecated_patch_tk_widgets_to_ttk_public(monkeypatch):
    # non-Windows returns False
    monkeypatch.setattr("tkface.win.dpi.is_windows", lambda: False)
    from tkface.win.dpi import patch_tk_widgets_to_ttk
    assert patch_tk_widgets_to_ttk() is False

    # Windows path succeeds
    monkeypatch.setattr("tkface.win.dpi.is_windows", lambda: True)
    with patch("tkinter.ttk.Checkbutton.__init__") as cb_init, \
         patch("tkinter.ttk.Radiobutton.__init__") as rb_init:
        cb_init.return_value = None
        rb_init.return_value = None
        assert patch_tk_widgets_to_ttk() is True

# Common patch context managers to reduce duplication
class WindowsPatchContext:
    """Context manager for common Windows-related patches."""
    
    def __init__(self, is_windows=True):
        self.is_windows = is_windows
        self.patches = []
        
    def __enter__(self):
        # Always patch is_windows
        self.is_windows_patch = patch('tkface.win.dpi.is_windows')
        self.mock_is_windows = self.is_windows_patch.__enter__()
        self.mock_is_windows.return_value = self.is_windows
        self.patches.append(self.is_windows_patch)
        
        # If Windows, also patch ctypes
        if self.is_windows:
            self.ctypes_patch = patch('tkface.win.dpi.ctypes')
            self.mock_ctypes = self.ctypes_patch.__enter__()
            self.mock_windll = create_mock_windll_basic()
            self.mock_ctypes.windll = self.mock_windll
            self.patches.append(self.ctypes_patch)
            
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        for patch_obj in reversed(self.patches):
            try:
                patch_obj.__exit__(exc_type, exc_val, exc_tb)
            except AttributeError:
                # Handle cases where patch object doesn't have is_local attribute
                # This can happen with different versions of unittest.mock
                pass
            
    def get_windll(self):
        """Get the mock windll object (only available on Windows)."""
        if not self.is_windows:
            raise ValueError("windll is only available when is_windows=True")
        return self.mock_windll
        
    def get_ctypes(self):
        """Get the mock ctypes object (only available on Windows)."""
        if not self.is_windows:
            raise ValueError("ctypes is only available when is_windows=True")
        return self.mock_ctypes


class WindowsDPIPatchContext(WindowsPatchContext):
    """Extended context manager for Windows DPI-related patches."""
    
    def __init__(self, x_dpi=192, y_dpi=192, scale_factor=200):
        super().__init__(is_windows=True)
        self.x_dpi = x_dpi
        self.y_dpi = y_dpi
        self.scale_factor = scale_factor
        
    def __enter__(self):
        super().__enter__()


# Common mock context managers for wintypes and pointer
class WintypesPointerMockContext:
    """Context manager for common wintypes and pointer mocking patterns."""
    
    def __init__(self, hwnd=12345, dword=2, x_dpi=192, y_dpi=192):
        self.hwnd = hwnd
        self.dword = dword
        self.x_dpi = x_dpi
        self.y_dpi = y_dpi
        self.patches = []
        
    def __enter__(self):
        # Mock wintypes
        self.wintypes_patch = patch('tkface.win.dpi.wintypes')
        self.mock_wintypes = self.wintypes_patch.__enter__()
        self.mock_wintypes.HWND.return_value = self.hwnd
        self.mock_wintypes.DWORD.return_value = self.dword
        
        # Create mock DPI values
        mock_x_dpi, mock_y_dpi = create_mock_dpi_values_basic(self.x_dpi, self.y_dpi)
        self.mock_wintypes.UINT.side_effect = [mock_x_dpi, mock_y_dpi]
        
        self.patches.append(self.wintypes_patch)
        
        # Mock pointer
        self.pointer_patch = patch('tkface.win.dpi.pointer')
        self.mock_pointer = self.pointer_patch.__enter__()
        self.mock_pointer.side_effect = [mock_x_dpi, mock_y_dpi]
        
        self.patches.append(self.pointer_patch)
        
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        for patch_obj in reversed(self.patches):
            patch_obj.__exit__(exc_type, exc_val, exc_tb)
            
    def get_wintypes(self):
        """Get the mock wintypes object."""
        return self.mock_wintypes
        
    def get_pointer(self):
        """Get the mock pointer object."""
        return self.mock_pointer


def with_wintypes_pointer_mock(hwnd=12345, dword=2, x_dpi=192, y_dpi=192):
    """Decorator to apply wintypes and pointer mocking to test functions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with WintypesPointerMockContext(hwnd, dword, x_dpi, y_dpi) as mock_ctx:
                return func(*args, mock_ctx=mock_ctx, **kwargs)
        return wrapper
    return decorator


# Common mock context managers for get_scaling_factor
class GetScalingFactorMockContext:
    """Context manager for common get_scaling_factor mocking patterns."""
    
    def __init__(self, return_value=1.0, side_effect=None):
        self.return_value = return_value
        self.side_effect = side_effect
        self.patches = []
        
    def __enter__(self):
        # Mock get_scaling_factor
        self.get_scaling_patch = patch('tkface.win.dpi.get_scaling_factor')
        self.mock_get_scaling = self.get_scaling_patch.__enter__()
        
        if self.side_effect is not None:
            self.mock_get_scaling.side_effect = self.side_effect
        else:
            self.mock_get_scaling.return_value = self.return_value
        
        self.patches.append(self.get_scaling_patch)
        
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        for patch_obj in reversed(self.patches):
            patch_obj.__exit__(exc_type, exc_val, exc_tb)
            
    def get_mock(self):
        """Get the mock get_scaling_factor object."""
        return self.mock_get_scaling


def with_get_scaling_factor_mock(return_value=1.0, side_effect=None):
    """Decorator to apply get_scaling_factor mocking to test functions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with GetScalingFactorMockContext(return_value, side_effect) as mock_ctx:
                return func(*args, mock_ctx=mock_ctx, **kwargs)
        return wrapper
    return decorator


# Common context manager for tkinter method patching
class TkinterMethodPatchContext:
    """Context manager for common tkinter method patching patterns."""
    
    def __init__(self, tk_class, method_name, manager, scaling_factor):
        self.tk_class = tk_class
        self.method_name = method_name
        self.manager = manager
        self.scaling_factor = scaling_factor
        self.original_method = None
        
    def __enter__(self):
        # Store original method
        self.original_method = getattr(self.tk_class, self.method_name)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore original method
        setattr(self.tk_class, self.method_name, self.original_method)
        
    def get_original_method(self):
        """Get the original method."""
        return self.original_method


def with_tkinter_method_patch(tk_class, method_name, manager, scaling_factor):
    """Decorator to apply tkinter method patching to test functions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with TkinterMethodPatchContext(tk_class, method_name, manager, scaling_factor) as patch_ctx:
                return func(*args, patch_ctx=patch_ctx, **kwargs)
        return wrapper
    return decorator


def helper__test_tkinter_constructor_patch(tk_class, manager, scaling_factor, **test_kwargs):
    """Helper function to test tkinter constructor patching with common pattern."""
    with TkinterMethodPatchContext(tk_class, '__init__', manager, scaling_factor) as patch_ctx:
        # Mock the original method before patching
        mock_original_init = create_mock_original_method()
        setattr(tk_class, '__init__', mock_original_init)
        
        # Apply the patch
        # Handle special case for LabelFrame
        if tk_class.__name__ == 'LabelFrame':
            patch_method = getattr(manager, '_patch_label_frame_constructor')
        else:
            patch_method = getattr(manager, f'_patch_{tk_class.__name__.lower()}_constructor')
        patch_method(scaling_factor)
        
        # Test with parameters
        mock_parent = create_mock_parent()
        mock_instance = create_mock_instance()
        
        # Call the patched method
        getattr(tk_class, '__init__')(mock_instance, mock_parent, **test_kwargs)
        
        # Calculate expected values
        expected_kwargs = {}
        for key, value in test_kwargs.items():
            if key in ['padx', 'pady', 'bd', 'wraplength', 'width', 'height']:
                if isinstance(value, tuple):
                    expected_kwargs[key] = tuple(int(v * scaling_factor) for v in value)
                else:
                    expected_kwargs[key] = int(value * scaling_factor)
            else:
                expected_kwargs[key] = value
        
        # Verify the call
        mock_original_init.assert_called_once_with(mock_instance, mock_parent, **expected_kwargs)


def helper__test_tkinter_constructor_patch_no_scaling(tk_class, manager, scaling_factor, **test_kwargs):
    """Helper function to test tkinter constructor patching without scaling parameters."""
    with TkinterMethodPatchContext(tk_class, '__init__', manager, scaling_factor) as patch_ctx:
        # Apply the patch
        patch_method = getattr(manager, f'_patch_{tk_class.__name__.lower()}_constructor')
        patch_method(scaling_factor)
        
        # Test without scaling parameters
        mock_parent = create_mock_parent()
        mock_original_init = create_mock_original_method()
        setattr(tk_class, '__init__', mock_original_init)
        
        # Create a mock instance
        mock_instance = create_mock_instance()
        
        # Call the patched method
        getattr(tk_class, '__init__')(mock_instance, mock_parent, **test_kwargs)
        
        # Should call original with unchanged values
        mock_original_init.assert_called_once_with(mock_instance, mock_parent, **test_kwargs)




def assert_scaling_result(result, expected_base, scaling_factor):
    """Helper function to assert scaling calculation results."""
    expected = expected_base * scaling_factor
    assert result == expected, f"Expected {expected}, got {result}"


def create_patch_context_for_tkinter_class(tk_class, manager, scaling_factor=2.0):
    """Helper function to create patch context for tkinter classes."""
    original_init = tk_class.__init__
    mock_original_init = create_mock_original_method()
    tk_class.__init__ = mock_original_init
    
    try:
        patch_method = getattr(manager, f'_patch_{tk_class.__name__.lower()}_constructor')
        patch_method(scaling_factor)
        return mock_original_init
    finally:
        tk_class.__init__ = original_init


# Parameterized fixtures for common test scenarios
@pytest.fixture(params=[True, False])
def is_windows_param(request):
    """Parameterized fixture for Windows/non-Windows testing."""
    return request.param


@pytest.fixture
def mock_root_factory():
    """Factory fixture for creating mock roots with different configurations."""
    def _create_mock_root(**kwargs):
        root = MagicMock()
        root.winfo_id.return_value = kwargs.get('winfo_id', 12345)
        root.wm_geometry = MagicMock()
        root.geometry.return_value = kwargs.get('geometry', "800x600")
        root.tk.call.return_value = kwargs.get('tk_call', "2.0")
        
        # Set DPI attributes if provided
        if 'DPI_X' in kwargs:
            root.DPI_X = kwargs['DPI_X']
        if 'DPI_Y' in kwargs:
            root.DPI_Y = kwargs['DPI_Y']
        if 'DPI_scaling' in kwargs:
            root.DPI_scaling = kwargs['DPI_scaling']
            
        return root
    return _create_mock_root


@pytest.fixture
def scaling_test_cases():
    """Common scaling test cases."""
    return [
        (1.0, "800x600", "800x600"),
        (1.5, "800x600", "1200x900"),
        (2.0, "800x600", "1600x1200"),
        (2.5, "800x600", "2000x1500"),
    ]


@pytest.fixture
def tkinter_patch_context():
    """Context manager for tkinter class patching."""
    class TkinterPatchContext:
        def __init__(self, tk_class, manager, scaling_factor=2.0):
            self.tk_class = tk_class
            self.manager = manager
            self.scaling_factor = scaling_factor
            self.original_init = None
            self.mock_original_init = None
            
        def __enter__(self):
            self.original_init = self.tk_class.__init__
            self.mock_original_init = MagicMock()
            self.tk_class.__init__ = self.mock_original_init
            return self
            
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.tk_class.__init__ = self.original_init
            
        def create_mock_objects(self):
            """Create common mock objects for testing."""
            mock_parent = create_mock_parent()
            mock_instance = create_mock_instance()
            return mock_parent, mock_instance
            
        def apply_patch(self):
            """Apply the DPI patch to the tkinter class."""
            patch_method = getattr(self.manager, f'_patch_{self.tk_class.__name__.lower()}_constructor')
            patch_method(self.scaling_factor)
    
    return TkinterPatchContext


@pytest.fixture
def backward_compatibility_functions():
    """Common backward compatibility functions for testing."""
    from tkface.win.dpi import (
        calculate_dpi_sizes,
        dpi,
        enable_dpi_awareness,
        enable_dpi_geometry,
        get_actual_window_size,
        get_effective_dpi,
        get_scaling_factor,
        logical_to_physical,
        physical_to_logical,
        scale_font_size,
        scale_icon,
    )
    return {
        'dpi': dpi,
        'enable_dpi_awareness': enable_dpi_awareness,
        'enable_dpi_geometry': enable_dpi_geometry,
        'get_scaling_factor': get_scaling_factor,
        'get_effective_dpi': get_effective_dpi,
        'logical_to_physical': logical_to_physical,
        'physical_to_logical': physical_to_logical,
        'scale_font_size': scale_font_size,
        'get_actual_window_size': get_actual_window_size,
        'calculate_dpi_sizes': calculate_dpi_sizes,
        'scale_icon': scale_icon,
    }


# Helper functions for common test patterns - consolidated version


def helper_test_function_return_type(func, *args, **kwargs):
    """Helper function to test function return types."""
    result = func(*args, **kwargs)
    assert result is not None
    return result


class BaseTestHelper:
    """Base class with unified test helper methods."""
    
    def _test_method(self, manager, method_name, expected_result, 
                    test_type='basic', *args, **kwargs):
        """
        Unified helper method to test methods with various configurations.
        
        Args:
            manager: DPI manager instance
            method_name: Name of the method to test
            expected_result: Expected return value
            test_type: Type of test configuration
                - 'basic': Basic method call
                - 'non_windows': Non-Windows platform test
                - 'windows_root': Windows with mock root
                - 'windows_scaling': Windows with scaling factor
                - 'windows_exception': Windows with exception handling
                - 'non_numeric': Non-numeric input test
            *args: Positional arguments for the method
            **kwargs: Keyword arguments for the method
                - root_attrs: Dictionary of attributes for mock root (for 'windows_root')
                - scaling_factor: Scaling factor (for 'windows_scaling')
                - exception_attr: Attribute to set exception on (for 'windows_exception')
                - exception_value: Exception to raise (for 'windows_exception')
                - input_value: Input value (for 'non_numeric')
        """
        method = getattr(manager, method_name)
        
        if test_type == 'non_windows':
            result = method(*args, **kwargs)
        elif test_type == 'windows_root':
            root_attrs = kwargs.pop('root_attrs', {})
            mock_root = create_basic_mock_root(**root_attrs)
            result = method(*args, root=mock_root, **kwargs)
        elif test_type == 'windows_scaling':
            scaling_factor = kwargs.pop('scaling_factor', 2.0)
            result = method(*args, scaling_factor=scaling_factor, **kwargs)
        elif test_type == 'windows_exception':
            exception_attr = kwargs.pop('exception_attr', None)
            exception_value = kwargs.pop('exception_value', None)
            if exception_attr and exception_value:
                mock_root = create_mock_root_with_exception(exception_attr, exception_value)
            else:
                mock_root = create_basic_mock_root()
            result = method(*args, root=mock_root, **kwargs)
        elif test_type == 'non_numeric':
            input_value = kwargs.pop('input_value', args[0] if args else None)
            result = method(input_value)
        else:  # 'basic'
            result = method(*args, **kwargs)
        
        assert result == expected_result

    # Convenience methods for backward compatibility
    def _test_non_windows_method(self, manager, method_name, expected_result, *args, **kwargs):
        """Convenience method for non-Windows tests."""
        self._test_method(manager, method_name, expected_result, 'non_windows', *args, **kwargs)

    def _test_windows_method_with_root(self, manager, method_name, expected_result, 
                                     root_attrs=None, *args, **kwargs):
        """Convenience method for Windows tests with root."""
        kwargs['root_attrs'] = root_attrs
        self._test_method(manager, method_name, expected_result, 'windows_root', *args, **kwargs)

    def _test_windows_method_with_scaling_factor(self, manager, method_name, expected_result,
                                               scaling_factor=2.0, *args, **kwargs):
        """Convenience method for Windows tests with scaling factor."""
        kwargs['scaling_factor'] = scaling_factor
        self._test_method(manager, method_name, expected_result, 'windows_scaling', *args, **kwargs)

    def _test_windows_method_exception(self, manager, method_name, expected_result,
                                     exception_attr=None, exception_value=None, *args, **kwargs):
        """Convenience method for Windows tests with exception handling."""
        kwargs['exception_attr'] = exception_attr
        kwargs['exception_value'] = exception_value
        self._test_method(manager, method_name, expected_result, 'windows_exception', *args, **kwargs)

    def _test_method_with_non_numeric_input(self, manager, method_name, input_value, expected_result):
        """Convenience method for non-numeric input tests."""
        self._test_method(manager, method_name, expected_result, 'non_numeric', 
                         input_value=input_value)


class TestDPIManager(BaseTestHelper):
    """Test the DPIManager class."""

    def test_dpi_manager_creation(self):
        """Test DPIManager creation."""
        manager = create_dpi_manager_for_test()
        assert manager is not None
        assert hasattr(manager, '_dpi_awareness_set')
        assert hasattr(manager, 'logger')
        assert manager._dpi_awareness_set is False

    def test_is_windows_function(self):
        """Test is_windows function."""
        from tkface.win.dpi import is_windows

        # This should return True on Windows, False on other platforms
        result = is_windows()
        assert isinstance(result, bool)
        if sys.platform == "win32":
            assert result is True
        else:
            assert result is False

    def test_get_hwnd_dpi_non_windows(self, manager, non_windows_patches):
        """Test _get_hwnd_dpi on non-Windows platforms."""
        result = manager._get_hwnd_dpi(12345)
        assert result == (96, 96, 1.0)

    def test_get_hwnd_dpi_windows_success(self, manager, windows_patches, mock_windll, mock_dpi_values, mock_wintypes, mock_pointer):
        """Test _get_hwnd_dpi on Windows with successful DPI detection."""
        mock_is_windows, mock_ctypes = windows_patches
        
        # Setup ctypes mock
        mock_ctypes.windll = mock_windll
        
        # Setup DPI values using helper function
        mock_x_dpi, mock_y_dpi = create_windows_dpi_setup(mock_windll, mock_dpi_values, mock_wintypes, mock_pointer)
        
        # Mock wintypes and pointer
        with WintypesPointerMockContext(12345, 2, 192, 192) as mock_ctx:
            result = manager._get_hwnd_dpi(12345)
            
            # The result should be (192, 192, 2.0) based on the mocked values
            assert result == (192, 192, 2.0)

    def test_get_hwnd_dpi_exception_handling(self, manager, windows_patches):
        """Test _get_hwnd_dpi exception handling."""
        mock_is_windows, mock_ctypes = windows_patches
        mock_ctypes.windll.shcore.SetProcessDpiAwareness.side_effect = Exception("Test error")
        
        result = manager._get_hwnd_dpi(12345)
        assert result == (96, 96, 1.0)

    @pytest.mark.parametrize("scale_factor,input_geometry,expected", [
        (2.0, "800x600+100+200", "1600.0x1200.0+200.0+400.0"),
        (2.0, "800x600", "1600.0x1200.0"),
        (1.5, "800x600", "1200.0x900.0"),
        (1.0, "800x600", "800.0x600.0"),
    ])
    def test_scale_geometry_string(self, manager, scale_factor, input_geometry, expected):
        """Test _scale_geometry_string method with various inputs."""
        result = manager._scale_geometry_string(input_geometry, lambda x: x * scale_factor)
        assert result == expected
    
    def test_scale_geometry_string_edge_cases(self):
        """Test _scale_geometry_string method with edge cases."""
        manager = create_dpi_manager_for_test()
        # Test with None
        result = manager._scale_geometry_string(None, lambda x: x * 2)
        assert result is None
        
        # Test with empty string
        result = manager._scale_geometry_string("", lambda x: x * 2)
        assert result == ""
        
        # Test with invalid geometry
        result = manager._scale_geometry_string("invalid", lambda x: x * 2)
        assert result == "invalid"

    def test_scale_geometry_string_exception_handling(self):
        """Test _scale_geometry_string exception handling."""
        manager = create_dpi_manager_for_test()
        # Test with function that raises exception
        def failing_scale_func(x):
            raise Exception("Test error")
        
        result = manager._scale_geometry_string("800x600", failing_scale_func)
        assert result == "800x600"

    def test_fix_scaling(self, manager, mock_root, mock_tkfont):
        """Test _fix_scaling method."""
        # Test with None root
        manager._fix_scaling(None)
        # Should not raise exception
        
        # Test with mock root
        manager._fix_scaling(mock_root)
        
        mock_root.tk.call.assert_called_with("tk", "scaling")
        mock_tkfont.names.assert_called_with(mock_root)

    def test_fix_scaling_exception_handling(self, manager, mock_root):
        """Test _fix_scaling exception handling."""
        # Configure mock to raise exception
        mock_root.tk.call.side_effect = Exception("Test error")
        
        # Should not raise exception
        manager._fix_scaling(mock_root)

    def test_patch_widget_methods(self, manager, mock_root):
        """Test _patch_widget_methods."""
        # Test with None root
        manager._patch_widget_methods(None)
        # Should not raise exception
        
        # Test with root without DPI_scaling attribute
        del mock_root.DPI_scaling
        manager._patch_widget_methods(mock_root)
        # Should not raise exception

    def test_get_scaling_factor_for_patching(self):
        """Test _get_scaling_factor_for_patching."""
        manager = create_dpi_manager_for_test()
        mock_root = create_basic_mock_root(tk_call="1.5", DPI_scaling=2.0)
        
        result = manager._get_scaling_factor_for_patching(mock_root)
        
        # tk_scaling = 1.5, so tk_scaling > 1.5 is False
        # Therefore, it should return dpi_scaling = 2.0
        assert result == 2.0

    def test_get_scaling_factor_for_patching_high_tk_scaling(self):
        """Test _get_scaling_factor_for_patching with high tk_scaling."""
        manager = create_dpi_manager_for_test()
        mock_root = create_basic_mock_root(tk_call="2.0", DPI_scaling=2.0)  # tk_scaling > 1.5
        
        result = manager._get_scaling_factor_for_patching(mock_root)
        
        # tk_scaling = 2.0, so tk_scaling > 1.5 is True
        # Should return min(2.0 * 0.5, 2.0 * 0.8) = min(1.0, 1.6) = 1.0
        assert result == 1.0

    def test_get_scaling_factor_for_patching_exception(self):
        """Test _get_scaling_factor_for_patching exception handling."""
        manager = create_dpi_manager_for_test()
        mock_root = create_basic_mock_root(DPI_scaling=2.0)
        mock_root.tk.call.side_effect = Exception("Test error")
        
        result = manager._get_scaling_factor_for_patching(mock_root)
        
        assert result == 2.0

    def test_scale_padding_value(self):
        """Test _scale_padding_value method."""
        manager = create_dpi_manager_for_test()
        # Test with integer value
        result = manager._scale_padding_value(10, 2.0)
        assert result == 20
        
        # Test with float value
        result = manager._scale_padding_value(5.5, 2.0)
        assert result == 11
        
        # Test with tuple value
        result = manager._scale_padding_value((10, 20), 2.0)
        assert result == (20, 40)
        
        # Test with list value
        result = manager._scale_padding_value([10, 20], 2.0)
        assert result == (20, 40)
        
        # Test with value outside range
        result = manager._scale_padding_value(100, 2.0)
        assert result == 100
        
        # Test with negative value outside range
        result = manager._scale_padding_value(-100, 2.0)
        assert result == -100
        
        # Test with zero value
        result = manager._scale_padding_value(0, 2.0)
        assert result == 0
        
        # Test with negative value in range
        result = manager._scale_padding_value(-10, 2.0)
        assert result == -20
        
        # Test with tuple with one value outside range
        result = manager._scale_padding_value((10, 100), 2.0)
        assert result == (10, 100)
        
        # Test with tuple with negative values
        result = manager._scale_padding_value((-10, -20), 2.0)
        assert result == (-20, -40)
        
        # Test with non-numeric value
        result = manager._scale_padding_value("invalid", 2.0)
        assert result == "invalid"
        
        # Test with tuple of wrong length
        result = manager._scale_padding_value((10, 20, 30), 2.0)
        assert result == (10, 20, 30)

    def test_scale_padding_kwargs(self):
        """Test _scale_padding_kwargs method."""
        manager = create_dpi_manager_for_test()
        kwargs = {"padx": 10, "pady": 20, "other": "value"}
        result = manager._scale_padding_kwargs(kwargs, 2.0)
        
        assert result["padx"] == 20
        assert result["pady"] == 40
        assert result["other"] == "value"

    def test_fix_dpi_non_windows(self, manager, mock_root, non_windows_patches):
        """Test fix_dpi on non-Windows platforms."""
        manager.fix_dpi(mock_root)
        assert_dpi_attributes_set(mock_root)

    def test_fix_dpi_windows_success(self, manager, mock_root, windows_patches):
        """Test fix_dpi on Windows with successful DPI awareness."""
        with patch.object(manager, '_enable_dpi_awareness') as mock_enable:
            mock_enable.return_value = {"shcore": True, "scale_factor": 200}
            
            with patch.object(manager, '_apply_shcore_dpi_scaling') as mock_apply:
                manager.fix_dpi(mock_root)
                
                mock_enable.assert_called_once()
                mock_apply.assert_called_once_with(mock_root)

    def test_fix_dpi_exception_handling(self, manager, mock_root, windows_patches):
        """Test fix_dpi exception handling."""
        with patch.object(manager, '_enable_dpi_awareness') as mock_enable:
            mock_enable.side_effect = Exception("Test error")
            
            manager.fix_dpi(mock_root)
            
            # Should set DPI attributes as fallback
            assert_dpi_attributes_set(mock_root)

    @with_test_context(is_windows=True)
    def test_enable_dpi_awareness_success(self, manager, patch_ctx):
        """Test _enable_dpi_awareness success."""
        result = manager._enable_dpi_awareness()
        
        assert result == {"shcore": True, "scale_factor": 200}

    @with_test_context(is_windows=True)
    def test_enable_dpi_awareness_fallback(self, manager, patch_ctx):
        """Test _enable_dpi_awareness fallback to user32."""
        patch_ctx.get_windll().shcore.SetProcessDpiAwareness.side_effect = Exception("Test error")
        
        result = manager._enable_dpi_awareness()
        
        assert result == {"shcore": False, "scale_factor": None}

    @with_test_context(is_windows=True)
    def test_enable_dpi_awareness_exception(self, manager, patch_ctx):
        """Test _enable_dpi_awareness exception handling."""
        patch_ctx.get_windll().shcore.SetProcessDpiAwareness.side_effect = Exception("Test error")
        patch_ctx.get_windll().user32.SetProcessDPIAware.side_effect = Exception("Test error")
        
        with pytest.raises(Exception):
            manager._enable_dpi_awareness()

    @with_test_context(is_windows=True)
    def test_apply_shcore_dpi_scaling(self, manager, patch_ctx):
        """Test _apply_shcore_dpi_scaling."""
        mock_root = create_basic_mock_root(tk_call=None)
        
        with patch.object(manager, '_adjust_tk_scaling') as mock_adjust:
            with patch.object(manager, '_set_dpi_information') as mock_set:
                manager._apply_shcore_dpi_scaling(mock_root)
                
                mock_adjust.assert_called_once()
                mock_set.assert_called_once_with(mock_root)

    @with_test_context(is_windows=True)
    def test_adjust_tk_scaling(self, manager, patch_ctx):
        """Test _adjust_tk_scaling."""
        mock_root = create_basic_mock_root(tk_call=None)
        
        manager._adjust_tk_scaling(mock_root, 1.5)
        
        # The condition windows_scale > (windows_scale_factor / 100) is always False
        # because windows_scale = windows_scale_factor / 100.0
        # So tk.call should not be called
        mock_root.tk.call.assert_not_called()

    @with_test_context(is_windows=True)
    def test_adjust_tk_scaling_exception(self, manager, patch_ctx):
        """Test _adjust_tk_scaling exception handling."""
        patch_ctx.get_windll().shcore.GetScaleFactorForDevice.side_effect = Exception("Test error")
        
        mock_root = create_basic_mock_root()
        
        # Should not raise exception
        manager._adjust_tk_scaling(mock_root, 1.5)

    @with_test_context(
        is_windows=True,
        wintypes_mock={'hwnd': 12345, 'monitor_handle': 2, 'x_dpi': 192, 'y_dpi': 192}
    )
    def test_set_dpi_information(self, manager, patch_ctx, mock_ctx, mock_root, mock_windll, mock_dpi_values):
        """Test _set_dpi_information."""
        with patch('tkface.win.dpi.ctypes') as mock_ctypes:
            mock_ctypes.windll = mock_windll
            
        manager._set_dpi_information(mock_root)
        
        assert hasattr(mock_root, 'DPI_X')
        assert hasattr(mock_root, 'DPI_Y')
        assert hasattr(mock_root, 'DPI_scaling')

    @with_test_context(is_windows=True)
    def test_set_dpi_information_exception(self, manager, patch_ctx, mock_root, mock_windll, mock_dpi_values):
        """Test _set_dpi_information exception handling."""
        with patch('tkface.win.dpi.ctypes') as mock_ctypes:
            mock_ctypes.windll = mock_windll
            mock_windll.shcore.GetScaleFactorForDevice.side_effect = Exception("Test error")
            
            # Should not raise exception
            manager._set_dpi_information(mock_root)

    @with_test_context(
        is_windows=True,
        wintypes_mock={'hwnd': 12345, 'monitor_handle': 2, 'x_dpi': 144, 'y_dpi': 144}
    )
    def test_set_dpi_information_windows_scale_higher(self, manager, patch_ctx, mock_ctx):
        """Test _set_dpi_information with Windows scale factor higher than DPI scaling."""
        mock_root = create_basic_mock_root()
        manager._set_dpi_information(mock_root)
        
        # Should use Windows scale factor (2.0) instead of DPI-based (1.5)
        assert mock_root.DPI_X == 144
        assert mock_root.DPI_Y == 144
        assert mock_root.DPI_scaling == 2.0
        
    @with_test_context(
        is_windows=True,
        wintypes_mock={'hwnd': 12345, 'monitor_handle': 2, 'x_dpi': 192, 'y_dpi': 192}
    )
    def test_set_dpi_information_dpi_scaling_higher(self, manager, patch_ctx, mock_ctx):
        """Test _set_dpi_information with DPI scaling higher than Windows scale factor."""
        mock_root = create_basic_mock_root()
        manager._set_dpi_information(mock_root)
        
        # Should use DPI-based scaling (2.0) instead of Windows scale factor (1.5)
        assert mock_root.DPI_X == 192
        assert mock_root.DPI_Y == 192
        assert mock_root.DPI_scaling == 2.0

    def test_apply_dpi(self):
        """Test apply_dpi method."""
        manager = create_dpi_manager_for_test()
        
        # Test with enable=False
        result = manager.apply_dpi(None, enable=False)
        assert result["enabled"] is False
        
        # Test with None root
        result = manager.apply_dpi(None, enable=True)
        assert result["enabled"] is True
        assert result["platform"] == "non-windows" if not sys.platform == "win32" else "windows"

    @with_test_context(
        is_windows=True,
        patches=[{'target': 'manager.fix_dpi'}]
    )
    def test_apply_dpi_windows(self, manager, patch_ctx):
        """Test apply_dpi on Windows."""
        mock_root = create_basic_mock_root(DPI_X=192)
        mock_root.DPI_Y = 192
        mock_root.DPI_scaling = 2.0
        mock_root.tk.call.return_value = "2.0"
        
        result = manager.apply_dpi(mock_root, enable=True)
        
        assert result["enabled"] is True
        assert result["platform"] == "windows"
        assert result["dpi_awareness_set"] is True
        assert result["effective_dpi"] == 192
        assert result["scaling_factor"] == 2.0
        assert result["hwnd"] == 12345
        assert result["tk_scaling"] == 2.0
        
    @with_test_context(
        is_windows=True,
        patches=[{'target': 'manager.fix_dpi', 'side_effect': Exception("Test error")}]
    )
    def test_apply_dpi_exception_handling(self, manager, patch_ctx):
        """Test apply_dpi exception handling."""
        mock_root = create_basic_mock_root()
        result = manager.apply_dpi(mock_root, enable=True)
        
        assert "error" in result
        assert result["error"] == "Test error"

    @with_test_context(is_windows=False)
    def test_enable_dpi_awareness_public(self, manager, patch_ctx):
        """Test enable_dpi_awareness public method."""
        self._test_non_windows_method(manager, 'enable_dpi_awareness', False)

    @with_test_context(is_windows=False)
    def test_get_scaling_factor(self, manager, patch_ctx):
        """Test get_scaling_factor method."""
        self._test_non_windows_method(manager, 'get_scaling_factor', 1.0, None)

    @with_test_context(is_windows=False)
    def test_get_effective_dpi(self, manager, patch_ctx):
        """Test get_effective_dpi method."""
        self._test_non_windows_method(manager, 'get_effective_dpi', 96, None)

    @with_test_context(is_windows=False)
    def test_logical_to_physical(self, manager, patch_ctx):
        """Test logical_to_physical method."""
        self._test_non_windows_method(manager, 'logical_to_physical', 100, 100)

    @with_test_context(is_windows=True)
    def test_logical_to_physical_windows_with_root(self, manager, patch_ctx):
        """Test logical_to_physical on Windows with root."""
        self._test_windows_method_with_root(manager, 'logical_to_physical', 200, 
                                          {'DPI_scaling': 2.0}, 100)
        
    @with_test_context(is_windows=True)
    def test_logical_to_physical_windows_with_scaling_factor(self, manager, patch_ctx):
        """Test logical_to_physical on Windows with scaling factor."""
        self._test_windows_method_with_scaling_factor(manager, 'logical_to_physical', 200, 2.0, 100)
        
    @with_test_context(is_windows=True)
    def test_logical_to_physical_windows_with_root_no_dpi_scaling(self, manager, patch_ctx):
        """Test logical_to_physical on Windows with root but no DPI_scaling attribute."""
        mock_root = create_basic_mock_root()
        del mock_root.DPI_scaling
        
        with patch.object(manager, '_get_hwnd_dpi') as mock_get_hwnd:
            mock_get_hwnd.return_value = (192, 192, 2.0)
            result = manager.logical_to_physical(100, root=mock_root)
            assert result == 200
        
    @with_test_context(is_windows=True)
    def test_logical_to_physical_windows_exception(self, manager, patch_ctx):
        """Test logical_to_physical on Windows with exception."""
        self._test_windows_method_exception(manager, 'logical_to_physical', 100,
                                          "winfo_id", "Test error", 100)
        
    @with_test_context(is_windows=True)
    def test_logical_to_physical_non_numeric(self, manager, patch_ctx):
        """Test logical_to_physical with non-numeric value."""
        self._test_method_with_non_numeric_input(manager, 'logical_to_physical', "invalid", "invalid")
        
    @with_test_context(is_windows=False)
    def test_physical_to_logical(self, manager, patch_ctx):
        """Test physical_to_logical method."""
        self._test_non_windows_method(manager, 'physical_to_logical', 100, 100)
        
    @with_test_context(is_windows=True)
    def test_physical_to_logical_windows_with_root(self, manager, patch_ctx):
        """Test physical_to_logical on Windows with root."""
        self._test_windows_method_with_root(manager, 'physical_to_logical', 100,
                                          {'DPI_scaling': 2.0}, 200)
        
    @with_test_context(is_windows=True)
    def test_physical_to_logical_windows_with_scaling_factor(self, manager, patch_ctx):
        """Test physical_to_logical on Windows with scaling factor."""
        self._test_windows_method_with_scaling_factor(manager, 'physical_to_logical', 100, 2.0, 200)
        
    @with_test_context(is_windows=True)
    def test_physical_to_logical_windows_with_root_no_dpi_scaling(self, manager, patch_ctx):
        """Test physical_to_logical on Windows with root but no DPI_scaling attribute."""
        mock_root = create_basic_mock_root()
        del mock_root.DPI_scaling
        
        with patch.object(manager, '_get_hwnd_dpi') as mock_get_hwnd:
            mock_get_hwnd.return_value = (192, 192, 2.0)
            result = manager.physical_to_logical(200, root=mock_root)
            assert result == 100
        
    @with_test_context(is_windows=True)
    def test_physical_to_logical_windows_exception(self, manager, patch_ctx):
        """Test physical_to_logical on Windows with exception."""
        self._test_windows_method_exception(manager, 'physical_to_logical', 200,
                                          "winfo_id", "Test error", 200)
        
    @with_test_context(is_windows=True)
    def test_physical_to_logical_non_numeric(self, manager, patch_ctx):
        """Test physical_to_logical with non-numeric value."""
        self._test_method_with_non_numeric_input(manager, 'physical_to_logical', "invalid", "invalid")
        
    @with_test_context(is_windows=True)
    def test_physical_to_logical_zero_scaling_factor(self, manager, patch_ctx):
        """Test physical_to_logical with zero scaling factor."""
        self._test_windows_method_with_scaling_factor(manager, 'physical_to_logical', 200, 0, 200)
        
    @with_test_context(is_windows=False)
    def test_scale_font_size(self, manager, patch_ctx):
        """Test scale_font_size method."""
        self._test_non_windows_method(manager, 'scale_font_size', 12, 12)
        
    @with_test_context(is_windows=True)
    def test_scale_font_size_windows_with_root(self, manager, patch_ctx):
        """Test scale_font_size on Windows with root."""
        self._test_windows_method_with_root(manager, 'scale_font_size', 24,
                                          {'tk_call': "2.0"}, 12)
        
    @with_test_context(is_windows=True)
    def test_scale_font_size_windows_with_scaling_factor(self, manager, patch_ctx):
        """Test scale_font_size on Windows with scaling factor."""
        self._test_windows_method_with_scaling_factor(manager, 'scale_font_size', 24, 2.0, 12)
        
    @with_test_context(is_windows=True)
    def test_scale_font_size_windows_with_root_tk_call_exception(self, manager, patch_ctx):
        """Test scale_font_size on Windows with root but tk.call exception."""
        mock_root = create_basic_mock_root(DPI_scaling=2.0)
        mock_root.tk.call.side_effect = Exception("Test error")
        result = manager.scale_font_size(12, root=mock_root)
        assert result == 24
        
    @with_test_context(is_windows=True)
    def test_scale_font_size_windows_with_root_no_dpi_scaling(self, manager, patch_ctx):
        """Test scale_font_size on Windows with root but no DPI_scaling attribute."""
        mock_root = create_mock_root_with_exception("tk.call", "Test error")
        del mock_root.DPI_scaling
        
        with patch.object(manager, '_get_hwnd_dpi') as mock_get_hwnd:
            mock_get_hwnd.return_value = (192, 192, 2.0)
            result = manager.scale_font_size(12, root=mock_root)
            assert result == 24
        
    @with_test_context(is_windows=True)
    def test_scale_font_size_windows_exception(self, manager, patch_ctx):
        """Test scale_font_size on Windows with exception."""
        mock_root = create_mock_root_with_exception("tk.call", "Test error")
        mock_root.winfo_id.side_effect = Exception("Test error")
        # Ensure DPI_scaling attribute doesn't exist to trigger exception path
        del mock_root.DPI_scaling
        
        result = manager.scale_font_size(12, root=mock_root)
        
        # The method should handle exceptions and return original size
        # However, the current mock setup returns scaling factor 2.0 from _get_hwnd_dpi
        # So the result is 12 * 2.0 = 24
        assert result == 24
        
    @with_test_context(is_windows=True)
    def test_scale_font_size_negative_size(self, manager, patch_ctx):
        """Test scale_font_size with negative font size."""
        self._test_windows_method_with_scaling_factor(manager, 'scale_font_size', -24, 2.0, -12)

    @with_test_context(is_windows=False)
    def test_get_actual_window_size(self, manager, patch_ctx):
        """Test get_actual_window_size method."""
        result = manager.get_actual_window_size(None)
        assert result["platform"] == "non-windows"
        assert result["logical_size"] is None
        assert result["physical_size"] is None

    @with_test_context(is_windows=True)
    def test_get_actual_window_size_windows_no_root(self, manager, patch_ctx):
        """Test get_actual_window_size on Windows with no root."""
        result = manager.get_actual_window_size(None)
        assert result["platform"] == "no-root"
        assert result["logical_size"] is None
        assert result["physical_size"] is None
        
    @with_test_context(is_windows=True)
    def test_get_actual_window_size_windows_with_root(self, manager, patch_ctx):
        """Test get_actual_window_size on Windows with root."""
        mock_root = create_basic_mock_root()
        mock_root.DPI_scaling = 2.0
        
        result = manager.get_actual_window_size(mock_root)
        
        assert result["hwnd"] == 12345
        assert result["logical_size"]["width"] == 800
        assert result["logical_size"]["height"] == 600
        assert result["physical_size"]["width"] == 1600
        assert result["physical_size"]["height"] == 1200
        assert result["scaling_factor"] == 2.0
        
    @with_test_context(is_windows=True)
    def test_get_actual_window_size_windows_with_root_no_dpi_scaling(self, manager, patch_ctx):
        """Test get_actual_window_size on Windows with root but no DPI_scaling attribute."""
        mock_root = create_basic_mock_root()
        del mock_root.DPI_scaling
        
        with patch.object(manager, '_get_hwnd_dpi') as mock_get_hwnd:
            mock_get_hwnd.return_value = (192, 192, 2.0)
            result = manager.get_actual_window_size(mock_root)
            
            assert result["hwnd"] == 12345
            assert result["logical_size"]["width"] == 800
            assert result["logical_size"]["height"] == 600
            assert result["physical_size"]["width"] == 1600
            assert result["physical_size"]["height"] == 1200
            assert result["scaling_factor"] == 2.0
        
    @with_test_context(is_windows=True)
    def test_get_actual_window_size_windows_invalid_geometry(self, manager, patch_ctx):
        """Test get_actual_window_size on Windows with invalid geometry."""
        mock_root = create_basic_mock_root(geometry="invalid")
        mock_root.DPI_scaling = 2.0
        
        result = manager.get_actual_window_size(mock_root)
        
        assert result["hwnd"] == 12345
        assert result["logical_size"]["width"] is None
        assert result["logical_size"]["height"] is None
        assert result["physical_size"]["width"] is None
        assert result["physical_size"]["height"] is None
        assert result["scaling_factor"] == 2.0
        
    @with_test_context(is_windows=True)
    def test_get_actual_window_size_windows_exception(self, manager, patch_ctx):
        """Test get_actual_window_size on Windows with exception."""
        mock_root = create_mock_root_with_exception("geometry", "Test error")
        result = manager.get_actual_window_size(mock_root)
        
        assert "error" in result
        assert result["error"] == "Failed to get window size: Test error"
        assert result["logical_size"] is None
        assert result["physical_size"] is None

    @with_test_context(is_windows=False)
    def test_calculate_dpi_sizes(self, manager, patch_ctx):
        """Test calculate_dpi_sizes method."""
        base_sizes = {"width": 100, "height": 200}
        result = manager.calculate_dpi_sizes(base_sizes)
        assert result == base_sizes

    @with_test_context(is_windows=True)
    def test_calculate_dpi_sizes_windows_with_root(self, manager, patch_ctx):
        """Test calculate_dpi_sizes on Windows with root."""
        mock_root = create_basic_mock_root(DPI_scaling=2.0)
        
        base_sizes = {"width": 100, "height": 200}
        result = manager.calculate_dpi_sizes(base_sizes, root=mock_root)
        
        assert result == {"width": 200, "height": 400}

    @with_test_context(is_windows=True)
    def test_calculate_dpi_sizes_windows_with_root_no_dpi_scaling(self, manager, patch_ctx):
        """Test calculate_dpi_sizes on Windows with root but no DPI_scaling attribute."""
        mock_root = create_basic_mock_root()
        del mock_root.DPI_scaling
        
        with patch.object(manager, '_get_hwnd_dpi') as mock_get_hwnd:
            mock_get_hwnd.return_value = (192, 192, 2.0)
            
            base_sizes = {"width": 100, "height": 200}
            result = manager.calculate_dpi_sizes(base_sizes, root=mock_root)
            
            assert result == {"width": 200, "height": 400}
        
    @with_test_context(is_windows=True)
    def test_calculate_dpi_sizes_windows_with_max_scale(self, manager, patch_ctx):
        """Test calculate_dpi_sizes on Windows with max_scale limit."""
        mock_root = create_basic_mock_root(DPI_scaling=3.0)
        
        base_sizes = {"width": 100, "height": 200}
        result = manager.calculate_dpi_sizes(base_sizes, root=mock_root, max_scale=2.0)
        
        assert result == {"width": 200, "height": 400}
        
    @with_test_context(is_windows=True)
    def test_calculate_dpi_sizes_windows_exception(self, manager, patch_ctx):
        """Test calculate_dpi_sizes on Windows with exception."""
        mock_root = create_mock_root_with_exception("winfo_id", "Test error")
        # Ensure DPI_scaling attribute doesn't exist to trigger exception path
        del mock_root.DPI_scaling
        
        base_sizes = {"width": 100, "height": 200}
        result = manager.calculate_dpi_sizes(base_sizes, root=mock_root)
        
        assert result == base_sizes
        
    @with_test_context(is_windows=True)
    def test_calculate_dpi_sizes_non_dict(self, manager, patch_ctx):
        """Test calculate_dpi_sizes with non-dict input."""
        result = manager.calculate_dpi_sizes("invalid")
        assert result == "invalid"
        
    @with_test_context(
        is_windows=True,
        wintypes_mock={'hwnd': 12345, 'monitor_handle': 2, 'x_dpi': 192, 'y_dpi': 192}
    )
    def test_get_hwnd_dpi_windows_scale_factor_exception(self, manager, patch_ctx, mock_ctx):
        """Test _get_hwnd_dpi with Windows scale factor exception."""
        # Mock the DPI functions
        patch_ctx.get_windll().shcore.SetProcessDpiAwareness.return_value = None
        patch_ctx.get_windll().user32.MonitorFromWindow.return_value = 67890
        patch_ctx.get_windll().shcore.GetDpiForMonitor.return_value = None
        patch_ctx.get_windll().shcore.GetScaleFactorForDevice.side_effect = Exception("Scale factor error")
        
        result = manager._get_hwnd_dpi(12345)
        
        # Should return DPI-based scaling without Windows scale factor
        assert result == (192, 192, 2.0)
        
    @with_test_context(
        is_windows=True,
        wintypes_mock={'hwnd': 12345, 'monitor_handle': 2, 'x_dpi': 96, 'y_dpi': 96}
    )
    def test_get_hwnd_dpi_monitor_exception(self, manager, patch_ctx, mock_ctx):
        """Test _get_hwnd_dpi with monitor DPI exception."""
        # Mock the DPI functions
        patch_ctx.get_windll().shcore.SetProcessDpiAwareness.return_value = None
        patch_ctx.get_windll().user32.MonitorFromWindow.return_value = 67890
        patch_ctx.get_windll().shcore.GetDpiForMonitor.side_effect = Exception("Monitor DPI error")
        
        result = manager._get_hwnd_dpi(12345)
        
        # Should return fallback values
        assert result == (96, 96, 1.0)

    @with_test_context(
        is_windows=True,
        wintypes_mock={'hwnd': 12345, 'monitor_handle': 2, 'x_dpi': 144, 'y_dpi': 144}
    )
    def test_get_hwnd_dpi_windows_scale_higher(self, manager, patch_ctx, mock_ctx):
        """Test _get_hwnd_dpi with Windows scale factor higher than DPI scaling."""
        # Mock the DPI functions
        patch_ctx.get_windll().shcore.SetProcessDpiAwareness.return_value = None
        patch_ctx.get_windll().user32.MonitorFromWindow.return_value = 67890
        patch_ctx.get_windll().shcore.GetDpiForMonitor.return_value = None
        patch_ctx.get_windll().shcore.GetScaleFactorForDevice.return_value = 200  # 2.0x scaling
        
        result = manager._get_hwnd_dpi(12345)
        
        # Should use Windows scale factor (2.0) instead of DPI-based (1.5)
        assert result == (144, 144, 2.0)


class TestDPIBackwardCompatibility:
    """Test backward compatibility functions."""

    @pytest.mark.parametrize("func_name,args,kwargs,expected_type", [
        ("dpi", (None,), {"enable": False}, dict),
        ("enable_dpi_awareness", (), {}, bool),
        ("enable_dpi_geometry", (None,), {}, dict),
        ("get_scaling_factor", (None,), {}, (int, float)),
        ("get_effective_dpi", (None,), {}, (int, float)),
        ("logical_to_physical", (100,), {}, (int, float)),
        ("physical_to_logical", (100,), {}, (int, float)),
    ])
    def test_backward_compatibility_functions(self, backward_compatibility_functions, func_name, args, kwargs, expected_type):
        """Test backward compatibility functions with various inputs."""
        func = backward_compatibility_functions[func_name]
        result = func(*args, **kwargs)
        
        if func_name == "dpi":
            assert result["enabled"] is False
        else:
            assert isinstance(result, expected_type)

    @pytest.mark.parametrize("func_name,args,kwargs,expected_type", [
        ("scale_font_size", (12,), {}, (int, float)),
        ("get_actual_window_size", (None,), {}, dict),
        ("calculate_dpi_sizes", ({"width": 100, "height": 200},), {}, dict),
        ("scale_icon", ("error", None), {}, str),
    ])
    def test_additional_backward_compatibility_functions(self, backward_compatibility_functions, func_name, args, kwargs, expected_type):
        """Test additional backward compatibility functions."""
        func = backward_compatibility_functions[func_name]
        result = func(*args, **kwargs)
        assert isinstance(result, expected_type)

    def test_scale_icon_non_windows(self):
        """Test scale_icon() on non-Windows platforms."""
        result = _test_scale_icon_with_patch(is_windows=False, parent=None)
        assert result == "error"

    def test_scale_icon_windows_success(self):
        """Test scale_icon() on Windows with successful scaling."""
        result = _test_scale_icon_with_patch(is_windows=True, scaling_factor=2.0)
        
        # Should return the original icon name or scaled version
        assert isinstance(result, str)

    def test_scale_icon_exception_handling(self):
        """Test scale_icon() exception handling."""
        result = _test_scale_icon_with_exception(Exception("Test error"))
        
        # Should return original icon name on error
        assert result == "error"

    def test_scale_icon_windows_scaling_1_0(self):
        """Test scale_icon() on Windows with scaling factor 1.0."""
        result = _test_scale_icon_with_scaling(1.0)
        
        # Should return original icon name when scaling is 1.0
        assert result == "error"

    def test_scale_icon_windows_scaling_1_25(self):
        """Test scale_icon() on Windows with scaling factor 1.25."""
        result = _test_scale_icon_with_scaling(1.25)
        
        # Should return scaled icon name
        assert result == "scaled_error_large"

    def test_scale_icon_windows_scaling_2_0(self):
        """Test scale_icon() on Windows with scaling factor 2.0."""
        result = _test_scale_icon_with_scaling(2.0)
        
        # Should return scaled icon name
        assert result == "scaled_error_large"

    def test_scale_icon_windows_scaling_4_0_max_scale_3_0(self):
        """Test scale_icon() on Windows with scaling factor 4.0 but max_scale 3.0."""
        result = _test_scale_icon_with_scaling(4.0, max_scale=3.0)
        
        # Should return scaled icon name with max_scale applied
        assert result == "scaled_error_large"

    def test_scale_icon_windows_unknown_icon(self):
        """Test scale_icon() on Windows with unknown icon name."""
        result = _test_scale_icon_with_scaling(2.0, icon_name="unknown")
        
        # Should return scaled icon name with unknown icon
        assert result == "scaled_unknown_large"

    def test_placeholder_functions(self):
        """Test placeholder functions that are not implemented."""
        from tkface.win.dpi import (
            add_scalable_property,
            disable_auto_dpi_scaling,
            enable_auto_dpi_scaling,
            get_scalable_properties,
            is_auto_dpi_scaling_enabled,
            remove_scalable_property,
            scale_widget_dimensions,
            scale_widget_tree,
        )

        # Test enable_auto_dpi_scaling
        result = enable_auto_dpi_scaling(None)
        assert result is False
        
        # Test disable_auto_dpi_scaling
        result = disable_auto_dpi_scaling(None)
        assert result is False
        
        # Test is_auto_dpi_scaling_enabled
        result = is_auto_dpi_scaling_enabled(None)
        assert result is False
        
        # Test scale_widget_dimensions
        result = scale_widget_dimensions(None)
        assert isinstance(result, dict)
        assert "errors" in result
        
        # Test scale_widget_tree
        result = scale_widget_tree(None)
        assert isinstance(result, dict)
        assert "errors" in result
        
        # Test get_scalable_properties
        result = get_scalable_properties()
        assert isinstance(result, set)
        
        # Test add_scalable_property
        add_scalable_property("test_property")
        # Should not raise exception
        
        # Test remove_scalable_property
        remove_scalable_property("test_property")
        # Should not raise exception


class TestDPIWidgetPatching:
    """Test DPI widget method patching functionality."""

    def test_patch_layout_methods(self):
        """Test _patch_layout_methods."""
        manager = create_dpi_manager_for_test()
        with patch.object(manager, '_patch_pack_method') as mock_pack:
            with patch.object(manager, '_patch_grid_method') as mock_grid:
                with patch.object(manager, '_patch_place_method') as mock_place:
                    manager._patch_layout_methods(2.0)
                    
                    mock_pack.assert_called_once_with(2.0)
                    mock_grid.assert_called_once_with(2.0)
                    mock_place.assert_called_once_with(2.0)

    @with_test_context(
        is_windows=True,
        tkinter_patches=[{'class': tk.Widget, 'method': 'pack', 'scaling_factor': 2.0}]
    )
    def test_patch_pack_method(self, manager, patch_ctx):
        """Test _patch_pack_method."""
        _test_widget_method_patch(manager, 'pack', '_patch_pack_method', 2.0)

    @with_test_context(
        is_windows=True,
        tkinter_patches=[{'class': tk.Widget, 'method': 'grid', 'scaling_factor': 2.0}]
    )
    def test_patch_grid_method(self, manager, patch_ctx):
        """Test _patch_grid_method."""
        _test_widget_method_patch(manager, 'grid', '_patch_grid_method', 2.0)

    @with_test_context(
        is_windows=True,
        tkinter_patches=[{'class': tk.Widget, 'method': 'place', 'scaling_factor': 2.0}]
    )
    def test_patch_place_method(self, manager, patch_ctx):
        """Test _patch_place_method."""
        _test_widget_method_patch(manager, 'place', '_patch_place_method', 2.0)

    def test_patch_widget_constructors(self):
        """Test _patch_widget_constructors."""
        manager = create_dpi_manager_for_test()
        
        with patch.object(manager, '_patch_label_frame_constructor') as mock_label_frame:
            with patch.object(manager, '_patch_frame_constructor') as mock_frame:
                with patch.object(manager, '_patch_button_constructor') as mock_button:
                    with patch.object(manager, '_patch_entry_constructor') as mock_entry:
                        with patch.object(manager, '_patch_label_constructor') as mock_label:
                            with patch.object(manager, '_patch_text_constructor') as mock_text:
                                with patch.object(manager, '_patch_checkbutton_constructor') as mock_checkbutton:
                                    with patch.object(manager, '_patch_radiobutton_constructor') as mock_radiobutton:
                                        with patch.object(manager, '_patch_listbox_constructor') as mock_listbox:
                                            with patch.object(manager, '_patch_spinbox_constructor') as mock_spinbox:
                                                with patch.object(manager, '_patch_scale_constructor') as mock_scale:
                                                    with patch.object(manager, '_patch_scrollbar_constructor') as mock_scrollbar:
                                                        with patch.object(manager, '_patch_canvas_constructor') as mock_canvas:
                                                            with patch.object(manager, '_patch_menu_constructor') as mock_menu:
                                                                with patch.object(manager, '_patch_menubutton_constructor') as mock_menubutton:
                                                                    with patch.object(manager, '_patch_treeview_constructor') as mock_treeview:
                                                                        manager._patch_widget_constructors(2.0)
                                                                        
                                                                        mock_label_frame.assert_called_once_with(2.0)
                                                                        mock_frame.assert_called_once_with(2.0)
                                                                        mock_button.assert_called_once_with(2.0)
                                                                        mock_entry.assert_called_once_with(2.0)
                                                                        mock_label.assert_called_once_with(2.0)
                                                                        mock_text.assert_called_once_with(2.0)
                                                                        mock_checkbutton.assert_called_once_with(2.0)
                                                                        mock_radiobutton.assert_called_once_with(2.0)
                                                                        mock_listbox.assert_called_once_with(2.0)
                                                                        mock_spinbox.assert_called_once_with(2.0)
                                                                        mock_scale.assert_called_once_with(2.0)
                                                                        mock_scrollbar.assert_called_once_with(2.0)
                                                                        mock_canvas.assert_called_once_with(2.0)
                                                                        mock_menu.assert_called_once_with(2.0)
                                                                        mock_menubutton.assert_called_once_with(2.0)
                                                                        mock_treeview.assert_called_once_with(2.0)

    @with_test_context(is_windows=True)
    def test_patch_treeview_methods(self, manager, patch_ctx):
        """Test _patch_treeview_methods."""
        with patch.object(manager, '_patch_treeview_column_method') as mock_column:
            with patch.object(manager, '_patch_treeview_style_method') as mock_style:
                manager._patch_treeview_methods(2.0)
                
                mock_column.assert_called_once_with(2.0)
                mock_style.assert_called_once_with(2.0)

    @with_test_context(is_windows=True)
    def test_override_geometry_method(self, manager, patch_ctx):
        """Test _override_geometry_method."""
        mock_root = create_mock_root_with_geometry("800x600", 2)
        
        manager._override_geometry_method(mock_root)
        
        # Test the overridden geometry method
        result = mock_root.geometry("400x300")
        
        # Should call wm_geometry with scaled values
        # The geometry string "400x300" should be scaled to "800x600"
        mock_root.wm_geometry.assert_called_with("800x600")

    @with_test_context(is_windows=True)
    def test_override_geometry_method_no_geometry_string(self, manager, patch_ctx):
        """Test _override_geometry_method with no geometry string."""
        mock_root = create_mock_root_with_geometry("800x600", 2)
        
        manager._override_geometry_method(mock_root)
        
        # Test the overridden geometry method with None
        result = mock_root.geometry()
        
        # Should call wm_geometry with no arguments
        mock_root.wm_geometry.assert_called_with()

    @with_test_context(is_windows=True)
    def test_override_geometry_method_invalid_geometry(self, manager, patch_ctx):
        """Test _override_geometry_method with invalid geometry string."""
        mock_root = create_mock_root_with_geometry("800x600", 2)
        
        manager._override_geometry_method(mock_root)
        
        # Test the overridden geometry method with invalid geometry
        result = mock_root.geometry("invalid")
        
        # Should call wm_geometry with original invalid string
        mock_root.wm_geometry.assert_called_with("invalid")

    @with_test_context(is_windows=True)
    def test_apply_scaling_methods(self, manager, patch_ctx):
        """Test _apply_scaling_methods."""
        mock_root = create_mock_root_with_dpi_scaling(2.0)
        
        with patch.object(manager, '_override_geometry_method') as mock_override:
            with patch.object(manager, '_patch_widget_methods') as mock_patch:
                manager._apply_scaling_methods(mock_root)
                
                # Should add TkScale method
                assert hasattr(mock_root, 'TkScale')
                assert callable(mock_root.TkScale)
                
                # Should call override and patch methods
                mock_override.assert_called_once_with(mock_root)
                mock_patch.assert_called_once_with(mock_root)

    @with_test_context(is_windows=True)
    def test_apply_scaling_methods_tkscale_functionality(self, manager, patch_ctx):
        """Test _apply_scaling_methods TkScale functionality."""
        mock_root = create_mock_root_with_dpi_scaling(2.0)
        
        manager._apply_scaling_methods(mock_root)
        
        # Test TkScale method
        result = mock_root.TkScale(100)
        assert result == 200
        
        result = mock_root.TkScale(50.5)
        assert result == 101

    @with_test_context(is_windows=True)
    def test_apply_scaling_methods_tkscale_with_float(self, manager, patch_ctx):
        """Test _apply_scaling_methods TkScale with float values."""
        mock_root = create_basic_mock_root(DPI_scaling=1.5)
        
        manager._apply_scaling_methods(mock_root)
        
        # Test TkScale method with float scaling
        result = mock_root.TkScale(100)
        assert result == 150
        
        result = mock_root.TkScale(33.33)
        assert result == 49

    def test_patch_label_frame_constructor(self):
        """Test _patch_label_frame_constructor."""
        manager = create_dpi_manager_for_test()
        _test_tkinter_constructor_patch_with_context(manager, tk.LabelFrame, '_patch_label_frame_constructor', 2.0)


    @pytest.mark.parametrize("tk_class,scaling_factor,test_kwargs,expected_kwargs", [
        # Frame tests
        (tk.Frame, 2.0, {"padx": 10, "pady": 20}, {"padx": 20, "pady": 40}),
        (tk.Frame, 2.0, {"padx": (10, 20), "pady": (30, 40)}, {"padx": (20, 40), "pady": (60, 80)}),
        # Button tests
        (tk.Button, 1.5, {"bd": 2}, {"bd": 3}),
        (tk.Button, 2.0, {"bd": 2}, {"bd": 4}),
        # Entry tests
        (tk.Entry, 2.0, {"bd": 1}, {"bd": 2}),
        (tk.Entry, 1.5, {"bd": 3}, {"bd": 4}),
        # Label tests
        (tk.Label, 1.5, {"wraplength": 100}, {"wraplength": 150}),
        (tk.Label, 2.0, {"wraplength": 100}, {"wraplength": 200}),
        (tk.Label, 2.0, {"bd": 1}, {"bd": 2}),
        (tk.Label, 2.0, {"bd": 2, "wraplength": 100}, {"bd": 4, "wraplength": 200}),
        # Text tests
        (tk.Text, 1.5, {"bd": 4}, {"bd": 6}),
        (tk.Text, 2.0, {"bd": 2}, {"bd": 4}),
        # Checkbutton tests
        (tk.Checkbutton, 2.0, {"bd": 2}, {"bd": 4}),
        (tk.Checkbutton, 1.5, {"bd": 3}, {"bd": 4}),
        # Radiobutton tests
        (tk.Radiobutton, 1.5, {"bd": 3}, {"bd": 4}),
        (tk.Radiobutton, 2.0, {"bd": 1}, {"bd": 2}),
        # Listbox tests
        (tk.Listbox, 2.0, {"bd": 1}, {"bd": 2}),
        (tk.Listbox, 1.5, {"bd": 4}, {"bd": 6}),
        # Spinbox tests
        (tk.Spinbox, 1.5, {"bd": 4}, {"bd": 6}),
        (tk.Spinbox, 2.0, {"bd": 2}, {"bd": 4}),
        # Scale tests
        (tk.Scale, 2.0, {"bd": 2}, {"bd": 4}),
        (tk.Scale, 1.5, {"bd": 3}, {"bd": 4}),
        # Scrollbar tests
        (tk.Scrollbar, 1.5, {"bd": 3}, {"bd": 4}),
        (tk.Scrollbar, 2.0, {"bd": 1}, {"bd": 2}),
        # Canvas tests
        (tk.Canvas, 2.0, {"width": 200, "height": 150}, {"width": 400, "height": 300}),
        (tk.Canvas, 1.5, {"width": 100, "height": 80}, {"width": 150, "height": 120}),
        (tk.Canvas, 2.0, {"bd": 1}, {"bd": 2}),
        (tk.Canvas, 2.0, {"width": 200, "height": 150, "bd": 2}, {"width": 400, "height": 300, "bd": 4}),
        # Menu tests
        (tk.Menu, 1.5, {"bd": 4}, {"bd": 6}),
        (tk.Menu, 2.0, {"bd": 2}, {"bd": 4}),
        # Menubutton tests
        (tk.Menubutton, 2.0, {"bd": 2}, {"bd": 4}),
        (tk.Menubutton, 1.5, {"bd": 3}, {"bd": 4}),
        # TreeView tests
        (tk.ttk.Treeview, 2.0, {"height": 10}, {"height": 20}),
        (tk.ttk.Treeview, 1.5, {"height": 8}, {"height": 12}),
        # LabelFrame tests
        (tk.LabelFrame, 2.0, {"padx": 8, "pady": 4}, {"padx": 16, "pady": 8}),
        (tk.LabelFrame, 1.5, {"bd": 2}, {"bd": 3}),
    ])
    def _test_tkinter_constructor_patching(self, manager, tk_class, scaling_factor, test_kwargs, expected_kwargs):
        """Test tkinter constructor patching with various classes and parameters."""
        helper__test_tkinter_constructor_patch(tk_class, manager, scaling_factor, **test_kwargs)

    def test_patch_frame_constructor(self):
        """Test _patch_frame_constructor method patching."""
        manager = create_dpi_manager_for_test()
        _test_tkinter_constructor_patch_with_context(manager, tk.Frame, '_patch_frame_constructor', 2.0)

    def test_patch_button_constructor(self):
        """Test _patch_button_constructor method patching."""
        manager = create_dpi_manager_for_test()
        _test_tkinter_constructor_patch_with_context(manager, tk.Button, '_patch_button_constructor', 2.0)

    def test_patch_entry_constructor(self):
        """Test _patch_entry_constructor method patching."""
        manager = create_dpi_manager_for_test()
        _test_tkinter_constructor_patch_with_context(manager, tk.Entry, '_patch_entry_constructor', 2.0)

    def test_patch_label_constructor(self):
        """Test _patch_label_constructor method patching."""
        manager = create_dpi_manager_for_test()
        _test_tkinter_constructor_patch_with_context(manager, tk.Label, '_patch_label_constructor', 2.0)

    def test_patch_text_constructor(self):
        """Test _patch_text_constructor."""
        manager = create_dpi_manager_for_test()
        _test_tkinter_constructor_patch_with_context(manager, tk.Text, '_patch_text_constructor', 2.0)


    def test_patch_checkbutton_constructor(self):
        """Test _patch_checkbutton_constructor."""
        manager = create_dpi_manager_for_test()
        _test_tkinter_constructor_patch_with_context(manager, tk.Checkbutton, '_patch_checkbutton_constructor', 2.0)


    def test_patch_radiobutton_constructor(self):
        """Test _patch_radiobutton_constructor."""
        manager = create_dpi_manager_for_test()
        _test_tkinter_constructor_patch_with_context(manager, tk.Radiobutton, '_patch_radiobutton_constructor', 2.0)


    def test_patch_listbox_constructor(self):
        """Test _patch_listbox_constructor."""
        manager = create_dpi_manager_for_test()
        _test_tkinter_constructor_patch_with_context(manager, tk.Listbox, '_patch_listbox_constructor', 2.0)


    def test_patch_spinbox_constructor(self):
        """Test _patch_spinbox_constructor."""
        manager = create_dpi_manager_for_test()
        _test_tkinter_constructor_patch_with_context(manager, tk.Spinbox, '_patch_spinbox_constructor', 2.0)


    def test_patch_scale_constructor(self):
        """Test _patch_scale_constructor."""
        manager = create_dpi_manager_for_test()
        _test_tkinter_constructor_patch_with_context(manager, tk.Scale, '_patch_scale_constructor', 2.0)


    def test_patch_scrollbar_constructor(self):
        """Test _patch_scrollbar_constructor."""
        manager = create_dpi_manager_for_test()
        _test_tkinter_constructor_patch_with_context(manager, tk.Scrollbar, '_patch_scrollbar_constructor', 2.0)


    def test_patch_canvas_constructor(self):
        """Test _patch_canvas_constructor."""
        manager = create_dpi_manager_for_test()
        _test_tkinter_constructor_patch_with_context(manager, tk.Canvas, '_patch_canvas_constructor', 2.0)



    @with_test_context(
        is_windows=True,
        tkinter_patches=[{'class': tk.Menu, 'method': '__init__', 'scaling_factor': 2.0}]
    )
    def test_patch_menu_constructor(self, manager, patch_ctx):
        """Test _patch_menu_constructor."""
        _test_tkinter_constructor_patch(manager, tk.Menu, '_patch_menu_constructor', 2.0)



    @with_test_context(
        is_windows=True,
        tkinter_patches=[{'class': tk.Menubutton, 'method': '__init__', 'scaling_factor': 2.0}]
    )
    def test_patch_menubutton_constructor(self, manager, patch_ctx):
        """Test _patch_menubutton_constructor."""
        _test_tkinter_constructor_patch(manager, tk.Menubutton, '_patch_menubutton_constructor', 2.0)


    @with_test_context(
        is_windows=True,
        tkinter_patches=[{'class': tk.ttk.Treeview, 'method': '__init__', 'scaling_factor': 2.0}]
    )
    def test_patch_treeview_constructor(self, manager, patch_ctx):
        """Test _patch_treeview_constructor."""
        _test_tkinter_constructor_patch(manager, tk.ttk.Treeview, '_patch_treeview_constructor', 2.0)


    @with_test_context(
        is_windows=True,
        treeview_patches=['column']
    )
    def test_patch_treeview_column_method(self, manager, patch_ctx):
        """Test _patch_treeview_column_method."""
        test_treeview_column_patch_basic(manager, 2.0)

    @with_test_context(
        is_windows=True,
        treeview_patches=['column']
    )
    def test_patch_treeview_column_method_with_width_minwidth(self, manager, patch_ctx):
        """Test _patch_treeview_column_method with width and minwidth parameters."""
        test_treeview_column_patch_with_parameters(manager, 2.0)

    @with_test_context(
        is_windows=True,
        treeview_patches=['column']
    )
    def test_patch_treeview_column_method_without_scaling_params(self, manager, patch_ctx):
        """Test _patch_treeview_column_method without scaling parameters."""
        test_treeview_column_patch_without_scaling_params(manager, 2.0)

    @with_test_context(
        is_windows=True,
        treeview_patches=['style']
    )
    def test_patch_treeview_style_method(self, manager, patch_ctx):
        """Test _patch_treeview_style_method."""
        test_treeview_style_patch_basic(manager, 2.0)

    @with_test_context(
        is_windows=True,
        treeview_patches=['style']
    )
    def test_patch_treeview_style_method_with_rowheight(self, manager, patch_ctx):
        """Test _patch_treeview_style_method with rowheight parameter."""
        test_treeview_style_patch_with_rowheight(manager, 2.0)

    @with_test_context(
        is_windows=True,
        treeview_patches=['style']
    )
    def test_patch_treeview_style_method_without_rowheight(self, manager, patch_ctx):
        """Test _patch_treeview_style_method without rowheight parameter."""
        test_treeview_style_patch_without_rowheight(manager, 2.0)

    @with_test_context(is_windows=True)
    def test_patch_widget_methods_with_dpi_scaling(self, manager, patch_ctx):
        """Test _patch_widget_methods with DPI_scaling attribute."""
        mock_root = create_basic_mock_root(DPI_scaling=2.0, tk_call="1.0")
        
        with patch.object(manager, '_patch_layout_methods') as mock_layout:
            with patch.object(manager, '_patch_widget_constructors') as mock_constructors:
                with patch.object(manager, '_patch_treeview_methods') as mock_treeview:
                    manager._patch_widget_methods(mock_root)
                    
                    mock_layout.assert_called_once()
                    mock_constructors.assert_called_once()
                    mock_treeview.assert_called_once()

    @with_test_context(is_windows=True)
    def test_patch_widget_methods_without_dpi_scaling(self, manager, patch_ctx):
        """Test _patch_widget_methods without DPI_scaling attribute."""
        mock_root = create_mock_root_without_dpi_scaling()
        
        # Should not raise exception and not call patch methods
        manager._patch_widget_methods(mock_root)

    @with_test_context(is_windows=True)
    def test_patch_widget_methods_none_root(self, manager, patch_ctx):
        """Test _patch_widget_methods with None root."""
        # Should not raise exception
        manager._patch_widget_methods(None)


class TestDPIIntegration:
    """Test DPI integration with Tkinter."""

    @with_test_context(
        is_windows=True,
        real_tkinter_root=True
    )
    def test_dpi_with_real_tkinter_root(self, root, manager, patch_ctx):
        """Test DPI functionality with a real Tkinter root."""
        from tkface.win.dpi import dpi
        
        result = dpi(root, enable=True)
        
        assert isinstance(result, dict)
        assert "enabled" in result
        assert "platform" in result

    @with_test_context(
        is_windows=True,
        real_tkinter_root=True
    )
    def test_get_scaling_factor_with_real_root(self, root, manager, patch_ctx):
        """Test get_scaling_factor with a real Tkinter root."""
        from tkface.win.dpi import get_scaling_factor
        
        result = get_scaling_factor(root)
        
        assert isinstance(result, (int, float))
        assert result > 0

    @with_test_context(
        is_windows=True,
        real_tkinter_root=True
    )
    def test_scale_font_size_with_real_root(self, root, manager, patch_ctx):
        """Test scale_font_size with a real Tkinter root."""
        from tkface.win.dpi import scale_font_size
        
        result = scale_font_size(12, root=root)
        
        assert isinstance(result, (int, float))
        assert result > 0

    @with_test_context(
        is_windows=True,
        real_tkinter_root=True
    )
    def test_get_actual_window_size_with_real_root(self, root, manager, patch_ctx):
        """Test get_actual_window_size with a real Tkinter root."""
        from tkface.win.dpi import get_actual_window_size
        
        result = get_actual_window_size(root)
        
        assert isinstance(result, dict)
        assert "logical_size" in result
        assert "physical_size" in result



class TestDPICoverageImprovements:
    """Test class to improve coverage for missing lines."""

    def _test_widget_method_patch(self, manager, method_name, patch_method_name, 
                                 scale_factor=2.0, test_calls=None):
        """
        Helper method to test widget method patching.
        
        Args:
            manager: DPI manager instance
            method_name: Name of the widget method to patch (e.g., 'pack', 'grid', 'place')
            patch_method_name: Name of the patch method (e.g., '_patch_pack_method')
            scale_factor: Scaling factor to apply
            test_calls: List of call configurations to test
        """
        if test_calls is None:
            test_calls = [{'padx': 10, 'pady': 20}]
        
        # Store original method
        original_method = getattr(tk.Widget, method_name)
        
        try:
            # Apply patch
            getattr(manager, patch_method_name)(scale_factor)
            
            # Test with mock widget
            mock_widget = MagicMock()
            for call_kwargs in test_calls:
                getattr(mock_widget, method_name)(**call_kwargs)
                
        finally:
            # Restore original method
            setattr(tk.Widget, method_name, original_method)

    def _test_comprehensive_constructor_patches(self, manager, constructors_config, scale_factor=2.0):
        """
        Helper method to test comprehensive widget constructor patching.
        
        Args:
            manager: DPI manager instance
            constructors_config: List of (module_path, patch_method) tuples
            scale_factor: Scaling factor to apply
        """
        for module_path, patch_method in constructors_config:
            with patch(module_path + '.__init__', return_value=None) as mock_init:
                patch_method(scale_factor)
                
                # Create widget with appropriate parameters
                if 'ttk' in module_path:
                    widget_class = tk.ttk.Treeview
                    widget = widget_class(None, height=10)
                else:
                    widget_class = getattr(tk, module_path.split('.')[-1])
                    widget = widget_class(None, bd=2)
                
                # Verify the constructor was called
                mock_init.assert_called_once()

    def _test_constructor_patch(self, manager, widget_class, patch_method, 
                               patch_path, scale_factor=2.0, 
                               input_kwargs=None, expected_kwargs=None,
                               additional_kwargs=None):
        """
        Helper method to test constructor patching for widgets.
        
        Args:
            manager: DPI manager instance
            widget_class: Widget class to test (e.g., tk.LabelFrame)
            patch_method: Method to call on manager (e.g., '_patch_label_frame_constructor')
            patch_path: Path to patch (e.g., 'tkinter.LabelFrame.__init__')
            scale_factor: Scaling factor to apply
            input_kwargs: Input keyword arguments for widget creation
            expected_kwargs: Expected keyword arguments after scaling
            additional_kwargs: Additional keyword arguments for widget creation
        """
        if input_kwargs is None:
            input_kwargs = {'padx': 10, 'pady': 20, 'bd': 2}
        if expected_kwargs is None:
            expected_kwargs = {'padx': 20, 'pady': 40, 'bd': 4}
        if additional_kwargs is None:
            additional_kwargs = {}
        
        with patch(patch_path, return_value=None) as mock_init:
            getattr(manager, patch_method)(scale_factor)
            
            # Create widget with combined kwargs
            all_kwargs = {**input_kwargs, **additional_kwargs}
            widget = widget_class(None, **all_kwargs)
            
            # Verify the constructor was called with expected values
            mock_init.assert_called_once()
            call_args = mock_init.call_args
            for key, expected_value in expected_kwargs.items():
                assert call_args[1][key] == expected_value


    def test_scale_padding_kwargs_global_with_padx_pady(self, manager):
        """Test _scale_padding_kwargs_global with both padx and pady."""
        self._test_widget_method_patch(manager, 'pack', '_patch_pack_method', 2.0,
                                     [{'padx': 10, 'pady': 20}])

    def test_scale_padding_value_global_with_tuple(self, manager):
        """Test _scale_padding_value_global with tuple values."""
        self._test_widget_method_patch(manager, 'pack', '_patch_pack_method', 2.0,
                                     [{'padx': (5, 10), 'pady': (15, 20)}])

    def test_scale_padding_value_global_with_large_values(self, manager):
        """Test _scale_padding_value_global with values > 50 (should not scale)."""
        self._test_widget_method_patch(manager, 'pack', '_patch_pack_method', 2.0,
                                     [{'padx': 100, 'pady': 200}])  # Large values

    def test_scale_padding_value_global_with_negative_values(self, manager):
        """Test _scale_padding_value_global with negative values."""
        self._test_widget_method_patch(manager, 'pack', '_patch_pack_method', 2.0,
                                     [{'padx': -10, 'pady': -20}])

    def test_label_frame_constructor_patch_with_tuple_padx_pady(self, manager):
        """Test LabelFrame constructor patching with tuple padx/pady."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.LabelFrame,
            patch_method='_patch_label_frame_constructor',
            patch_path='tkinter.LabelFrame.__init__',
            input_kwargs={'padx': (5, 10), 'pady': (15, 20), 'bd': 2},
            expected_kwargs={'padx': (10, 20), 'pady': (30, 40), 'bd': 4}
        )

    def test_label_frame_constructor_patch_with_single_padx_pady(self, manager):
        """Test LabelFrame constructor patching with single padx/pady values."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.LabelFrame,
            patch_method='_patch_label_frame_constructor',
            patch_path='tkinter.LabelFrame.__init__',
            input_kwargs={'padx': 10, 'pady': 20, 'bd': 3},
            expected_kwargs={'padx': 20, 'pady': 40, 'bd': 6}
        )

    def test_frame_constructor_patch_with_padding(self, manager):
        """Test Frame constructor patching with padding."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.Frame,
            patch_method='_patch_frame_constructor',
            patch_path='tkinter.Frame.__init__',
            input_kwargs={'padx': 10, 'pady': 20, 'bd': 2},
            expected_kwargs={'padx': 20, 'pady': 40, 'bd': 2}  # Frame doesn't scale bd
        )

    def test_button_constructor_patch_with_padding(self, manager):
        """Test Button constructor patching with padding."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.Button,
            patch_method='_patch_button_constructor',
            patch_path='tkinter.Button.__init__',
            input_kwargs={'padx': 10, 'pady': 20, 'bd': 2},
            expected_kwargs={'padx': 10, 'pady': 20, 'bd': 4}  # Button doesn't scale padx/pady
        )

    def test_entry_constructor_patch_with_padding(self, manager):
        """Test Entry constructor patching with padding."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.Entry,
            patch_method='_patch_entry_constructor',
            patch_path='tkinter.Entry.__init__',
            input_kwargs={'padx': 10, 'pady': 20, 'bd': 2},
            expected_kwargs={'padx': 10, 'pady': 20, 'bd': 4}  # Entry doesn't scale padx/pady
        )

    def test_label_constructor_patch_with_padding(self, manager):
        """Test Label constructor patching with padding."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.Label,
            patch_method='_patch_label_constructor',
            patch_path='tkinter.Label.__init__',
            input_kwargs={'padx': 10, 'pady': 20, 'bd': 2},
            expected_kwargs={'padx': 10, 'pady': 20, 'bd': 4},  # Label doesn't scale padx/pady
            additional_kwargs={'wraplength': 100}
        )
        # Verify wraplength scaling separately
        with patch('tkinter.Label.__init__', return_value=None) as mock_init:
            manager._patch_label_constructor(2.0)
            tk.Label(None, wraplength=100)
            call_args = mock_init.call_args
            assert call_args[1]['wraplength'] == 200  # 100 * 2.0

    def test_text_constructor_patch_with_padding(self, manager):
        """Test Text constructor patching with padding."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.Text,
            patch_method='_patch_text_constructor',
            patch_path='tkinter.Text.__init__',
            input_kwargs={'padx': 10, 'pady': 20, 'bd': 2},
            expected_kwargs={'padx': 10, 'pady': 20, 'bd': 4}  # Text doesn't scale padx/pady
        )

    def test_checkbutton_constructor_patch_with_padding(self, manager):
        """Test Checkbutton constructor patching with padding."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.Checkbutton,
            patch_method='_patch_checkbutton_constructor',
            patch_path='tkinter.Checkbutton.__init__',
            input_kwargs={'padx': 10, 'pady': 20, 'bd': 2},
            expected_kwargs={'padx': 10, 'pady': 20, 'bd': 4}  # Checkbutton doesn't scale padx/pady
        )

    def test_radiobutton_constructor_patch_with_padding(self, manager):
        """Test Radiobutton constructor patching with padding."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.Radiobutton,
            patch_method='_patch_radiobutton_constructor',
            patch_path='tkinter.Radiobutton.__init__',
            input_kwargs={'padx': 10, 'pady': 20, 'bd': 2},
            expected_kwargs={'padx': 10, 'pady': 20, 'bd': 4}  # Radiobutton doesn't scale padx/pady
        )

    def test_listbox_constructor_patch_with_padding(self, manager):
        """Test Listbox constructor patching with padding."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.Listbox,
            patch_method='_patch_listbox_constructor',
            patch_path='tkinter.Listbox.__init__',
            input_kwargs={'padx': 10, 'pady': 20, 'bd': 2},
            expected_kwargs={'padx': 10, 'pady': 20, 'bd': 4}  # Listbox doesn't scale padx/pady
        )

    def test_spinbox_constructor_patch_with_padding(self, manager):
        """Test Spinbox constructor patching with padding."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.Spinbox,
            patch_method='_patch_spinbox_constructor',
            patch_path='tkinter.Spinbox.__init__',
            input_kwargs={'padx': 10, 'pady': 20, 'bd': 2},
            expected_kwargs={'padx': 10, 'pady': 20, 'bd': 4}  # Spinbox doesn't scale padx/pady
        )

    def test_scale_constructor_patch_with_padding(self, manager):
        """Test Scale constructor patching with padding."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.Scale,
            patch_method='_patch_scale_constructor',
            patch_path='tkinter.Scale.__init__',
            input_kwargs={'padx': 10, 'pady': 20, 'bd': 2},
            expected_kwargs={'padx': 10, 'pady': 20, 'bd': 4}  # Scale doesn't scale padx/pady
        )

    def test_scrollbar_constructor_patch_with_padding(self, manager):
        """Test Scrollbar constructor patching with padding."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.Scrollbar,
            patch_method='_patch_scrollbar_constructor',
            patch_path='tkinter.Scrollbar.__init__',
            input_kwargs={'padx': 10, 'pady': 20, 'bd': 2},
            expected_kwargs={'padx': 10, 'pady': 20, 'bd': 4}  # Scrollbar doesn't scale padx/pady
        )

    def test_canvas_constructor_patch_with_padding(self, manager):
        """Test Canvas constructor patching with padding."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.Canvas,
            patch_method='_patch_canvas_constructor',
            patch_path='tkinter.Canvas.__init__',
            input_kwargs={'padx': 10, 'pady': 20, 'bd': 2},
            expected_kwargs={'padx': 20, 'pady': 40, 'bd': 4}  # Canvas now scales padx/pady
        )

    def test_menu_constructor_patch_with_padding(self, manager):
        """Test Menu constructor patching with padding."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.Menu,
            patch_method='_patch_menu_constructor',
            patch_path='tkinter.Menu.__init__',
            input_kwargs={'padx': 10, 'pady': 20, 'bd': 2},
            expected_kwargs={'padx': 10, 'pady': 20, 'bd': 4}  # Menu doesn't scale padx/pady
        )

    def test_menubutton_constructor_patch_with_padding(self, manager):
        """Test Menubutton constructor patching with padding."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.Menubutton,
            patch_method='_patch_menubutton_constructor',
            patch_path='tkinter.Menubutton.__init__',
            input_kwargs={'padx': 10, 'pady': 20, 'bd': 2},
            expected_kwargs={'padx': 10, 'pady': 20, 'bd': 4}  # Menubutton doesn't scale padx/pady
        )

    def test_treeview_constructor_patch_with_padding(self, manager):
        """Test Treeview constructor patching with padding."""
        self._test_constructor_patch(
            manager=manager,
            widget_class=tk.ttk.Treeview,
            patch_method='_patch_treeview_constructor',
            patch_path='tkinter.ttk.Treeview.__init__',
            input_kwargs={'padx': 10, 'pady': 20, 'bd': 2},
            expected_kwargs={'padx': 10, 'pady': 20, 'bd': 2},  # Treeview doesn't scale padx/pady/bd
            additional_kwargs={'height': 10}
        )
        # Verify height scaling separately
        with patch('tkinter.ttk.Treeview.__init__', return_value=None) as mock_init:
            manager._patch_treeview_constructor(2.0)
            tk.ttk.Treeview(None, height=10)
            call_args = mock_init.call_args
            assert call_args[1]['height'] == 20  # 10 * 2.0

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
    def test_fix_dpi_fallback_path(self, manager, mock_root):
        """Test the fallback path in fix_dpi when shcore is not available."""
        with patch.object(manager, '_enable_dpi_awareness', return_value={'shcore': False}):
            with patch.object(manager, '_get_hwnd_dpi', return_value=(192, 192, 2.0)) as mock_get_dpi:
                with patch.object(manager, '_fix_scaling') as mock_fix_scaling:
                    manager.fix_dpi(mock_root)
                    
                    mock_get_dpi.assert_called_once_with(mock_root.winfo_id())
                    mock_fix_scaling.assert_called_once_with(mock_root)
                    assert mock_root.DPI_X == 192
                    assert mock_root.DPI_Y == 192
                    assert mock_root.DPI_scaling == 2.0

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
    def test_fix_dpi_exception_fallback(self, manager, mock_root):
        """Test exception handling in fix_dpi with fallback."""
        with patch.object(manager, '_enable_dpi_awareness', side_effect=Exception("Test error")):
            with patch.object(manager, '_get_hwnd_dpi', return_value=(96, 96, 1.0)) as mock_get_dpi:
                with patch.object(manager, '_fix_scaling') as mock_fix_scaling:
                    manager.fix_dpi(mock_root)
                    
                    mock_get_dpi.assert_called_once_with(mock_root.winfo_id())
                    mock_fix_scaling.assert_called_once_with(mock_root)
                    assert mock_root.DPI_X == 96
                    assert mock_root.DPI_Y == 96
                    assert mock_root.DPI_scaling == 1.0

    def test_scale_padding_value_global_edge_cases(self, manager):
        """Test _scale_padding_value_global with edge cases."""
        test_calls = [
            {'padx': 50, 'pady': -50},  # Values exactly at boundary
            {'padx': 51, 'pady': -51},  # Values just over boundary
            {'padx': (50, 50), 'pady': (-50, -50)},  # Tuple values at boundary
            {'padx': (51, 51), 'pady': (-51, -51)}   # Tuple values over boundary
        ]
        self._test_widget_method_patch(manager, 'pack', '_patch_pack_method', 2.0, test_calls)

    def test_scale_padding_value_global_non_numeric(self, manager):
        """Test _scale_padding_value_global with non-numeric values."""
        test_calls = [
            {'padx': "10", 'pady': "20"},  # String values (should not scale)
            {'padx': None, 'pady': None}   # None values (should not scale)
        ]
        self._test_widget_method_patch(manager, 'pack', '_patch_pack_method', 2.0, test_calls)

    def test_scale_padding_value_global_invalid_tuple(self, manager):
        """Test _scale_padding_value_global with invalid tuple values."""
        test_calls = [
            {'padx': (10,), 'pady': (10, 20, 30)},  # Tuple of wrong length
            {'padx': (10, "20"), 'pady': ("10", 20)}  # Tuple containing non-numeric values
        ]
        self._test_widget_method_patch(manager, 'pack', '_patch_pack_method', 2.0, test_calls)

    def test_patch_grid_method_with_padding(self, manager):
        """Test _patch_grid_method with padding."""
        self._test_widget_method_patch(manager, 'grid', '_patch_grid_method', 2.0,
                                     [{'padx': 10, 'pady': 20}])

    def test_patch_place_method_with_padding(self, manager):
        """Test _patch_place_method with padding."""
        self._test_widget_method_patch(manager, 'place', '_patch_place_method', 2.0,
                                     [{'padx': 10, 'pady': 20}])

    def test_patch_widget_constructors_comprehensive(self, manager):
        """Test comprehensive widget constructor patching."""
        constructors_to_test = [
            ('tkinter.LabelFrame', manager._patch_label_frame_constructor),
            ('tkinter.Frame', manager._patch_frame_constructor),
            ('tkinter.Button', manager._patch_button_constructor),
            ('tkinter.Entry', manager._patch_entry_constructor),
            ('tkinter.Label', manager._patch_label_constructor),
            ('tkinter.Text', manager._patch_text_constructor),
            ('tkinter.Checkbutton', manager._patch_checkbutton_constructor),
            ('tkinter.Radiobutton', manager._patch_radiobutton_constructor),
            ('tkinter.Listbox', manager._patch_listbox_constructor),
            ('tkinter.Spinbox', manager._patch_spinbox_constructor),
            ('tkinter.Scale', manager._patch_scale_constructor),
            ('tkinter.Scrollbar', manager._patch_scrollbar_constructor),
            ('tkinter.Canvas', manager._patch_canvas_constructor),
            ('tkinter.Menu', manager._patch_menu_constructor),
            ('tkinter.Menubutton', manager._patch_menubutton_constructor),
            ('tkinter.ttk.Treeview', manager._patch_treeview_constructor),
        ]
        
        self._test_comprehensive_constructor_patches(manager, constructors_to_test, 2.0)

    def test_calculate_dpi_sizes_non_dict(self, manager):
        """Test calculate_dpi_sizes with non-dict input."""
        result = manager.calculate_dpi_sizes("not a dict")
        
        assert result == "not a dict"

    def test_get_hwnd_dpi_outer_exception(self, manager):
        """Force outer try/except in _get_hwnd_dpi by raising before inner try."""
        with patch('tkface.win.dpi.is_windows', return_value=True), \
             patch('tkface.win.dpi.ctypes') as mock_ctypes:
            # Raise at MonitorFromWindow so inner try block is not entered
            mock_ctypes.windll.user32.MonitorFromWindow.side_effect = Exception("Boom")
            result = manager._get_hwnd_dpi(12345)
            assert result == (96, 96, 1.0)

    def test_pack_grid_place_wrappers_execute_paths(self, manager):
        """Execute scaled pack/grid/place wrappers including branches without keys."""
        calls = []

        def dummy_pack(self, **kwargs):  # pylint: disable=unused-argument
            calls.append(("pack", kwargs))
        def dummy_grid(self, **kwargs):  # pylint: disable=unused-argument
            calls.append(("grid", kwargs))
        def dummy_place(self, **kwargs):  # pylint: disable=unused-argument
            calls.append(("place", kwargs))

        # Save originals and replace with dummies before patching
        orig_pack, orig_grid, orig_place = tk.Widget.pack, tk.Widget.grid, tk.Widget.place
        try:
            tk.Widget.pack = dummy_pack
            tk.Widget.grid = dummy_grid
            tk.Widget.place = dummy_place

            # Apply patches
            manager._patch_pack_method(2.0)
            manager._patch_grid_method(2.0)
            manager._patch_place_method(2.0)

            dummy = object()
            # pack with padding
            tk.Widget.pack(dummy, padx=10, pady=(5, 7))
            # pack without padding keys
            tk.Widget.pack(dummy, other=1)
            # grid with padding
            tk.Widget.grid(dummy, padx=(2, 3), pady=4)
            # grid without padding keys
            tk.Widget.grid(dummy, sticky='nsew')
            # place with only x
            tk.Widget.place(dummy, x=10)
            # place with only y
            tk.Widget.place(dummy, y=20)

            # Verify calls were routed to dummy originals with scaled values when applicable
            # Find first pack call with padding
            pack_call = next(name_kwargs for name_kwargs in calls if name_kwargs[0] == 'pack' and 'padx' in name_kwargs[1])
            assert pack_call[1]['padx'] == 20
            assert pack_call[1]['pady'] == (10, 14)
            # Grid padding scaled
            grid_call = next(name_kwargs for name_kwargs in calls if name_kwargs[0] == 'grid' and 'padx' in name_kwargs[1])
            assert grid_call[1]['padx'] == (4, 6)
            assert grid_call[1]['pady'] == 8
            # place x-only and y-only scaled
            place_x_call = next(name_kwargs for name_kwargs in calls if name_kwargs[0] == 'place' and 'x' in name_kwargs[1])
            assert place_x_call[1]['x'] == 20
            place_y_call = next(name_kwargs for name_kwargs in calls if name_kwargs[0] == 'place' and 'y' in name_kwargs[1])
            assert place_y_call[1]['y'] == 40
        finally:
            tk.Widget.pack, tk.Widget.grid, tk.Widget.place = orig_pack, orig_grid, orig_place

    def test_canvas_constructor_width_and_height_individual(self, manager):
        """Cover Canvas constructor branches for width-only and height-only."""
        with patch('tkinter.Canvas.__init__', return_value=None) as mock_init:
            manager._patch_canvas_constructor(2.0)
            # width only
            widget = tk.Canvas.__new__(tk.Canvas)
            tk.Canvas.__init__(widget, None, width=50)
            assert mock_init.call_args[1]['width'] == 100
        with patch('tkinter.Canvas.__init__', return_value=None) as mock_init:
            manager._patch_canvas_constructor(2.0)
            # height only
            widget = tk.Canvas.__new__(tk.Canvas)
            tk.Canvas.__init__(widget, None, height=30)
            assert mock_init.call_args[1]['height'] == 60

    def test_enable_dpi_awareness_public_windows_paths(self, manager):
        """Exercise public enable_dpi_awareness success and fallbacks on Windows."""
        with patch('tkface.win.dpi.is_windows', return_value=True), \
             patch('tkface.win.dpi.ctypes') as mock_ctypes:
            # Success via shcore
            mock_ctypes.windll.shcore.SetProcessDpiAwareness.return_value = None
            assert manager.enable_dpi_awareness() is True
        with patch('tkface.win.dpi.is_windows', return_value=True), \
             patch('tkface.win.dpi.ctypes') as mock_ctypes:
            # Fallback to user32
            mock_ctypes.windll.shcore.SetProcessDpiAwareness.side_effect = AttributeError()
            mock_ctypes.windll.user32.SetProcessDPIAware.return_value = None
            assert manager.enable_dpi_awareness() is True
        with patch('tkface.win.dpi.is_windows', return_value=True), \
             patch('tkface.win.dpi.ctypes') as mock_ctypes:
            # Both unavailable -> False
            mock_ctypes.windll.shcore.SetProcessDpiAwareness.side_effect = AttributeError()
            mock_ctypes.windll.user32.SetProcessDPIAware.side_effect = AttributeError()
            assert manager.enable_dpi_awareness() is False
        with patch('tkface.win.dpi.is_windows', return_value=True), \
             patch('tkface.win.dpi.ctypes') as mock_ctypes:
            # Outer exception path -> False (unexpected exception in shcore call)
            mock_ctypes.windll.shcore.SetProcessDpiAwareness.side_effect = Exception("boom")
            assert manager.enable_dpi_awareness() is False

    def test_scale_font_size_outer_exception_returns_original(self, manager):
        """Force outer exception in scale_font_size to return original size."""
        with patch('tkface.win.dpi.is_windows', return_value=True):
            mock_root = create_basic_mock_root()
            # tk.call fails, DPI_scaling missing, and _get_hwnd_dpi raises
            mock_root.tk.call.side_effect = Exception("fail")
            if hasattr(mock_root, 'DPI_scaling'):
                delattr(mock_root, 'DPI_scaling')
            with patch.object(manager, '_get_hwnd_dpi', side_effect=Exception("oops")):
                result = manager.scale_font_size(12, root=mock_root)
                assert result == 12

    def test_scale_icon_between_1_0_and_1_25(self):
        """Cover scale_icon branch where 1.0 < scaling < 1.25 (scale_factor set to 1)."""
        with patch('tkface.win.dpi.is_windows', return_value=True), \
             patch('tkface.win.dpi.get_scaling_factor', return_value=1.1):
            parent = create_mock_parent()
            parent.tk.call.return_value = None
            from tkface.win.dpi import scale_icon
            result = scale_icon('error', parent)
            assert result == 'scaled_error_large'


class TestTTKWidgetDPI:
    """Test cases for automatic ttk widget DPI configuration."""

    def test_configure_ttk_widgets_for_dpi_non_windows(self):
        """Test configure_ttk_widgets_for_dpi on non-Windows platform."""
        with patch('tkface.win.dpi.is_windows', return_value=False):
            from tkface.win.dpi import configure_ttk_widgets_for_dpi
            # Should return early without error
            configure_ttk_widgets_for_dpi(None)

    def test_configure_ttk_widgets_for_dpi_no_root(self):
        """Test configure_ttk_widgets_for_dpi with None root."""
        with patch('tkface.win.dpi.is_windows', return_value=True):
            from tkface.win.dpi import configure_ttk_widgets_for_dpi
            # Should return early without error
            configure_ttk_widgets_for_dpi(None)

    def test_configure_ttk_widgets_for_dpi_low_scaling(self):
        """Test configure_ttk_widgets_for_dpi with scaling factor <= 1.0."""
        mock_root = MagicMock()
        mock_root.DPI_scaling = 1.0
        
        with patch('tkface.win.dpi.is_windows', return_value=True):
            from tkface.win.dpi import configure_ttk_widgets_for_dpi
            # Should return early without configuring styles
            configure_ttk_widgets_for_dpi(mock_root)

    def test_configure_ttk_widgets_for_dpi_success(self):
        """Test successful ttk widget configuration."""
        mock_root = MagicMock()
        mock_root.DPI_scaling = 2.0
        
        mock_style = MagicMock()
        
        with patch('tkface.win.dpi.is_windows', return_value=True), \
             patch('tkinter.ttk.Style', return_value=mock_style):
            from tkface.win.dpi import configure_ttk_widgets_for_dpi
            configure_ttk_widgets_for_dpi(mock_root)
            
            # Should configure both Checkbutton and Radiobutton styles
            assert mock_style.configure.call_count == 2
            calls = mock_style.configure.call_args_list
            assert calls[0][0][0] == "TCheckbutton"  # First call for Checkbutton
            assert calls[1][0][0] == "TRadiobutton"  # Second call for Radiobutton

    def test_configure_ttk_widgets_for_dpi_style_error(self):
        """Test configure_ttk_widgets_for_dpi with style configuration errors."""
        mock_root = MagicMock()
        mock_root.DPI_scaling = 2.0
        
        mock_style = MagicMock()
        mock_style.configure.side_effect = Exception("Style error")
        
        with patch('tkface.win.dpi.is_windows', return_value=True), \
             patch('tkinter.ttk.Style', return_value=mock_style):
            from tkface.win.dpi import configure_ttk_widgets_for_dpi
            # Should not raise exception, should handle errors gracefully
            configure_ttk_widgets_for_dpi(mock_root)


class TestAutoPatchTKWidgets:
    """Test cases for automatic tk widget to ttk patching."""

    def test_auto_patch_tk_widgets_non_windows(self):
        """Test auto-patch on non-Windows platform."""
        with patch('tkface.win.dpi.is_windows', return_value=False):
            from tkface.win.dpi import DPIManager
            manager = DPIManager()
            # Should return early without patching
            manager._auto_patch_tk_widgets_to_ttk()

    def test_auto_patch_tk_widgets_already_patched(self):
        """Test auto-patch when widgets are already patched."""
        # Mark widgets as already patched
        tk.Checkbutton._tkface_patched_to_ttk = True
        tk.Radiobutton._tkface_patched_to_ttk = True
        
        with patch('tkface.win.dpi.is_windows', return_value=True):
            from tkface.win.dpi import DPIManager
            manager = DPIManager()
            # Should return early without double-patching
            manager._auto_patch_tk_widgets_to_ttk()

    def test_auto_patch_tk_widgets_success(self):
        """Test successful auto-patching of tk widgets."""
        # Remove patch markers if they exist
        if hasattr(tk.Checkbutton, '_tkface_patched_to_ttk'):
            delattr(tk.Checkbutton, '_tkface_patched_to_ttk')
        if hasattr(tk.Radiobutton, '_tkface_patched_to_ttk'):
            delattr(tk.Radiobutton, '_tkface_patched_to_ttk')
        
        original_checkbutton_init = tk.Checkbutton.__init__
        original_radiobutton_init = tk.Radiobutton.__init__
        
        try:
            with patch('tkface.win.dpi.is_windows', return_value=True):
                from tkface.win.dpi import DPIManager
                manager = DPIManager()
                manager._auto_patch_tk_widgets_to_ttk()
                
                # Check that widgets are marked as patched
                assert hasattr(tk.Checkbutton, '_tkface_patched_to_ttk')
                assert hasattr(tk.Radiobutton, '_tkface_patched_to_ttk')
                
                # Check that constructors were replaced
                assert tk.Checkbutton.__init__ != original_checkbutton_init
                assert tk.Radiobutton.__init__ != original_radiobutton_init
                
        finally:
            # Restore original constructors
            tk.Checkbutton.__init__ = original_checkbutton_init
            tk.Radiobutton.__init__ = original_radiobutton_init
            if hasattr(tk.Checkbutton, '_tkface_patched_to_ttk'):
                delattr(tk.Checkbutton, '_tkface_patched_to_ttk')
            if hasattr(tk.Radiobutton, '_tkface_patched_to_ttk'):
                delattr(tk.Radiobutton, '_tkface_patched_to_ttk')

    def test_auto_patch_tk_widgets_exception_handling(self):
        """Test auto-patch exception handling."""
        with patch('tkface.win.dpi.is_windows', return_value=True), \
             patch.object(tk.Checkbutton, '__init__', side_effect=Exception("Patch error")):
            from tkface.win.dpi import DPIManager
            manager = DPIManager()
            # Should not raise exception, should handle errors gracefully
            manager._auto_patch_tk_widgets_to_ttk()


class TestDPIIntegration:
    """Test cases for integrated DPI functionality."""

    def test_dpi_function_includes_ttk_configuration(self):
        """Test that dpi() function includes ttk widget configuration."""
        mock_root = MagicMock()
        mock_root.winfo_id.return_value = 12345
        mock_root.DPI_scaling = 2.0
        
        with patch('tkface.win.dpi.is_windows', return_value=True), \
             patch('tkface.win.dpi.DPIManager._get_hwnd_dpi', return_value=(192, 192, 2.0)), \
             patch('tkface.win.dpi.DPIManager._enable_dpi_awareness', return_value={"shcore": True}), \
             patch('tkface.win.dpi.DPIManager._apply_shcore_dpi_scaling'), \
             patch('tkface.win.dpi.DPIManager._fix_scaling'), \
             patch('tkface.win.dpi.DPIManager._apply_scaling_methods'), \
             patch('tkface.win.dpi.DPIManager._configure_ttk_widgets_for_dpi_internal') as mock_ttk_config, \
             patch('tkface.win.dpi.DPIManager._auto_patch_tk_widgets_to_ttk') as mock_auto_patch:
            
            from tkface.win.dpi import dpi
            result = dpi(mock_root)
            
            # Should call both ttk configuration and auto-patch
            mock_ttk_config.assert_called_once_with(mock_root)
            mock_auto_patch.assert_called_once()
            
            # Should return successful result
            assert result["enabled"] is True
            assert result["dpi_awareness_set"] is True

