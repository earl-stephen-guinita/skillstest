from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# READ


@app.route("/")
def index():
    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("index.html", students=students)

# CREATE


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        course = request.form["course"]
        yrLvl = request.form["yearLevel"]
        conn = get_db()
        conn.execute("INSERT INTO students (firstName, lastName, course, yearLevel) VALUES (?, ?, ?, ?)",
                     (fName, lName, course, yrLvl))
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
        course = request.form["course"]
        yrLvl = request.form["yearLevel"]
        conn.execute("UPDATE students SET firstName=?, lastName=?, course=?, yearLevel=? WHERE id=?",
                     (fName, lName, course, yrLvl, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    student = conn.execute(
        "SELECT * FROM students WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", student=student)

# DELETE


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
