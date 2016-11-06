from bs4 import BeautifulSoup
import requests


BASE_URL = "https://mobile.apps.upenn.edu/mobile/jsp/fast.do?fastStart=academicCalendarPage"


class Calendar(object):
    def __init__(self):
        pass

    def pull(self):
        d = {}
        soup = BeautifulSoup(requests.get(BASE_URL).text, 'html5lib')
        raw_calendar = soup.find_all('table', border='1')[0]
        soup = BeautifulSoup(raw_calendar, 'html5lib')
        events = soup.find_all('tr')[2:-1]
        for event in events:
            soup = BeautifulSoup(event, 'html5lib')
            dates = soup.find_all('td')
            dates_across_years = []
            key = dates[0][5:-5]
            key = BeautifulSoup(key, 'html5lib').a.content
            for date in dates[1:]:
                value = BeautifulSoup(date[5:-5], 'html5lib').a.content
                dates_across_years.append(value)
            d[key] = dates_across_years
        return d