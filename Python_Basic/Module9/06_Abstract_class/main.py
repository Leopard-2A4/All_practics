# TODO здесь писать код
import math

class Shape:
    def area(self):
        pass

    """
    Абстрактный класс для геометрических фигур.
    Содержит абстрактный метод area, который должен быть реализован в подклассах.
    """

class Rectangle(Shape):
    def __init__(self, width:float, height:float)-> None:
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height
    """
    Класс:
       Принимает длинну и высоту прямоугольника
       Метод:
          Возвращает значение площади прямоугольника
    """

class Circle(Shape):
    def __init__(self, radius:float)-> None:
        self.radius = radius

    def area(self):
        return round(math.pi * self.radius ** 2,1)
    """
    Класс:
       Принимает радиус круга
    :returns 
       значение площади круга
    """

class Triangle(Shape):
    def __init__(self, width:float, height:float)-> None:
        self.width = width
        self.height = height

    def area(self):
        return round((self.width * self.height) / 2,1)

    """
    Класс:
       Принимает длинну и высоту треугольника
    :returns 
       Возвращает значение площади треугольника
    """

# Примеры работы с классом:
# Создание экземпляров классов
prt = Shape
circle = Circle(5)
rectangle = Rectangle(4, 6)
triangle = Triangle(3, 8)

# Вычисление площади фигур
circle_area = circle.area()
rectangle_area = rectangle.area()
triangle_area = triangle.area()

# Вывод результатов
print("Площадь круга:", circle_area)
print("Площадь прямоугольника:", rectangle_area)
print("Площадь треугольника:", triangle_area)