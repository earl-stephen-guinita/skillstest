from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# READ


@app.route("/")
def index():
    conn = get_db()
    suppliers = conn.execute("SELECT * FROM suppliers").fetchall()
    conn.close()
    return render_template("index.html", suppliers=suppliers)

# CREATE


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["supplierName"]
        contactPerson = request.form["contactPerson"]
        contactNum = request.form["contactNumber"]
        address = request.form["address"]
        conn = get_db()
        conn.execute("INSERT INTO suppliers (supplierName, contactPerson, contactNumber, address) VALUES (?, ?, ?, ?)",
                     (name, contactPerson, contactNum, address))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

# UPDATE


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()
    if request.method == "POST":
        name = request.form["supplierName"]
        contactPerson = request.form["contactPerson"]
        contactNum = request.form["contactNumber"]
        address = request.form["address"]
        conn.execute("UPDATE suppliers SET supplierName=?, contactPerson=?, contactNumber=?, address=? WHERE id=?",
                     (name, contactPerson, contactNum, address, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    supplier = conn.execute(
        "SELECT * FROM suppliers WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", supplier=supplier)

# DELETE


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM suppliers WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
