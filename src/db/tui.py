from .backend.memory import create_record, select_record


def _print_menu() -> None:

    print("\n=== Магазин Авто ===")
    print("1. Добавить запись")
    print("2. Показать все записи")
    print("3. Найти записи по фильтру")
    print("0. Выход")


def _read_int(prompt: str) -> int:

    while True:

        # в начале и в конце строки.
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
    age = _read_int("age: ")
    horsepower = input("horsepower: ")

    try:

        record = create_record(car_id, brand, model, age, horsepower)


        print(f"Запись добавлена: {record}")

    except ValueError as exc:

        print(f"Ошибка: {exc}")


def _print_records(records: list[tuple[int, str, str, int, int]]) -> None:

    if not records:
        print("Записи не найдены.")
        return


    for record in records:
        print(record)


def _show_all_cars() -> None:
    print("\nСписок записей")
    _print_records(select_record())


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

    age = _read_optional_int("age: ")
    horsepower = input("horsepower: ").strip() or None

    records = select_record(
        car_id=car_id,
        brand=brand,
        model=model,
        age=age,
        horsepower=horsepower,
    )

    _print_records(records)

def run() -> None:
    """
    Запускает основной цикл текстового пользовательского интерфейса.

    Цикл выполняется до тех пор, пока пользователь явно
    не выберет завершение программы.
    """
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