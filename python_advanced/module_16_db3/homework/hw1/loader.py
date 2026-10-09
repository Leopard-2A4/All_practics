import sqlite3

with open('create_schema.sql', 'r') as sql_file:
    sql_script: str = sql_file.read()

with sqlite3.connect('sql_request.db') as conn:
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
