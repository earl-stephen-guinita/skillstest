from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# READ


@app.route("/")
def index():
    conn = get_db()
    items = conn.execute("SELECT * FROM items").fetchall()
    conn.close()
    return render_template("index.html", items=items)

# CREATE


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        desc = request.form["description"]
        conn = get_db()
        conn.execute(
            "INSERT INTO items (name, description) VALUES (?, ?)", (name, desc))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

# UPDATE


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()
    if request.method == "POST":
        name = request.form["name"]
        desc = request.form["description"]
        conn.execute(
            "UPDATE items SET name=?, description=? WHERE id=?", (name, desc, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    item = conn.execute("SELECT * FROM items WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", item=item)

# DELETE


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM items WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
