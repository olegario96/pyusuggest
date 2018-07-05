import pytest

from pyusuggest import Ubersuggest

@pytest.fixture(scope='session')
def ubersuggest():
    ubersuggest = Ubersuggest('algorithm')
    return ubersuggest

def test_get_language_from_locale(ubersuggest):
    language = ubersuggest.get_language_from_locale(Ubersuggest.DEFAULT_LOCALE)
    assert language == 'en'

def test_get_country_from_locale(ubersuggest):
    country = ubersuggest.get_country_from_locale(Ubersuggest.DEFAULT_LOCALE)
    assert country == 'us'
