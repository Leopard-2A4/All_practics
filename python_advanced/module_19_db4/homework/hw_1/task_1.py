import sqlite3

DATABASE = 'homework.db'

def answer():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""SELECT t.full_name AS "преподаватель",
        ROUND(AVG(g.grade), 2) AS "средняя_оценка"
        FROM teachers t
        JOIN students_groups sg ON t.teacher_id = sg.teacher_id
        JOIN assignments a ON sg.group_id = a.group_id AND t.teacher_id = a.teacher_id
        JOIN assignments_grades g ON a.assisgnment_id = g.assisgnment_id
        GROUP BY t.teacher_id, t.full_name
        ORDER BY AVG(g.grade) ASC
        LIMIT 1;""")

    result = cursor.fetchall()

    print("Strict teacher:",result[0][0])

if __name__ == '__main__':
   answer()