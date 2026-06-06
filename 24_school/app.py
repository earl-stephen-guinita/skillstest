from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# MENU


@app.route("/")
def index():
    return render_template("menu.html")

# ===== STUDENTS =====

# READ


@app.route("/students")
def students():
    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("students/students.html", students=students)

# CREATE


@app.route("/students/add", methods=["GET", "POST"])
def students_add():
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        course = request.form["course"]
        yrLvl = request.form["yearLevel"]
        stat = request.form["status"]
        conn = get_db()
        conn.execute("INSERT INTO students (firstName, lastName, course, yearLevel, status) VALUES (?, ?, ?, ?, ?)",
                     (fName, lName, course, yrLvl, stat))
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
        yrLvl = request.form["yearLevel"]
        stat = request.form["status"]
        conn.execute("UPDATE students SET firstName=?, lastName=?, course=?, yearLevel=?, status=? WHERE id=?",
                     (fName, lName, course, yrLvl, stat, id))
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

# SEARCH


@app.route("/students/search")
def students_search():
    course = request.args.get("course", "")
    conn = get_db()
    students = conn.execute(
        "SELECT * FROM students WHERE course = ?",
        (course,)
    ).fetchall()
    conn.close()
    return render_template("students/search.html", students=students, course=course)

# ===== TEACHERS =====

# READ


@app.route("/teachers")
def teachers():
    conn = get_db()
    teachers = conn.execute("SELECT * FROM teachers").fetchall()
    conn.close()
    return render_template("teachers/teachers.html", teachers=teachers)

# CREATE


@app.route("/teachers/add", methods=["GET", "POST"])
def teachers_add():
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        sub = request.form["subject"]
        contact = request.form["contactNumber"]
        stat = request.form["status"]
        conn = get_db()
        conn.execute("INSERT INTO teachers (firstName, lastName, subject, contactNumber, status) VALUES (?, ?, ?, ?, ?)",
                     (fName, lName, sub, contact, stat))
        conn.commit()
        conn.close()
        return redirect(url_for("teachers"))
    return render_template("teachers/add.html")

# UPDATE


@app.route("/teachers/edit/<int:id>", methods=["GET", "POST"])
def teachers_edit(id):
    conn = get_db()
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        sub = request.form["subject"]
        contact = request.form["contactNumber"]
        stat = request.form["status"]
        conn.execute("UPDATE teachers SET firstName=?, lastName=?, subject=?, contactNumber=?, status=? WHERE id=?",
                     (fName, lName, sub, contact, stat, id))
        conn.commit()
        conn.close()
        return redirect(url_for("teachers"))
    teacher = conn.execute(
        "SELECT * FROM teachers WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("teachers/edit.html", teacher=teacher)

# DELETE


@app.route("/teachers/delete/<int:id>")
def teachers_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM teachers WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("teachers"))

# SEARCH


@app.route("/teachers/search")
def teachers_search():
    keyword = request.args.get("keyword", "")
    conn = get_db()
    teachers = conn.execute(
        "SELECT * FROM teachers WHERE subject LIKE ?",
        ('%' + keyword + '%',)
    ).fetchall
    conn.close()
    return render_template("teachers/search.html", teachers=teachers, keyword=keyword)

# ===== SUBJECTS =====

# READ


@app.route("/subjects")
def subjects():
    conn = get_db()
    subjects = conn.execute("SELECT * FROM subjects").fetchall()
    conn.close()
    return render_template("subjects/subjects.html", subjects=subjects)

# CREATE


@app.route("/subjects/add", methods=["GET", "POST"])
def subjects_add():
    if request.method == "POST":
        code = request.form["subjectCode"]
        name = request.form["subjectName"]
        unit = request.form["units"]
        dept = request.form["department"]
        conn = get_db()
        conn.execute(
            "INSERT INTO subjects (subjectCode, subjectName, units, department) VALUES (?, ?, ?, ?)", (code, name, unit, dept))
        conn.commit()
        conn.close()
        return redirect(url_for("subjects"))
    return render_template("subjects/add.html")

# UPDATE


@app.route("/subjects/edit/<int:id>", methods=["GET", "POST"])
def subjects_edit(id):
    conn = get_db()
    if request.method == "POST":
        code = request.form["subjectCode"]
        name = request.form["subjectName"]
        unit = request.form["units"]
        dept = request.form["department"]
        conn.execute(
            "UPDATE subjects SET subjectCode=?, subjectName=?, units=?, department=? WHERE id=?", (code, name, unit, dept, id))
        conn.commit()
        conn.close()
        return redirect(url_for("subjects"))
    subject = conn.execute(
        "SELECT * FROM subjects WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("subjects/edit.html", subject=subject)

# DELETE


@app.route("/subjects/delete/<int:id>")
def subjects_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM subjects WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("subjects"))

# SEARCH


@app.route("/subjects")
def subjects_search():
    department = request.args.get("department", "")
    conn = get_db()
    subjects = conn.execute(
        "SELECT * FROM subjects WHERE department = ?",
        (department,)
    ).fetchall()
    conn.close()
    return render_template("subjects/search.html", subjects=subjects, department=department)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
