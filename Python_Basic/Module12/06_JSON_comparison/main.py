# TODO здесь писать код
import json


def compare_json_diff(old_file: str, new_file: str, diff_list: list) -> dict:
    """
    Сравнивает JSON файлы и возвращает изменения только для указанных ключей.
    Args:
        old_file: Путь к старому JSON файлу
        new_file: Путь к новому JSON файлу
        diff_list: Список ключей для отслеживания
    Returns:
        Словарь {параметр: новое_значение} для изменившихся ключей
    """
    with open(old_file, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    with open(new_file, 'r', encoding='utf-8') as f:
        new_data = json.load(f)

    old_data = old_data['data']
    new_data = new_data['data']

    result = {}

    for key in diff_list:
        old_value = old_data.get(key)
        new_value = new_data.get(key)

        if old_value != new_value:
            result[key] = new_value
            print(f"'{key}' изменился: {old_value} → {new_value}")

    return result


if __name__ == "__main__":
    diff_list = ["services", "staff", "datetime"]

    result = compare_json_diff('json_old.json', 'json_new.json', diff_list)

    print("\nИтоговые изменения:")
    print(result)

    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\nРезультат сохранён в result.json")