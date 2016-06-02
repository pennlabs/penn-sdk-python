"""A module for consuming the Penn Libraries API"""
import requests

BASE_URL = "http://dla.library.upenn.edu/2.0.0/search"


def search(query):
    """Search Penn Libraries Franklin for documents
    The maximum pagesize currently is 50.
    """
    params = {
        's.cmd': 'setTextQuery(%s)setPageSize(50)setHoldingsOnly(true)' % query
    }
    return requests.get(BASE_URL, params=params, timeout=10).json()
