class DatabaseError(Exception):
    """Базовая ошибка базы данных."""


class TableAlreadyExistsError(DatabaseError):
    """Таблица уже существует."""


class TableNotFoundError(DatabaseError):
    """Таблица не найдена."""


class MissingColumnError(DatabaseError):
    """Отсутствует обязательное поле."""


class UnknownColumnError(DatabaseError):
    """Неизвестное поле в записи."""


class DuplicateIDError(DatabaseError):
    """Попытка добавить запись с уже существующим ID."""


class InvalidCarDataError(DatabaseError):
    """Ошибка валидации данных автомобиля."""


class InvalidStorageDataError(DatabaseError):
    """Ошибка при чтении повреждённого JSON файла."""
