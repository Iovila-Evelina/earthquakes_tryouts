import unittest
import csv
import sqlite3
import os
from earthquake_app.db_handler import query_db


class TestProject(unittest.TestCase):
    """
    Test suite for the Earthquake Project.

    This class implements the tests required by the Project Manual (Step 7).
    """

    def test_bounding_box(self):
        """
        Test 1: Check if Padova, Palermo, Parma are in the bounding box.
        """
        cities = {
            "Padova": (45.4064, 11.8768),
            "Palermo": (38.1157, 13.3615),
            "Parma": (44.8015, 10.3279)
        }

        bbox = {}
        csv_filename = 'bounding_box.csv'

        if not os.path.exists(csv_filename):
            self.fail(
                f"File {csv_filename} non trovato! Esegui write_bounding_box."
            )

        with open(csv_filename, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                bbox[row['key']] = float(row['value'])

        for city, (lat, lon) in cities.items():
            with self.subTest(city=city):
                self.assertGreaterEqual(
                    lat, bbox['minlatitude'], f"{city} è troppo a Sud!"
                )
                self.assertLessEqual(
                    lat, bbox['maxlatitude'], f"{city} è troppo a Nord!"
                )
                self.assertGreaterEqual(
                    lon, bbox['minlongitude'], f"{city} è troppo a Ovest!"
                )
                self.assertLessEqual(
                    lon, bbox['maxlongitude'], f"{city} è troppo a Est!"
                )

    def test_magnitude(self):
        """
        Test 2: Check that there are no earthquakes with magnitude > 9.5.
        """
        conn = sqlite3.connect('earthquakes.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM earthquakes_db WHERE mag > 9.5")
        results = cursor.fetchall()

        conn.close()

        self.assertEqual(
            len(results), 0, "Trovato un terremoto impossibile (> 9.5)!"
        )

    def test_order(self):
        """
        Test 3: Check that query_db outputs a list ordered decreasingly.
        """
        results = query_db(K=10, days=30, min_magnitude=1.0)

        for i in range(len(results) - 1):
            mag_curr = results[i][2]
            mag_next = results[i + 1][2]

            self.assertGreaterEqual(
                mag_curr, mag_next,
                f"Errore: {mag_curr} è minore di {mag_next}"
            )

    def test_limit_K(self):
        """
        Test 4 (Extra): Verifica che la funzione rispetti il limite K.
        """
        k_req = 3
        results = query_db(K=k_req, days=30, min_magnitude=0.0)

        self.assertLessEqual(
            len(results), k_req,
            f"Troppi risultati ({len(results)} invece di max {k_req})"
        )


if __name__ == '__main__':
    unittest.main()
