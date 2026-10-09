from flask import Flask, request
from flask_restful import Api, Resource, abort
from marshmallow import ValidationError

from models import (
    init_db, get_all_books, add_book, get_book_by_id, update_book_by_id, delete_book_by_id,
    get_all_authors, add_author, get_author_by_id, get_books_by_author_id, delete_author_by_id
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self):
        return BookSchema().dump(get_all_books(), many=True), 200

    def post(self):
        try:
            book = BookSchema().load(request.json)
            book = add_book(book)
            return BookSchema().dump(book), 201
        except ValidationError as e:
            return e.messages, 400


class BookResource(Resource):
    def get(self, book_id: int):
        """GET /api/books/{id}"""
        book = get_book_by_id(book_id)
        if not book:
            abort(404, message="Book not found")
        return BookSchema().dump(book), 200

    def put(self, book_id: int):
        """PUT /api/books/{id}"""
        try:
            data = request.json
            book = BookSchema().load(data)
            book.id = book_id

            author = get_author_by_id(book.author_id)
            if not author:
                abort(400, message=f"Author ID {book.author_id} not found")

            update_book_by_id(book)
            return BookSchema().dump(book), 200
        except ValidationError as e:
            return e.messages, 400

    def delete(self, book_id: int):
        """DELETE /api/books/{id}"""
        book = get_book_by_id(book_id)
        if not book:
            abort(404, message="Book not found")
        delete_book_by_id(book_id)
        return {}, 204

    def patch(self, book_id: int):
        """PATCH /api/books/{id} — Бонус!"""
        book = get_book_by_id(book_id)
        if not book:
            abort(404, message="Book not found")

        data = request.json or {}

        if 'title' in data:
            book.title = data['title']
        if 'author_id' in data:
            author = get_author_by_id(data['author_id'])
            if not author:
                abort(400, message=f"Author ID {data['author_id']} not found")
            book.author_id = data['author_id']

        update_book_by_id(book)
        return BookSchema().dump(book), 200


class AuthorList(Resource):
    def get(self):
        return AuthorSchema().dump(get_all_authors(), many=True), 200

    def post(self):
        try:
            author = AuthorSchema().load(request.json)
            author = add_author(author)
            return AuthorSchema().dump(author), 201
        except ValidationError as e:
            return e.messages, 400


class AuthorResource(Resource):
    def get(self, author_id: int):
        """GET /api/authors/{id} — книги автора"""
        author = get_author_by_id(author_id)
        if not author:
            abort(404, message="Author not found")

        books = get_books_by_author_id(author_id)
        return {
            "author": AuthorSchema().dump(author),
            "books": BookSchema().dump(books, many=True)
        }, 200

    def delete(self, author_id: int):
        """DELETE /api/authors/{id} — удаление автора + книг (CASCADE!)"""
        author = get_author_by_id(author_id)
        if not author:
            abort(404, message="Author not found")

        delete_author_by_id(author_id)
        return {}, 204


api.add_resource(BookList, '/api/books')
api.add_resource(BookResource, '/api/books/<int:book_id>')
api.add_resource(AuthorList, '/api/authors')
api.add_resource(AuthorResource, '/api/authors/<int:author_id>')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
