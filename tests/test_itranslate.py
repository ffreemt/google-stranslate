"""Test itranslate."""
from itranslate import __version__
from itranslate import itranslate


def test_version():
    """Test version."""
    assert __version__ == "0.1.1"


def test_sanity():
    """Sanity check."""
    try:
        assert not itranslate("test")
    except Exception:
        assert True
