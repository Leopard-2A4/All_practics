from datetime import datetime
from flask import Flask, jsonify, request
from db import SessionLocal, Book, Student, func, ReceivingBook
from functools import wraps
from sqlalchemy.orm import joinedload, subqueryload
from sqlalchemy import desc
import csv
from io import StringIO

app = Flask(__name__)

def get_db():
    """Dependency: возвращает сессию"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def db_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session = next(get_db())
        try:
            return f(session=session, *args, **kwargs)
        finally:
            pass
    return decorated_function

@app.route('/books', methods=['GET'])
@db_session
def get_books(session):
    """Получить все книги с авторами"""
    books = session.query(Book).options(joinedload(Book.author)).all()
    return jsonify([{
        'id': book.id, 'name': book.name, 'author': book.author.name,
        'count': book.count, 'release_date': book.release_date.isoformat()
    } for book in books])

@app.route('/debtors', methods=['GET'])
@db_session
def get_debtors(session):
    """Должники (>14 дней) с деталями книги/студента"""
    debtors = session.query(ReceivingBook).options(
        joinedload(ReceivingBook.book).joinedload(Book.author),
        joinedload(ReceivingBook.student)
    ).filter(
        func.julianday(func.coalesce(ReceivingBook.date_of_return, func.now())) -
        func.julianday(ReceivingBook.date_of_issue) > 14
    ).all()
    return jsonify([{
        'id': debtor.id, 'book': debtor.book.name, 'author': debtor.book.author.name,
        'student': f"{debtor.student.name} {debtor.student.surname}", 'days': debtor.count_date_with_book
    } for debtor in debtors])

@app.route('/issue_book', methods=['POST'])
@db_session
def issue_book(session):
    """Выдать книгу (POST JSON: {"book_id":1, "student_id":1})"""
    data = request.json
    book = session.query(Book).options(joinedload(Book.author)).get(data['book_id'])
    if not book or book.count <= 0:
        return jsonify({'error': 'Book unavailable'}), 400

    existing = session.query(ReceivingBook).options(joinedload(ReceivingBook.student)).filter_by(
        book_id=data['book_id'], student_id=data['student_id'], date_of_return=None
    ).first()
    if existing:
        return jsonify({'error': f'Already issued to {existing.student.name}'}), 400

    issue = ReceivingBook(book_id=data['book_id'], student_id=data['student_id'], date_of_issue=datetime.now())
    session.add(issue)
    book.count -= 1
    session.commit()
    return jsonify({'message': f'Issued {book.name}'})

@app.route('/return_book', methods=['POST'])
@db_session
def return_book(session):
    """Вернуть книгу (POST JSON: {"book_id":1, "student_id":1})"""
    data = request.json
    record = session.query(ReceivingBook).options(
        joinedload(ReceivingBook.book), joinedload(ReceivingBook.student)
    ).filter_by(book_id=data['book_id'], student_id=data['student_id'], date_of_return=None).first()
    if not record:
        return jsonify({'error': 'No active issue'}), 404

    record.date_of_return = datetime.now()
    record.book.count += 1
    session.commit()
    return jsonify({'message': f'Returned {record.book.name} to {record.student.name}'})

@app.route('/scholarship', methods=['GET'])
@db_session
def scholarship_students(session):
    """Стипендиаты с количеством книг"""
    students = Student.get_scholarship_students(session).options(
        subqueryload(Student.receiving_books).subqueryload(ReceivingBook.book)
    ).all()
    return jsonify([{
        'id': s.id, 'name': f"{s.name} {s.surname}", 'books_count': len(s.receiving_books)
    } for s in students])

@app.route('/high_score/<float:min_score>', methods=['GET'])
@db_session
def high_score_students(session, min_score):
    """Студенты с баллом >= min_score + активные книги (/high_score/4.0)"""
    students = Student.get_high_score_students(session, min_score).options(
        joinedload(Student.receiving_books)
    ).all()
    return jsonify([{
        'id': s.id, 'name': f"{s.name} {s.surname}", 'score': s.average_score,
        'active_books': len([rb for rb in s.receiving_books if not rb.date_of_return])
    } for s in students])

@app.route('/books_by_author/<int:author_id>', methods=['GET'])
@db_session
def books_by_author(session, author_id):
    """Оставшиеся книги по автору"""
    total = session.query(func.sum(Book.count)).filter(Book.author_id == author_id).scalar() or 0
    return jsonify({'remaining_books': total})

@app.route('/unread_by_author/<int:student_id>', methods=['GET'])
@db_session
def unread_by_author(session, student_id):
    """Книги автора, которые студент не читал (но другие брал), count>0 (/unread_by_author/1)"""
    taken_books = session.query(ReceivingBook.book_id).filter(ReceivingBook.student_id == student_id).subquery()
    author_ids = session.query(Book.author_id.distinct()).join(taken_books).subquery()
    unread = session.query(Book).filter(
        Book.author_id.in_(author_ids),
        ~Book.id.in_(taken_books),
        Book.count > 0
    ).options(joinedload(Book.author)).all()
    return jsonify([{'id': b.id, 'title': b.name, 'author': b.author.name} for b in unread])

@app.route('/avg_books_month', methods=['GET'])
@db_session
def avg_books_month(session):
    """Среднее количество выдач в текущем месяце"""
    month = func.strftime('%Y-%m', func.now())
    total_issues = session.query(func.count(ReceivingBook.id)).filter(
        func.strftime('%Y-%m', ReceivingBook.date_of_issue) == month
    ).scalar()
    avg = total_issues / session.query(func.count(Student.id)).scalar() if total_issues else 0
    return jsonify({'avg_books_this_month': float(avg)})

@app.route('/popular_high_score', methods=['GET'])
@db_session
def popular_high_score(session):
    """Самая популярная книга у студентов >4.0"""
    pop_book = session.query(ReceivingBook.book_id, func.count().label('issues')).join(Student).filter(
        Student.average_score > 4.0
    ).group_by(ReceivingBook.book_id).order_by(desc(func.count())).first()
    return jsonify({'popular_book_id': pop_book[0], 'issues': pop_book[1]} if pop_book else {})

@app.route('/top_students_year', methods=['GET'])
@db_session
def top_students_year(session):
    """ТОП-10 студентов по книгам в году"""
    year_start = datetime(datetime.now().year, 1, 1)
    top = session.query(Student.id, Student.name, Student.surname, func.count(ReceivingBook.id).label('books')).\
        outerjoin(ReceivingBook).filter(ReceivingBook.date_of_issue >= year_start).\
        group_by(Student.id, Student.name, Student.surname).order_by(desc(func.count())).limit(10).all()
    return jsonify([{'id': t[0], 'name': f"{t[1]} {t[2]}", 'books': t[3]} for t in top])


@app.route('/upload_students', methods=['POST'])
@db_session
def upload_students(session):
    """Загрузка студентов из CSV (multipart file, delimiter ';')"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400

    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'Empty file'}), 400

    data = file.read().decode('utf-8')
    reader = csv.DictReader(StringIO(data), delimiter=';')

    mappings = []
    for row in reader:
        row = dict(row)
        row['average_score'] = float(row['average_score'])
        row['scholarship'] = row['scholarship'].lower() in ('true', '1', 'yes', 'on')
        mappings.append(row)

    session.bulk_insert_mappings(Student, mappings)
    session.commit()
    return jsonify({'inserted': len(mappings), 'students': mappings})
