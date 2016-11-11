from bs4 import BeautifulSoup
import requests
import datetime


BASE_URL = "http://www.upenn.edu/almanac/3yearcal.html"


class Calendar(object):
    def __init__(self):
        pass

    def pull():
        '''Returns a list containing all the events from the 3 year calendar.

        Each element of the list is formatted as follows:
        [ <event name>, <year 1 date range>, <year 2 date range>, <year 3 date range> ]
        '''
        l = []
        soup = BeautifulSoup(requests.get(BASE_URL).text, 'html5lib')
        raw_calendar = soup.find_all('tbody')[16]
        events = raw_calendar.find_all('tr')[1:-1]
        for event in events:
            if str(event['class'][0]) == 'bodytext':
                dates = event.find_all('td')
                dates_across_years = []
                key = list(dates[0].descendants)[-1].encode('utf-8').strip()
                for date in dates[2:]:
                    value = list(date.descendants)[-1].encode('utf-8').strip()
                    print value
                    dates_across_years.append(value)
                l.append([key] + list(dates_across_years))
        return l



