def create_record():
    """Добавляет новую запись в существующую таблицу."""
    pass


def select_record():
    """Возвращает записи, подходящие под запрос или фильтр."""
    pass


def update_record():
    """Обновляет поля существующей записи по идентификатору или фильтру."""
    pass


def delete_record():
    """Удаляет запись из таблицы по идентификатору или фильтру."""
    pass


# Определение пользовательского алиаса типа для записи таблицы.
# В качестве структуры записи используется кортеж,
# поскольку кортеж является неизменяемым типом данных.
# Структура записи Car: (id, first_name, second_name, age, sex)
type CarRecord = tuple[int, str, str, int, int]

# Таблица Car представлена списком записей (кортежей).
Car: list[CarRecord] = []

def create_record(
    car_id: int,   # Уникальный идентификатор записи
    brand: str,   # Имя
    model: str,  # Фамилия
    age: int,          # Возраст
    horsepower: int,          # Пол
) -> CarRecord:
    """
    Создаёт новую запись и добавляет её в таблицу Car.

    Выполняется валидация возраста и проверка уникальности идентификатора.
    В случае нарушения условий возбуждается исключение ValueError.
    """

    # Проверка корректности возраста.
    # Возраст не может быть отрицательным значением.
    if age > 2026 or age < 1885:
        raise ValueError("Неправильный год выпуска.")

    # Проверка уникальности идентификатора.
    # Функция any() возвращает True, если хотя бы один элемент
    # последовательности удовлетворяет условию.
    if any(record[0] == car_id for record in Car):
        raise ValueError(f"Запись с id={car_id} уже существует.")

    # Формирование новой записи.
    # Метод strip() удаляет пробельные символы
    # в начале и в конце строки.
    new_record: CarRecord = (
        car_id,
        brand.strip(),
        model.strip(),
        age,
        horsepower,
    )

    # Добавление записи в таблицу.
    Car.append(new_record)

    # Возврат созданной записи.
    return new_record

def select_record(
    car_id: int | None = None,   # Фильтр по идентификатору
    brand: str | None = None,   # Фильтр по имени
    model: str | None = None,  # Фильтр по фамилии
    age: int | None = None,          # Фильтр по возрасту
    horsepower: int | None = None,          # Фильтр по полу
) -> list[CarRecord]:
    """
    Выполняет выборку записей из таблицы Car
    в соответствии с переданными фильтрами.

    Если фильтры не заданы, возвращается копия всей таблицы.
    """

    # Проверка отсутствия всех фильтров.
    # В этом случае возвращается копия списка,
    # чтобы предотвратить изменение исходной таблицы
    # внешним кодом.
    if (
        car_id is None
        and brand is None
        and model is None
        and age is None
        and horsepower is None
    ):
        return Car.copy()

    # Формирование результирующего списка.
    result: list[CarRecord] = []

    # Итерация по всем записям таблицы.
    for record in Car:

        # Проверка соответствия каждому фильтру.
        # Если фильтр задан и запись ему не соответствует,
        # выполняется переход к следующей итерации цикла.

        if car_id is not None and record[0] != car_id:
            continue

        if brand is not None and record[1] != brand:
            continue

        if model is not None and record[2] != model:
            continue

        if age is not None and record[3] != age:
            continue

        if horsepower is not None and record[4] != horsepower:
            continue

        # Если запись удовлетворяет всем заданным условиям,
        # она добавляется в результирующий список.
        result.append(record)

    # Возврат списка найденных записей.
    return result