from requests import get


BASE_URL = "https://esb.isc-seo.upenn.edu/8091/open_data"


class Registrar:
    def __init__(self, bearer, token):
        self.bearer = bearer
        self.token = token

    @property
    def headers(self):
        return {
            "Authorization-Bearer": self.bearer,
            "Authorization-Token": self.token,
            "Content-Type": "application/json; charset=utf-8"
        }

    def course(self, dept, course_number=""):
        return get(BASE_URL + '/course_info/' + dept + '/' + course_number,
                   headers=self.headers).json()

    def search(self,
               course_id="",
               description="",
               ):
        pass
