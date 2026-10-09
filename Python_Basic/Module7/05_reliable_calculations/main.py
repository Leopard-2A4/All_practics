# TODO здесь писать код

# Здесь создайте функцию get_sage_sqrt
def get_sage_sqrt(value):
    import math
    try:
        if not isinstance(value, (int, float)):
            raise TypeError("Ожидается число (int или float)")
        if value < 0:
            raise ValueError("Нельзя вычислить квадратный корень отрицательного числа")
        return math.sqrt(value)
    except ValueError as exc:
        print(f"Ошибка значения: {exc}")
        return None
    except TypeError as exc:
        print(f"Ошибка типа: {exc}")
        return None
    except Exception as exc:
        print(f"Неизвестная ошибка: {exc}")
        return None
# Тестовые случаи
numbers = [16, 25, -9, 0, 4.5, "abc"]
for number in numbers:
    result = get_sage_sqrt(number)
    print(f"Квадратный корень numbers {number}: {result}")