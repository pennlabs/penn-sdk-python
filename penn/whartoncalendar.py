from bs4 import BeautifulSoup
import re
import requests
import datetime

BASE_URL = "https://spike.wharton.upenn.edu/calendar/index.cfm?format=list&date="

def clean_spike_time_string(s):
    """Takes the string native to spike and 
    cleans them to array of times in the string
  
    :param s: string from spike event description
    """
    regex = re.compile("1?[0-9]:[0-9][0-9] [AP]M")
    all_times = regex.findall(s)
    return all_times

def events_on_date(d):
    """Pulls the calendar from the Penn website and
    filters out which events are 2 weeks away from date d.

    :param d: date object that specifies the date
    """
    r = requests.get(BASE_URL + d.strftime('%Y-%m/%d')) 
    soup = BeautifulSoup(r.text, "html5lib")
    cal = soup.find("body").find(id="content").find(id="calendar_content").find(id="calendar_event_list")
    divs = cal.find_all("div")
    events = []
    for e in divs:
        event_div = e.find(id="calendar_event")
        if event_div:
            event = {}
            link = event_div.find("a")
            event["title"] = link.text
            event["link"] = link.get("href")
            time_range = event_div.text
            times = cleanSpikeTimeString(time_range)
            if len(times) == 2:
                event["startTime"] = times[0]
                event["endTime"] = times[1]
                event["date"] = d.strftime('%Y-%m-%d')
                events.append(event)
    return events


def pull_wharton_events_today():
    """Returns JSON object with all 
    events on the current date.
    """
    today = datetime.datetime.now().date()
    return events_on_date(today)

def pull_wharton_events_on_date(date):
    """Return JSON object with all events on the
    date passed in as an argument.
    """
    d = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    return events_on_date(d) 
