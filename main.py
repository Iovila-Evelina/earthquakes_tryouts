"""
Earthquake Search Tool (INGV) - Main Module.

This script orchestrates the fetching of earthquake data, database updates,
and querying based on user input. It also supports an optional add-on
to find the closest municipalities to each earthquake.
"""

import argparse
from earthquake_app.db_handler import create_earthquake_db, query_db
from earthquake_app.nearby_municipalities import (
    load_municipalities,
    get_closest_municipalities
)


def print_earthquakes(earthquakes, show_closest, municipalities_data):
    """
    Prints the list of earthquakes to the console.
    If 'show_closest' is True, it also prints the nearest municipalities.
    """
    if not earthquakes:
        print("No earthquakes found matching the criteria.")
        return

    for eq in earthquakes:
        day, time, mag, lat, lon, place = eq

        print("-" * 50)
        print(f"day: {day}, time: {time}, magnitude: {mag},")
        print(f"lat: {lat}, lon: {lon}, place: {place}")

        if show_closest and municipalities_data:
            closest = get_closest_municipalities(
                lat, lon, municipalities_data
            )
            print("\n   >>> Closest Municipalities (Add-on):")
            for name, dist in closest:
                print(f"       * {name}: {dist:.2f} km")


def main():
    """
    Main execution function. Handles argument parsing and program flow.
    """
    parser = argparse.ArgumentParser(
        description="Search for the strongest earthquakes in Italy."
    )

    parser.add_argument(
        "--days", type=int, required=True,
        help="Number of days to search."
    )
    parser.add_argument(
        "--K", type=int, required=True,
        help="Number of strongest earthquakes to show."
    )
    parser.add_argument(
        "--magnitude", type=float, required=True,
        help="Minimum magnitude allowed."
    )
    parser.add_argument(
        "--addon", action="store_true",
        help="Show the closest municipalities."
    )

    args = parser.parse_args()

    municipalities_data = []
    if args.addon:
        print("Loading municipalities data...")
        municipalities_data = load_municipalities()
        if not municipalities_data:
            print("WARNING: Could not load municipalities. Skipping add-on.")

    print(f"Updating database (Last {args.days} days)...")
    create_earthquake_db(args.days)

    results = query_db(args.K, args.days, args.magnitude)

    print("\n--- Results ---")
    print_earthquakes(results, args.addon, municipalities_data)


if __name__ == "__main__":
    main()
