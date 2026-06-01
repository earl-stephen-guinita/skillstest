from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# READ


@app.route("/")
def index():
    conn = get_db()
    expenses = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()
    return render_template("index.html", expenses=expenses)

# CREATE


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        desc = request.form["description"]
        amount = request.form["amount"]
        cat = request.form["category"]
        date = request.form["date"]
        conn = get_db()
        conn.execute(
            "INSERT INTO expenses (description, amount, category, date) VALUES (?, ?, ?, ?)", (desc, amount, cat, date))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

# UPDATE


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()
    if request.method == "POST":
        desc = request.form["description"]
        amount = request.form["amount"]
        cat = request.form["category"]
        date = request.form["date"]
        conn.execute("UPDATE expenses SET description=?, amount=?, category=?, date=? WHERE id=?",
                     (desc, amount, cat, date, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    expense = conn.execute(
        "SELECT * FROM expenses WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", expense=expense)

# DELETE


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
