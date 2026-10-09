import sqlite3

DATABASE = 'homework.db'


def answer():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
    sg.group_id,
    ROUND(AVG(late_count.late_count), 2) AS avg_late,
    MAX(late_count.late_count) AS max_late,
    MIN(late_count.late_count) AS min_late
    FROM students_groups sg
    JOIN students s ON sg.group_id = s.group_id
    LEFT JOIN (
    SELECT 
        g.student_id,
        COUNT(*) AS late_count
    FROM assignments_grades g
    JOIN assignments a ON g.assisgnment_id = a.assisgnment_id
    WHERE g.date > a.due_date  -- Просрочка
    GROUP BY g.student_id
    ) late_count ON s.student_id = late_count.student_id
    GROUP BY sg.group_id
    ORDER BY sg.group_id;
    """)

    result = cursor.fetchall()

    for elem in result:
        classes = elem[0]
        average = elem[1]
        maximum = elem[2]
        minimum = elem[3]
        print(f"| Class: {classes}, Ave: {average}, Max: {maximum}, Min: {minimum} |")


if __name__ == '__main__':
    answer()