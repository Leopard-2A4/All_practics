# TODO здесь писать код
import random

class Player:
    def __init__(self, name, health=100):
        self.name = name
        self.health = health

    def attack(self, enemy):
        if self.health > 0:
            damage = 20
            enemy.health -= damage
            print(f'{self.name} attacks {enemy.name} and deals {damage} damage.')
        else:
            print(f'{self.name} cannot attack, he is defeated.')


def battle(unit_1, unit_2):
    while unit_1.health > 0 and unit_2.health > 0:
        choose = random.randint(1, 2)
        if choose == 1:
            unit_1.attack(unit_2)
        else:
            unit_2.attack(unit_1)
        print(f'{unit_1.name}: {unit_1.health} HP | {unit_2.name}: {unit_2.health} HP\n')

    if unit_1.health <= 0:
        print(f'{unit_2.name} is winner!')
    else:
        print(f'{unit_1.name} is winner!')

unit_1 = Player('unit_1')
unit_2 = Player('unit_2')
battle(unit_1, unit_2)