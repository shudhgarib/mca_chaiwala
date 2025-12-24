from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "secret123"

PASSWORD = "satyanas"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def get_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            mobile_number TEXT UNIQUE,
            tea_count INTEGER DEFAULT 0,
            coffee_count INTEGER DEFAULT 0,
            visit_count INTEGER DEFAULT 0,
            last_order TEXT,
            order_date TEXT,
            order_time TEXT
        )
    """)
    db.commit()
    db.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    cursor = db.cursor()

    # 🔹 Add Order (Admin only)
    if request.method == "POST" and session.get("admin"):
        name = request.form["name"].strip()
        mobile = request.form["mobile"].strip()
        order = request.form["order"]

        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        if order == "Tea":
            cursor.execute("""
                INSERT INTO orders
                (customer_name, mobile_number, tea_count, visit_count,
                 last_order, order_date, order_time)
                VALUES (?, ?, 1, 1, 'Tea', ?, ?)
                ON CONFLICT(mobile_number) DO UPDATE SET
                tea_count = tea_count + 1,
                visit_count = visit_count + 1,
                last_order = 'Tea',
                order_date = excluded.order_date,
                order_time = excluded.order_time
            """, (name, mobile, date, time))

        else:
            cursor.execute("""
                INSERT INTO orders
                (customer_name, mobile_number, coffee_count, visit_count,
                 last_order, order_date, order_time)
                VALUES (?, ?, 1, 1, 'Coffee', ?, ?)
                ON CONFLICT(mobile_number) DO UPDATE SET
                coffee_count = coffee_count + 1,
                visit_count = visit_count + 1,
                last_order = 'Coffee',
                order_date = excluded.order_date,
                order_time = excluded.order_time
            """, (name, mobile, date, time))

        db.commit()

    # 🔹 Public table (mobile hidden)
    cursor.execute("""
        SELECT customer_name, tea_count, coffee_count,
               visit_count, last_order, order_date, order_time
        FROM orders
        ORDER BY order_time DESC
    """)
    orders = cursor.fetchall()

    db.close()
    return render_template("index.html",
                           orders=orders,
                           admin=session.get("admin"))

@app.route("/login", methods=["POST"])
def login():
    if request.form["password"] == PASSWORD:
        session["admin"] = True
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
