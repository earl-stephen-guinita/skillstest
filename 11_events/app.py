from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# READ


@app.route("/")
def index():
    conn = get_db()
    events = conn.execute("SELECT * FROM events").fetchall()
    conn.close()
    return render_template("index.html", events=events)

# CREATE


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["eventName"]
        loc = request.form["location"]
        date = request.form["date"]
        stat = request.form["status"]
        conn = get_db()
        conn.execute(
            "INSERT INTO events (eventName, location, date, status) VALUES (?, ?, ?, ?)", (name, loc, date, stat))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

# UPDATE


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()
    if request.form == "POST":
        name = request.form["eventName"]
        loc = request.form["location"]
        date = request.form["date"]
        stat = request.form["status"]
        conn.execute("UPDATE events SET eventName=?, location=?, date=?, status=? WHERE id=?",
                     (name, loc, date, stat, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    event = conn.execute("SELECT * FROM events WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", event=event)

# DELETE


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM events WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
