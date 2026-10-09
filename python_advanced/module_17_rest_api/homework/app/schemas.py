from marshmallow import Schema, fields, validates, ValidationError, post_load
from models import get_book_by_title, Book, Author

class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str()

    @post_load
    def make_author(self, data):
        return Author(**data)

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author_id = fields.Int(required=True)

    @validates('title')
    def validate_title(self, title: str):
        existing_book = get_book_by_title(title)
        if existing_book:
            raise ValidationError(f'Book "{title}" already exists')

    @post_load
    def make_book(self, data):
        return Book(**data)

class BookSchemaWithAuthor(BookSchema):
    """Книга с данными автора"""
    author = fields.Nested(AuthorSchema, only=('id', 'first_name', 'last_name'))