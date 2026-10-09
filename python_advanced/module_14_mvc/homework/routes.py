from flask import Flask, render_template, redirect, url_for, flash
from typing import List
from forms import BookForm
from models import init_db, get_all_books, DATA, create_book, get_books_by_author, increment_views, get_book_by_id

app: Flask = Flask(__name__)
app.secret_key = 'super-secret-dev-key-12345'
app.config['WTF_CSRF_ENABLED'] = False

def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</td>
        <th>Title</td>
        <th>Author</td>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ''
    for book in books:
        rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


@app.route('/books')
def all_books():
    books = get_all_books()
    for book in books:
        increment_views(book.id)
    return render_template('index.html', books=books)


@app.route('/books/id/<int:book_id>')
def book_detail(book_id: int):
    book = get_book_by_id(book_id)
    if not book:
        return "Книга не найдена", 404

    increment_views(book_id)

    return render_template('book_detail.html', book=book)


@app.route('/books/form', methods=['GET', 'POST'])
def books_form():
    form = BookForm()

    if form.validate_on_submit():
        create_book(form.book_title.data, form.author_name.data)
        flash('Книга добавлена!')
        return redirect(url_for('all_books'))

    return render_template('add_book.html', form=form)

@app.route('/author/<author_name>')
def books_by_author(author_name: str):
    author_books = get_books_by_author(author_name)
    return render_template(
        'author_books.html',
        author_name=author_name,
        books=author_books
    )

if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
