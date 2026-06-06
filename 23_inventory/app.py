from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# MENU


@app.route("/")
def index():
    return render_template("index.html")

# ===== PRODUCTS =====

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
        cat = request.form["category"]
        conn = get_db()
        conn.execute(
            "INSERT INTO products (productName, price, stock, category) VALUES (?, ?, ?, ?)", (name, price, stock, cat))
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
        cat = request.form["category"]
        conn.execute("UPDATE products SET productName=?, price=?, stock=?, category=? WHERE id=?",
                     (name, price, stock, cat, id))
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

# SEARCH


@app.route("/products/search")
def products_search():
    keyword = request.args.get("keyword", "")
    conn = get_db()
    products = conn.execute(
        "SELECT * FROM products WHERE productName LIKE ?",
        ('%' + keyword + '%',)
    ).fetchall()
    conn.close()
    return render_template("products/search.html", products=products, keyword=keyword)

# SUPPLIERS

# READ


@app.route("/suppliers")
def suppliers():
    conn = get_db()
    suppliers = conn.execute("SELECT * FROM suppliers").fetchall()
    conn.close()
    return render_template("suppliers/index.html", suppliers=suppliers)

# CREATE


@app.route("/suppliers/add", methods=["GET", "POST"])
def suppliers_add():
    if request.method == "POST":
        name = request.form["supplierName"]
        contact = request.form["contactNumber"]
        address = request.form["address"]
        stat = request.form["status"]
        conn = get_db()
        conn.execute("INSERT INTO suppliers (supplierName, contactNumber, address, status) VALUES (?, ?, ?, ?)",
                     (name, contact, address, stat))
        conn.commit()
        conn.close()
        return redirect(url_for("suppliers"))
    return render_template("suppliers/add.html")

# UPDATE


@app.route("/suppliers/edit/<int:id>", methods=["GET", "POST"])
def suppliers_edit(id):
    conn = get_db()
    if request.method == "POST":
        name = request.form["supplierName"]
        contact = request.form["contactNumber"]
        address = request.form["address"]
        stat = request.form["status"]
        conn.execute("UPDATE suppliers SET supplierName=?, contactNumber=?, address=?, status=? WHERE id=?",
                     (name, contact, address, stat, id))
        conn.commit()
        conn.close()
        return redirect(url_for("suppliers"))
    supplier = conn.execute(
        "SELECT * FROM suppliers WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("suppliers/edit.html", supplier=supplier)

# DELETE


@app.route("/suppliers/delete/<int:id>")
def suppliers_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM suppliers WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("suppliers"))

# SEARCH


@app.route("/suppliers/search")
def suppliers_search():
    status = request.args.get("status", "")
    conn = get_db()
    suppliers = conn.execute(
        "SELECT * FROM suppliers WHERE status = ?",
        (status,)
    ).fetchall()
    conn.close()
    return render_template("suppliers/search.html", suppliers=suppliers, status=status)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
