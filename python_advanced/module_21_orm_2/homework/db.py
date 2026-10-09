from datetime import datetime, timedelta, date
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, Date, DateTime, func, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///library_2.db', echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    author = relationship("Author", back_populates="books")
    receiving_books = relationship("ReceivingBook", back_populates="book")

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)
    receiving_books = relationship("ReceivingBook", back_populates="student")
    books = association_proxy('receiving_books', 'book')

    @classmethod
    def get_scholarship_students(cls, session):
        return session.query(cls).filter_by(scholarship=True)

    @classmethod
    def get_high_score_students(cls, session, min_score):
        return session.query(cls).filter(cls.average_score > min_score)

class ReceivingBook(Base):
    __tablename__ = 'receiving_books'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)
    book = relationship("Book", back_populates="receiving_books")
    student = relationship("Student", back_populates="receiving_books")

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return:
            delta = self.date_of_return - self.date_of_issue
        else:
            delta = datetime.now() - self.date_of_issue
        return delta.days

    @count_date_with_book.expression
    def count_date_with_book(cls):
        return func.julianday(func.coalesce(cls.date_of_return, func.now())) - \
               func.julianday(cls.date_of_issue)

def init_test_data():
    """Заполняет БД тестовыми данными"""
    Base.metadata.create_all(engine)
    session = SessionLocal()
    session.query(ReceivingBook).delete()
    session.query(Student).delete()
    session.query(Book).delete()
    session.query(Author).delete()
    session.commit()

    authors = [
        Author(name='Лев', surname='Толстой'),
        Author(name='Фёдор', surname='Достоевский'),
        Author(name='Антон', surname='Чехов')
    ]
    session.add_all(authors)
    session.commit()

    books = [
        Book(name='Война и мир', count=3, release_date=date(1869, 1, 1), author_id=1),
        Book(name='Преступление и наказание', count=2, release_date=date(1866, 1, 1), author_id=2),
        Book(name='Вишнёвый сад', count=5, release_date=date(1904, 1, 1), author_id=3),
        Book(name='Анна Каренина', count=1, release_date=date(1877, 1, 1), author_id=1)
    ]
    session.add_all(books)

    students = [
        Student(name='Валентин', surname='Захаров', phone='+375291234567', email='valentin@example.com',
                average_score=4.5, scholarship=True),
        Student(name='Иван', surname='Иванов', phone='+375291234568', email='ivan@example.com',
                average_score=3.2, scholarship=False),
        Student(name='Мария', surname='Петрова', phone='+375291234569', email='maria@example.com',
                average_score=4.8, scholarship=True)
    ]
    session.add_all(students)

    now = datetime.now()
    session.add_all([
        ReceivingBook(book_id=1, student_id=1, date_of_issue=now - timedelta(days=5)),
        ReceivingBook(book_id=2, student_id=2, date_of_issue=now - timedelta(days=20)),
        ReceivingBook(book_id=3, student_id=3, date_of_issue=now - timedelta(days=3),
                      date_of_return=now - timedelta(days=1))
    ])
    session.commit()
    session.close()
    print("Тестовые данные загружены!")
