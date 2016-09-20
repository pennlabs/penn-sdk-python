from bs4 import BeautifulSoup
import requests
import re

ALL_URL = 'https://www.laundryalert.com/cgi-bin/penn6389/LMPage?Login=True'
HALL_BASE_URL = 'https://www.laundryalert.com/cgi-bin/penn6389/LMRoom?Halls='


class Laundry(object):
    """The client for Laundry. Used to make requests to the API.

    Usage::

      >>> from penn import Laundry
      >>> l = Laundry()
    """

    def __init__(self):
        pass

    @staticmethod
    def get_hall_no(href):
        return int(re.search(r"Halls=(\d+)", href).group(1))

    def all_status(self):
        """Return names, hall numbers, and the washers/dryers available for all
        rooms in the system

        >>> all_laundry = l.all_status()
        """
        r = requests.get(ALL_URL)
        r.raise_for_status()

        parsed = BeautifulSoup(r.text, 'html5lib')
        info_table = parsed.find_all('table')[2]

        # This bit of code generates a dict of hallname->hall number by
        # parsing the link href of each room
        hall_dict = {}
        for link in info_table.find_all('a', class_='buttlink'):
            clean_link = link.get_text().strip()
            hall_dict[clean_link] = self.get_hall_no(link.get('href'))

        # Parse the table into the relevant data
        data = []
        for row in info_table.find_all('tr'):
            row_data = (val.get_text().strip() for val in row.find_all('td'))
            clean_row = [val for val in row_data if len(val) > 0]
            data.append(clean_row)

        # Remove the header row, service row, and all empty rows
        data_improved = [row for row in data if len(row) > 0][1:]

        # Construct the final JSON
        laundry_rooms = []
        for row in data_improved:
            try:
                room_dict = dict()
                room_dict['washers_available'] = int(row[1])
                room_dict['dryers_available'] = int(row[2])
                room_dict['washers_in_use'] = int(row[3])
                room_dict['dryers_in_use'] = int(row[4])
                room_dict['hall_no'] = hall_dict[row[0]]
                room_dict['name'] = row[0]
                laundry_rooms.append(room_dict)
            except ValueError:
                # TODO: Log that row has been skipped
                # Current exceptions are the title row, warnings, and halls
                # without washers and have placeholders (looking at you, New
                # College House)
                pass
        return laundry_rooms

    def hall_status(self, hall_no):
        """Return the status of each specific washer/dryer in a particular
        laundry room.

        :param hall_no:
             integer corresponding to the id number for the hall. Thus number
             is returned as part of the all_status call.

        >>> english_house = l.hall_status(2)
        """
        try:
            num = int(hall_no)
        except ValueError:
            raise ValueError("Room Number must be integer")

        r = requests.get(HALL_BASE_URL + str(num))
        r.raise_for_status()

        parsed = BeautifulSoup(r.text, 'html5lib')
        tables = parsed.find_all('table')
        hall_name = tables[2].get_text().strip()
        info_table = tables[4]

        # Parse the table into the relevant data
        data = []
        for row in info_table.find_all('tr'):
            row_data = (val.get_text().strip() for val in row.find_all('td'))
            clean_row = [val for val in row_data if len(val) > 0]
            data.append(clean_row)

        # Remove the header row and all empty rows
        data_improved = [row for row in data if len(row) > 0][1:]

        def toDict(data_row):
            d = dict()
            d['number'] = data_row[0]
            d['machine_type'] = data_row[1]
            d['available'] = data_row[2] == u'Available'
            if len(data_row) == 4:
                d['time_left'] = data_row[3]
            else:
                d['time_left'] = None
            return d

        return {'machines': list(map(toDict, data_improved)), 'hall_name': hall_name}
