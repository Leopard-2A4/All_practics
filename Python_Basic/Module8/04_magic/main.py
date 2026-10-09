# TODO здесь писать код
class Water:
    def __add__(self, other):
        if isinstance(other, Air):
            return Storm()
        elif isinstance(other, Fire):
            return Steam()
        elif isinstance(other, Earth):
            return Mud()
        elif isinstance(other, Gravity):
            return Ice_10()
        return None

class Air:
    def __add__(self, other):
        if isinstance(other, Water):
            return Storm()
        elif isinstance(other, Fire):
            return Lightning()
        elif isinstance(other, Earth):
            return Dust()
        elif isinstance(other, Gravity):
            return Star()
        return None

class Fire:
    def __add__(self, other):
        if isinstance(other, Water):
            return Steam()
        elif isinstance(other, Air):
            return Lightning()
        elif isinstance(other, Earth):
            return Lava()
        return None

class Earth:
    def __add__(self, other):
        if isinstance(other, Water):
            return Mud()
        elif isinstance(other, Air):
            return Dust()
        elif isinstance(other, Fire):
            return Lava()
        return None

class Gravity:
    def __add__(self, other):
        if isinstance(other, Water):
            return Ice_10()
        elif isinstance(other, Vacuum):
            return Gravastar()
        elif isinstance(other, Air):
            return Star()
        return None

class Vacuum:
    n = 0
    #вакуум работает только с гравитацией

class Storm:
    answer = 'Шторм'

class Steam:
    answer = 'Пар'

class Mud:
    answer = 'Грязь'

class Lightning:
    answer = 'Молния'

class Dust:
    answer = 'Пыль'

class Lava:
    answer = 'Лава'

class Ice_10:
    answer = ('Лёд X (крайне плотный лёд образующийся при высоком давлении,'
              ' является одной из модификации обычного льда)')

class Gravastar:
    answer = ('Gravastar (теоритический астрономический объект.\n'
              'Свойство "поглощения" гравастара схожи с чёрной дырой,\n'
              'но при этом это два разных объекта.')

class Star:
    answer = ('Звезда (при сильном сжатии под действием\n'
              'большой массы водорода или гелия, образуется Звезда)')
# Пример использования
water = Water()
air = Air()
fire = Fire()
earth = Earth()
gravity = Gravity()
vacuum = Vacuum()


print((water + air).answer)
print((water + fire).answer)
print((water + earth).answer)
print((air + fire).answer)
print((air + earth).answer)
print((fire + earth).answer)
print((gravity + water).answer)
print((gravity + vacuum).answer)
print((gravity + air).answer)