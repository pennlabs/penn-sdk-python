from bs4 import BeautifulSoup
import requests


BASE_URL = "http://libcal.library.upenn.edu"
ENDPOINTS = {
    'IDS': BASE_URL + ''
}


class StudySpaces(object):
    def __init__(self):
        pass

    @staticmethod
    def date_parse(d):
        """Parses the date to dashed format.

        :param d: string with date in the format MM/DD/YYYY.
        """
        l = d.split("-")
        final = [l[1], l[2], l[0]]
        return '-'.join(final)

    def get_id_json(self):
        """Extracts the ID's of the rooms to a JSON.
        """
        groupStudyCodes = []
        url = BASE_URL + "/booking/vpdlc"
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        l = soup.find_all('option')
        for element in l:
            if element['value'] != '0':
                url2 = BASE_URL + str(element['value'])
                soup2 = BeautifulSoup(requests.get(url2).text, 'lxml')
                id = soup2.find('input', attrs={"id": "gid"})['value']
                newDict = {}
                newDict['id'] = int(id)
                newDict['name'] = str(element.contents[0])
                groupStudyCodes.append(newDict)
        return groupStudyCodes

    def get_id_dict(self):
        """Extracts the ID's of the room into a dictionary.
        """
        groupStudyCodes = {}
        url = BASE_URL + "/booking/vpdlc"
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        l = soup.find_all('option')
        for element in l:
            if element['value'] != '0':
                url2 = BASE_URL + str(element['value'])
                soup2 = BeautifulSoup(requests.get(url2).text, 'lxml')
                id = soup2.find('input', attrs={"id": "gid"})['value']
                groupStudyCodes[int(id)] = str(element.contents[0])
        return groupStudyCodes

    def extract_times(self, id, date, name):
        """Scrapes the avaiable rooms with the given ID and date.

        :param id: the ID of the building
        :param date: the date to acquire available rooms from
        :param name: the name of the building; obtained via get_id_dict
        """
        url = BASE_URL + "/rooms_acc.php?gid=%s&d=%s&cap=0" % (int(id), date)
        soup = BeautifulSoup(requests.get(url).text, 'lxml')

        timeSlots = soup.find_all('form')
        unparsedRooms = timeSlots[1].contents[2:-2]

        roomTimes = []

        for i in unparsedRooms:
            room = BeautifulSoup(str(i), 'lxml')
            try:
                # extract room names
                roomName = room.fieldset.legend.h2.contents[0]
            except AttributeError:
                # in case the contents aren't a list
                continue
            newRoom = str(roomName)[:-1]
            times = []

            filt = room.fieldset.find_all('label')

            for t in filt:
                # getting the individual times for each room
                dictItem = {}
                dictItem['room_name'] = newRoom
                time = str(t).split("\t\t\t\t\t")[1][1:-1]
                times.append(time)
                startAndEnd = time.split(" - ")
                dictItem['start_time'] = startAndEnd[0].upper()
                dictItem['end_time'] = startAndEnd[1].upper()
                roomTimes.append(dictItem)
                dictItem['date'] = self.date_parse(date)
                dictItem['building'] = name
        return roomTimes
