import requests
from bs4 import BeautifulSoup

FITNESS_URL = "https://connect2concepts.com/connect2/?type=bar&key=650471C6-D72E-4A16-B664-5B9C3F62EEAC"


class Fitness(object):
    """Used to interact with the Penn Recreation usage pages.

    Usage::

        >>> from penn import Fitness
        >>> fit = Fitness()
        >>> fit.get_usage()
    """

    def get_usage(self):
        """Get fitness locations and their current usage."""

        resp = requests.get(FITNESS_URL, timeout=30)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html5lib")
        output = []
        for item in soup.findAll("div", {"class": "barChart"}):
            data = [x.strip() for x in item.get_text("\n").strip().split("\n")]
            data = [x for x in data if x]
            output.append({
                "name": data[0],
                "open": "Open" in data[1],
                "count": int(data[2].rsplit(" ", 1)[-1]),
                "updated": data[3][8:].strip(),
                "percent": int(data[4][:-1])
            })
        return output
