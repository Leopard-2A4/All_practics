from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length

class BookForm(FlaskForm):
    book_title = StringField(
        'Book title',
        validators=[InputRequired(message='Название обязательно!')]
    )
    author_name = StringField(
        'Author name',
        validators=[InputRequired(message='Автор обязателен!')]
    )
    submit = SubmitField('Add new book')