from .errors import DuplicateIDError, InvalidCarDataError

type CarRecord = tuple[int, str, str, int, int]


class CarTable:
    def __init__(self) -> None:
        self._cars: list[CarRecord] = []

    def create_record(
        self,
        car_id: int,
        brand: str,
        model: str,
        year: int,
        horsepower: int,
    ) -> CarRecord:

        if year < 1886 or year > 2026:
            raise InvalidCarDataError("Некорректный год выпуска.")

        if horsepower <= 0:
            raise InvalidCarDataError("Некорректная мощность двигателя.")

        if any(record[0] == car_id for record in self._cars):
            raise DuplicateIDError(f"Запись с id={car_id} уже существует.")

        new_record: CarRecord = (
            car_id,
            brand.strip(),
            model.strip(),
            year,
            horsepower,
        )

        self._cars.append(new_record)
        return new_record

    def select_record(
        self,
        car_id: int | None = None,
        brand: str | None = None,
        model: str | None = None,
        year: int | None = None,
        horsepower: int | None = None,
    ) -> list[CarRecord]:

        if (
            car_id is None
            and brand is None
            and model is None
            and year is None
            and horsepower is None
        ):
            return self._cars.copy()

        result: list[CarRecord] = []

        for record in self._cars:

            if car_id is not None and record[0] != car_id:
                continue

            if brand is not None and record[1] != brand.strip():
                continue

            if model is not None and record[2] != model.strip():
                continue

            if year is not None and record[3] != year:
                continue

            if horsepower is not None and record[4] != horsepower:
                continue

            result.append(record)

        return result
