from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# READ


@app.route("/")
def index():
    conn = get_db()
    vehicles = conn.execute("SELECT * FROM vehicles").fetchall()
    conn.close()
    return render_template("index.html", vehicles=vehicles)

# CREATE


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        plateNum = request.form["plateNumber"]
        owner = request.form["owner"]
        brand = request.form["brand"]
        vehicleType = request.form["type"]
        conn = get_db()
        conn.execute("INSERT INTO vehicles (plateNumber, owner, brand, type) VALUES (?, ?, ?, ?)",
                     (plateNum, owner, brand, vehicleType))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

# UPDATE


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()
    if request.method == "POST":
        plateNum = request.form["plateNumber"]
        owner = request.form["owner"]
        brand = request.form["brand"]
        vehicleType = request.form["type"]
        conn.execute("UPDATE vehicles SET plateNumber=?, owner=?, brand=?, type=? WHERE id=?",
                     (plateNum, owner, brand, vehicleType, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    vehicle = conn.execute(
        "SELECT * FROM vehicles WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", vehicle=vehicle)

# DELETE


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM vehicles WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
