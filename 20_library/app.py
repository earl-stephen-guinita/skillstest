from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# Menu


@app.route("/")
def index():
    return render_template("index.html")

# ===== Books =====

# READ


@app.route("/books")
def books():
    conn = get_db()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return render_template("books/index.html", books=books)

# CREATE


@app.route("/books/add", methods=["GET", "POST"])
def books_add():
    if request.method == "POST":
        title = request.form["title"]
        genre = request.form["genre"]
        yrPublish = request.form["yearPublished"]
        stat = request.form["status"]
        conn = get_db()
        conn.execute("INSERT INTO books (title, genre, yearPublished, status) VALUES (?, ?, ?, ?)",
                     (title, genre, yrPublish, stat))
        conn.commit()
        conn.close()
        return redirect(url_for("books"))
    return render_template("books/add.html")

# UPDATE


@app.route("/books/edit/<int:id>", methods=["GET", "POST"])
def books_edit(id):
    conn = get_db()
    if request.method == "POST":
        title = request.form["title"]
        genre = request.form["genre"]
        yrPublish = request.form["yearPublished"]
        stat = request.form["status"]
        conn.execute("UPDATE books SET title=?, genre=?, yearPublished=?, status=? WHERE id=?",
                     (title, genre, yrPublish, stat, id))
        conn.commit()
        conn.close()
        return redirect(url_for("books"))
    book = conn.execute("SELECT * FROM books WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("books/edit.html", book=book)

# DELETE


@app.route("/books/delete/<int:id>")
def books_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("books"))

# ===== Members =====

# READ


@app.route("/members")
def members():
    conn = get_db()
    members = conn.execute("SELECT * FROM members").fetchall()
    conn.close()
    return render_template("members/index.html", members=members)

# CREATE


@app.route("/members/add", methods=["GET", "POST"])
def members_add():
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        email = request.form["email"]
        membership = request.form["membershipDate"]
        conn = get_db()
        conn.execute("INSERT INTO members (firstName, lastName, email, membershipDate) VALUES (?, ?, ?, ?)",
                     (fName, lName, email, membership))
        conn.commit()
        conn.close()
        return redirect(url_for("members"))
    return render_template("members/add.html")

# UPDATE


@app.route("/members/edit/<int:id>", methods=["GET", "POST"])
def members_edit(id):
    conn = get_db()
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        email = request.form["email"]
        membership = request.form["membershipDate"]
        conn.execute("UPDATE members SET firstName=?, lastName=?, email=?, membershipDate=? WHERE id=?",
                     (fName, lName, email, membership, id))
        conn.commit()
        conn.close()
        return redirect(url_for("members"))
    member = conn.execute("SELECT * FROM members WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("members/edit.html", member=member)

# DELETE


@app.route("/members/delete/<int:id>")
def members_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM members WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("members"))

# ===== Authors =====

# READ


@app.route("/authors")
def authors():
    conn = get_db()
    authors = conn.execute("SELECT * FROM authors").fetchall()
    conn.close()
    return render_template("authors/index.html", authors=authors)

# CREATE


@app.route("/authors/add", methods=["GET", "POST"])
def authors_add():
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        nation = request.form["nationality"]
        date = request.form["birthDate"]
        conn = get_db()
        conn.execute("INSERT INTO authors (firstName, lastName, nationality, birthDate) VALUES (?, ?, ?, ?)",
                     (fName, lName, nation, date))
        conn.commit()
        conn.close()
        return redirect(url_for("authors"))
    return render_template("authors/add.html")

# UPDATE


@app.route("/authors/edit/<int:id>", methods=["GET", "POST"])
def authors_edit(id):
    conn = get_db()
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        nation = request.form["nationality"]
        date = request.form["birthDate"]
        conn.execute("UPDATE authors SET firstName=?, lastName=?, nationality=?, birthDate=? WHERE id=?",
                     (fName, lName, nation, date, id))
        conn.commit()
        conn.close()
        return redirect(url_for("authors"))
    author = conn.execute("SELECT * FROM authors WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("authors/edit.html", author=author)

# DELETE


@app.route("/authors/delete/<int:id>")
def authors_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM authors WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("authors"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
