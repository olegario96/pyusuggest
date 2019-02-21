import os
import pytest
import random

from pyusuggest import Ubersuggest
from pyusuggest import LookupNotExecuted
from pyusuggest import NoKeyWordSupplied
from pyusuggest import TimeOutUbersuggest

LOCALE_PT_BR = 'pt-br'
KEYWORD_ALGORITHM = 'algorithm'
KEYWORD_DATABASES = 'database'
FILTER = 'java'

@pytest.fixture(scope='session')
def ubersuggest():
    ubersuggest = Ubersuggest(KEYWORD_ALGORITHM)
    return ubersuggest

def test_default_result(ubersuggest):
    assert ubersuggest.results == ''

def test_keyword(ubersuggest):
    assert ubersuggest.keyword == KEYWORD_ALGORITHM

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

def test_set_keyword_with_whitespaces(ubersuggest):
    ubersuggest.set_keyword('software development')
    assert ubersuggest.keyword == 'software%20development'

def test_keyword_exception(ubersuggest):
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

def test_look_up_exception_not_executed_on_competition(ubersuggest):
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
        ubersuggest.download_results_as_csv()
    assert str(e.value) == 'Can not create csv file without executing look up'

def test_look_up_exception_not_executed_on_statistics(ubersuggest):
    with pytest.raises(LookupNotExecuted) as e:
        ubersuggest.get_monthly_statistics()
    assert str(e.value) == 'Can not get monthly results without executing look up'

def test_look_up_exception_not_executed_on_statistics_csv(ubersuggest):
    with pytest.raises(LookupNotExecuted) as e:
        ubersuggest.download_monthly_statistics_as_csv()
    assert str(e.value) == 'Can not create csv file without executing look up'

def test_timeout_exception(ubersuggest):
    with pytest.raises(TimeOutUbersuggest) as e:
        ubersuggest.set_keyword(KEYWORD_ALGORITHM)
        ubersuggest.look_up(tries=3)

    assert str(e.value) == 'The server may be offline or too busy right now! Please try again later'

def test_look_up(ubersuggest):
    ubersuggest.set_locale('en-us')
    ubersuggest.set_keyword(KEYWORD_ALGORITHM)
    assert len(ubersuggest.look_up()) == Ubersuggest.DEFAULT_RESULTS

def test_look_up_with_big_result(ubersuggest):
    assert len(ubersuggest.look_up(99999999)) == len(ubersuggest.results)

def test_get_volume(ubersuggest):
    assert ubersuggest.get_volume() == 90500

def test_download_as_csv(ubersuggest):
    ubersuggest.download_results_as_csv()
    assert os.path.isfile('ubersuggest_' + KEYWORD_ALGORITHM + '.csv') == True

def test_download_statistics_as_csv(ubersuggest):
    ubersuggest.download_monthly_statistics_as_csv()
    assert os.path.isfile('ubersuggest_' + KEYWORD_ALGORITHM + '_monthly_statistics.csv') == True

def test_filter_results(ubersuggest):
    results = ubersuggest.filter_results([FILTER])
    assert (FILTER in random.choice(results)['keyword']) == True

def test_filter_with_negative_keywords(ubersuggest):
    results = ubersuggest.filter_with_negative_keywords([FILTER])
    assert (FILTER in random.choice(results)['keyword']) == False

def test_volume_default_return(ubersuggest):
    ubersuggest.set_keyword('gigantic search that wont find nothing')
    ubersuggest.look_up()
    assert ubersuggest.get_volume() == 0

def test_cpc_default_return(ubersuggest):
    assert ubersuggest.get_cpc() == 0

def test_competition_default_return(ubersuggest):
    assert ubersuggest.get_competition() == 0

def test_get_related_results(ubersuggest):
    ubersuggest.set_locale(LOCALE_PT_BR)
    ubersuggest.set_keyword(KEYWORD_DATABASES)
    ubersuggest.look_up()
    unprocessed_keywords = ubersuggest.related_keywords()
    assert ('database analyst' in unprocessed_keywords) == True

def test_get_monthly_statistics(ubersuggest):
    ubersuggest.set_locale(LOCALE_PT_BR)
    ubersuggest.set_keyword(KEYWORD_DATABASES)
    ubersuggest.look_up()
    monthly_statistics = ubersuggest.get_monthly_statistics()
    for keyword in monthly_statistics:
        assert ('year' in monthly_statistics.get(keyword)[0] and \
                'month' in monthly_statistics.get(keyword)[0] and \
                'count' in monthly_statistics.get(keyword)[0]) == True
