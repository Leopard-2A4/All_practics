import sqlite3

DATABASE = 'homework.db'


def answer():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
    sg.group_id,
    COUNT(DISTINCT s.student_id) AS total_students,
    ROUND(AVG(g.grade), 2) AS avg_grade,
    COUNT(DISTINCT CASE WHEN g.grade < 4 THEN s.student_id END) AS failed_students,
    COUNT(CASE WHEN g.date > a.due_date THEN 1 END) AS late_submissions,
    SUM(CASE WHEN g.grade_id IN (
    SELECT grade_id 
    FROM assignments_grades g2 
    WHERE g2.student_id = g.student_id 
    AND g2.assisgnment_id = g.assisgnment_id
    GROUP BY g2.assisgnment_id, g2.student_id
    HAVING COUNT(*) > 1
    ) THEN 1 ELSE 0 END) AS retries
    FROM students_groups sg
    LEFT JOIN students s ON sg.group_id = s.group_id
    LEFT JOIN assignments_grades g ON s.student_id = g.student_id
    LEFT JOIN assignments a ON g.assisgnment_id = a.assisgnment_id
    GROUP BY sg.group_id
    ORDER BY sg.group_id;
    """)

    result = cursor.fetchall()

    for elem in result:
        group_id = elem[0]
        total_students = elem[1]
        avg_grade = elem[2]
        failed_students = elem[3]
        late_submissions = elem[4]
        retries = elem[5]

        print(f"| group_id: {group_id} | total_students: {total_students} "
              f"| avg_grade: {avg_grade} | failed_students: {failed_students} "
              f"| late_submissions: {late_submissions} | retries: {retries}")

if __name__ == '__main__':
    answer()