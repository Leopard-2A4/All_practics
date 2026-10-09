import sqlite3
from typing import Any, Optional, List

DATA: List[dict] = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy'},
]


class Book:

    def __init__(self, id: int, title: str, author: str, views: int) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.views: int = views

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_books'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()

        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `table_books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, 
                    author TEXT,
                    views INTEGER DEFAULT 0
                )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `table_books` (title, author, views) 
                VALUES (?, ?, 0)
                """,
                [(item['title'], item['author']) for item in initial_records]
            )
        else:
            cursor.execute(
                """
                PRAGMA table_info(table_books)
                """
            )
            columns = [col[1] for col in cursor.fetchall()]
            if 'views' not in columns:
                cursor.execute(
                    """
                    ALTER TABLE table_books ADD COLUMN views INTEGER DEFAULT 0
                    """
                )
                conn.commit()


def get_all_books() -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_books`
            """
        )
        return [Book(*row) for row in cursor.fetchall()]

def create_book(title: str, author: str) -> None:
    """Добавляет новую книгу в БД."""
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO `table_books` (title, author) 
            VALUES (?, ?)
            """,
            (title, author)
        )
        conn.commit()

def get_books_by_author(author_name: str) -> List[Book]:
    """Возвращает все книги указанного автора."""
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM `table_books` 
            WHERE LOWER(author) = LOWER(?)
            """,
            (author_name,)
        )
        return [Book(*row) for row in cursor.fetchall()]

def increment_views(book_id: int) -> None:
    """Увеличивает счётчик просмотров книги."""
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE `table_books` SET views = views + 1 
            WHERE id = ?
            """,
            (book_id,)
        )
        conn.commit()

def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("SELECT * FROM `table_books` WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        return Book(*row) if row else None