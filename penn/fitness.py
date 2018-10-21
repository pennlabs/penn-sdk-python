import re
import requests
import datetime
import pytz
from bs4 import BeautifulSoup

FITNESS_URL = "https://connect2concepts.com/connect2/?type=bar&key=650471C6-D72E-4A16-B664-5B9C3F62EEAC"
CALENDAR_URL = "https://api.teamup.com/ks13d3ccc86a21d29e/events"


class Fitness(object):
    """Used to interact with the Penn Recreation usage pages.

    Usage::

        >>> from penn import Fitness
        >>> fit = Fitness('SCHEDULE_TOKEN')
        >>> fit.get_usage()
    """

    def __init__(self, schedule_token):
        self.token = schedule_token

    def get_schedule(self):
        resp = requests.get(CALENDAR_URL, timeout=30, headers={
            "Teamup-Token": self.token
        })
        resp.raise_for_status()
        raw_data = resp.json()
        data = []
        for item in raw_data["events"]:
            out = {
                "name": re.sub(r"\s*-?\s*CLOSED$", "", item["title"], re.I),
                "all_day": item["all_day"]
            }
            if not item["all_day"]:
                out["start"] = item["start_dt"]
                out["end"] = item["end_dt"]
            else:
                out["day"] = item["start_dt"].split("T")[0]
            data.append(out)
        return data

    def get_usage(self):
        """Get fitness locations and their current usage."""

        resp = requests.get(FITNESS_URL, timeout=30)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html5lib")
        eastern = pytz.timezone('US/Eastern')
        output = []
        for item in soup.findAll("div", {"class": "barChart"}):
            data = [x.strip() for x in item.get_text("\n").strip().split("\n")]
            data = [x for x in data if x]
            output.append({
                "name": re.sub(r"\s*-?\s*CLOSED$", "", data[0], re.I),
                "open": "Open" in data[1],
                "count": int(data[2].rsplit(" ", 1)[-1]),
                "updated": eastern.localize(datetime.datetime.strptime(data[3][8:].strip(), '%m/%d/%Y %I:%M %p')).isoformat(),
                "percent": int(data[4][:-1])
            })
        return output
