import os
import csv
import requests
import pkg_resources
from bs4 import BeautifulSoup

LAUNDRY_DOMAIN = os.environ.get("LAUNDRY_DOMAIN", "suds.kite.upenn.edu")
ALL_URL = 'http://{}/'.format(LAUNDRY_DOMAIN)
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
        self.id_to_location = {}
        self.hall_id_list = []
        self.create_hall_to_link_mapping()

    def create_hall_to_link_mapping(self):
        """
        :return: Mapping from hall name to associated link in SUDS. Creates inverted index from id to hall.
        """
        laundry_path = pkg_resources.resource_filename("penn", "data/laundry.csv")
        with open(laundry_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                hall_id, hall_name, location, uuid = row
                hall_id = int(hall_id)
                self.hall_to_link[hall_name] = ALL_URL + uuid
                self.id_to_hall[hall_id] = hall_name
                self.id_to_location[hall_id] = location
                self.hall_id_list.append({"hall_name": hall_name, "id": hall_id, "location": location})

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
        """Return names, hall numbers, and the washers/dryers available for a certain hall.

        :param hall:
            The ID of the hall to retrieve data for.
        :type hall: int
        """
        if hall not in self.hall_to_link:
            return None  # change to to empty json idk

        page = requests.get(ALL_URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup.prettify()
        washers = {"open": 0, "running": 0, "out_of_order": 0, "offline": 0, "time_remaining": []}
        dryers = {"open": 0, "running": 0, "out_of_order": 0, "offline": 0, "time_remaining": []}
        found_hall = False
        detailed = []

        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 1 and len(cols[0].find_all('center')) == 1 and len(cols[0].find_all('center')[0].find_all('h2')) == 1: # Title element
                if(cols[0].find_all('center')[0].find_all('h2')[0].find_all('a')[0].getText() == hall): # Check if found correct hall
                    found_hall = True
                else:
                    found_hall = False
            elif len(cols) == 5 and cols[2]['class'][0] == 'status' and found_hall == True: # Content element for relevant hall
                machine_type = cols[1].getText()
                if machine_type == "Washer":
                    washers = Laundry.update_machine_object(cols, washers)
                elif machine_type == "Dryer":
                    dryers = Laundry.update_machine_object(cols, dryers)
                if machine_type in ["Washer", "Dryer"]:
                    try:
                        time = int(cols[3].getText().split(" ")[0])
                    except ValueError:
                        time = 0
                    detailed.append({
                        "id": int(cols[0].getText().split(" ")[1][1:]),
                        "type": cols[1].getText().lower(),
                        "status": cols[2].getText(),
                        "time_remaining": time
                    })

        machines = {"washers": washers, "dryers": dryers, "details": detailed}
        return machines

    def parse_halls(self, lhall):
        """Return list of names, hall numbers, and the washers/dryers available for a list of halls.

        :param halls:
            The IDs of the halls to retrieve data for.
        :type halls: list(int)
        """
        lmachines = []
        page = requests.get(ALL_URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup.prettify()
        for hall in lhall:
            if hall not in self.id_to_hall:
                lmachines.append({}) # empty machine? Can also just skip to next id 
            else:
                hall = self.id_to_hall[hall]
                washers = {"open": 0, "running": 0, "out_of_order": 0, "offline": 0, "time_remaining": []}
                dryers = {"open": 0, "running": 0, "out_of_order": 0, "offline": 0, "time_remaining": []}
                found_hall = False
                detailed = []

                rows = soup.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) == 1 and len(cols[0].find_all('center')) == 1 and len(cols[0].find_all('center')[0].find_all('h2')) == 1: # Title element
                        if(cols[0].find_all('center')[0].find_all('h2')[0].find_all('a')[0].getText() == hall): # Check if found correct hall
                            found_hall = True
                        else:
                            found_hall = False
                    elif len(cols) == 5 and cols[2]['class'][0] == 'status' and found_hall == True: # Content element for relevant hall
                        machine_type = cols[1].getText()
                        if machine_type == "Washer":
                            washers = Laundry.update_machine_object(cols, washers)
                        elif machine_type == "Dryer":
                            dryers = Laundry.update_machine_object(cols, dryers)
                        if machine_type in ["Washer", "Dryer"]:
                            try:
                                time = int(cols[3].getText().split(" ")[0])
                            except ValueError:
                                time = 0
                            detailed.append({
                                "id": int(cols[0].getText().split(" ")[1][1:]),
                                "type": cols[1].getText().lower(),
                                "status": cols[2].getText(),
                                "time_remaining": time
                            })

                machines = {"washers": washers, "dryers": dryers, "details": detailed}
                lmachines.append(machines)
        return lmachines

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

        :param hall_id:
             Integer corresponding to the id of the hall. This id
             is returned as part of the all_status call.

        >>> english_house = l.hall_status("English%20House")
        """
        if hall_id not in self.id_to_hall:
            raise ValueError("No hall with id %s exists." % hall_id)

        hall_name = self.id_to_hall[hall_id]
        location = self.id_to_location[hall_id]
        machines = self.parse_a_hall(hall_name)

        return {
            'machines': machines,
            'hall_name': hall_name,
            'location': location
        }
