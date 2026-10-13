
from app import app, inventory
from external_api import find_product as search_openfoodfacts


def view_inventory():
    if not inventory:
        print("Inventory is empty.")
        return

    print("\nCurrent Inventory:")

    for product in inventory:
        print(product)


def view_product():
    product_id = input("Enter product ID: ")

    for product in inventory:
        if str(product["id"]) == product_id:
            print("\nProduct found:")
            print(product)
            return

    print("Product not found.")


def add_product():
    try:
        product_id = int(input("Enter product ID: "))
        product_name = input("Enter product name: ")
        category = input("Enter category: ")
        price = float(input("Enter price: "))
        stock_quantity = int(input("Enter stock quantity: "))

        product = {
            "id": product_id,
            "product_name": product_name,
            "category": category,
            "price": price,
            "stock_quantity": stock_quantity
        }

        response = app.test_client().post(
            "/products",
            json=product
        )

        print(response.get_json())

    except ValueError:
        print("Please enter valid numbers for ID, price, and stock quantity.")


def update_product():
    try:
        product_id = int(input("Enter product ID to update: "))

        print("Enter the fields you want to update.")
        product_name = input("New product name (leave blank to skip): ")
        category = input("New category (leave blank to skip): ")
        price_input = input("New price (leave blank to skip): ")
        stock_input = input("New stock quantity (leave blank to skip): ")

        updates = {}

        if product_name:
            updates["product_name"] = product_name

        if category:
            updates["category"] = category

        if price_input:
            updates["price"] = float(price_input)

        if stock_input:
            updates["stock_quantity"] = int(stock_input)

        if not updates:
            print("No changes entered.")
            return

        response = app.test_client().patch(
            f"/products/{product_id}",
            json=updates
        )

        print(response.get_json())

    except ValueError:
        print("Please enter valid numbers for the ID, price, and stock quantity.")


def delete_product():
    try:
        product_id = int(input("Enter product ID to delete: "))

        response = app.test_client().delete(
            f"/products/{product_id}"
        )

        print(response.get_json())

    except ValueError:
        print("Please enter a valid product ID.")


def find_product():
    search = input("Enter product barcode or product name: ").strip()

    if not search:
        print("Please enter a barcode or product name.")
        return

    products = search_openfoodfacts(search)

    if not products:
        print("Product not found or API unavailable.")
        return

    # Barcode searches return one product dictionary
    if isinstance(products, dict):
        print("\nProduct found:")
        print(products)
        return

    # Name searches return a list of matching products
    print("\nMatching products:")

    for index, product in enumerate(products, start=1):
        print(f"{index}. {product['product_name']} - {product['brand']}")
        print(f"   Barcode: {product['barcode']}")

    choice = input(
        "\nEnter the number of the product to view, or 0 to cancel: "
    )

    if not choice.isdigit():
        print("Please enter a valid number.")
        return

    choice = int(choice)

    if choice == 0:
        print("Search cancelled.")
    elif 1 <= choice <= len(products):
        print("\nSelected product:")
        print(products[choice - 1])
    else:
        print("Invalid product number.")


def main():
    while True:
        print("\nInventory Management System")
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
            print("Invalid option. Please choose from 1 to 7.")


if __name__ == "__main__":
    main()
