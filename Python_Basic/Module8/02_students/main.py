# TODO здесь писать код
class Student:
    def __init__(self, name, group_number, grades):
        self.name = name
        self.group_number = group_number
        self.grades = grades
        self.average = round(sum(grades) / 5, 1)

    def __repr__(self):
        return f"{self.name}, группа {self.group_number}, средний балл: {self.average}"

    def print_sorted(students):
        sorted_students = sorted(students, key=lambda student: student.average, reverse=True)
        for student in sorted_students:
            print(student)


students = [
    Student('Иванов Иван', 1, [5, 6, 7, 4, 3]),
    Student('Сидоров Пётр', 2, [7, 8, 7, 7, 8]),
    Student('Андреева Ольга', 3, [9, 6, 8, 7, 9]),
    Student('Соловей Василий', 4, [5, 6, 7, 6, 7]),
    Student('Быков Пётр', 5, [8, 6, 7, 9, 7]),
    Student('Абубамир Кашмир', 6, [5, 5, 4, 5, 5]),
    Student('Ян Синцзин', 7, [7, 6, 7, 5, 6]),
    Student('Сидорова Валерия', 8, [7, 6, 7, 6, 6]),
    Student('Иванова Ксения', 9, [9, 10, 9, 8, 10]),
    Student('Нет Идей', 10, [9, 9, 8, 8, 9])
]

Student.print_sorted(students)