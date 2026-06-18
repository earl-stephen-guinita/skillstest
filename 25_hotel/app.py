from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# MENU


@app.route("/")
def index():
    return render_template("hotel.html")

# ===== ROOMS =====

# READ


@app.route("/rooms")
def rooms():
    conn = get_db()
    rooms = conn.execute("SELECT * FROM rooms").fetchall()
    conn.close()
    return render_template("rooms/rooms.html", rooms=rooms)

# CREATE


@app.route("/rooms/add", methods=["GET", "POST"])
def rooms_add():
    if request.method == "POST":
        roomNum = request.form["roomNumber"]
        roomType = request.form["roomType"]
        price = request.form["price"]
        stat = request.form["status"]
        conn = get_db()
        conn.execute("INSERT INTO rooms (roomNumber, roomType, price, status) VALUES (?, ?, ?, ?)",
                     (roomNum, roomType, price, stat))
        conn.commit()
        conn.close()
        return redirect(url_for("rooms"))
    return render_template("rooms/add.html")

# UPDATE


@app.route("/rooms/edit/<int:id>", methods=["GET", "POST"])
def rooms_edit(id):
    conn = get_db()
    if request.method == "POST":
        roomNum = request.form["roomNumber"]
        roomType = request.form["roomType"]
        price = request.form["price"]
        stat = request.form["status"]
        conn.execute("UPDATE rooms SET roomNumber=?, roomType=?, price=?, status=? WHERE id=?",
                     (roomNum, roomType, price, stat, id))
        conn.commit()
        conn.close()
        return redirect(url_for("rooms"))
    room = conn.execute("SELECT * FROM rooms WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("rooms/edit.html", room=room)

# DELETE


@app.route("/rooms/delete/<int:id>")
def rooms_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM rooms WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("rooms"))

# SEARCH


@app.route("/rooms/search")
def rooms_search():
    status = request.args.get("status", "")
    conn = get_db()
    rooms = conn.execute(
        "SELECT * FROM rooms WHERE STATUS = ?",
        (status,)
    ).fetchall()
    conn.close()
    return render_template("rooms/search.html", rooms=rooms, status=status)

# ===== GUESTS =====

# READ


@app.route("/guests")
def guests():
    conn = get_db()
    guests = conn.execute("SELECT * FROM guests").fetchall()
    conn.close()
    return render_template("guests/guests.html", guests=guests)

# CREATE


@app.route("/guests/add", methods=["GET", "POST"])
def guests_add():
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        contact = request.form["contactNumber"]
        checkIn = request.form["checkIn"]
        checkOut = request.form["checkOut"]
        stat = request.form["status"]
        conn = get_db()
        conn.execute("INSERT INTO guests (firstName, lastName, contactNumber, checkIn, checkOut, status) VALUES (?, ?, ?, ?, ?, ?)",
                     (fName, lName, contact, checkIn, checkOut, stat))
        conn.commit()
        conn.close()
        return redirect(url_for("guests"))
    return render_template("guests/add.html")

# UPDATE


@app.route("/guests/edit/<int:id>", methods=["GET", "POST"])
def guests_edit(id):
    conn = get_db()
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        contact = request.form["contactNumber"]
        checkIn = request.form["checkIn"]
        checkOut = request.form["checkOut"]
        stat = request.form["status"]
        conn.execute("UPDATE guests SET firstName=?, lastName=?, contactNumber=?, checkIn=?, checkOut=?, status=? WHERE id=?",
                     (fName, lName, contact, checkIn, checkOut, stat))
        conn.commit()
        conn.close()
        return redirect(url_for("guests"))
    guest = conn.execute("SELECT * FROM guests WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("guests/edit.html", guest=guest)

# DELETE


@app.route("/guests/delete/<int:id>")
def guests_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM guests WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("guests"))

# SEARCH


@app.route("/guests/search")
def guests_search():
    keyword = request.args.get("keyword", "")
    conn = get_db()
    guests = conn.execute(
        "SELECT * FROM guests WHERE lastName LIKE ?",
        ('%' + keyword + '%',)
    ).fetchall()
    conn.close()
    return render_template("guests/search.html", guests=guests, keyword=keyword)

# ===== RESERVATIONS =====

# READ


@app.route("/reservations")
def reservations():
    conn = get_db()
    reservations = conn.execute("SELECT * FROM reservations").fetchall()
    conn.close()
    return render_template("reservations/reservations.html", reservations=reservations)

# CREATE


@app.route("/reservations/add", methods=["GET", "POST"])
def reservations_add():
    if request.method == "POST":
        guest = request.form["guestName"]
        room = request.form["roomNumber"]
        checkIn = request.form["checkIn"]
        checkOut = request.form["checkOut"]
        stat = request.form["status"]
        conn = get_db()
        conn.execute("INSERT INTO reservations (guestName, roomNumber, checkIn, checkOut, status) VALUES (?, ?, ?, ?, ?)",
                     (guest, room, checkIn, checkOut, stat))
        conn.commit()
        conn.close()
        return redirect(url_for("reservations"))
    return render_template("reservations/add.html")

# UPDATE


@app.route("/reservations/edit/<int:id>", methods=["GET", "POST"])
def reservations_edit(id):
    conn = get_db()
    if request.method == "POST":
        guest = request.form["guestName"]
        room = request.form["roomNumber"]
        checkIn = request.form["checkIn"]
        checkOut = request.form["checkOut"]
        stat = request.form["status"]
        conn.execute("UPDATE reservations SET guestName=?, roomNumber=?, checkIn=?, checkOut=?, status=? WHERE id=?",
                     (guest, room, checkIn, checkOut, stat, id))
        conn.commit()
        conn.close()
        return redirect(url_for("reservations"))
    reservation = conn.execute(
        "SELECT * FROM reservations WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("reservations/edit.html", reservation=reservation)

# DELETE


@app.route("/reservations/delete/<int:id>")
def reservations_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM reservations WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("reservations"))

# SEARCH


@app.route("/reservations/search")
def reservations_search():
    status = request.args.get("status", "")
    conn = get_db()
    reservations = conn.execute(
        "SELECT * FROM reservations WHERE status = ?",
        (status,)
    ).fetchall()
    conn.close()
    return render_template("reservations/search.html", reservations=reservations, status=status)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
