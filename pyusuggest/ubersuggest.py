from .exceptions import LookupNotExecuted
from .exceptions import NoKeyWordSupplied
from .exceptions import TimeOutUbersuggest

import csv
import json
import os
import requests

class Ubersuggest(object):
    """
        TODO
    """
    #: The default locale in the class
    DEFAULT_LOCALE = 'en-us'
    #: Amount of results to be returned when query finishes.
    DEFAULT_RESULTS = 50
    # Period to track keyword in last months
    DEFAULT_PERIOD = 'ALL'
    #: URL target to send the request. Already pre-formatted
    QUERY_URL = 'https://dk1ecw0kik.execute-api.us-east-1.amazonaws.com/prod/query?query={}&language=' + \
                '{}&country={}&google=http://www.google.com&service=i'

    # Path to current working directory
    PWD = os.getcwd()

    def __init__(self, keyword, locale=DEFAULT_LOCALE):
        """
            Create a class with necessary params to use Ubersuggest service
            and an attribute to store the result of the query
        """
        self.keyword = keyword
        self.language = self.get_language_from_locale(locale)
        self.country = self.get_country_from_locale(locale)
        self.results = ''
        self.unprocessed_keywords = []

    def set_keyword(self, keyword):
        """
          Set a new keyword for current instance. Will be used in the next call
          of look_up method.
        """
        if ' ' in keyword:
            keyword = '%20'.join(keyword.split())
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

    def look_up(self, results=DEFAULT_RESULTS, tries=0):
        """
            Triggers the request for the Ubersuggest tool. At least, one google
            attribute must be set as True. Will format the query url and will
            return the results with same amount as passed as param. If the
            length of the results is less than the results param, so all
            results will be returned. The request is inside a while loop, because
            sometimes the server may respond with a message saying that the
            request timed out. After 3 attempts, if it was not possible
            query the url, an exception will be throw. The tries param is used
            for test only.
        """
        if not self.keyword:
            raise NoKeyWordSupplied('A keyword or phrase must be supplied')

        url_formatted = Ubersuggest.QUERY_URL.format(self.keyword, self.language, self.country)
        success = False

        while (tries < 3 and not success):
            res = requests.get(url_formatted).text
            if not json.loads(res).get('message') == 'Endpoint request timed out':
                success = True
            tries += 1

        if success:
            json_result = json.loads(res)
            self.results = json_result.get('results').get('processed_keywords')
            self.unprocessed_keywords = json_result.get('results').get('unprocessed_keywords')
            if results >= len(self.results):
                return self.results
            else:
                return self.results[:results]
        elif tries == 3:
            raise TimeOutUbersuggest('The server may be offline or too busy right now! Please try again later')

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

    def related_keywords(self):
        """
            Get words related to the search that are marked as "unprocessed_keywords"
            in the JSON.
        """
        return self.unprocessed_keywords

    def get_monthly_statistics(self, period=DEFAULT_PERIOD):
        """
            Get the monthly statistics for each keyword in last months. This method
            is only available after use the "look_up" is being executed. The period
            passed as argument must be a integer. Will iterate through each keyword
            and get its monthly statistics. If the period is greater than all
            available months, will get all months. Return a dictionary in each
            keyword maps its statistics in a list of dicts format.
        """
        if not self.results:
            raise LookupNotExecuted('Can not get monthly results without executing look up')

        monthly_statistics_per_word = {}
        for result in self.results:
            monthly_statistics = result.get('ms')
            if period == Ubersuggest.DEFAULT_PERIOD or int(period) >= len(monthly_statistics):
                if not monthly_statistics:
                    monthly_statistics_per_word[result.get('keyword')] = []
                else:
                    monthly_statistics_per_word[result.get('keyword')] = monthly_statistics
            else:
                monthly_statistics_per_word[result.get('keyword')] = monthly_statistics[:period]

        return monthly_statistics_per_word

    def download_results_as_csv(self):
        """
            Create a csv file on the current path with data returned by the
            query. This method is only available after look_up be triggered.
        """
        if not self.results:
            raise LookupNotExecuted('Can not create csv file without executing look up')

        row = []
        header = ['Keyword', 'Search Volume', 'CPC', 'Competition']
        csv_file = open(Ubersuggest.PWD + '/ubersuggest_' + self.keyword + '.csv', 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        for result in self.results:
            row = [result['keyword'], result['volume'], result['cpc'], result['competition']]
            csv_writer.writerow(row)

        csv_file.close()

    def download_monthly_statistics_as_csv(self, period=DEFAULT_PERIOD):
        """
            Creates a CSV file in the current working directory with the statistics
            related to each keyword found during the search process. This method
            is only available after the "look_up" method being triggered. The header
            is created using a column for the keyword, year, month and how many
            times that word has been searched.
        """
        if not self.results:
            raise LookupNotExecuted('Can not create csv file without executing look up')

        row = []
        header = ['keyword', 'year', 'month', 'count']
        csv_file = open(Ubersuggest.PWD + '/ubersuggest_' + self.keyword + '_monthly_statistics.csv', 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        monthly_statistics_per_word = self.get_monthly_statistics(period)

        for key in monthly_statistics_per_word:
            for statistic in monthly_statistics_per_word.get(key):
                csv_writer.writerow([key, statistic.get('year'), statistic.get('month'), statistic.get('count')])

        csv_file.close()
