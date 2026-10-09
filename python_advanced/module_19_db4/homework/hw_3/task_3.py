import sqlite3

DATABASE = 'homework.db'
def answer():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT DISTINCT s.full_name
    FROM students s
    JOIN assignments_grades g ON s.student_id = g.student_id
    JOIN assignments a ON g.assisgnment_id = a.assisgnment_id
    WHERE a.teacher_id = (
    SELECT t.teacher_id
    FROM teachers t
    JOIN students_groups sg ON t.teacher_id = sg.teacher_id
    JOIN assignments a2 ON sg.group_id = a2.group_id AND t.teacher_id = a2.teacher_id
    JOIN assignments_grades g2 ON a2.assisgnment_id = g2.assisgnment_id
    GROUP BY t.teacher_id
    ORDER BY AVG(g2.grade) DESC
    LIMIT 1
    )
    ORDER BY s.full_name;
    """)

    result = cursor.fetchall()

    print("Kind teacher:", result[0][0])

if __name__ == '__main__':
   answer()