import re
import requests
try:
    import urllib2
except:
    import urllib.parse as urlib2
from bs4 import BeautifulSoup

ALL_URL = 'http://suds.kite.upenn.edu/?location='
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
        self.id_to_hall = {}
        self.hall_id_list = []
        self.create_hall_to_link_mapping()

    def create_hall_to_link_mapping(self):
        """
        :return: Mapping from hall name to associated link in SUDS. Creates inverted index from id to hall
        """
        data = {1: {'loc': 'Quad', 'hall': u'Bishop White', 'uuid': u'5faec7e9-a4aa-47c2-a514-950c03fac460'},
                2: {'loc': 'Quad', 'hall': u'Chestnut Butcher', 'uuid': u'7dfa4b34-f44a-4a38-a6b9-44cdb968a915'},
                3: {'loc': 'Quad', 'hall': u'Class of 1928 Fisher', 'uuid': u'e6697dca-d164-4980-8843-ea0a29b1cf49'},
                4: {'loc': 'Quad', 'hall': u'Craig', 'uuid': u'37d661ce-3e50-4746-ab68-a5c61cd0bd0a'},
                5: {'loc': 'DuBois', 'hall': u'DuBois', 'uuid': u'3ffa8978-e742-4076-9bcb-4a3e5c0eca92'},
                6: {'loc': 'KCEH', 'hall': u'English House', 'uuid': u'b655a5be-1287-4ce2-b693-e9c1ae526f38'},
                7: {'loc': 'Harnwell', 'hall': u'Harnwell Floor 02', 'uuid': u'1c7a9fb3-a938-4756-83c6-42d601d46036'},
                8: {'loc': 'Harnwell', 'hall': u'Harnwell Floor 04', 'uuid': u'fba67cc0-336e-42f7-9603-c0b8a0e5030c'},
                9: {'loc': 'Harnwell', 'hall': u'Harnwell Floor 06', 'uuid': u'87195ec7-eb3d-42fd-84aa-d63f4e45e285'},
                10: {'loc': 'Harnwell', 'hall': u'Harnwell Floor 08', 'uuid': u'1bbb2ff6-d5e6-406d-a3a2-96c7972cceeb'},
                11: {'loc': 'Harnwell', 'hall': u'Harnwell Floor 10', 'uuid': u'987bf30b-e8e1-4a9e-b842-c9cd8aeafddc'},
                12: {'loc': 'Harnwell', 'hall': u'Harnwell Floor 12', 'uuid': u'dcb76f10-0137-4783-8604-bece4111b6dd'},
                13: {'loc': 'Harnwell', 'hall': u'Harnwell Floor 14', 'uuid': u'941b2fcb-2b1b-4afd-8e8e-c100fbcbe0f2'},
                14: {'loc': 'Harnwell', 'hall': u'Harnwell Floor 16', 'uuid': u'c74b2798-2d09-42a6-b65c-a5834219be59'},
                15: {'loc': 'Harnwell', 'hall': u'Harnwell Floor 18', 'uuid': u'f30af904-72ad-49f6-aecf-f44c8301fb6b'},
                16: {'loc': 'Harnwell', 'hall': u'Harnwell Floor 20', 'uuid': u'80a413fd-e0fa-456d-b922-f1576ded1f98'},
                17: {'loc': 'Harnwell', 'hall': u'Harnwell Floor 22', 'uuid': u'35119e5e-92c0-45fb-bfeb-f2059196f644'},
                18: {'loc': 'Harnwell', 'hall': u'Harnwell Floor 24', 'uuid': u'5880b051-8216-4cf4-92d6-5c7475f43eea'},
                19: {'loc': 'Harrison', 'hall': u'Harrison Floor 04', 'uuid': u'447b5682-4c3c-441d-ab49-5f45aee6991f'},
                20: {'loc': 'Harrison', 'hall': u'Harrison Floor 06', 'uuid': u'f77f7c68-f719-4843-8987-d64dabc0abff'},
                21: {'loc': 'Harrison', 'hall': u'Harrison Floor 08', 'uuid': u'6561bb14-634f-437d-84fd-a0837ef991e7'},
                22: {'loc': 'Harrison', 'hall': u'Harrison Floor 10', 'uuid': u'2dd7a63d-7d13-48e5-b038-98054b4f039f'},
                23: {'loc': 'Harrison', 'hall': u'Harrison Floor 12', 'uuid': u'fdb607c7-63eb-4d55-a312-0c16b682cbe7'},
                24: {'loc': 'Harrison', 'hall': u'Harrison Floor 14', 'uuid': u'53fdd440-e887-49e1-9ca9-7bb3cb4ab541'},
                25: {'loc': 'Harrison', 'hall': u'Harrison Floor 16', 'uuid': u'8cedf60a-8f87-4128-89dd-4c75343ca64a'},
                26: {'loc': 'Harrison', 'hall': u'Harrison Floor 18', 'uuid': u'116a8d6f-045b-47a5-b3f7-af31f4e661eb'},
                27: {'loc': 'Harrison', 'hall': u'Harrison Floor 20', 'uuid': u'f6a8b303-1302-49e6-be53-c8e345316ed8'},
                28: {'loc': 'Harrison', 'hall': u'Harrison Floor 22', 'uuid': u'b21c78af-1ebf-418c-a73b-85dc5ff49763'},
                29: {'loc': 'Harrison', 'hall': u'Harrison Floor 24', 'uuid': u'9b95c471-053c-46ea-bc3b-d23bcad7a3a1'},
                30: {'loc': 'Hill', 'hall': u'Hill House', 'uuid': u'82a00eb7-f70d-4a4c-9f0a-c2dafa4b67ea'},
                31: {'loc': 'Quad', 'hall': u'Magee Amhurst', 'uuid': u'f6825dac-5a5a-4e4b-b66f-ea8226cbe78e'},
                32: {'loc': 'Stouffer', 'hall': u'Mayer', 'uuid': u'6e3531d1-eebd-48b4-ad04-cf5983d42b02'},
                33: {'loc': 'Quad', 'hall': u'Morgan', 'uuid': u'f249ca9f-ef84-4a35-9477-449b14612057'},
                34: {'loc': 'Rodin', 'hall': u'Rodin Floor 02', 'uuid': u'7f25802d-31ad-4f80-ba26-d68a3f403aa8'},
                35: {'loc': 'Rodin', 'hall': u'Rodin Floor 04', 'uuid': u'49e560fb-c1aa-4c98-a88a-cc9564481ec0'},
                36: {'loc': 'Rodin', 'hall': u'Rodin Floor 06', 'uuid': u'701ce966-aa3c-4063-b3db-548ad89cb643'},
                37: {'loc': 'Rodin', 'hall': u'Rodin Floor 08', 'uuid': u'4998a8a2-fb86-4900-bcb7-9d7cc6d9b938'},
                38: {'loc': 'Rodin', 'hall': u'Rodin Floor 10', 'uuid': u'030c81c4-2300-4e8e-ae3a-303397a2e216'},
                39: {'loc': 'Rodin', 'hall': u'Rodin Floor 12', 'uuid': u'c561f889-5898-41ba-99f5-2e6d4243e4d3'},
                40: {'loc': 'Rodin', 'hall': u'Rodin Floor 14', 'uuid': u'2d211700-5b59-4c61-8922-991c0f7d7c15'},
                41: {'loc': 'Rodin', 'hall': u'Rodin Floor 16', 'uuid': u'a10ede1d-044d-4852-87c7-eba7588c2497'},
                42: {'loc': 'Rodin', 'hall': u'Rodin Floor 18', 'uuid': u'c3d3f9ae-792c-401c-8bd5-8c61fffe2ab1'},
                43: {'loc': 'Rodin', 'hall': u'Rodin Floor 20', 'uuid': u'e88d3561-dce7-4188-89e7-b72cff7d69d6'},
                44: {'loc': 'Rodin', 'hall': u'Rodin Floor 22', 'uuid': u'6b7dcd18-fe4e-4dc2-893f-35f0d7939c3c'},
                45: {'loc': 'Rodin', 'hall': u'Rodin Floor 24', 'uuid': u'18397cd6-202e-4680-b82e-33ccd9ded1a7'},
                46: {'loc': 'Sansom', 'hall': u'Sansom East', 'uuid': u'ad980c78-bf6d-429a-9a08-1b0899f83d62'},
                47: {'loc': 'Sansom', 'hall': u'Sansom West', 'uuid': u'd1637690-098b-4eca-b48b-6d137207a38e'},
                48: {'loc': 'Stouffer', 'hall': u'Stouffer Commons', 'uuid': u'd4848e7d-fdd0-4faa-b6bd-dc152842cf84'}}

        for hall_id, info in data.items():
            self.hall_to_link[info['hall']] = ALL_URL + info['uuid']
            self.id_to_hall[hall_id] = info['hall']
            self.hall_id_list.append({"hall_name": info['hall'], "id": hall_id, "location": info['loc']})


    @staticmethod
    def update_machine_object(cols, machine_object):
        if cols[2].getText() == "In use" or cols[2].getText() == "Almost done":
            time_remaining = cols[3].getText().split(" ")[0]
            machine_object["running"] += 1
            try:
                machine_object["time_remaining"].append(int(time_remaining))
            except ValueError:
                pass
        elif cols[2].getText() == "Out of order":
            machine_object["out_of_order"] += 1
        elif cols[2].getText() == "Not online":
            machine_object["offline"] += 1
        else:
            machine_object["open"] += 1

        # edge case that handles machine not sending time data
        diff = int(machine_object["running"]) - len(machine_object["time_remaining"])
        while diff > 0:
            machine_object["time_remaining"].append(-1)
            diff = diff - 1

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
                elif machine_type == "Dryer":
                    dryers = Laundry.update_machine_object(cols, dryers)

        machines = {"washers": washers, "dryers": dryers}
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

    def hall_status(self, hall_id):
        """Return the status of each specific washer/dryer in a particular
        laundry room.

        :param hall_name:
             Unescaped string corresponding to the name of the hall hall. This name
             is returned as part of the all_status call.

        >>> english_house = l.hall_status("English%20House")
        """
        hall_name = self.id_to_hall[hall_id]
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
