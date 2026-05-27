from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

MENU = {
    "떡볶이": 4000,
    "잔치국수": 5000,
    "김치전": 6000,
    "마른안주": 10000,
    "골뱅이무침": 20000,
    "콜팝": 5000,
    "컵라면": 2000,
    "캔맥주": 3000,
    "막걸리": 3000,
    "음료": 2000
}

ORDERS_FILE = "db/orders.json"
SALES_FILE = "db/sales.json"


def load_json(file):
    if not os.path.exists(file):
        return []

    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/order", methods=["GET", "POST"])
def order():
    if request.method == "POST":
        orders = load_json(ORDERS_FILE)

        order_data = {
            "id": len(orders) + 1,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": {}
        }

        for menu in MENU:
            qty = int(request.form.get(menu, 0))

            if qty > 0:
                order_data["items"][menu] = qty

        orders.append(order_data)
        save_json(ORDERS_FILE, orders)

        return redirect(url_for("stats"))

    return render_template("order.html", menu=MENU)


@app.route("/sales", methods=["GET", "POST"])
def sales():
    orders = load_json(ORDERS_FILE)
    sales_data = load_json(SALES_FILE)

    total_orders = {menu: 0 for menu in MENU}
    total_sales = {menu: 0 for menu in MENU}

    for order in orders:
        for menu, qty in order["items"].items():
            total_orders[menu] += qty

    for sale in sales_data:
        for menu, qty in sale["items"].items():
            total_sales[menu] += qty

    if request.method == "POST":
        sale_record = {
            "id": len(sales_data) + 1,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": {}
        }

        for menu in MENU:
            qty = int(request.form.get(menu, 0))

            if qty > 0:
                sale_record["items"][menu] = qty

        sales_data.append(sale_record)
        save_json(SALES_FILE, sales_data)

        return redirect(url_for("stats"))

    return render_template(
        "sales.html",
        menu=MENU,
        total_orders=total_orders,
        total_sales=total_sales
    )

@app.route("/stats")
def stats():
    orders = load_json(ORDERS_FILE)
    sales = load_json(SALES_FILE)

    total_orders = {menu: 0 for menu in MENU}
    total_sales = {menu: 0 for menu in MENU}

    for order in orders:
        for menu, qty in order["items"].items():
            total_orders[menu] += qty

    for sale in sales:
        for menu, qty in sale["items"].items():
            total_sales[menu] += qty

    remain = {}

    for menu in MENU:
        remain[menu] = total_orders[menu] - total_sales[menu]

    return render_template(
        "stats.html",
        menu=MENU,
        total_orders=total_orders,
        total_sales=total_sales,
        remain=remain
    )


if __name__ == "__main__":
    app.run(debug=True)