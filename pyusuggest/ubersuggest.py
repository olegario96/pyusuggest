from .exceptions import GoogleAttributeError
from .exceptions import LookupNotExecuted
from .exceptions import NoKeyWordSupplied

import csv
import json
import requests

class Ubersuggest(object):
    """
        Ubersuggest implements a class that do requests to the service
    """
    #: The default locale in the class
    DEFAULT_LOCALE = 'en-us'
    #: Amount of results to be returned when query finishes.
    DEFAULT_RESULTS = 50
    #: URL target to send the request. Already pre-formatted
    QUERY_URL = 'https://dk1ecw0kik.execute-api.us-east-1.amazonaws.com/prod/query?query={}&language={}&country={}&google=http://www.google.com&service=i'
    #: Target area of the query. This options came from the own Ubersuggest
    #: tool.
    AREA = {
        'web':      'Web',
        'image':    'Image',
        'shopping': 'Shopping',
        'youtube':  'Youtube',
        'news':     'News',
    }

    def __init__(self, keyword, area=AREA['web'], locale=DEFAULT_LOCALE):
        """
            Create a class with necessary params to use Ubersuggest service
            and an attribute to store the result of the query
        """
        self.keyword = keyword
        self.area = area
        self.language = self.get_language_from_locale(locale)
        self.country = self.get_country_from_locale(locale)
        self.google_keyword_planner = True
        self.google_suggest = True
        self.results = ''

    def set_keyword(self, keyword):
        """
          Set a new keyword for current instance. Will be used in the next call
          of look_up method.
        """
        self.keyword = keyword

    def set_locale(self, locale=DEFAULT_LOCALE):
        """
            Set a new locale for current instance. Must follow the padron en-us
        """
        self.language = self.get_language_from_locale(locale)
        self.country = self.get_country_from_locale(locale)

    def set_area(self, area=AREA['web']):
        """
            Set a new target area for the query. Other options can be checked
            at the top of the file.
        """
        self.area = area

    def set_google_keyword_planner(self, boolean=True):
        """
            Set if query result must bring google keyword planner or not.
        """
        self.google_keyword_planner = boolean

    def set_google_suggest(self, boolean=True):
        """
            Set if query result must bring google suggestions or not.
        """
        self.google_suggest = boolean

    def get_volume(self):
        """
            Get the number of searches about the current keyword. This
            method is only available after look_up be triggered.
        """
        if not self.results:
            raise LookupNotExecuted('Can not get volume without executing look up')

        for key in self.results:
            if key['keyword'] == self.keyword and key['volume']:
                return int(key['volume'])

        return 0

    def get_cpc(self):
        """
            Get the CPC (cost per click) about the current keyword. This
            method is only available after look_up be triggered.
        """
        if not self.results:
            raise LookupNotExecuted('Can not get CPC without executing look up')

        for key in self.results:
            if key['keyword'] == self.keyword and key['cpc']:
                return float(key['cpc'])

        return 0

    def get_competition(self):
        """
            Get the competition value about the current keyword. This
            method is only available after look_up be triggered.
        """
        if not self.results:
            raise LookupNotExecuted('Can not get competition without executing look up')

        for key in self.results:
            if key['keyword'] == self.keyword and key['competition']:
                return float(key['competition'])

        return 0

    def get_language_from_locale(self, locale):
        """
            Returns the language from a locale string
        """
        return locale.lower().split('-')[0]

    def get_country_from_locale(self, locale):
        """
            Returns the country from a locale string
        """
        return locale.lower().split('-')[1]

    def look_up(self, results=DEFAULT_RESULTS):
        """
            Triggers the request for the Ubersuggest tool. At least, one google
            attribute must be set as True. Will format the query url and will
            return the results with same amount as passed as param. If the
            length of the results is less than the results param, so all
            results will be returned.
        """
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

    def filter_results(self, filters):
        """
            Filter current results with new keywords. This method is only available
            after look_up be triggered.
        """
        if not self.results:
            raise LookupNotExecuted('Can not filter results without executing look up')

        new_results = []
        for filter in filters:
            for key in self.results:
                if filter in key['keyword']:
                    new_results.append(key)

        return new_results

    def filter_with_negative_keywords(self, negative_keywords):
        """
            Filter current results with keywords that must not be in the results.
            This method is only available after look_up be triggered.
        """
        if not self.results:
            raise LookupNotExecuted('Can not filter negative keywords without executing look up')

        new_results = []
        for keyword in negative_keywords:
            for key in self.results:
                if not keyword in key['keyword']:
                    new_results.append(key)

        return new_results

    def download_as_csv(self):
        """
            Create a csv file on the current path with data returned by the
            query. This method is only available after look_up be triggered.
        """
        if not self.results:
            raise LookupNotExecuted('Can not create csv file without executing look up')

        row = []
        header = ['Keyword', 'Search Volume', 'CPC', 'Competition']
        csv_file = open('ubersuggest_' + self.keyword + '.csv', 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Keyword', 'Search Volume', 'CPC', 'Competition'])
        for result in self.results:
            row = [result['keyword'], result['volume'], result['cpc'], result['competition']]
            csv_writer.writerow(row)
