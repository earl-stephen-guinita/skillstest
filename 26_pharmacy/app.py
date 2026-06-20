from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_db

app = Flask(__name__)

# MENU


@app.route("/")
def index():
    return render_template("pharmacy.html")

# ===== MEDICINES =====

# READ


@app.route("/medicines")
def medicines():
    conn = get_db()
    medicines = conn.execute("SELECT * FROM medicines").fetchall()
    conn.close()
    return render_template("medicines/medicines.html", medicines=medicines)

# CREATE


@app.route("/medicines/add", methods=["GET", "POST"])
def medicines_add():
    if request.method == "POST":
        med = request.form["medicineName"]
        cat = request.form["category"]
        price = request.form["price"]
        stock = request.form["stock"]
        stat = request.form["status"]
        conn = get_db()
        conn.execute("INSERT INTO medicines (medicineName, category, price, stock, status) VALUES (?, ?, ?, ?, ?)",
                     (med, cat, price, stock, stat))
        conn.commit()
        conn.close()
        return redirect(url_for("medicines"))
    return render_template("medicines/add.html")

# UPDATE


@app.route("/medicines/edit/<int:id>", methods=["GET", "POST"])
def medicines_edit(id):
    conn = get_db()
    if request.method == "POST":
        med = request.form["medicineName"]
        cat = request.form["category"]
        price = request.form["price"]
        stock = request.form["stock"]
        stat = request.form["status"]
        conn.execute("UPDATE medicines SET medicineName=?, category=?, price=?, stock=?, status=? WHERE id=?",
                     (med, cat, price, stock, stat, id))
        conn.commit()
        conn.close()
        return redirect(url_for("medicines"))
    medicine = conn.execute(
        "SELECT * FROM medicines WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("medicines/edit.html", medicine=medicine)

# DELETE


@app.route("/medicines/delete/<int:id>")
def medicines_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM medicines WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("medicines"))

# SEARCH


@app.route("/medicines/search")
def medicines_search():
    category = request.args.get("category", "")
    conn = get_db()
    medicines = conn.execute(
        "SELECT * FROM medicines WHERE category = ?",
        (category,)
    ).fetchall()
    conn.close()
    return render_template("medicines/search.html", medicines=medicines, category=category)

# ===== CUSTOMERS =====

# READ


@app.route("/customers")
def customers():
    conn = get_db()
    customers = conn.execute("SELECT * FROM customers").fetchall()
    conn.close()
    return render_template("customers/customers.html", customers=customers)

# CREATE


@app.route("/customers/add", methods=["GET", "POST"])
def customers_add():
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        contact = request.form["contactNumber"]
        add = request.form["address"]
        conn = get_db()
        conn.execute("INSERT INTO customers (firstName, lastName, contactNumber, address) VALUES (?, ?, ?, ?)",
                     (fName, lName, contact, add))
        conn.commit()
        conn.close()
        return redirect(url_for("customers"))
    return render_template("customers/add.html")

# UPDATE


@app.route("/customers/edit/<int:id>", methods=["GET", "POST"])
def customers_edit(id):
    conn = get_db()
    if request.method == "POST":
        fName = request.form["firstName"]
        lName = request.form["lastName"]
        contact = request.form["contactNumber"]
        add = request.form["address"]
        conn.execute("UPDATE customers SET firstName=?, lastName=?, contactNumber=?, address=? WHERE id=?",
                     (fName, lName, contact, add, id))
        conn.commit()
        conn.close()
        return redirect(url_for("customers"))
    customer = conn.execute(
        "SELECT * FROM customers WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("customers/edit.html", customer=customer)

# DELETE


@app.route("/customers/delete/<int:id>")
def customers_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM customers WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("customers"))

# SEARCH


@app.route("/customers/search")
def customers_search():
    keyword = request.args.get("keyword", "")
    conn = get_db()
    customers = conn.execute(
        "SELECT * FROM customers WHERE lastName LIKE ?",
        ('%' + keyword + '%',)
    ).fetchall()
    conn.close()
    return render_template("customers/search.html", customers=customers, keyword=keyword)

# ===== SALES =====

# READ


@app.route("/sales")
def sales():
    conn = get_db()
    sales = conn.execute("SELECT * FROM sales").fetchall()
    conn.close()
    return render_template("sales/sales.html", sales=sales)

# CREATE


@app.route("/sales/add", methods=["GET", "POST"])
def sales_add():
    if request.method == "POST":
        customer = request.form["customerName"]
        medicine = request.form["medicineName"]
        quantity = request.form["quantity"]
        price = request.form["totalPrice"]
        date = request.form["saleDate"]
        conn = get_db()
        conn.execute("INSERT INTO sales (customerName, medicineName, quantity, totalPrice, saleDate) VALUES (?, ?, ?, ?, ?)",
                     (customer, medicine, quantity, price, date))
        conn.commit()
        conn.close()
        return redirect(url_for("sales"))
    return render_template("sales/add.html")

# UPDATE


@app.route("/sales/edit/<int:id>", methods=["GET", "POST"])
def sales_edit(id):
    conn = get_db()
    if request.method == "POST":
        customer = request.form["customerName"]
        medicine = request.form["medicineName"]
        quantity = request.form["quantity"]
        price = request.form["totalPrice"]
        date = request.form["saleDate"]
        conn.execute("UPDATE sales SET customerName=?, medicineName=?, quantity=?, totalPrice=?, saleDate=? WHERE id=?",
                     (customer, medicine, quantity, price, date, id))
        conn.commit()
        conn.close()
        return redirect(url_for("sales"))
    sale = conn.execute("SELECT * FROM sales WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("sales/edit.html", sale=sale)

# DELETE


@app.route("/sales/delete/<int:id>")
def sales_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM sales WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("sales"))

# SEARCH


@app.route("/sales/search")
def sales_search():
    keyword = request.args.get("keyword", "")
    conn = get_db()
    sales = conn.execute(
        "SELECT * FROM sales WHERE medicineName LIKE ?",
        ('%' + keyword + '%',)
    ).fetchall()
    conn.close()
    return render_template("sales/search.html", sales=sales, keyword=keyword)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
