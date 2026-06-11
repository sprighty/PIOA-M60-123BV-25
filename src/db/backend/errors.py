class CarTableError(Exception):
    """Базовый класс для ошибок, связанных с таблицей автомобилей."""
    pass


class InvalidCarDataError(CarTableError):
    """Ошибка при некорректных данных автомобиля (год, мощность и т.п.)."""
    pass


class DuplicateIDError(CarTableError):
    """Ошибка при попытке добавить запись с уже существующим ID."""
    pass
