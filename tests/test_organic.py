"""Test single word special case: organic."""
from itranslate import itranslate


def test_organic_es():
    """Test organic_es."""
    word = "organic"
    to_lang = "es"
    res = itranslate(word, to_lang=to_lang)
    assert len(res) > 4
