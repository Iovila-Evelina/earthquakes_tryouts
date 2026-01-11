import sqlite3
from datetime import datetime, timedelta
from .fetch_data import gather_earthquakes


def create_earthquake_db(days):
    """
    Creates the database, fetches fresh data, and populates the table.

    Args:
        days (int): Number of past days to fetch data for.
    """
    print(f"Fetching data for the last {days} days...")
    earthquakes = gather_earthquakes(days)

    conn = sqlite3.connect('earthquakes.db')
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS earthquakes_db (
        day TEXT,
        time TEXT,
        mag REAL,
        latitude REAL,
        longitude REAL,
        place TEXT
    );
    """
    cursor.execute(create_table_sql)
    cursor.execute("DELETE FROM earthquakes_db")
    conn.commit()

    insert_sql = """
    INSERT INTO earthquakes_db (day, time, mag, latitude, longitude, place)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.executemany(insert_sql, earthquakes)

    conn.commit()
    conn.close()
    print(f"Database updated with {len(earthquakes)} events.")


def query_db(K, days, min_magnitude):
    """
    Queries the database to find the strongest earthquakes.

    Args:
        K (int): Max number of results.
        days (int): Time range in days.
        min_magnitude (float): Minimum magnitude threshold.

    Returns:
        list: A list of tuples matching the criteria, sorted by magnitude.
    """
    conn = sqlite3.connect('earthquakes.db')
    cursor = conn.cursor()

    cutoff_date = datetime.utcnow() - timedelta(days=days)
    cutoff_str = cutoff_date.strftime("%Y-%m-%d")

    query = """
        SELECT day, time, mag, latitude, longitude, place
        FROM earthquakes_db
        WHERE mag >= ? AND day >= ?
        ORDER BY mag DESC
        LIMIT ?
    """

    cursor.execute(query, (min_magnitude, cutoff_str, K))
    results = cursor.fetchall()
    conn.close()

    return results
