import sqlite3

DATABASE = 'homework.db'
def answer():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
    s.full_name AS "ученик",
    ROUND(AVG(g.grade), 2) AS "средний_балл"
    FROM students s
    JOIN assignments_grades g ON s.student_id = g.student_id
    GROUP BY s.student_id, s.full_name
    ORDER BY AVG(g.grade) DESC
    LIMIT 10;
        """)
    result = cursor.fetchall()

    print("Top 10 of students:\n")
    print("="*20)

    for student in result:
        print(student[0],student[1])
        print("=" * 20)

if __name__ == '__main__':
   answer()