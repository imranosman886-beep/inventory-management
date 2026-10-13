
import requests


def find_product(search):
    search = search.strip()

    if not search:
        return None

    headers = {
        "User-Agent": "InventoryManagementApp/1.0 (student project)"
    }

    try:
        # Search by barcode
        if search.isdigit():
            url = f"https://world.openfoodfacts.org/api/v2/product/{search}.json"

            response = requests.get(
                url,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            if data.get("status") != 1:
                return None

            product = data.get("product", {})

            return {
                "product_name": product.get("product_name", "Unknown"),
                "brand": product.get("brands", "Unknown"),
                "ingredients_text": product.get("ingredients_text", ""),
                "barcode": search
            }

        # Search by product name
        url = "https://world.openfoodfacts.org/cgi/search.pl"

        params = {
            "search_terms": search,
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": 10,
            "fields": "code,product_name,brands,ingredients_text"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])
        matches = []

        for product in products:
            if product.get("product_name"):
                matches.append({
                    "product_name": product.get("product_name", "Unknown"),
                    "brand": product.get("brands", "Unknown"),
                    "ingredients_text": product.get("ingredients_text", ""),
                    "barcode": product.get("code", "")
                })

        return matches if matches else None

    except requests.Timeout:
        print("The OpenFoodFacts search took too long. Please try again later.")
        return None

    except (requests.RequestException, ValueError) as error:
        print("OpenFoodFacts API error:", error)
        return None
