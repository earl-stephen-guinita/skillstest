from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# Menu


@app.route("/")
def index():
    return render_template("index.html")

# ===== Appointments =====

# READ


@app.route("/appointments")
def appointments():
    conn = get_db()
    appointments = conn.execute("SELECT * FROM appointments").fetchall()
    conn.close()
    return render_template("appointments/index.html", appointments=appointments)

# CREATE


@app.route("/appointments/add", methods=["GET", "POST"])
def appointments_add():
    if request.method == "POST":
        patientName = request.form["patientName"]
        docName = request.form["doctorName"]
        date = request.form["date"]
        time = request.form["time"]
        stat = request.form["status"]
        conn = get_db()
        conn.execute("INSERT INTO appointments (patientName, doctorName, date, time, status) VALUES (?, ?, ?, ?, ?)",
                     (patientName, docName, date, time, stat))
        conn.commit()
        conn.close()
        return redirect(url_for("appointments"))
    return render_template("appointments/add.html")

# UPDATE


@app.route("/appointments/edit/<int:id>", methods=["GET", "POST"])
def appointments_edit(id):
    conn = get_db()
    if request.method == "POST":
        patientName = request.form["patientName"]
        docName = request.form["doctorName"]
        date = request.form["date"]
        time = request.form["time"]
        stat = request.form["status"]
        conn.execute("UPDATE appointments SET patientName=?, doctorName=?, date=?, time=?, status=? WHERE id=?",
                     (patientName, docName, date, time, stat, id))
        conn.commit()
        conn.close()
        return redirect(url_for("appointments"))
    appointment = conn.execute(
        "SELECT * FROM appointments WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("appointments/edit.html", appointment=appointment)

# DELETE


@app.route("/appointments/delete/<int:id>")
def appointments_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM appointments WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("appointments"))

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
        special = request.form["specialization"]
        contact = request.form["contactNumber"]
        stat = request.form["status"]
        conn = get_db()
        conn.execute("INSERT INTO doctors (firstName, lastName, specialization, contactNumber, status) VALUES (?, ?, ?, ?, ?)",
                     (fName, lName, special, contact, stat))
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
        special = request.form["specialization"]
        contact = request.form["contactNumber"]
        stat = request.form["status"]
        conn.execute("UPDATE doctors SET firstName=?, lastName=?, specialization=?, contactNumber=?, status=? WHERE id=?",
                     (fName, lName, special, contact, stat, id))
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
        date = request.form["birthDate"]
        contact = request.form["contactNumber"]
        gender = request.form["gender"]
        conn = get_db()
        conn.execute("INSERT INTO patients (firstName, lastName, birthDate, contactNumber, gender) VALUES (?, ?, ?, ?, ?)",
                     (fName, lName, date, contact, gender))
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
        date = request.form["birthDate"]
        contact = request.form["contactNumber"]
        gender = request.form["gender"]
        conn.execute("UPDATE patients SET firstName=?, lastName=?, birthDate=?, contactNumber=?, gender=? WHERE id=?",
                     (fName, lName, date, contact, gender, id))
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


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
