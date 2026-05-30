from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# READ


@app.route("/")
def index():
    conn = get_db()
    patients = conn.execute("SELECT * FROM patients").fetchall()
    conn.close()
    return render_template("index.html", patients=patients)

# CREATE


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        birthDate = request.form["birthDate"]
        contactNumber = request.form["contactNumber"]
        conn = get_db()
        conn.execute("INSERT INTO patients (firstName, lastName, birthDate, contactNumber) VALUES (?, ?, ?, ?)",
                     (fName, lName, birthDate, contactNumber))
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
        birthDate = request.form["birthDate"]
        contactNumber = request.form["contactNumber"]
        conn.execute("UPDATE patients SET firstName=?, lastName=?, birthDate=?, contactNumber=? WHERE id=?",
                     (fName, lName, birthDate, contactNumber, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    patient = conn.execute(
        "SELECT * FROM patients WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", patient=patient)

# DELETE


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM patients WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
