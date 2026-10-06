import requests


def find_product(search):
    try:
        # If the search is only numbers, treat it as a barcode
        if search.isdigit():
            url = f"https://world.openfoodfacts.org/api/v2/product/{search}.json"

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("status") == 1:
                product = data.get("product", {})

                return {
                    "product_name": product.get("product_name", "Unknown"),
                    "brand": product.get("brands", "Unknown"),
                    "ingredients_text": product.get("ingredients_text", ""),
                    "barcode": search
                }

            return None

        # Otherwise search by product name
        url = "https://world.openfoodfacts.org/cgi/search.pl"

        params = {
            "search_terms": search,
            "search_simple": 1,
            "action": "process",
            "json": 1
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        products = data.get("products", [])

        if products:
            product = products[0]

            return {
                "product_name": product.get("product_name", "Unknown"),
                "brand": product.get("brands", "Unknown"),
                "ingredients_text": product.get("ingredients_text", ""),
                "barcode": product.get("code", "")
            }

        return None

    except (requests.RequestException, ValueError):
        return None