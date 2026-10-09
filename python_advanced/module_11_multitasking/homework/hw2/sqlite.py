import sqlite3

conn = sqlite3.connect('starwars.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM characters")
print(f"Всего персонажей: {cursor.fetchone()[0]}")

cursor.execute("SELECT id, name, age, gender FROM characters ORDER BY id LIMIT 5")
print("Первые 5:", cursor.fetchall())

conn.close()
