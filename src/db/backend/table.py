from typing import Any
from .errors import MissingColumnError, UnknownColumnError, InvalidCarDataError, DuplicateIDError


class Table:
    """Таблица с фиксированной схемой (колонками)."""

    def __init__(
        self,
        columns: tuple[str, ...],
        records: list[dict[str, Any]] | None = None,
    ) -> None:
        self.columns = columns
        self.records: list[dict[str, Any]] = []

        if records is not None:
            for record in records:
                self.insert_record(record)

    def insert_record(self, record: dict[str, Any]) -> None:

        if "year" in record:
            if record["year"] < 1886 or record["year"] > 2026:
                raise InvalidCarDataError("Некорректный год выпуска.")

        if "horsepower" in record:
            if record["horsepower"] <= 0:
                raise InvalidCarDataError("Некорректная мощность двигателя.")

        missing = [c for c in self.columns if c not in record]
        if missing:
            raise MissingColumnError(f"Отсутствует поле '{missing[0]}'")

        extra = [c for c in record if c not in self.columns]
        if extra:
            raise UnknownColumnError(f"Поле '{extra[0]}' не определено в таблице")

        if "car_id" in record:
            if any(r.get("car_id") == record["car_id"] for r in self.records):
                raise DuplicateIDError(f"ID {record['car_id']} уже существует")

        self.records.append(record.copy())

    def select_records(self, **filters: Any) -> list[dict[str, Any]]:

        unknown = [k for k in filters if k not in self.columns]
        if unknown:
            raise UnknownColumnError(f"Поле '{unknown[0]}' не существует")

        if not filters:
            return [r.copy() for r in self.records]

        result: list[dict[str, Any]] = []

        for record in self.records:
            if all(record.get(k) == v for k, v in filters.items()):
                result.append(record.copy())

        return result
