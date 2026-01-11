import csv
import requests
import os
from datetime import datetime, timedelta


def gather_earthquakes(days):
    """
    Fetches earthquake data from the INGV API for the specified days.

    Args:
        days (int): The number of days in the past to query for.

    Returns:
        list: A list of tuples (day, time, mag, lat, lon, place).
    """
    bounding_box = {}

    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'bounding_box.csv')

    try:
        if not os.path.exists(csv_path):
            csv_path = os.path.join(
                os.path.dirname(current_dir), 'bounding_box.csv'
            )

        with open(csv_path, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                bounding_box[row['key']] = float(row['value'])
    except FileNotFoundError:
        print(f"Error: 'bounding_box.csv' not found at {csv_path}.")
        return []

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    url = "https://webservices.ingv.it/fdsnws/event/1/query?"

    params = {
        "format": "geojson",
        "starttime": start_time.strftime("%Y-%m-%d"),
        "endtime": end_time.strftime("%Y-%m-%d"),
        "minlatitude": bounding_box['minlatitude'],
        "maxlatitude": bounding_box['maxlatitude'],
        "minlongitude": bounding_box['minlongitude'],
        "maxlongitude": bounding_box['maxlongitude']
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to INGV: {e}")
        return []

    data = response.json()
    events = data.get("features", [])
    earthquakes_list = []

    for event in events:
        properties = event["properties"]
        geometry = event["geometry"]

        magnitude = properties["mag"]
        place = properties["place"]
        time_raw = properties["time"]

        longitude = geometry["coordinates"][0]
        latitude = geometry["coordinates"][1]

        if isinstance(time_raw, str):
            clean_time = time_raw[:19]
            dt_object = datetime.fromisoformat(clean_time)

            day = dt_object.strftime("%Y-%m-%d")
            time = dt_object.strftime("%H:%M:%S")

            quake_tuple = (day, time, magnitude, latitude, longitude, place)
            earthquakes_list.append(quake_tuple)

    return earthquakes_list
