import requests
import datetime


BASE_URL = "https://www.stanza.co/api/schedules/almanacacademiccalendar/"


class Calendar(object):
    def __init__(self):
        pass

    def pull_3year(self):
        """Returns a list (in JSON format) containing all the events from the Penn iCal Calendar.

        List contains events in chronological order.

        Each element of the list is a dictionary, containing:
            - Name of the event 'name'
            - Start date 'start'
            - End date 'end'
        """
        events = []
        for term in ["fall", "summer", "spring"]:
            url = "{}{}{}term.ics".format(BASE_URL, datetime.datetime.now().year, term)
            resp = requests.get(url)
            resp.raise_for_status()
            r = resp.text
            lines = r.split("\n")
            d = {}
            for line in lines:
                if line == "BEGIN:VEVENT":
                    d = {}
                elif line.startswith("DTSTART"):
                    raw_date = line.split(":")[1]
                    start_date = datetime.datetime.strptime(raw_date, '%Y%m%d').date()
                    d['start'] = start_date.strftime('%Y-%m-%d')
                elif line.startswith("DTEND"):
                    raw_date = line.split(":")[1]
                    end_date = datetime.datetime.strptime(raw_date, '%Y%m%d').date()
                    d['end'] = end_date.strftime('%Y-%m-%d')
                elif line.startswith("SUMMARY"):
                    name = line.split(":")[1]
                    d['name'] = str(name).strip()
                elif line == "END:VEVENT":
                    events.append(d)

        events.sort(key=lambda d: d['start'])
        return events
