import tempfile
import unittest

from src.db.backend.errors import TableNotFoundError
from src.db.backend.file import FileDatabase


class TestFileDatabase(unittest.TestCase):

    def test_data_is_saved_between_instances(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first_db = FileDatabase(directory)

            first_db.create_table(
                "cars",
                ("car_id", "brand", "model", "year", "horsepower"),
            )

            first_db.insert_record(
                "cars",
                {
                    "car_id": 1,
                    "brand": "BMW",
                    "model": "X5",
                    "year": 2020,
                    "horsepower": 300,
                },
            )

            second_db = FileDatabase(directory)
            records = second_db.select_records("cars")

            self.assertEqual(
                records,
                [
                    {
                        "car_id": 1,
                        "brand": "BMW",
                        "model": "X5",
                        "year": 2020,
                        "horsepower": 300,
                    }
                ],
            )

    def test_select_with_filters(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)

            db.create_table(
                "cars",
                ("car_id", "brand", "model", "year", "horsepower"),
            )

            db.insert_record("cars", {
                "car_id": 1,
                "brand": "BMW",
                "model": "X5",
                "year": 2020,
                "horsepower": 300,
            })

            db.insert_record("cars", {
                "car_id": 2,
                "brand": "Audi",
                "model": "A6",
                "year": 2021,
                "horsepower": 250,
            })

            records = db.select_records("cars", brand="Audi")

            self.assertEqual(
                records,
                [{
                    "car_id": 2,
                    "brand": "Audi",
                    "model": "A6",
                    "year": 2021,
                    "horsepower": 250,
                }],
            )

    def test_select_from_missing_table(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)

            with self.assertRaises(TableNotFoundError):
                db.select_records("cars")
