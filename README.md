# Inventory Management System

This is a simple Flask inventory management system.

It allows users to:

* View inventory products
* View one product
* Add a product
* Update a product's price and stock
* Delete a product
* Search for products using the OpenFoodFacts API
* Use a command-line interface (CLI)

## Technologies Used

* Python
* Flask
* Requests
* Pytest
* OpenFoodFacts API

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

## Running the Flask API

Run:

```bash
python app.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

## API Routes

| Method | Route             | Description       |
| ------ | ----------------- | ----------------- |
| GET    | `/inventory`      | View all products |
| GET    | `/inventory/<id>` | View one product  |
| POST   | `/inventory`      | Add a product     |
| PATCH  | `/inventory/<id>` | Update a product  |
| DELETE | `/inventory/<id>` | Delete a product  |

## Using the CLI

Keep the Flask server running in one terminal.

Open another terminal and run:

```bash
python cli.py
```

The CLI gives you options to:

1. View all inventory
2. View one product
3. Add a product
4. Update a product
5. Delete a product
6. Find a product on OpenFoodFacts
7. Exit

## OpenFoodFacts

The project uses the OpenFoodFacts API to search for food products.

You can search using:

* A product barcode
* A product name

The API returns information such as the product name, brand, ingredients, and barcode.

## Running Tests

Run all tests with:

```bash
python -m pytest
```

The tests cover the Flask API, CLI, and OpenFoodFacts API functions.

## Project Structure

```text
inventory-management/
├── app.py
├── cli.py
├── data.py
├── external_api.py
├── requirements.txt
├── README.md
└── tests/
    ├── test_api.py
    ├── test_cli.py
    └── test_external_api.py
```

## Notes

The inventory uses a simple Python list as a mock database.

The data will reset when the Flask application is restarted.
