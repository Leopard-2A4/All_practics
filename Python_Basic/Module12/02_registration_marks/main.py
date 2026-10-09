# TODO здесь писать код
import re

cars = 'А578ВЕ777 ОР233787 К901МН666 СТ46599 СНИ2929П777 666АМР666'

per_pattern = re.compile(r'\b[АВЕКМНОРСТУХ]\d{3}[АВЕКМНОРСТУХ]{2}\d{3}\b')  # Частные авто
tax_pattern = re.compile(r'\b[АВЕКМНОРСТУХ]{2}\d+\b')
print('Список номеров частных автомобилей:',per_pattern.findall(cars))
print('Список номеров такси: ',tax_pattern.findall(cars))