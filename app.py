from flask import Flask, jsonify, request
from data import inventory

app = Flask(__name__)


# GET all inventory
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200


# GET one inventory item
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item), 200

    return jsonify({"error": "Product not found"}), 404


# POST - add a new inventory item
@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    new_id = 1

    if inventory:
        new_id = max(item["id"] for item in inventory) + 1

    new_item = {
        "id": new_id,
        "product_name": data.get("product_name"),
        "brand": data.get("brand"),
        "price": data.get("price"),
        "stock": data.get("stock"),
        "barcode": data.get("barcode"),
        "ingredients_text": data.get("ingredients_text", "")
    }

    inventory.append(new_item)

    return jsonify(new_item), 201


# PATCH - update an inventory item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json()

    for item in inventory:
        if item["id"] == item_id:

            if "product_name" in data:
                item["product_name"] = data["product_name"]

            if "brand" in data:
                item["brand"] = data["brand"]

            if "price" in data:
                item["price"] = data["price"]

            if "stock" in data:
                item["stock"] = data["stock"]

            if "barcode" in data:
                item["barcode"] = data["barcode"]

            if "ingredients_text" in data:
                item["ingredients_text"] = data["ingredients_text"]

            return jsonify(item), 200

    return jsonify({"error": "Product not found"}), 404


# DELETE - remove an inventory item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            return jsonify({"message": "Product deleted"}), 200

    return jsonify({"error": "Product not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)