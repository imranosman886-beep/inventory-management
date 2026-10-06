import pytest

from app import app
from data import inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_inventory():
    inventory.clear()

    inventory.extend([
        {
            "id": 1,
            "product_name": "Organic Almond Milk",
            "brand": "Silk",
            "price": 5.99,
            "stock": 20,
            "barcode": "0123456789012",
            "ingredients_text": "Filtered water, almonds, cane sugar"
        },
        {
            "id": 2,
            "product_name": "Corn Flakes",
            "brand": "Kellogg's",
            "price": 4.50,
            "stock": 15,
            "barcode": "1234567890123",
            "ingredients_text": "Corn, sugar, malt flavor"
        }
    ])

    yield


def test_get_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2
    assert data[0]["product_name"] == "Organic Almond Milk"


def test_get_one_product(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1
    assert data["product_name"] == "Organic Almond Milk"


def test_get_product_not_found(client):
    response = client.get("/inventory/99")

    assert response.status_code == 404


def test_add_product(client):
    new_product = {
        "product_name": "Apple Juice",
        "brand": "Minute Maid",
        "price": 3.50,
        "stock": 10,
        "barcode": "9876543210123",
        "ingredients_text": "Apples, water, sugar"
    }

    response = client.post("/inventory", json=new_product)

    assert response.status_code == 201

    data = response.get_json()

    assert data["id"] == 3
    assert data["product_name"] == "Apple Juice"
    assert data["price"] == 3.50


def test_update_product(client):
    updated_data = {
        "price": 6.50,
        "stock": 25
    }

    response = client.patch("/inventory/1", json=updated_data)

    assert response.status_code == 200

    data = response.get_json()

    assert data["price"] == 6.50
    assert data["stock"] == 25


def test_update_product_not_found(client):
    response = client.patch(
        "/inventory/99",
        json={"price": 10.00}
    )

    assert response.status_code == 404


def test_delete_product(client):
    response = client.delete("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Product deleted"

    # Make sure the product was actually removed
    response = client.get("/inventory/1")

    assert response.status_code == 404


def test_delete_product_not_found(client):
    response = client.delete("/inventory/99")

    assert response.status_code == 404