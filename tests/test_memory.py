import unittest

from src.db.backend.memory import MemoryDatabase
from src.db.backend.errors import InvalidCarDataError, DuplicateIDError


class TestMemory(unittest.TestCase):

    def setUp(self):
        self.db = MemoryDatabase()
        self.table = "cars"

    def test_insert_record(self):
        cases = [
            (1, "BMW", "X5", 2020, 300),
            (2, "Audi", "A6", 2021, 250),
            (3, "Toyota", "Camry", 2019, 180),
        ]

        for test_data in cases:
            with self.subTest(test_data=test_data):

                record = {
                    "car_id": test_data[0],
                    "brand": test_data[1],
                    "model": test_data[2],
                    "year": test_data[3],
                    "horsepower": test_data[4],
                }

                self.db.insert_record(self.table, record)

                records = self.db.select_records(self.table, car_id=test_data[0])
                self.assertEqual(records[0]["car_id"], test_data[0])

    def test_invalid_data(self):
        self.db.insert_record(self.table, {
            "car_id": 1,
            "brand": "BMW",
            "model": "X5",
            "year": 1800,   
            "horsepower": 300
        })


    def test_duplicate_id(self):
        self.db.insert_record(self.table, {
            "car_id": 1,
            "brand": "BMW",
            "model": "X5",
            "year": 2020,
            "horsepower": 300
        })

        with self.assertRaises(DuplicateIDError):
            self.db.insert_record(self.table, {
                "car_id": 1,
                "brand": "Audi",
                "model": "A6",
                "year": 2021,
                "horsepower": 250
            })

    def test_select_records(self):
        data = [
            {"car_id": 1, "brand": "BMW", "model": "X5", "year": 2020, "horsepower": 300},
            {"car_id": 2, "brand": "Audi", "model": "A6", "year": 2021, "horsepower": 250},
            {"car_id": 3, "brand": "Toyota", "model": "Camry", "year": 2019, "horsepower": 180},
        ]

        for record in data:
            self.db.insert_record(self.table, record)

        all_records = self.db.select_records(self.table)
        self.assertEqual(len(all_records), 3)

        bmw = self.db.select_records(self.table, brand="BMW")
        self.assertEqual(bmw[0]["brand"], "BMW")


        year_2020 = self.db.select_records(self.table, year=2020)
        self.assertEqual(year_2020[0]["year"], 2020)
