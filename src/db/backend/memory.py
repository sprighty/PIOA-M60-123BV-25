type CarRecord = tuple[int, str, str, int, int]


Car: list[CarRecord] = []

def create_record(
    car_id: int,
    brand: str,
    model: str,
    age: int,
    horsepower: int,
) -> CarRecord:
    
    if age > 2026 or age < 1885:
        raise ValueError("Неправильный год выпуска.")
    
    if any(record[0] == car_id for record in Car):
        raise ValueError(f"Запись с id={car_id} уже существует.")
     
    new_record: CarRecord = (
        car_id,
        brand.strip(),
        model.strip(),
        age,
        horsepower,
    )
  
    Car.append(new_record)
 
    return new_record

def select_record(
    car_id: int | None = None,
    brand: str | None = None,
    model: str | None = None,
    age: int | None = None,
    horsepower: int | None = None,
) -> list[CarRecord]:

    if (
        car_id is None
        and brand is None
        and model is None
        and age is None
        and horsepower is None
    ):
        return Car.copy()
    
    result: list[CarRecord] = []

    for record in Car:

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
        
        result.append(record)
    return result
