from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# Menu


@app.route("/")
def index():
    return render_template("index.html")

# ===== Doctors =====

# READ


@app.route("/doctors")
def doctors():
    conn = get_db()
    doctors = conn.execute("SELECT * FROM doctors").fetchall()
    conn.close()
    return render_template("doctors/index.html", doctors=doctors)

# CREATE


@app.route("/doctors/add", methods=["GET", "POST"])
def doctors_add():
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        contact = request.form["contactNumber"]
        special = request.form["specialization"]
        conn = get_db()
        conn.execute("INSERT INTO doctors (firstName, lastName, contactNumber, specialization) VALUES (?, ?, ?, ?)",
                     (fName, lName, contact, special))
        conn.commit()
        conn.close()
        return redirect(url_for("doctors"))
    return render_template("doctors/add.html")

# UPDATE


@app.route("/doctors/edit/<int:id>", methods=["GET", "POST"])
def doctors_edit(id):
    conn = get_db()
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        contact = request.form["contactNumber"]
        special = request.form["specialization"]
        conn.execute("UPDATE doctors SET firstName=?, lastName=?, contactNumber=?, specialization=? WHERE id=?",
                     (fName, lName, contact, special, id))
        conn.commit()
        conn.close()
        return redirect(url_for("doctors"))
    doctor = conn.execute("SELECT * FROM doctors WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("doctors/edit.html", doctor=doctor)

# DELETE


@app.route("/doctors/delete/<int:id>")
def doctors_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM doctors WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("doctors"))

# SEARCH


@app.route("/doctors/search")
def doctors_search():
    keyword = request.args.get("keyword", "")
    conn = get_db()
    doctors = conn.execute(
        "SELECT * FROM doctors WHERE specialization LIKE ?",
        ('%' + keyword + '%',)
    ).fetchall()
    conn.close()
    return render_template("doctors/search.html", doctors=doctors, keyword=keyword)


# ===== Patients =====

# READ
@app.route("/patients")
def patients():
    conn = get_db()
    patients = conn.execute("SELECT * FROM patients").fetchall()
    conn.close()
    return render_template("patients/index.html", patients=patients)

# CREATE


@app.route("/patients/add", methods=["GET", "POST"])
def patients_add():
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        bDate = request.form["birthDate"]
        contact = request.form["contactNumber"]
        conn = get_db()
        conn.execute("INSERT INTO patients (firstName, lastName, birthDate, contactNumber) VALUES (?, ?, ?, ?)",
                     (fName, lName, bDate, contact))
        conn.commit()
        conn.close()
        return redirect(url_for("patients"))
    return render_template("patients/add.html")

# UPDATE


@app.route("/patients/edit/<int:id>", methods=["GET", "POST"])
def patients_edit(id):
    conn = get_db()
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        bDate = request.form["birthDate"]
        contact = request.form["contactNumber"]
        conn.execute("UPDATE patients SET firstName=?, lastName=?, birthDate=?, contactNumber=? WHERE id=?",
                     (fName, lName, bDate, contact, id))
        conn.commit()
        conn.close()
        return redirect(url_for("patients"))
    patient = conn.execute(
        "SELECT * FROM patients WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("patients/edit.html", patient=patient)

# DELETE


@app.route("/patients/delete/<int:id>")
def patients_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM patients WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("patients"))

# SEARCH


@app.route("/patients/search")
def patients_search():
    keyword = request.args.get("keyword", "")
    conn = get_db()
    patients = conn.execute(
        "SELECT * FROM patients WHERE lastName LIKE ?",
        ('%' + keyword + '%',)
    ).fetchall()
    conn.close()
    return render_template("patients/search.html", patients=patients, keyword=keyword)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
