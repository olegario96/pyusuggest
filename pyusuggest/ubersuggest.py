from .exceptions import GoogleAttributeError
from .exceptions import LookupNotExecuted
from .exceptions import NoKeyWordSupplied

import json
import requests

class Ubersuggest(object):
    DEFAULT_LOCALE = 'en-us'
    DEFAULT_RESULTS = 50
    QUERY_URL = 'https://dk1ecw0kik.execute-api.us-east-1.amazonaws.com/prod/query?query={}&language={}&country={}&google=http://www.google.com&service=i'

    AREA = {
        'web':      'Web',
        'image':    'Image',
        'shopping': 'Shopping',
        'youtube':  'Youtube',
        'news':     'News',
    }

    def __init__(self, keyword, area=AREA['web'], locale=DEFAULT_LOCALE):
        self.keyword = keyword
        self.area = area
        self.language = self.get_language_from_locale(locale)
        self.country = self.get_country_from_locale(locale)
        self.google_keyword_planner = True
        self.google_suggest = True
        self.results = ''

    def set_keyword(self, keyword):
        self.keyword = keyword

    def set_locale(self, locale=DEFAULT_LOCALE):
        self.language = self.get_language_from_locale(locale)
        self.country = self.get_country_from_locale(locale)

    def set_area(self, area=AREA['web']):
        self.area = area

    def set_google_keyword_planner(self, boolean=True):
        self.google_keyword_planner = boolean

    def set_google_suggest(self, boolean=True):
        self.google_suggest = boolean

    def get_volume(self):
        if not self.results:
            raise LookupNotExecuted('Can not get volume without executing look up')

        for key in self.results:
            if key['keyword'] == self.keyword and key['volume']:
                return int(key['volume'])

        return 'Ubersuggest could not return volume for this keyword'

    def get_cpc(self):
        if not self.results:
            raise LookupNotExecuted('Can not get CPC without executing look up')

        for key in self.results:
            if key['keyword'] == self.keyword and key['cpc']:
                return float(key['cpc'])

        return 'Ubersuggest could not return CPC for this keyword'

    def get_competition(self):
        if not self.results:
            raise LookupNotExecuted('Can not get competition without executing look up')

        for key in self.results:
            if key['keyword'] == self.keyword and key['competition']:
                return float(key['competition'])

        return 'Ubersuggest could not return competition for this keyword'

    def get_language_from_locale(self, locale):
        return locale.split('-')[0]

    def get_country_from_locale(self, locale):
        return locale.split('-')[1]

    def look_up(self, results=DEFAULT_RESULTS):
        if not self.google_keyword_planner and not self.google_suggest:
            raise GoogleAttributeError('At least, one of Google options must be set as True')

        if not self.keyword:
            raise NoKeyWordSupplied('A keyword or phrase must be supplied')

        url_formatted = Ubersuggest.QUERY_URL.format(self.keyword, self.language, self.country)
        self.results = json.loads(requests.get(url_formatted).text)['results']['processed_keywords']
        if results >= len(self.results):
            return self.results
        else:
            return self.results[:results]

