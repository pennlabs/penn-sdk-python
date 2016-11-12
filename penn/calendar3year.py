import requests
import datetime


BASE_URL = "https://www.google.com/calendar/ical/pennalmanac@gmail.com/public/basic.ics"


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
        """Returns a list (in JSON format) containing all the events from the Penn iCal Calendar.

        List contains events in chronological order.

        Each element of the list is a dictionary, containing:
            - Name of the event 'name'
            - Start date 'start'
            - End date 'end'
        """
        events = []
        r = requests.get(BASE_URL).text
        l = r.split("\r\n")
        d = {}
        for line in l:
            if line == "BEGIN:VEVENT":
                d = {}
            elif line[:7] == "DTSTART":
                raw_date = line.split(":")[1]
                start_date = datetime.datetime.strptime(raw_date, '%Y%m%d').date()
                d['start'] = start_date
            elif line[:5] == "DTEND":
                raw_date = line.split(":")[1]
                end_date = datetime.datetime.strptime(raw_date,'%Y%m%d').date()
                d['end'] = end_date
            elif line[:7] == "SUMMARY":
                name = line.split(":")[1]
                d['name'] = name.encode('utf-8').strip()
            elif line == "END:VEVENT":
                events.append(d)

        events.sort(key=lambda d: d['start'])
        print events
        return events
