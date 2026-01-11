import csv
import os
import math


def load_municipalities():
    """
    Reads the 'italian_municipalities.csv' file.
    Returns a list of dicts: {'name': str, 'lat': float, 'lon': float}.
    """
    municipalities = []

    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'italian_municipalities.csv')

    if not os.path.exists(csv_path):
        print(
            f"WARNING: File {csv_path} not found. The add-on will not work."
        )
        return []

    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                name = row['name']
                lat = float(row['latitude'])
                lon = float(row['longitude'])

                municipalities.append({'name': name, 'lat': lat, 'lon': lon})
            except (ValueError, KeyError):
                continue

    return municipalities


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates distance in km between two points (Haversine formula).
    """
    R = 6371.0  # Earth radius in km

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def get_closest_municipalities(eq_lat, eq_lon, municipalities, n=5):
    """
    Returns the top 'n' municipalities closest to the given coordinates.
    """
    distances = []

    for city in municipalities:
        dist = haversine_distance(eq_lat, eq_lon, city['lat'], city['lon'])
        distances.append((city['name'], dist))

    distances.sort(key=lambda x: x[1])

    return distances[:n]
