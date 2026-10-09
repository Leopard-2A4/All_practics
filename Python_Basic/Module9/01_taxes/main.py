# TODO здесь писать код
class Property:
    """
    Базовый класс для имущества.
    Хранит стоимость объекта и предоставляет абстрактный метод для расчёта налога.
    """
    def __init__(self, worth: float) -> None:
        """
        Инициализирует объект имущества.
        :param worth: Стоимость имущества.
        """
        self.worth: float = worth

    def calculate_tax(self) -> float:
        """
        Метод для расчёта налога. Должен быть переопределён в подклассах.
        :raises NotImplementedError: Если метод не переопределён.
        :return: Налог на имущество.
        """
        raise NotImplementedError("Метод должен быть переопределён в дочернем классе")


class Apartment(Property):
    """
    Класс для квартиры.
    Наследуется от Property и реализует расчёт налога для квартиры.
    """
    def __init__(self, worth: float) -> None:
        """
        Инициализирует объект квартиры.
        :param worth: Стоимость квартиры.
        """
        super().__init__(worth)

    def calculate_tax(self) -> float:
        """
        Рассчитывает налог на квартиру (1/1000 от стоимости).
        :return: Налог на квартиру.
        """
        return self.worth / 1000


class Car(Property):
    """
    Класс для машины.
    Наследуется от Property и реализует расчёт налога для машины.
    """
    def __init__(self, worth: float) -> None:
        """
        Инициализирует объект машины.
        :param worth: Стоимость машины.
        """
        super().__init__(worth)

    def calculate_tax(self) -> float:
        """
        Рассчитывает налог на машину (1/200 от стоимости).
        :return: Налог на машину.
        """
        return self.worth / 200


class CountryHouse(Property):
    """
    Класс для дачи.
    Наследуется от Property и реализует расчёт налога для дачи.
    """
    def __init__(self, worth: float) -> None:
        """
        Инициализирует объект дачи.
        :param worth: Стоимость дачи.
        """
        super().__init__(worth)

    def calculate_tax(self) -> float:
        """
        Рассчитывает налог на дачу (1/500 от стоимости).
        :return: Налог на дачу.
        """
        return self.worth / 500


def main() -> None:
    """
    Основная функция программы.
    Запрашивает у пользователя стоимость имущества и количество денег,
    рассчитывает налоги и выводит результаты.
    """
    money: float = float(input("Введите количество ваших денег: "))
    apartment_worth: float = float(input("Введите стоимость квартиры: "))
    car_worth: float = float(input("Введите стоимость машины: "))
    house_worth: float = float(input("Введите стоимость дачи: "))

    apartment: Apartment = Apartment(apartment_worth)
    car: Car = Car(car_worth)
    house: CountryHouse = CountryHouse(house_worth)

    total_tax: float = apartment.calculate_tax() + car.calculate_tax() + house.calculate_tax()
    print(f"Налог на квартиру: {apartment.calculate_tax()}")
    print(f"Налог на машину: {car.calculate_tax()}")
    print(f"Налог на дачу: {house.calculate_tax()}")
    print(f"Общий налог: {total_tax}")

    if money >= total_tax:
        print("Денег хватает на оплату налога.")
    else:
        print(f"Денег не хватает. Нужно ещё: {total_tax - money}")


main()