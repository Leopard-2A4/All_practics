students = {
    1: {
        'name': 'Bob',
        'surname': 'Vazovski',
        'age': 23,
        'interests': ['biology, swimming']
    },
    2: {
        'name': 'Rob',
        'surname': 'Stepanov',
        'age': 24,
        'interests': ['math', 'computer games', 'running']
    },
    3: {
        'name': 'Alexander',
        'surname': 'Krug',
        'age': 22,
        'interests': ['languages', 'health food']
    }
}
# TODO исправить код

def get_interests_and_surnames_length(students_dict):
    all_interests = set()
    total_surnames_length = 0
    for student in students_dict.values():
        all_interests.update(student['interests'])
        total_surnames_length += len(student['surname'])
    return all_interests, total_surnames_length

student_age_pairs = [(student_id, info['age']) for student_id, info in students.items()]

interests, surnames_length = get_interests_and_surnames_length(students)

print("Список пар «ID студента — возраст»:", student_age_pairs)
print("Полный список интересов всех студентов:", interests)
print("Общая длина всех фамилий студентов:", surnames_length)
