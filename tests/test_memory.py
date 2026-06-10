import unittest

from src.db.backend.memory import CarTable
from src.db.backend.errors import InvalidCarDataError, DuplicateIDError


class TestMemory(unittest.TestCase):

    def setUp(self):
        self.db = CarTable()
        self.assertIsInstance(self.db, CarTable)

    def test_create_record(self):
        cases = [
            (1, "BMW", "X5", 2020, 300),
            (2, "Audi", "A6", 2021, 250),
            (3, "Toyota", "Camry", 2019, 180),
            (4, "Mercedes", "C200", 2022, 200),
            (5, "Ford", "Focus", 2018, 150),
            (6, "Honda", "Civic", 2020, 160),
            (7, "Skoda", "Octavia", 2021, 170),
            (8, "Kia", "K5", 2022, 190),
            (9, "Hyundai", "Elantra", 2019, 155),
            (10, "VW", "Passat", 2020, 180),
            (11, "Mazda", "6", 2021, 175),
            (12, "Nissan", "Teana", 2018, 165),
        ]

        for test_data in cases:
            with self.subTest(test_data=test_data):
                record = self.db.create_record(*test_data)

                self.assertEqual(record[0], test_data[0])
                self.assertEqual(record[1], test_data[1])
                self.assertEqual(record[2], test_data[2])
                self.assertEqual(record[3], test_data[3])
                self.assertEqual(record[4], test_data[4])

    def test_create_record_invalid_data(self):
        cases = [
            (1, "BMW", "X5", 1800, 300),   # неправильный год
            (2, "Audi", "A6", 2021, -10),  # неправильная мощность
        ]

        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(InvalidCarDataError):
                    self.db.create_record(*test_data)

    def test_create_record_duplicate_id(self):
        self.db.create_record(1, "BMW", "X5", 2020, 300)

        with self.assertRaises(DuplicateIDError):
            self.db.create_record(1, "Audi", "A6", 2021, 250)

    def test_select_record(self):
        test_data = [
            (1, "BMW", "X5", 2020, 300),
            (2, "Audi", "A6", 2021, 250),
            (3, "Toyota", "Camry", 2019, 180),
            (4, "Mercedes", "C200", 2022, 200),
            (5, "Ford", "Focus", 2018, 150),
            (6, "Honda", "Civic", 2020, 160),
            (7, "Skoda", "Octavia", 2021, 170),
            (8, "Kia", "K5", 2022, 190),
            (9, "Hyundai", "Elantra", 2019, 155),
            (10, "VW", "Passat", 2020, 180),
        ]

        for data in test_data:
            self.db.create_record(*data)

        cases = [
            {
                "name": "Без фильтров",
                "filters": {},
                "expected": test_data,
            },
            {
                "name": "Фильтр по ID",
                "filters": {"car_id": 1},
                "expected": [test_data[0]],
            },
            {
                "name": "Фильтр по бренду",
                "filters": {"brand": "BMW"},
                "expected": [test_data[0]],
            },
            {
                "name": "Фильтр по модели",
                "filters": {"model": "Camry"},
                "expected": [test_data[2]],
            },
            {
                "name": "Фильтр по году",
                "filters": {"year": 2020},
                "expected": [test_data[0], test_data[5], test_data[9]],
            },
            {
                "name": "Фильтр по мощности",
                "filters": {"horsepower": 300},
                "expected": [test_data[0]],
            },
        ]

        for case in cases:
            with self.subTest(case=case["name"]):
                records = self.db.select_record(**case["filters"])
                self.assertEqual(records, case["expected"])
