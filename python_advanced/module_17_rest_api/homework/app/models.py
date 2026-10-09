import sqlite3
from dataclasses import dataclass
from typing import Optional, List

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE = 'books'
AUTHORS_TABLE = 'authors'


@dataclass
class Author:
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    middle_name: str = ""


@dataclass
class Book:
    id: Optional[int] = None
    title: str = ""
    author_id: int = 0


def init_db():
    """Создает БД + заполняет начальными данными"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS `{AUTHORS_TABLE}` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            middle_name TEXT
        )
    """)

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS `{BOOKS_TABLE}` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES `{AUTHORS_TABLE}`(id) ON DELETE CASCADE,
            UNIQUE(title)
        )
    """)

    authors_data = [
        ("Swaroop", "C. H.", ""),
        ("Herman", "Melville", ""),
        ("Leo", "Tolstoy", "")
    ]
    cursor.executemany(
        f"INSERT OR IGNORE INTO `{AUTHORS_TABLE}` (first_name, last_name, middle_name) VALUES (?, ?, ?)",
        authors_data
    )

    books_data = [
        ("A Byte of Python", 1),
        ("Moby-Dick", 2),
        ("War and Peace", 3)
    ]
    cursor.executemany(
        f"INSERT OR IGNORE INTO `{BOOKS_TABLE}` (title, author_id) VALUES (?, ?)",
        books_data
    )

    conn.commit()
    conn.close()


def get_all_authors() -> List[Author]:
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM `{AUTHORS_TABLE}`")
    authors = [Author(id=r[0], first_name=r[1], last_name=r[2], middle_name=r[3])
               for r in cursor.fetchall()]
    conn.close()
    return authors


def add_author(author: Author) -> Author:
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO `{AUTHORS_TABLE}` (first_name, last_name, middle_name) VALUES (?, ?, ?)",
        (author.first_name, author.last_name, author.middle_name)
    )
    author.id = cursor.lastrowid
    conn.commit()
    conn.close()
    return author


def get_all_books() -> List[Book]:
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, title, author_id FROM `{BOOKS_TABLE}`")
    books = [Book(id=r[0], title=r[1], author_id=r[2]) for r in cursor.fetchall()]
    conn.close()
    return books


def get_book_by_title(title: str) -> Optional[Book]:
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, title, author_id FROM `{BOOKS_TABLE}` WHERE title = ?", (title,))
    row = cursor.fetchone()
    conn.close()
    return Book(id=row[0], title=row[1], author_id=row[2]) if row else None


def add_book(book: Book) -> Book:
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO `{BOOKS_TABLE}` (title, author_id) VALUES (?, ?)",
        (book.title, book.author_id)
    )
    book.id = cursor.lastrowid
    conn.commit()
    conn.close()
    return book

def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, title, author_id FROM `{BOOKS_TABLE}` WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        if row:
            return Book(id=row[0], title=row[1], author_id=row[2])
        return None

def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE `{BOOKS_TABLE}` SET title = ?, author_id = ? WHERE id = ?",
            (book.title, book.author_id, book.id)
        )
        conn.commit()

def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM `{BOOKS_TABLE}` WHERE id = ?", (book_id,))
        conn.commit()

def get_author_by_id(author_id: int) -> Optional[Author]:
    """Получить автора по ID"""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `{AUTHORS_TABLE}` WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        if row:
            return Author(
                id=row[0],
                first_name=row[1],
                last_name=row[2],
                middle_name=row[3] if len(row) > 3 else ""
            )
        return None


def get_books_by_author_id(author_id: int) -> List[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(
            f"SELECT id, title, author_id FROM `{BOOKS_TABLE}` WHERE author_id = ?",
            (author_id,)
        )
        rows = cursor.fetchall()

        books = [Book(id=r[0], title=r[1], author_id=r[2]) for r in rows]
        return books

def delete_author_by_id(author_id: int) -> None:
    """Удаление автора (книги удалятся CASCADE)"""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM `{AUTHORS_TABLE}` WHERE id = ?", (author_id,))
        conn.commit()