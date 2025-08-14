from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from models import Book, db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    books = Book.query.order_by(Book.published_year).all()
    return render_template('index.html', books=books)

@main.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        quantity = int(request.form['quantity'])
        year = int(request.form['published_year'])

        book = Book(title=title, author=author, quantity=quantity, published_year=year)
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_book.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.quantity = int(request.form['quantity'])
        book.published_year = int(request.form['published_year'])
        db.session.commit()
        flash('Book updated successfully!', 'info')
        return redirect(url_for('main.index'))
    return render_template('edit_book.html', book=book)

@main.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'danger')
    return redirect(url_for('main.index'))

def init_routes(app):
    app.register_blueprint(main)
