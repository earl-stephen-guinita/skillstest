from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_db

app = Flask(__name__)

# MENU


@app.route("/")
def index():
    return render_template("restaurant.html")

# ===== MENU ITEMS =====

# READ


@app.route("/menu_items")
def menu_items():
    conn = get_db()
    menu_items = conn.execute("SELECT * FROM menu_items").fetchall()
    conn.close()
    return render_template("menu_items/menu_items.html", menu_items=menu_items)

# CREATE


@app.route("/menu_items/add", methods=["GET", "POST"])
def menu_items_add():
    if request.method == "POST":
        item = request.form["itemName"]
        category = request.form["category"]
        price = request.form["price"]
        status = request.form["status"]
        conn = get_db()
        conn.execute("INSERT INTO menu_items (itemName, category, price, status) VALUES (?, ?, ?, ?)",
                     (item, category, price, status))
        conn.commit()
        conn.close()
        return redirect(url_for("menu_items"))
    return render_template("menu_items/add.html")

# UPDATE


@app.route("/menu_items/edit/<int:id>", methods=["GET", "POST"])
def menu_items_edit(id):
    conn = get_db()
    if request.method == "POST":
        item = request.form["itemName"]
        category = request.form["category"]
        price = request.form["price"]
        status = request.form["status"]
        conn.execute("UPDATE menu_items SET itemName=?, category=?, price=?, status=? WHERE id=?",
                     (item, category, price, status, id))
        conn.commit()
        conn.close()
        return redirect(url_for("menu_items"))
    menu_item = conn.execute(
        "SELECT * FROM menu_items WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("menu_items/edit.html", menu_item=menu_item)

# DELETE


@app.route("/menu_items/delete/<int:id>")
def menu_items_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM menu_items WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("menu_items"))

# SEARCH


@app.route("/menu_items/search")
def menu_items_search():
    category = request.args.get("category", "")
    conn = get_db()
    menu_items = conn.execute(
        "SELECT * FROM menu_items WHERE category = ?",
        (category,)
    ).fetchall()
    conn.close()
    return render_template("menu_items/search.html", menu_items=menu_items, category=category)

# ===== ORDERS =====

# READ


@app.route("/orders")
def orders():
    conn = get_db()
    orders = conn.execute("SELECT * FROM orders").fetchall()
    conn.close()
    return render_template("orders/orders.html", orders=orders)

# CREATE


@app.route("/orders/add", methods=["GET", "POST"])
def orders_add():
    if request.method == "POST":
        customer = request.form["customerName"]
        item = request.form["itemName"]
        quantity = request.form["quantity"]
        price = request.form["totalPrice"]
        order = request.form["orderDate"]
        conn = get_db()
        conn.execute("INSERT INTO orders (customerName, itemName, quantity, totalPrice, orderDate) VALUES (?, ?, ?, ?, ?)",
                     (customer, item, quantity, price, order))
        conn.commit()
        conn.close()
        return redirect(url_for("orders"))
    return render_template("orders/add.html")

# UPDATE


@app.route("/orders/edit/<int:id>", methods=["GET", "POST"])
def orders_edit(id):
    conn = get_db()
    if request.method == "POST":
        customer = request.form["customerName"]
        item = request.form["itemName"]
        quantity = request.form["quantity"]
        price = request.form["totalPrice"]
        order = request.form["orderDate"]
        conn.execute("UPDATE orders SET customerName=?, itemName=?, quantity=?, totalPrice=?, orderDate=? WHERE id=?",
                     (customer, item, quantity, price, order, id))
        conn.commit()
        conn.close()
        return redirect(url_for("orders"))
    order = conn.execute("SELECT * FROM orders WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("orders/edit.html", order=order)

# DELETE


@app.route("/orders/delete/<int:id>")
def orders_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM orders WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("orders"))

# SEARCH


@app.route("/orders/search")
def orders_search():
    keyword = request.args.get("keyword", "")
    conn = get_db()
    orders = conn.execute(
        "SELECT * FROM orders WHERE customerName LIKE ?",
        ('%' + keyword + '%',)
    ).fetchall()
    conn.close()
    return render_template("orders/search.html", orders=orders, keyword=keyword)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
