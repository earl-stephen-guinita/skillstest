from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# READ


@app.route("/")
def index():
    conn = get_db()
    libraryMembers = conn.execute("SELECT * FROM libraryMembers").fetchall()
    conn.close()
    return render_template("index.html", libraryMembers=libraryMembers)

# CREATE


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        email = request.form["email"]
        date = request.form["membershipDate"]
        conn = get_db()
        conn.execute("INSERT INTO libraryMembers (firstName, lastName, email, membershipDate) VALUES (?, ?, ?, ?)",
                     (fName, lName, email, date))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

# UPDATE


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        email = request.form["email"]
        date = request.form["membershipDate"]
        conn.execute("UPDATE libraryMembers SET firstName=?, lastName=?, email=?, membershipDate=? WHERE id=?",
                     (fName, lName, email, date, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    libraryMember = conn.execute(
        "SELECT * FROM libraryMembers WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", libraryMember=libraryMember)

# DELETE


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM libraryMembers WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
