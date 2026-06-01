from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# READ


@app.route("/")
def index():
    conn = get_db()
    appointments = conn.execute("SELECT * FROM appointments").fetchall()
    conn.close()
    return render_template("index.html", appointments=appointments)

# CREATE


@app.route("/add", methods=["GET", "POST"])
def add():
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
        return redirect(url_for("index"))
    return render_template("add.html")

# UPDATE


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
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
        return redirect(url_for("index"))
    appointment = conn.execute(
        "SELECT * FROM appointments WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", appointment=appointment)

# DELETE


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM appointments WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
