import requests
from datetime import datetime

def get_next_bus(stop=7726):
    r = requests.get('https://www.metlink.org.nz/api/v1/StopDepartures/{0}'.format(stop))
    return r.json()['Services'][0]

def get_hour(time):
    d = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S+12:00")
    if d.hour > 12:
        hr = d.hour - 12
    else:
        hr = d.hour
    return hr

def get_minutes(time):
    d = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S+12:00")
    if d.minute == 0:
        minutes = "oh clock"
    elif d.minute > 9:
        minutes = d.minute
    else:
        minutes = "oh {}".format(d.minute)
    return minutes