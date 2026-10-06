import requests
from external_api import find_product as search_openfoodfacts


BASE_URL = "http://127.0.0.1:5000"


def view_inventory():
    try:
        response = requests.get(f"{BASE_URL}/inventory")

        if response.status_code == 200:
            products = response.json()

            for product in products:
                print(product)
        else:
            print("Could not get inventory.")

    except requests.RequestException:
        print("Could not connect to the Flask API.")


def view_product():
    item_id = input("Enter product ID: ")

    try:
        item_id = int(item_id)
    except ValueError:
        print("Product ID must be a number.")
        return

    try:
        response = requests.get(f"{BASE_URL}/inventory/{item_id}")

        if response.status_code == 200:
            print(response.json())
        else:
            print("Product not found.")

    except requests.RequestException:
        print("Could not connect to the Flask API.")


def add_product():
    product_name = input("Product name: ")
    brand = input("Brand: ")

    try:
        price = float(input("Price: "))
    except ValueError:
        print("Price must be a number.")
        return

    try:
        stock = int(input("Stock: "))
    except ValueError:
        print("Stock must be a whole number.")
        return

    barcode = input("Barcode: ")
    ingredients = input("Ingredients: ")

    product = {
        "product_name": product_name,
        "brand": brand,
        "price": price,
        "stock": stock,
        "barcode": barcode,
        "ingredients_text": ingredients
    }

    try:
        response = requests.post(
            f"{BASE_URL}/inventory",
            json=product
        )

        if response.status_code == 201:
            print("Product added successfully.")
            print(response.json())
        else:
            print("Could not add product.")

    except requests.RequestException:
        print("Could not connect to the Flask API.")


def update_product():
    item_id = input("Enter product ID: ")

    try:
        item_id = int(item_id)
    except ValueError:
        print("Product ID must be a number.")
        return

    price = input("New price (press Enter to skip): ")
    stock = input("New stock (press Enter to skip): ")

    data = {}

    if price:
        try:
            data["price"] = float(price)
        except ValueError:
            print("Price must be a number.")
            return

    if stock:
        try:
            data["stock"] = int(stock)
        except ValueError:
            print("Stock must be a whole number.")
            return

    if not data:
        print("No changes were entered.")
        return

    try:
        response = requests.patch(
            f"{BASE_URL}/inventory/{item_id}",
            json=data
        )

        if response.status_code == 200:
            print("Product updated successfully.")
            print(response.json())
        else:
            print("Product not found.")

    except requests.RequestException:
        print("Could not connect to the Flask API.")


def delete_product():
    item_id = input("Enter product ID: ")

    try:
        item_id = int(item_id)
    except ValueError:
        print("Product ID must be a number.")
        return

    try:
        response = requests.delete(
            f"{BASE_URL}/inventory/{item_id}"
        )

        if response.status_code == 200:
            print("Product deleted successfully.")
        else:
            print("Product not found.")

    except requests.RequestException:
        print("Could not connect to the Flask API.")


def find_product():
    search = input("Enter product barcode or product name: ")

    if not search:
        print("Please enter a barcode or product name.")
        return

    product = search_openfoodfacts(search)

    if product:
        print("\nProduct found:")
        print(product)
    else:
        print("Product not found or API unavailable.")


def main():
    while True:
        print("\n===== INVENTORY MANAGEMENT =====")
        print("1. View all inventory")
        print("2. View one product")
        print("3. Add product")
        print("4. Update product")
        print("5. Delete product")
        print("6. Find product on OpenFoodFacts")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            view_inventory()

        elif choice == "2":
            view_product()

        elif choice == "3":
            add_product()

        elif choice == "4":
            update_product()

        elif choice == "5":
            delete_product()

        elif choice == "6":
            find_product()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()