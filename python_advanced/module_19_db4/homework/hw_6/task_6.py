import sqlite3

DATABASE = 'homework.db'


def answer():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT ROUND(AVG(g.grade), 2) AS avg_reading_score
    FROM assignments_grades g
    JOIN assignments a ON g.assisgnment_id = a.assisgnment_id
    WHERE a.assignment_text LIKE '%прочитать%' 
    OR a.assignment_text LIKE '%выучить%' 
    OR a.assignment_text LIKE '%изучить%';
    """)

    result = cursor.fetchall()

    print("Average mark of reading:", result[0][0])


if __name__ == '__main__':
    answer()
