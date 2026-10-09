# TODO здесь писать код
import random

class House:
    def __init__(self):
        self.food = 50
        self.money = 0

class Human:
    def __init__(self, name, house):
        self.name = name
        self.satiety = 50
        self.house = house
        self.alive = True

    def eat(self):
        if self.house.food > 0:
            self.satiety += 10
            self.house.food -= 10
        else:
            print(f"{self.name} не может поесть: нет еды.")

    def work(self):
        self.satiety -= 10
        self.house.money += 50

    def play(self):
        self.satiety -= 10

    def go_shopping(self):
        if self.house.money >= 50:
            self.house.food += 50
            self.house.money -= 50
        else:
            print(f"{self.name} не может сходить в магазин: недостаточно денег.")

    def live_one_day(self):
        if not self.alive:
            return
        dice = random.randint(1, 6)
        if self.satiety < 20:
            self.eat()
        elif self.house.food < 10:
            self.go_shopping()
        elif self.house.money < 50:
            self.work()
        elif dice == 1:
            self.work()
        elif dice == 2:
            self.eat()
        else:
            self.play()

        if self.satiety <= 0:
            self.alive = False
            print(f"{self.name} умер от голода.")

    def status(self):
        return f"{self.name}: сытость={self.satiety}, еда={self.house.food}, деньги={self.house.money}"

house = House()
person1 = Human("Артём", house)
person2 = Human("Марина", house)

for day in range(1, 366):
    print(f"\nДень {day}")
    person1.live_one_day()
    person2.live_one_day()
    print(person1.status())
    print(person2.status())

    if not person1.alive and not person2.alive:
        print("Оба умерли.")
        break

print("\nЭксперимент завершён.")
