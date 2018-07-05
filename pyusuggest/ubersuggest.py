import requests
import json

class Ubersuggest(object):
    DEFAULT_LOCALE = 'en-us'
    DEFAULT_RESULTS = 50
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

    def set_keyword(self, keyword):
        pass

    def set_locale(self, locale=DEFAULT_LOCALE):
        pass

    def set_area(self, area):
        pass

    def set_google_keyword_planner(self, boolean=True):
        pass

    def set_google_suggest(self, boolean=True):
        pass

    def get_volume(self):
        pass

    def get_cpc(self):
        pass

    def get_competition(self):
        pass

    def get_language_from_locale(self, locale):
        return locale.split('-')[0]

    def get_country_from_locale(self, locale):
        return locale.split('-')[1]

    def look_up(self, results=DEFAULT_RESULTS):
        pass
