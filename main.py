
from flask import Flask, render_template, request, redirect,     url_for

app = Flask(__name__)


class Book:
    def __init__(self, title, author, category):
        self.title = title
        self.author = author
        self.category = category


book_list = [
    Book("1984", "George Orwell", "Dystopian"),
    Book("To Kill a Mockingbird", "Harper Lee", "Classic"),
    Book("The Great Gatsby", "F. Scott Fitzgerald", "Classic"),
    Book("Brave New World", "Aldous Huxley", "Dystopian"),
    Book("Moby Dick", "Herman Melville", "Adventure"),
    Book("Pride and Prejudice", "Jane Austen", "Romance"),
    Book("The Hobbit", "J.R.R. Tolkien", "Fantasy"),
    Book("Fahrenheit 451", "Ray Bradbury", "Dystopian"),
    Book("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy"),
    Book("The Catcher in the Rye", "J.D. Salinger", "Classic"),
    Book("The Lord of the Rings", "J.R.R. Tolkien", "Fantasy"),
    Book("Crime and Punishment", "Fyodor Dostoevsky", "Philosophical"),
    Book("The Brothers Karamazov", "Fyodor Dostoevsky", "Philosophical"),
    Book("War and Peace", "Leo Tolstoy", "Historical"),
    Book("Anna Karenina", "Leo Tolstoy", "Romance"),
    Book("The Alchemist", "Paulo Coelho", "Adventure"),
    Book("The Picture of Dorian Gray", "Oscar Wilde", "Gothic"),
    Book("The Martian", "Andy Weir", "Science Fiction"),
    Book("Dune", "Frank Herbert", "Science Fiction"),
    Book("Dracula", "Bram Stoker", "Gothic"),
]


custom_categories = []


@app.route('/')
def home():
    selected_category = request.args.get("category", "all")
    msg = request.args.get("msg", None)
   
    filtered_books = book_list  if selected_category == "all" else [book for book in book_list if book.category == selected_category] 

    categories = sorted(set(book.category for book in book_list).union(custom_categories))


    return render_template("index.html", books=filtered_books, categories=categories, selected_category=selected_category, msg=msg)

@app.route("/edit", methods=['POST', 'GET']) 
def edit():
    new_title = request.form.get("title")
    new_author = request.form.get("author")
    new_category = request.form.get("category")
    old_title_value = request.form.get("old_title")


    if new_title and new_author and new_category and old_title_value:
        for book in book_list:
            if book.title == old_title_value:
                book.title = new_title
                book.author = new_author
                book.category = new_category
                return redirect(url_for("home", msg=f"Книга '{new_title}' оновлена"))

    if request.args.get("title"):
        title_to_edit = request.args.get("title")
        book_to_edit = None

        for book in book_list:
            if book.title == title_to_edit:
                book_to_edit = book
                break 


        return render_template("edit.html", book=book_to_edit, old_title=title_to_edit,  categories = sorted(set(book.category for book in book_list).union(custom_categories)))

@app.route("/delete")
def delete():
    for book in book_list:
        if book.title == request.args.get("title"):
            book_list.remove(book)
    return redirect(url_for("home"))


@app.route("/add_category", methods=["GET"])
def add_category():
    category_name = request.args.get("name")
    
    if category_name:
        if category_name not in custom_categories:
            custom_categories.append(category_name)
            return redirect(url_for("home", msg=f"Категория '{category_name}' добавлена!"))
        else:
            return redirect(url_for("home", msg=f"Категория '{category_name}' уже существует!"))
    else:
        return redirect(url_for("home", msg="Введите название категории!"))


@app.route("/search")
def search():
    name = request.args.get("name")
    if name:
        name = name.strip().lower()
    else:
        name = ""

        
    if name:
        for book in book_list:
            if name == book.title.lower() or name == book.author.lower():
                return render_template("search.html", book=book)

        return render_template("search.html", book=None, msg="Ничего не найдено")

    return render_template("search.html", book=None)




















if __name__ == "__main__":
    app.run(debug=True)

