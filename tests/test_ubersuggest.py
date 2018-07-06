import os
import pytest
import random

from pyusuggest import Ubersuggest
from pyusuggest import GoogleAttributeError
from pyusuggest import LookupNotExecuted
from pyusuggest import NoKeyWordSupplied

LOCALE_PT_BR = 'pt-br'
KEYWORD = 'algorithm'
FILTER = 'java'

@pytest.fixture(scope='session')
def ubersuggest():
    ubersuggest = Ubersuggest(KEYWORD)
    return ubersuggest

def test_default_result(ubersuggest):
    assert ubersuggest.results == ''

def test_keyword(ubersuggest):
    assert ubersuggest.keyword == KEYWORD

def test_default_google_keyword_planner(ubersuggest):
    assert ubersuggest.google_keyword_planner == True

def test_default_google_suggest(ubersuggest):
    assert ubersuggest.google_suggest == True

def test_default_area(ubersuggest):
    assert ubersuggest.area == Ubersuggest.AREA['web']

def test_default_language(ubersuggest):
    assert ubersuggest.language == 'en'

def test_default_country(ubersuggest):
    assert ubersuggest.country == 'us'

def test_get_language_from_locale(ubersuggest):
    language = ubersuggest.get_language_from_locale(LOCALE_PT_BR)
    assert language == 'pt'

def test_get_country_from_locale(ubersuggest):
    country = ubersuggest.get_country_from_locale(LOCALE_PT_BR)
    assert country == 'br'

def test_set_locale(ubersuggest):
    ubersuggest.set_locale(LOCALE_PT_BR)
    assert ubersuggest.language == 'pt'
    assert ubersuggest.country == 'br'

def test_set_keyword(ubersuggest):
    ubersuggest.set_keyword('software')
    assert ubersuggest.keyword == 'software'

def test_set_area(ubersuggest):
    ubersuggest.set_area(Ubersuggest.AREA['youtube'])
    ubersuggest.area == Ubersuggest.AREA['youtube']

def test_set_google_keyword_planner(ubersuggest):
    ubersuggest.set_google_keyword_planner(False)
    ubersuggest.google_keyword_planner == False

def test_set_google_suggest(ubersuggest):
    ubersuggest.set_google_suggest(False)
    ubersuggest.google_suggest == False

def test_google_attribute_exception(ubersuggest):
    ubersuggest.set_google_keyword_planner(False)
    ubersuggest.set_google_suggest(False)
    with pytest.raises(GoogleAttributeError) as e:
        ubersuggest.look_up()
    assert str(e.value) == 'At least, one of Google options must be set as True'

def test_keyword_exception(ubersuggest):
    ubersuggest.set_google_keyword_planner(True)
    ubersuggest.set_google_suggest(True)
    ubersuggest.keyword = ''
    with pytest.raises(NoKeyWordSupplied) as e:
        ubersuggest.look_up()
    assert str(e.value) == 'A keyword or phrase must be supplied'

def test_look_up_exception_not_executed_on_volume(ubersuggest):
    with pytest.raises(LookupNotExecuted) as e:
        ubersuggest.get_volume()
    assert str(e.value) == 'Can not get volume without executing look up'

def test_look_up_exception_not_executed_on_cpc(ubersuggest):
    with pytest.raises(LookupNotExecuted) as e:
        ubersuggest.get_cpc()
    assert str(e.value) == 'Can not get CPC without executing look up'

def test_look_up_exception_not_executed_on_cpc(ubersuggest):
    with pytest.raises(LookupNotExecuted) as e:
        ubersuggest.get_competition()
    assert str(e.value) == 'Can not get competition without executing look up'

def test_look_up_exception_not_executed_on_filter(ubersuggest):
    with pytest.raises(LookupNotExecuted) as e:
        ubersuggest.filter_results(FILTER)
    assert str(e.value) == 'Can not filter results without executing look up'

def test_look_up_exception_not_executed_on_negative(ubersuggest):
    with pytest.raises(LookupNotExecuted) as e:
        ubersuggest.filter_with_negative_keywords(FILTER)
    assert str(e.value) == 'Can not filter negative keywords without executing look up'

def test_look_up_exception_not_executed_on_csv(ubersuggest):
    with pytest.raises(LookupNotExecuted) as e:
        ubersuggest.download_as_csv()
    assert str(e.value) == 'Can not create csv file without executing look up'

def test_look_up(ubersuggest):
    ubersuggest.set_google_keyword_planner(True)
    ubersuggest.set_google_suggest(True)
    ubersuggest.set_locale('en-us')
    ubersuggest.set_keyword(KEYWORD)
    assert len(ubersuggest.look_up()) == Ubersuggest.DEFAULT_RESULTS

def test_look_up_with_big_result(ubersuggest):
    assert len(ubersuggest.look_up(99999999)) == len(ubersuggest.results)

def test_get_volume(ubersuggest):
    assert ubersuggest.get_volume() == 90500

def test_get_cpc(ubersuggest):
    assert ubersuggest.get_cpc() == 0.07

def test_get_competition(ubersuggest):
    assert ubersuggest.get_competition() == 0.02

def test_download_as_csv(ubersuggest):
    ubersuggest.download_as_csv()
    assert os.path.isfile('./ubersuggest_' + KEYWORD + '.csv') == True

def test_filter_results(ubersuggest):
    results = ubersuggest.filter_results([FILTER])
    assert (FILTER in random.choice(results)['keyword']) == True

def test_filter_with_negative_keywords(ubersuggest):
    results = ubersuggest.filter_with_negative_keywords([FILTER])
    assert (FILTER in random.choice(results)['keyword']) == False

def test_volume_not_found_message(ubersuggest):
    ubersuggest.set_keyword('gigantic search that wont find nothing')
    ubersuggest.look_up()
    assert ubersuggest.get_volume() == 0

def test_cpc_not_found_message(ubersuggest):
    assert ubersuggest.get_cpc() == 0

def test_competition_not_found_message(ubersuggest):
    assert ubersuggest.get_competition() == 0

