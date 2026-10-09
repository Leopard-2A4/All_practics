from datetime import datetime
from flask import Flask, jsonify, request
from db import SessionLocal, Book, Student, func, ReceivingBook
from functools import wraps

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
    books = session.query(Book).all()
    return jsonify([{'id': book.id, 'name': book.name, 'count': book.count,
                     'release_date': book.release_date.isoformat()} for book in books])


@app.route('/debtors', methods=['GET'])
@db_session
def get_debtors(session):
    debtors = session.query(ReceivingBook).filter(
        func.julianday(func.coalesce(ReceivingBook.date_of_return, func.now())) -
        func.julianday(ReceivingBook.date_of_issue) > 14
    ).all()
    return jsonify([{
        'id': debtor.id, 'book_id': debtor.book_id, 'student_id': debtor.student_id,
        'days': debtor.count_date_with_book
    } for debtor in debtors])


@app.route('/issue_book', methods=['POST'])
@db_session
def issue_book(session):
    data = request.json
    book = session.query(Book).get(data['book_id'])
    if not book or book.count <= 0:
        return jsonify({'error': 'Book unavailable'}), 400

    existing = session.query(ReceivingBook).filter_by(
        book_id=data['book_id'], student_id=data['student_id'], date_of_return=None
    ).first()
    if existing:
        return jsonify({'error': 'Already issued'}), 400

    issue = ReceivingBook(
        book_id=data['book_id'],
        student_id=data['student_id'],
        date_of_issue=datetime.now()
    )
    session.add(issue)
    book.count -= 1
    session.commit()
    return jsonify({'message': 'Issued'})


@app.route('/return_book', methods=['POST'])
@db_session
def return_book(session):
    data = request.json
    record = session.query(ReceivingBook).filter_by(
        book_id=data['book_id'], student_id=data['student_id'], date_of_return=None
    ).first()
    if not record:
        return jsonify({'error': 'No active issue'}), 404

    record.date_of_return = datetime.now()
    book = session.query(Book).get(data['book_id'])
    book.count += 1
    session.commit()
    return jsonify({'message': 'Returned'})


@app.route('/scholarship', methods=['GET'])
@db_session
def scholarship_students(session):
    students = Student.get_scholarship_students(session)
    return jsonify([{'id': elem.id, 'name': f"{elem.name} {elem.surname}"} for elem in students])


@app.route('/high_score/<float:min_score>', methods=['GET'])
@db_session
def high_score_students(session, min_score):
    students = Student.get_high_score_students(session, min_score)
    return jsonify([{'id': elem.id, 'name': f"{elem.name} {elem.surname}", 'score': elem.average_score} for elem in students])
