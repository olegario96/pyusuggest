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
    QUERY_URL = 'https://dk1ecw0kik.execute-api.us-east-1.amazonaws.com/prod/query?query={}&language=' + \
                '{}&country={}&google=http://www.google.com&service=i'

    def __init__(self, keyword, locale=DEFAULT_LOCALE):
        """
            Create a class with necessary params to use Ubersuggest service
            and an attribute to store the result of the query
        """
        self.keyword = keyword
        self.language = self.get_language_from_locale(locale)
        self.country = self.get_country_from_locale(locale)
        self.results = ''
        self.related_words = []

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

    def get_volume(self):
        """
            Get the number of searches about the current keyword. This
            method is only available after look_up be triggered.
        """
        if not self.results:
            raise LookupNotExecuted('Can not get volume without executing look up')

        for key in self.results:
            if key.get('keyword') == self.keyword and key.get('volume'):
                return int(key.get('volume'))

        return 0

    def get_cpc(self):
        """
            Get the CPC (cost per click) about the current keyword. This
            method is only available after look_up be triggered.
        """
        if not self.results:
            raise LookupNotExecuted('Can not get CPC without executing look up')

        for key in self.results:
            if key.get('keyword') == self.keyword and key.get('cpc'):
                return float(key.get('cpc'))

        return 0

    def get_competition(self):
        """
            Get the competition value about the current keyword. This
            method is only available after look_up be triggered.
        """
        if not self.results:
            raise LookupNotExecuted('Can not get competition without executing look up')

        for key in self.results:
            if key.get('keyword') == self.keyword and key.get('competition'):
                return float(key.get('competition'))

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

        if not self.keyword:
            raise NoKeyWordSupplied("A keyword must be supplied")

        url_formatted = Ubersuggest.QUERY_URL.format(self.keyword, self.language, self.country)
        json_result = json.loads(requests.get(url_formatted).text)
        self.results = json_result.get('results').get('processed_keywords')
        self.related_results = json_result.get('results').get('unprocessed_keywords')
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
                if filter in key.get('keyword'):
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
                if not keyword in key.get('keyword'):
                    new_results.append(key)

        return new_results

    def related_results(self):
        """
            Get words related to the search that are marked as "unprocessed_keywords"
            in the JSON.
        """
        return self.related_results

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
