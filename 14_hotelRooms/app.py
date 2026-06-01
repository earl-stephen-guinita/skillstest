from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# READ


@app.route("/")
def index():
    conn = get_db()
    hotelRooms = conn.execute("SELECT * FROM hotelRooms").fetchall()
    conn.close()
    return render_template("index.html", hotelRooms=hotelRooms)

# CREATE


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        roomNum = request.form["roomNumber"]
        roomType = request.form["roomType"]
        cap = request.form["capacity"]
        price = request.form["price"]
        stat = request.form["status"]
        conn = get_db()
        conn.execute("INSERT INTO hotelRooms (roomNumber, roomType, capacity, price, status) VALUES (?, ?, ?, ?, ?)",
                     (roomNum, roomType, cap, price, stat))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

# UPDATE


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()
    if request.method == "POST":
        roomNum = request.form["roomNumber"]
        roomType = request.form["roomType"]
        cap = request.form["capacity"]
        price = request.form["price"]
        stat = request.form["status"]
        conn.execute("UPDATE hotelRooms SET roomNumber=?, roomType=?, capacity=?, price=?, status=? WHERE id=?",
                     (roomNum, roomType, cap, price, stat, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    hotelRoom = conn.execute(
        "SELECT * FROM hotelRooms WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", hotelRoom=hotelRoom)

# DELETE


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM hotelRooms WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
