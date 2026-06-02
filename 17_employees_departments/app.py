from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# MENU


@app.route("/")
def index():
    return render_template("index.html")

# ===== Employees =====

# READ


@app.route("/employees")
def employees():
    conn = get_db()
    employees = conn.execute("SELECT * FROM employees").fetchall()
    conn.close()
    return render_template("employees/index.html", employees=employees)

# CREATE


@app.route("/employees/add", methods=["GET", "POST"])
def employees_add():
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        position = request.form["position"]
        salary = request.form["salary"]
        stat = request.form["status"]
        conn = get_db()
        conn.execute("INSERT INTO employees (firstName, lastName, position, salary, status) VALUES (?, ?, ?, ?, ?)",
                     (fName, lName, position, salary, stat))
        conn.commit()
        conn.close()
        return redirect(url_for("employees"))
    return render_template("employees/add.html")

# UPDATE


@app.route("/employees/edit/<int:id>", methods=["GET", "POST"])
def employees_edit(id):
    conn = get_db()
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        position = request.form["position"]
        salary = request.form["salary"]
        stat = request.form["status"]
        conn.execute("UPDATE employees SET firstName=?, lastName=?, position=?, salary=?, status=? WHERE id=?",
                     (fName, lName, position, salary, stat, id))
        conn.commit()
        conn.close()
        return redirect(url_for("employees"))
    employee = conn.execute(
        "SELECT * FROM employees WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("employees/edit.html", employee=employee)

# DELETE


@app.route("/employees/delete/<int:id>")
def employees_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM employees WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("employees"))

# ===== Departments =====

# READ


@app.route("/departments")
def departments():
    conn = get_db()
    departments = conn.execute("SELECT * FROM departments").fetchall()
    conn.close()
    return render_template("departments/index.html", departments=departments)

# CREATE


@app.route("/departments/add", methods=["GET", "POST"])
def departments_add():
    if request.method == "POST":
        code = request.form["deptCode"]
        name = request.form["deptName"]
        loc = request.form["location"]
        conn = get_db()
        conn.execute("INSERT INTO departments (deptCode, deptName, location) VALUES (?, ?, ?)",
                     (code, name, loc))
        conn.commit()
        conn.close()
        return redirect(url_for("departments"))
    return render_template("departments/add.html")

# UPDATE


@app.route("/departments/edit/<int:id>", methods=["GET", "POST"])
def departments_edit(id):
    conn = get_db()
    if request.method == "POST":
        code = request.form["deptCode"]
        name = request.form["deptName"]
        loc = request.form["location"]
        conn.execute("UPDATE departments SET deptCode=?, deptName=?, location=? WHERE id=?",
                     (code, name, loc, id))
        conn.commit()
        conn.close()
        return redirect(url_for("departments"))
    department = conn.execute(
        "SELECT * FROM departments WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("departments/edit.html", department=department)

# DELETE


@app.route("/departments/delete/<int:id>")
def departments_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM departments WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("departments"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
