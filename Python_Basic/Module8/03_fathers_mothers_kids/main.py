# TODO здесь писать код
class Parent():
    def __init__(self, name,age,children):
        self.name = name
        self.age = age
        self.children = []
    def print_info(self):
        print(
            f'Имя родителя: {self.name}, Возраст: {self.age}, Список детей: {[child.name for child in self.children]}')

    def feed(self,child):
        if child.hungry:
           child.hungry = False
           print(f'Ребёнок {child.name} сыт')
        else:
            print(f'Ребёнок {child.name} недавно поел')

    def be_silent(self,child):
        if child.silent == False:
           child.silent = True
           print(f'Ребёнок {child.name} успокоился')
        else:
            print(f'Ребёнок {child.name} уже спокоен')


class Child():
    def __init__(self, name,age, hungry, silent):
        self.name = name
        self.age = age
        self.hungry = True
        self.silent = False


child_1 = Child('Ксения',10, True, False)
child_2 = Child('Пётр',16, False, True)
parent_1 = Parent('Василий',26, [])

for child in [child_1, child_2]:
    age_difference = parent_1.age - child.age
    if age_difference >= 16:
        parent_1.children.append(child)

print(f"{parent_1.name} имеет детей: {[child.name for child in parent_1.children]}")
for child in parent_1.children:
    parent_1.feed(child)
    parent_1.be_silent(child)
parent_1.print_info()