
from flask import Flask, render_template, request, redirect,     url_for

app = Flask(__name__)


class Book:
    def __init__(self, title, author, category, year):
        self.title = title
        self.author = author
        self.category = category
        self.year = year


book_list = [
    Book("1984", "George Orwell", "Dystopian", 1949),
    Book("To Kill a Mockingbird", "Harper Lee", "Classic", 1960),
    Book("The Great Gatsby", "F. Scott Fitzgerald", "Classic", 1925),
    Book("Brave New World", "Aldous Huxley", "Dystopian", 1932),
    Book("Moby Dick", "Herman Melville", "Adventure", 1851),
    Book("Pride and Prejudice", "Jane Austen", "Romance", 1813),
    Book("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937),
    Book("Fahrenheit 451", "Ray Bradbury", "Dystopian", 1953),
    Book("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 1997),
    Book("The Catcher in the Rye", "J.D. Salinger", "Classic", 1951),
    Book("The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 1954),
    Book("Crime and Punishment", "Fyodor Dostoevsky", "Philosophical", 1866),
    Book("The Brothers Karamazov", "Fyodor Dostoevsky", "Philosophical", 1880),
    Book("War and Peace", "Leo Tolstoy", "Historical", 1869),
    Book("Anna Karenina", "Leo Tolstoy", "Romance", 1877),
    Book("The Alchemist", "Paulo Coelho", "Adventure", 1988),
    Book("The Picture of Dorian Gray", "Oscar Wilde", "Gothic", 1890),
    Book("The Martian", "Andy Weir", "Science Fiction", 2011),
    Book("Dune", "Frank Herbert", "Science Fiction", 1965),
    Book("Dracula", "Bram Stoker", "Gothic", 1897),
]


custom_categories = []


@app.route('/')
def home():
    from_year = request.args.get("from_year")
    to_year = request.args.get("to_year")


    selected_category = "all"

    if from_year and to_year:
        from_year = int(from_year)
        to_year = int(to_year)
        filtered_books = [book for book in book_list if book.year >= from_year and book.year <= to_year]
    else:
        selected_category = request.args.get("category", "all")
        filtered_books = book_list if selected_category == "all" else [book for book in book_list if book.category == selected_category]

    categories = sorted(set(book.category for book in book_list).union(custom_categories))
    msg = request.args.get("msg", None)

    return render_template("index.html", books=filtered_books, categories=categories, selected_category=selected_category, msg=msg)



@app.route("/edit", methods=['POST', 'GET']) 
def edit():
    new_title = request.form.get("title")
    new_author = request.form.get("author")
    new_category = request.form.get("category")
    new_year = request.form.get("year")
    old_title_value = request.form.get("old_title")


    if new_title and new_author and new_category and new_year and old_title_value:
        for book in book_list:
            if book.title == old_title_value:
                book.title = new_title
                book.author = new_author
                book.category = new_category
                book.year = int(new_year)
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


@app.route("/add_book")
def add_book():
    name = request.args.get("name")
    author = request.args.get("author")
    category = request.args.get("category")
    year = request.args.get("year")

    if name and author and category and year:
        book_list.append(Book(name, author, category, int(year)))
        return redirect(url_for("home", msg=name))

    return render_template("add_book.html", categories = sorted(set(book.category for book in book_list).union(custom_categories)))




@app.route("/filter_by_year")
def filter_by_year():
    from_year = request.args.get("from")
    to_year = request.args.get("to")

    return redirect ( url_for("home", from_year=from_year, to_year=to_year))





if __name__ == "__main__":
    app.run(debug=True)

