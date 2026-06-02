from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# MENU


@app.route("/")
def index():
    return render_template("index.html")

# =====  STUDENTS ======

# READ


@app.route("/students")
def students():
    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("students/index.html", students=students)

# CREATE


@app.route("/students/add", methods=["GET", "POST"])
def students_add():
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        course = request.form["course"]
        conn = get_db()
        conn.execute(
            "INSERT INTO students (firstName, lastName, course) VALUES (?, ?, ?)", (fName, lName, course))
        conn.commit()
        conn.close()
        return redirect(url_for("students"))
    return render_template("students/add.html")

# UPDATE


@app.route("/students/edit/<int:id>", methods=["GET", "POST"])
def students_edit(id):
    conn = get_db()
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        course = request.form["course"]
        conn.execute("UPDATE students SET firstName=?, lastName=?, course=? WHERE id=?",
                     (fName, lName, course, id))
        conn.commit()
        conn.close()
        return redirect(url_for("students"))
    student = conn.execute(
        "SELECT * FROM students WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("students/edit.html", student=student)

# DELETE


@app.route("/students/delete/<int:id>")
def students_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("students"))

# ===== COURSES =====

# READ


@app.route("/courses")
def courses():
    conn = get_db()
    courses = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()
    return render_template("courses/index.html", courses=courses)

# CREATE


@app.route("/courses/add", methods=["GET", "POST"])
def courses_add():
    if request.method == "POST":
        code = request.form["courseCode"]
        name = request.form["courseName"]
        units = request.form["units"]
        conn = get_db()
        conn.execute(
            "INSERT INTO courses (courseCode, courseName, units) VALUES (?, ?, ?)", (code, name, units))
        conn.commit()
        conn.close()
        return redirect(url_for("courses"))
    return render_template("courses/add.html")

# UPDATE


@app.route("/courses/edit/<int:id>", methods=["GET", "POST"])
def courses_edit(id):
    conn = get_db()
    if request.method == "POST":
        code = request.form["courseCode"]
        name = request.form["courseName"]
        units = request.form["units"]
        conn.execute(
            "UPDATE courses SET courseCode=?, courseName=?, units=? WHERE id=?", (code, name, units, id))
        conn.commit()
        conn.close()
        return redirect(url_for("courses"))
    course = conn.execute("SELECT * FROM courses WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("courses/edit.html", course=course)

# DELETE


@app.route("/courses/delete/<int:id>")
def courses_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM courses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("courses"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
