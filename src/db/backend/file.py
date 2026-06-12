import json
from pathlib import Path

from .database import Database
from .errors import (
    InvalidStorageDataError,
    TableNotFoundError,
)
from .table import Table


class FileDatabase(Database):
    """Файловая реализация базы данных (JSON)."""

    def __init__(self, directory: str = "data") -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _table_exists(self, table_name: str) -> bool:
        return self._get_table_path(table_name).exists()

    def _load_table(self, table_name: str) -> Table:
        path = self._get_table_path(table_name)

        if not path.exists():
            raise TableNotFoundError(f"Таблица '{table_name}' не существует.")

        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

        except (json.JSONDecodeError, OSError) as error:
            raise InvalidStorageDataError(
                "Ошибка чтения файла таблицы."
            ) from error

        return self._deserialize_table(data)

    def _save_table(self, table_name: str, table: Table) -> None:
        path = self._get_table_path(table_name)

        with path.open("w", encoding="utf-8") as file:
            json.dump(
                self._serialize_table(table),
                file,
                ensure_ascii=False,
                indent=2,
            )

    def _get_table_path(self, table_name: str) -> Path:
        return self.directory / f"{table_name}.json"

    def _serialize_table(self, table: Table) -> dict:
        return {
            "columns": list(table.columns),
            "records": [r.copy() for r in table.records],
        }

    def _deserialize_table(self, data: dict) -> Table:
        if not isinstance(data, dict):
            raise InvalidStorageDataError("Некорректная структура файла.")

        if "columns" not in data or "records" not in data:
            raise InvalidStorageDataError("Файл не содержит columns/records.")

        if not isinstance(data["columns"], list) or not isinstance(data["records"], list):
            raise InvalidStorageDataError("Неверные типы данных в файле.")

        return Table(tuple(data["columns"]), data["records"])
