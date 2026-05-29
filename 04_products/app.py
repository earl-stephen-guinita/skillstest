from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# READ


@app.route("/")
def index():
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template("index.html", products=products)

# CREATE


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        quantity = request.form["quantity"]
        conn = get_db()
        conn.execute("INSERT INTO products (name, category, price, quantity) VALUES (?, ?, ?, ?)",
                     (name, category, price, quantity))
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
        category = request.form["category"]
        price = request.form["price"]
        quantity = request.form["quantity"]
        conn.execute("UPDATE products SET name=?, category=?, price=?, quantity=? WHERE id=?",
                     (name, category, price, quantity, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    product = conn.execute(
        "SELECT * FROM products WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", product=product)

# DELETE


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
