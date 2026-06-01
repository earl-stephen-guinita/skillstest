from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# READ


@app.route("/")
def index():
    conn = get_db()
    courses = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()
    return render_template("index.html", courses=courses)

# CREATE


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        code = request.form["courseCode"]
        name = request.form["courseName"]
        unit = request.form["units"]
        dept = request.form["department"]
        conn = get_db()
        conn.execute(
            "INSERT INTO courses (courseCode, courseName, units, department) VALUES (?, ?, ?, ?)", (code, name, unit, dept))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

# UPDATE


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()
    if request.method == "POST":
        code = request.form["courseCode"]
        name = request.form["courseName"]
        unit = request.form["units"]
        dept = request.form["department"]
        conn.execute("UPDATE courses SET courseCode=?, courseName=?, units=?, department=? WHERE id=?",
                     (code, name, unit, dept, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    course = conn.execute("SELECT * FROM courses WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", course=course)

# DELETE


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM courses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
