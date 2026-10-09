import sqlite3
from pathlib import Path


def print_header(title: str, separator: str = "═"):
    print(f"\n{separator * 80}")
    print(f"{title}")
    print(f"{separator * 80}")


def run_query(db_path: str, sql_file: str, title: str):
    """Запускает SQL-запрос и выводит результат"""
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql = f.read()

            cursor = conn.execute(sql)
            rows = cursor.fetchall()

            print_header(title)

            if rows:
                headers = [desc[0] for desc in cursor.description]
                print(" | ".join(headers))
                print("-" * (sum(len(h) for h in headers) + len(headers) * 3))

                for row in rows[:10]:
                    print(" | ".join(str(row[key]) for key in headers))
                if len(rows) > 10:
                    print(f"... и еще {len(rows) - 10} строк")
            else:
                print("Нет данных")

    except Exception as e:
        print(f"Ошибка в {sql_file}: {e}")


def main():
    db_path = "/home/artem/PycharmProjects/python_advanced/module_16_db3/homework/hw.db"

    if not Path(db_path).exists():
        print(f"База {db_path} не найдена!")
        print("Запусти: python generate_hw_database.py")
        return

    queries = [
        ("2_1.sql", "Вся информация о заказах"),
        ("2_2.sql", "Покупатели без заказов"),
        ("2_3.sql", "Разные города"),
        ("2_4.sql", "Заказы без менеджеров"),
        ("2_5.sql", "Пары покупателей (бонус)")
    ]

    for sql_file, title in queries:
        if Path(sql_file).exists():
            run_query(db_path, sql_file, title)
        else:
            print(f"Файл {sql_file} не найден")


if __name__ == "__main__":
    main()
