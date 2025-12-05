"""
Earthquakes Module.

This module provides functions to connect to the USGS API and
retrieve earthquake data based on specific magnitude criteria.
"""

import requests
import datetime
import json


USGS_URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query?starttime={}&format=geojson&limit=20000'

def get_earthquake(days_past):
    """
    Retrieve the strongest earthquake in the last N days.

    Keyword arguments:
    days_past -- the number of days to look back (int)

    Returns:
    tuple -- a tuple containing (magnitude, place) of the strongest event
    """
    #get the date of today - days_past days at 00 AM
    start_date = (datetime.datetime.now() + datetime.timedelta(days=-days_past)).strftime("%Y-%m-%d")
    URL = USGS_URL.format(start_date)
    r = requests.get(URL)
    events = json.loads(requests.get(URL).text)
    magnitude = 0
    place = ''
    for event in events['features']:
        try:
            mag = float(event['properties']['mag'])
        except TypeError:
            pass 
        if mag > magnitude:
            magnitude = mag
            place = event['properties']['place']
    return magnitude, place
