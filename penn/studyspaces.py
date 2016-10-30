from bs4 import BeautifulSoup
import requests


BASE_URL = "http://libcal.library.upenn.edu"


class StudySpaces(object):
    def __init__(self):
        pass

    @staticmethod
    def date_parse(original):
        """Parses the date to dashed format.

        :param original: string with date in the format MM/DD/YYYY.
        """
        l = original.split("-")
        final = [l[1], l[2], l[0]]
        return '-'.join(final)

    def get_id_json(self):
        """Makes JSON with each element associating URL, ID, and building
        name.
        """
        group_study_codes = []
        url = BASE_URL + "/booking/vpdlc"
        soup = BeautifulSoup(requests.get(url).text, 'html5lib')
        l = soup.find_all('option')
        for element in l:
            if element['value'] != '0':
                url2 = BASE_URL + str(element['value'])
                soup2 = BeautifulSoup(requests.get(url2).text, 'html5lib')
                id = soup2.find('input', attrs={"id": "gid"})['value']
                new_dict = {}
                new_dict['id'] = int(id)
                new_dict['name'] = str(element.contents[0])
                new_dict['url'] = url2
                group_study_codes.append(new_dict)
        return group_study_codes

    def get_id_dict(self):
        """Extracts the ID's of the room into a dictionary. Used as a
        helper for the extract_times method.
        """
        group_study_codes = {}
        url = BASE_URL + "/booking/vpdlc"
        soup = BeautifulSoup(requests.get(url).text, 'html5lib')
        options = soup.find_all('option')
        for element in options:
            if element['value'] != '0':
                url2 = BASE_URL + str(element['value'])
                soup2 = BeautifulSoup(requests.get(url2).text, 'html5lib')
                id = soup2.find('input', attrs={"id": "gid"})['value']
                group_study_codes[int(id)] = str(element.contents[0])
        return group_study_codes

    def extract_times(self, id, date, name):
        """Scrapes the avaiable rooms with the given ID and date.

        :param id: the ID of the building
        :param date: the date to acquire available rooms from
        :param name: the name of the building; obtained via get_id_dict
        """
        url = BASE_URL + "/rooms_acc.php?gid=%s&d=%s&cap=0" % (int(id), date)
        soup = BeautifulSoup(requests.get(url).text, 'html5lib')

        time_slots = soup.find_all('form')
        unparsed_rooms = time_slots[1].contents[2:-2]

        roomTimes = []

        for i in unparsed_rooms:
            room = BeautifulSoup(str(i), 'html5lib')
            try:
                # extract room names
                roomName = room.fieldset.legend.h2.contents[0]
            except AttributeError:
                # in case the contents aren't a list
                continue
            newRoom = str(roomName)[:-1]
            times = []

            filtered = room.fieldset.find_all('label')

            for t in filtered:
                # getting the individual times for each room
                dict_item = {}
                dict_item['room_name'] = newRoom
                time = str(t).split("\t\t\t\t\t")[2][1:-1]
                times.append(time)
                startAndEnd = time.split(" - ")
                dict_item['start_time'] = startAndEnd[0].upper()
                dict_item['end_time'] = startAndEnd[1].upper()
                roomTimes.append(dict_item)
                dict_item['date'] = self.date_parse(date)
                dict_item['building'] = name
        return roomTimes
