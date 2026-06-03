from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# Menu


@app.route("/")
def index():
    return render_template("index.html")

# ===== Products =====

# READ


@app.route("/products")
def products():
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template("products/index.html", products=products)

# CREATE


@app.route("/products/add", methods=["GET", "POST"])
def products_add():
    if request.method == "POST":
        name = request.form["productName"]
        price = request.form["price"]
        stock = request.form["stock"]
        stat = request.form["status"]
        conn = get_db()
        conn.execute("INSERT INTO products (productName, price, stock, status) VALUES (?, ?, ?, ?)",
                     (name, price, stock, stat))
        conn.commit()
        conn.close()
        return redirect(url_for("products"))
    return render_template("products/add.html")

# UPDATE


@app.route("/products/edit/<int:id>", methods=["GET", "POST"])
def products_edit(id):
    conn = get_db()
    if request.method == "POST":
        name = request.form["productName"]
        price = request.form["price"]
        stock = request.form["stock"]
        stat = request.form["status"]
        conn.execute("UPDATE products SET productName=?, price=?, stock=?, status=? WHERE id=?",
                     (name, price, stock, stat, id))
        conn.commit()
        conn.close()
        return redirect(url_for("products"))
    product = conn.execute(
        "SELECT * FROM products WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("products/edit.html", product=product)

# DELETE


@app.route("/products/delete/<int:id>")
def products_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("products"))

# ===== Categories =====

# READ


@app.route("/categories")
def categories():
    conn = get_db()
    categories = conn.execute("SELECT * FROM categories").fetchall()
    conn.close()
    return render_template("categories/index.html", categories=categories)

# CREATE


@app.route("/categories/add", methods=["GET", "POST"])
def categories_add():
    if request.method == "POST":
        name = request.form["categoryName"]
        desc = request.form["description"]
        conn = get_db()
        conn.execute("INSERT INTO categories (categoryName, description) VALUES (?, ?)",
                     (name, desc))
        conn.commit()
        conn.close()
        return redirect(url_for("categories"))
    return render_template("categories/add.html")

# UPDATE


@app.route("/categories/edit/<int:id>", methods=["GET", "POST"])
def categories_edit(id):
    conn = get_db()
    if request.method == "POST":
        name = request.form["categoryName"]
        desc = request.form["description"]
        conn.execute("UPDATE categories SET categoryName=?, description=? WHERE id=?",
                     (name, desc, id))
        conn.commit()
        conn.close()
        return redirect(url_for("categories"))
    category = conn.execute(
        "SELECT * FROM categories WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("categories/edit.html", category=category)

# DELETE


@app.route("/categories/delete/<int:id>")
def categories_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM categories WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("categories"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
