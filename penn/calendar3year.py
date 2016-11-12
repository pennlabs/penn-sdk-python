from bs4 import BeautifulSoup
import requests
import datetime


BASE_URL = "http://www.upenn.edu/almanac/3yearcal.html"


class Calendar(object):
    def __init__(self):
        pass

    @staticmethod
    def title_parse(title):
        """Parses the title of the calendar to determine
        the current year range, to be used in the pull() method.
        Assumes the calendar is of 3 years.

        :param title: pre-formatted title with years
        """

        ranges = title.split('-')
        return [int(ranges[3]) - 3, int(ranges[3])]

    @staticmethod
    def range_parse(ran, year):
        """Given a date range, returns a start and end date object
        from the datetime module.

        If the event lasts only for a day, the start and end date
        will be the same.

        :param ran: raw string with date range, either of the forms:
            1. "<month> <day>-<day>"
            2. "<month> <day>-<month> <day>"
            3. "<month> <day>"
        :param year: integer containing the year
        """

        # get rid of excess parentheses
        modified = ran.split('(')[0].strip()
        endpoints = modified.split('-')
        start = endpoints[0]
        start_date = datetime.datetime.strptime(start + ' ' + str(year), '%B %d %Y').date()
        if len(endpoints) == 1:
            return [start_date, start_date]
        end = endpoints[1]

        # two cases to consider, month or no month present
        try:
            end_date = datetime.datetime.strptime(end + ' ' + str(year), '%B %d %Y').date()
        except ValueError:
            month = start_date.month
            end_date = datetime.date(year, month, int(end))
        return [start_date, end_date]

    def pull_3year(self):
        """Returns a list containing all the events from the 3 year calendar.

        List contains events in chronological order.

        Each element of the list is formatted as follows:
        [ <event name>, <year 1 date range>, <year 2 date range>, <year 3 date range>, <year 1> ]
        """
        l = []
        # year_change shows when the date changes to the next year
        year_change = 0
        summer = 0
        soup = BeautifulSoup(requests.get(BASE_URL).text, 'html5lib')
        title = soup.find_all('p', class_='h2')[0].get_text(strip=True)
        year_range = self.title_parse(title)
        raw_calendar = soup.find_all('tbody')[16]
        events = raw_calendar.find_all('tr')[2:-1]

        for event in events:
            if str(event['class'][0]) == 'bodytext':
                dates = event.find_all('td')
                dates_across_years = []
                key = list(dates[0].descendants)[-1].encode('utf-8').strip()
                # key is the event name
                for date in dates[2 - summer:]:
                    value = list(date.descendants)[-1].encode('utf-8').strip()
                    dates_across_years.append(value)
                l.append([key] + list(dates_across_years) + [year_range[0] + year_change])
            elif year_change != 1 and str(event['class'][0]) == 'rightSideLinkHeadings':
                # account for spring semester
                year_change = 1
            elif year_change == 1:
                # account for summer; table changes format then
                summer = 1

        return l
