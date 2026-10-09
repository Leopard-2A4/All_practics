# TODO здесь писать код
import requests
import json


def get_xwing():
    """Находит X-wing и возвращает его данные из swapi.tech."""
    response = requests.get('https://swapi.tech/api/starships/')
    data = response.json()

    for elem in data['results']:
        if elem['name'] == 'X-wing':
            detail_response = requests.get(elem['url'])
            detail_data = detail_response.json()
            ship_data = detail_data['result']['properties']
            print(f"Найден X-wing: {ship_data['name']}")
            return ship_data

    print("X-wing не найден!")
    return None


def find_pilots(ship_data):
    """Находит и детализирует пилотов корабля."""
    pilots = []
    pilots_urls = ship_data.get('pilots', [])
    print(f"Найдено ссылок на пилотов: {len(pilots_urls)}")

    for pilot_url in pilots_urls:
        try:
            pilot_response = requests.get(pilot_url)
            pilot_data = pilot_response.json()['result']['properties']

            # Получаем планету
            planet_response = requests.get(pilot_data['homeworld'])
            planet_data = planet_response.json()['result']['properties']

            pilot_info = {
                "имя": pilot_data['name'],
                "рост": pilot_data['height'],
                "вес": pilot_data['mass'],
                "родная планета": planet_data['name'],
                "ссылка на информацию о родной планете": pilot_data['homeworld']
            }
            pilots.append(pilot_info)
            print(f"Добавлен пилот: {pilot_data['name']}")

        except Exception as e:
            print(f"Ошибка пилота {pilot_url}: {e}")

    return pilots


if __name__ == "__main__":
    ship = get_xwing()
    if ship:
        pilots = find_pilots(ship)

        result = {
            "название": ship['name'],
            "максимальная скорость": ship['max_atmosphering_speed'],
            "класс": ship['starship_class'],
            "список пилотов": pilots
        }

        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))

        with open('xwing_info.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print("\nДанные сохранены в xwing_info.json")
