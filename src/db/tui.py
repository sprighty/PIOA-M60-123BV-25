from .backend.memory import MemoryDatabase
from .backend.file import FileDatabase
from .backend.errors import (
    InvalidCarDataError,
    DuplicateIDError,
    DatabaseError,
)


class TUI:
    def __init__(self) -> None:
        print("Выберите тип базы данных:")
        print("1. Memory")
        print("2. File")

        choice = input(">> ").strip()

        self.database = FileDatabase() if choice == "2" else MemoryDatabase()
        self.table_name = "cars"

        # создаём таблицу (без глушения всех ошибок)
        try:
            self.database.create_table(
                self.table_name,
                ("car_id", "brand", "model", "year", "horsepower"),
            )
        except DatabaseError:
            # таблица уже существует или другая ожидаемая БД-ошибка
            pass

    def _print_menu(self) -> None:
        print("\n=== Магазин Авто ===")
        print("1. Добавить запись")
        print("2. Показать все записи")
        print("3. Найти записи по фильтру")
        print("0. Выход")

    def _read_int(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt).strip())
            except ValueError:
                print("Ошибка: введите целое число.")

    def _add_car(self) -> None:
        print("\nДобавление записи")

        record = {
            "car_id": self._read_int("id: "),
            "brand": input("brand: ").strip(),
            "model": input("model: ").strip(),
            "year": self._read_int("year: "),
            "horsepower": self._read_int("horsepower: "),
        }

        try:
            self.database.insert_record(self.table_name, record)
            print("Запись добавлена:", record)

        except DatabaseError as exc:
            # ловим ВСЕ ошибки БД (как требует методичка)
            print("Ошибка:", exc)

    def _print_records(self, records: list[dict]) -> None:
        if not records:
            print("Записи не найдены.")
            return

        for r in records:
            print(r)

    def _show_all_cars(self) -> None:
        print("\nСписок записей")

        try:
            records = self.database.select_records(self.table_name)
            self._print_records(records)

        except DatabaseError as exc:
            print("Ошибка:", exc)

    def _read_optional_int(self, prompt: str):
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            return int(raw)
        except ValueError:
            return None

    def _find_cars_by_filter(self) -> None:
        print("\nПоиск по фильтру")

        filters = {
            "car_id": self._read_optional_int("id: "),
            "brand": input("brand: ").strip() or None,
            "model": input("model: ").strip() or None,
            "year": self._read_optional_int("year: "),
            "horsepower": self._read_optional_int("horsepower: "),
        }

        filters = {k: v for k, v in filters.items() if v is not None}

        try:
            records = self.database.select_records(self.table_name, **filters)
            self._print_records(records)
        except DatabaseError as exc:
            print("Ошибка:", exc)

    def run(self) -> None:
        while True:
            self._print_menu()
            action = input("Выберите действие: ").strip()

            if action == "1":
                self._add_car()
            elif action == "2":
                self._show_all_cars()
            elif action == "3":
                self._find_cars_by_filter()
            elif action == "0":
                print("Выход из программы.")
                break
            else:
                print("Неизвестная команда")
