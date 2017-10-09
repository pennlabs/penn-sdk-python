import re
import requests
import urllib2
from bs4 import BeautifulSoup

ALL_URL = 'http://suds.kite.upenn.edu/'
USAGE_BASE_URL = 'https://www.laundryalert.com/cgi-bin/penn6389/LMRoomUsage?CallingPage=LMRoom&Password=penn6389&Halls='


class Laundry(object):
    """The client for Laundry. Used to make requests to the API.

    Usage::

      >>> from penn import Laundry
      >>> l = Laundry()
    """

    def __init__(self):
        self.busy_dict = {
            'LowBusyNightColor': 'Low',
            'LowBusyDayColor': 'Low',
            'MediumLowBusyColor': 'Medium',
            'MediumHighBusyColor': 'High',
            'HighBusyColor': 'Very High',
            'NoDataBusyColor': 'No Data'
        }
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                     'Saturday', 'Sunday']
        self.hall_to_link = {}
        self.create_hall_to_link_mapping()

    def create_hall_to_link_mapping(self):
        """
        :return: Mapping from hall name to associated link in SUDS.
        """
        r = requests.get(ALL_URL)
        r.raise_for_status()

        parsed = BeautifulSoup(r.text, 'html5lib')
        halls = parsed.find_all('h2')
        for hall in halls:
            self.hall_to_link[hall.contents[0].string] = ALL_URL + hall.contents[0]['href']

    @staticmethod
    def update_machine_object(cols, machine_object):
        if cols[2].getText() == "In use" or cols[2].getText() == "Almost done":
            machine_object["running"] += 1
            time_remaining = cols[3].getText().split(" ")[0]
            machine_object["time_remaining"].append(time_remaining)

        elif cols[2].getText() == "Out of order":
            machine_object["out_of_order"] += 1
        elif cols[2].getText() == "Not online":
            machine_object["offline"] += 1
        else:
            machine_object["open"] += 1
        return machine_object

    def parse_a_hall(self, hall):
        if hall not in self.hall_to_link:
            return None  # change to to empty json idk
        page = requests.get(self.hall_to_link[hall])
        soup = BeautifulSoup(page.content, 'html.parser')
        soup.prettify()
        washers = {"open": 0, "running": 0, "out_of_order": 0, "offline": 0, "time_remaining": []}
        dryers = {"open": 0, "running": 0, "out_of_order": 0, "offline": 0, "time_remaining": []}

        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 1:
                machine_type = cols[1].getText()
                if machine_type == "Washer":
                    washers = Laundry.update_machine_object(cols, washers)
                else:
                    dryers = Laundry.update_machine_object(cols, dryers)

        machines = {"Washers": washers, "Dryers": dryers}
        return machines

    @staticmethod
    def get_hall_no(href):
        return int(re.search(r"Halls=(\d+)", href).group(1))

    def all_status(self):
        """Return names, hall numbers, and the washers/dryers available for all
        rooms in the system

        >>> all_laundry = l.all_status()
        """
        laundry_rooms = {}
        for room in self.hall_to_link:
            laundry_rooms[room] = self.parse_a_hall(room)

        return laundry_rooms

    def hall_status(self, hall_name):
        """Return the status of each specific washer/dryer in a particular
        laundry room.

        :param hall_name:
             Unescaped string corresponding to the name of the hall hall. This name
             is returned as part of the all_status call.

        >>> english_house = l.hall_status("English%20House")
        """
        machines = self.parse_a_hall((urllib2.unquote(hall_name)))

        return {
            'machines': machines,
            'hall_name': hall_name
        }

    def machine_usage(self, hall_no):
        """Returns the average usage of laundry machines every hour
        for a given hall.

        The usages are returned in a dictionary, with the key being
        the day of the week, and the value being an array listing the usages
        per hour.

        :param hall_no:
             integer corresponding to the id number for the hall. Thus number
             is returned as part of the all_status call.

        >>> english_house = l.machine_usage(2)
        """

        try:
            num = int(hall_no)
        except ValueError:
            raise ValueError("Room Number must be integer")
        r = requests.get(USAGE_BASE_URL + str(num))
        parsed = BeautifulSoup(r.text, 'html5lib')
        usage_table = parsed.find_all('table', width='504px')[0]
        rows = usage_table.find_all('tr')
        usages = {}
        for i, row in enumerate(rows):
            day = []
            hours = row.find_all('td')
            for hour in hours:
                day.append(self.busy_dict[str(hour['class'][0])])
            usages[self.days[i]] = day
        return usages


# if __name__ == "__main__":
#     l = Laundry()
#     l.create_hall_to_link_mapping()
#     print(l.hall_status("English%20House"))
