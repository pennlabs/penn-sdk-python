from bs4 import BeautifulSoup
import requests
import datetime


BASE_URL = "http://www.upenn.edu/almanac/3yearcal.html"


class Calendar(object):
    def __init__(self):
        pass

    def pull(self):
        '''Returns a list containing all the events from the 3 year calendar.

        Each element of the list is formatted as follows:
        [ <event name>, <year 1 date range>, <year 2 date range>, <year 3 date range> ]
        '''
        l = []
        soup = BeautifulSoup(requests.get(BASE_URL).text, 'html5lib')
        title = soup.find_all('p', class_='h2')[0].get_text(strip=True)
        raw_calendar = soup.find_all('tbody')[16]
        events = raw_calendar.find_all('tr')[1:-1]
        for event in events:
            if str(event['class'][0]) == 'bodytext':
                dates = event.find_all('td')
                dates_across_years = []
                key = list(dates[0].descendants)[-1].encode('utf-8').strip()
                for date in dates[2:]:
                    value = list(date.descendants)[-1].encode('utf-8').strip()
                    dates_across_years.append(value)
                l.append([key] + list(dates_across_years))
        return l

    @staticmethod
    def range_parse(self, ran):
        '''Given a date range, returns a start and end date object
        from the datetime module.

        If the event lasts only for a day, the start and end date
        will be the same.
        '''
        # get rid of excess parentheses
        modified = ran.split('(')[0].strip()
        endpoints = modified.split('-')
        start = endpoints[0]
        start_date = datetime.datetime.strptime(start, '%B %d').date()
        if len(endpoints) == 1:
            return [start_date, start_date]
        end = endpoints[1]
        # two cases to consider, month or no month present
        try:
            end_date = datetime.datetime.strptime(end, '%B %d').date()
        except ValueError:
            month = start_date.month
            end_date = datetime.date(1900, month, int(end))
        return [start_date, end_date]

    @staticmethod
    def title_parse(self, title):
        '''Parses the title of the calendar to determine
        the current year range.'''

        ranges = title.split('-')
        return [int(ranges[0]), int(ranges[2])]
