from .backend.memory import CarTable
from .backend.errors import InvalidCarDataError, DuplicateIDError

car_table = CarTable()


def _print_menu() -> None:
    print("\n=== Магазин Авто ===")
    print("1. Добавить запись")
    print("2. Показать все записи")
    print("3. Найти записи по фильтру")
    print("0. Выход")


def _read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число.")


def _add_car() -> None:
    print("\nДобавление записи")

    car_id = _read_int("id: ")
    brand = input("brand: ").strip()
    model = input("model: ").strip()
    year = _read_int("year: ")
    horsepower = _read_int("horsepower: ")

    try:
        record = car_table.create_record(
            car_id, brand, model, year, horsepower
        )
        print(f"Запись добавлена: {record}")

    except (InvalidCarDataError, DuplicateIDError) as exc:
        print(f"Ошибка: {exc}")


def _print_records(records: list[tuple[int, str, str, int, int]]) -> None:
    if not records:
        print("Записи не найдены.")
        return

    for record in records:
        print(record)


def _show_all_cars() -> None:
    print("\nСписок записей")
    _print_records(car_table.select_record())


def _read_optional_int(prompt: str) -> int | None:
    while True:
        raw = input(prompt).strip()

        if raw == "":
            return None

        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым.")


def _find_cars_by_filter() -> None:
    print("\nПоиск по фильтру (Enter = пропустить поле)")

    car_id = _read_optional_int("id: ")
    brand = input("brand: ").strip() or None
    model = input("model: ").strip() or None
    year = _read_optional_int("year: ")
    horsepower = _read_optional_int("horsepower: ")

    records = car_table.select_record(
        car_id=car_id,
        brand=brand,
        model=model,
        year=year,
        horsepower=horsepower,
    )

    _print_records(records)


def run() -> None:
    while True:
        _print_menu()
        action = input("Выберите действие: ").strip()

        if action == "1":
            _add_car()

        elif action == "2":
            _show_all_cars()

        elif action == "3":
            _find_cars_by_filter()

        elif action == "0":
            print("Выход из программы.")
            break

        else:
            print("Неизвестная команда. Повторите ввод.")
