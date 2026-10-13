from unittest.mock import patch, Mock

import requests

from external_api import find_product


def test_find_product_success():
    fake_response = Mock()
    fake_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Chocolate Bar",
            "brands": "Example Brand",
            "ingredients_text": "Sugar, cocoa, milk"
        }
    }

    with patch("external_api.requests.get", return_value=fake_response):
        result = find_product("123456789")

    assert result["product_name"] == "Chocolate Bar"
    assert result["brand"] == "Example Brand"
    assert result["ingredients_text"] == "Sugar, cocoa, milk"
    assert result["barcode"] == "123456789"


def test_find_product_not_found():
    fake_response = Mock()
    fake_response.json.return_value = {
        "status": 0
    }

    with patch("external_api.requests.get", return_value=fake_response):
        result = find_product("999999999")

    assert result is None


def test_find_product_api_error():
    with patch(
        "external_api.requests.get",
        side_effect=requests.RequestException("API error")
    ):
        result = find_product("123456789")

    assert result is None


def test_find_product_by_name():
        fake_response = Mock()
        fake_response.json.return_value = {
            "products": [
                {
                    "product_name": "Chocolate Bar",
                    "brands": "Example Brand",
                    "ingredients_text": "Sugar, cocoa, milk",
                    "code": "123456789"
                },
                {"brands": "Unnamed product"}
            ]
        }

        with patch("external_api.requests.get", return_value=fake_response) as mock_get:
            result = find_product(" Chocolate Bar ")

        assert result == [{
            "product_name": "Chocolate Bar",
            "brand": "Example Brand",
            "ingredients_text": "Sugar, cocoa, milk",
            "barcode": "123456789"
        }]
        assert mock_get.call_args.kwargs["params"]["fields"] == (
            "code,product_name,brands,ingredients_text"
        )