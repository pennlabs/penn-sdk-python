from requests import get
from trees import ObjectifiedDict


BASE_URL = "https://esb.isc-seo.upenn.edu/8091/open_data/"


class Registrar:
    def __init__(self, bearer, token):
        self.headers = {
            "Authorization-Bearer": bearer,
            "Authorization-Token": token,
            "Content-Type": "application/json; charset=utf-8"
        }

    def course(self, dept, course_number=""):
        r = get(BASE_URL + 'course_info/' + dept + '/' + course_number,
                headers=self.headers)
        course = ObjectifiedDict(r.json())
        return course

    def search(self, options):
        pass
