import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False

def get_db_connection():
    conn = sqlite3.connect("menu.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/menu", methods=["GET"])
def get_menu():
    available = request.args.get("available")
    max_price = request.args.get("max_price")
    category = request.args.get("category")

    conn = get_db_connection()
    cursor = conn.cursor()

    conditions = []
    params = []

    if category:
        conditions.append("category = ?")
        params.append(category)

    if max_price:
        conditions.append("price <= ?")
        params.append(max_price)

    if available:
        conditions.append("available = ?")
        params.append(available)

    query = "SELECT * FROM dishes"

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    dishes = []
    
    for row in rows:
        dishes.append({
            "id": row["id"],
            "name": row["name"],
            "category": row["category"],
            "price": row["price"],
            "available": bool(row["available"])
        })

    return jsonify(dishes)


@app.route("/menu/<int:id>", methods=['GET'])
def get_dish(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dishes WHERE id = ?", (id,))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return jsonify({"error": "Dish not found"}), 404

    dish = {
        "id": row["id"],
        "name": row["name"],
        "category": row["category"],
        "price": row["price"],
        "available": bool(row["available"])
    }

    return jsonify(dish)

@app.route("/menu", methods=['POST'])
def add_dish():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get("name")
    category = data.get("category")
    price = data.get("price")
    available = data.get("available", True)

    if not name or not category or price is None:
        return jsonify({"error": "Fields name, category, price are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO dishes (name, category, price, available) VALUES (?, ?, ?, ?)",
        (name, category, price, 1 if available else 0)
    )

    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "id": new_id,
        "name": name,
        "category": category,
        "price": price,
        "available": available
    }), 201

@app.route("/menu/<int:id>", methods=['DELETE'])
def delete_dish(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dishes WHERE id = ?", (id,))
    if cursor.rowcount is None:
        return jsonify({"error":"No such dish"}),404

    cursor.execute("DELETE FROM dishes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted", "id": id})

@app.route("/menu/<int:id>", methods=['PATCH'])
def update_dish(id):
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    fields = []
    values = []
    for field in ["name", "category", "price", "available"]:
        if field in data:
            fields.append(f"{field} = ?")
            values.append(data[field])

    if not fields:
        return jsonify({"error": "No fields to update"}), 400

    values.append(id)

    query = f"""
        UPDATE dishes
        SET {", ".join(fields)}
        WHERE id = ?
    """

    cursor.execute(query, values)
    conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "Dish not found"}), 404
    conn.close()
    return jsonify({"message": "Dish updated"})


if __name__ == "__main__":
    app.run(debug=True)