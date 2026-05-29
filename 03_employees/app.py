from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# READ


@app.route("/")
def index():
    conn = get_db()
    employees = conn.execute("SELECT * FROM employees").fetchall()
    conn.close()
    return render_template("index.html", employees=employees)

# CREATE


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        position = request.form["position"]
        salary = request.form["salary"]
        conn = get_db()
        conn.execute("INSERT INTO employees (firstName, lastName, position, salary) VALUES (?, ?, ?, ?)",
                     (fName, lName, position, salary))
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
        position = request.form["position"]
        salary = request.form["salary"]
        conn.execute("UPDATE employees SET firstName=?, lastName=?, position=?, salary=? WHERE id=?",
                     (fName, lName, position, salary, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    employee = conn.execute(
        "SELECT * FROM employees WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", employee=employee)

# DELETE


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM employees WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
