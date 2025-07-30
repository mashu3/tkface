import pytest
import tkface

def test_version_attribute_exists():
    """Test that __version__ attribute exists."""
    assert hasattr(tkface, '__version__')

def test_version_is_string():
    """Test that __version__ is a string."""
    assert isinstance(tkface.__version__, str)

def test_version_format():
    """Test that version follows semantic versioning format."""
    version = tkface.__version__
    # Should be in format x.y.z
    parts = version.split('.')
    assert len(parts) >= 2
    assert all(part.isdigit() for part in parts)

def test_version_matches_pyproject():
    """Test that version matches pyproject.toml."""
    try:
        import toml
        with open('pyproject.toml', 'r') as f:
            pyproject = toml.load(f)
        expected_version = pyproject['project']['version']
        assert tkface.__version__ == expected_version
    except ImportError:
        # Skip this test if toml is not available
        pytest.skip("toml not available")
    except (FileNotFoundError, KeyError):
        # Skip this test if pyproject.toml not found or malformed
        pytest.skip("pyproject.toml not found or malformed")

def test_version_not_empty():
    """Test that version is not empty."""
    assert tkface.__version__.strip() != "" 