from unittest.mock import patch, Mock

import cli


def test_view_inventory(capsys):
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = [
        {
            "id": 1,
            "product_name": "Organic Almond Milk",
            "price": 5.99
        }
    ]

    with patch("cli.requests.get", return_value=fake_response):
        cli.view_inventory()

    captured = capsys.readouterr()

    assert "Organic Almond Milk" in captured.out


def test_view_product(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")

    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "price": 5.99
    }

    with patch("cli.requests.get", return_value=fake_response):
        cli.view_product()

    captured = capsys.readouterr()

    assert "Organic Almond Milk" in captured.out


def test_add_product(capsys, monkeypatch):
    inputs = iter([
        "Apple Juice",
        "Minute Maid",
        "3.50",
        "10",
        "9876543210123",
        "Apples, water, sugar"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    fake_response = Mock()
    fake_response.status_code = 201
    fake_response.json.return_value = {
        "id": 3,
        "product_name": "Apple Juice"
    }

    with patch("cli.requests.post", return_value=fake_response):
        cli.add_product()

    captured = capsys.readouterr()

    assert "Product added successfully." in captured.out


def test_update_product(capsys, monkeypatch):
    inputs = iter([
        "1",
        "6.50",
        "25"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "id": 1,
        "price": 6.50,
        "stock": 25
    }

    with patch("cli.requests.patch", return_value=fake_response):
        cli.update_product()

    captured = capsys.readouterr()

    assert "Product updated successfully." in captured.out


def test_delete_product(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")

    fake_response = Mock()
    fake_response.status_code = 200

    with patch("cli.requests.delete", return_value=fake_response):
        cli.delete_product()

    captured = capsys.readouterr()

    assert "Product deleted successfully." in captured.out


def test_find_product(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0123456789012")

    fake_product = {
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "barcode": "0123456789012"
    }

    with patch("cli.search_openfoodfacts", return_value=fake_product):
        cli.find_product()

    captured = capsys.readouterr()

    assert "Product found:" in captured.out
    assert "Organic Almond Milk" in captured.out