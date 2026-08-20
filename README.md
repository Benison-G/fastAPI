# FastAPI Product API

A small CRUD API for managing products with FastAPI, PostgreSQL, and SQLAlchemy. The project is intended as a learning example of how a FastAPI application connects to a relational database, defines models, initializes seed data, and exposes REST-style endpoints.

## Features

- FastAPI application with automatic interactive API documentation
- PostgreSQL database connection through SQLAlchemy
- SQLAlchemy ORM model for the `products` table
- Pydantic validation model for product request data
- Automatic table creation when the application module is imported
- Automatic insertion of four sample products when the table is empty
- CRUD endpoints for products
- Dependency-based database sessions that are closed after each request

## Technology Used

| Technology | Purpose |
| --- | --- |
| Python 3.14.7 | Runtime language used by the project environment |
| FastAPI 0.141.1 | Web framework and API routing |
| Uvicorn 0.52.3 | ASGI server used to run the application |
| SQLAlchemy 2.0.52 | ORM and database table operations |
| PostgreSQL | Relational database |
| psycopg2 2.9.12 | PostgreSQL driver used by SQLAlchemy |
| Pydantic 2.13.4 | Request data validation and serialization 

The versions above reflect the local virtual environment when this README was written. If you create a new environment, install compatible current versions instead.

## Project Structure

```text
fastAPI/
├── main.py              # FastAPI app, routes, table creation, and seed data
├── database.py          # SQLAlchemy engine and session factory
├── database_models.py   # SQLAlchemy ORM model and database metadata
├── models.py            # Pydantic request model
├── README.md            # Project documentation
└── myenv/               # Local virtual environment; do not commit this folder
```

### How the files work together

1. `database.py` creates a SQLAlchemy engine using the PostgreSQL connection URL and creates a session factory.
2. `database_models.py` defines the SQLAlchemy declarative base and the `Product` database table.
3. `models.py` defines the Pydantic `Product` model used to validate incoming JSON.
4. `main.py` creates the tables, seeds initial data if necessary, and registers the API routes.
5. `get_db()` creates a database session for a request and closes it in the `finally` block.

## Prerequisites

Install the following before running the application:

- Python 3.14 or a compatible Python 3 version
- PostgreSQL server
- Git, if you are cloning the project
- A PostgreSQL database named `fastapi-demo`

The current connection configuration expects:

```text
Host:     localhost
Port:     5432
Database: fastapi-demo
User:     postgres
Password: 1234
```

These values are currently hard-coded in `database.py`. Change them to match your local PostgreSQL installation before starting the app. For a shared or production application, move the credentials to environment variables instead of storing them in source code.

## PostgreSQL Setup

Create the database using `psql` or pgAdmin. With `psql`, an example command is:

```sql
CREATE DATABASE "fastapi-demo";
```

Make sure the PostgreSQL service is running and that the configured user can connect to this database.

## Installation on Windows

Open PowerShell in the project directory:

```powershell
cd "C:\Users\ADMIN\OneDrive\Documents\fastAPI"
```

Create a virtual environment if you do not already have one:

```powershell
py -m venv myenv
```

Activate it:

```powershell
.\myenv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use Command Prompt instead:

```bat
myenv\Scripts\activate.bat
```

Install the dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn sqlalchemy psycopg2
```

The current environment contains `psycopg2`. On Windows, `psycopg2-binary` is often easier to install for local development. Use one PostgreSQL driver, not both in the same environment.

## Configure the Database

Open `database.py` and verify the connection URL:

```python
db_url = "postgresql://postgres:1234@localhost:5432/fastapi-demo"
```

The format is:

```text
postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE
```

## Run the Application

Start the development server from the project root:

```powershell
python -m uvicorn main:app --reload
```

The API will normally be available at:

- API root: <http://127.0.0.1:8000/>
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

`--reload` watches for source changes and restarts the development server. Do not use it as the production process configuration.

## Database Initialization

When `main.py` loads:

1. `Base.metadata.create_all(bind=engine)` creates the `products` table if it does not exist.
2. `init_db()` counts the rows in the table.
3. If the table is empty, the four products in the `products` list are inserted and committed.
4. If rows already exist, no seed products are added again.

The seed data is:

| ID | Name | Price | Quantity |
| ---: | --- | ---: | ---: |
| 1 | Mobile | 9999.99 | 10 |
| 2 | Laptop | 19999.99 | 12 |
| 3 | Table | 999 | 8 |
| 4 | Utensils | 999 | 20 |

`create_all()` creates tables only; it does not insert rows. The insert happens because `init_db()` is called explicitly in `main.py`.

## API Usage

All product request bodies must include these fields:

```json
{
  "id": 5,
  "name": "Chair",
  "description": "A wooden chair",
  "price": 1499.99,
  "quantity": 6
}
```

### `GET /`

Returns a welcome message.

```powershell
Invoke-RestMethod http://127.0.0.1:8000/
```

### `GET /products`

Returns all products stored in PostgreSQL.

```powershell
Invoke-RestMethod http://127.0.0.1:8000/products
```

### `GET /products/{id}`

Returns one product by its ID.

```powershell
Invoke-RestMethod http://127.0.0.1:8000/products/1
```

### `POST /products`

Adds a product. The client currently supplies the ID, so the ID must be unique.

```powershell
$body = @{
  id = 5
  name = "Chair"
  description = "A wooden chair"
  price = 1499.99
  quantity = 6
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/products `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

### `PUT /products?id={id}`

Updates the product identified by the query-string `id`. The `id` is not part of the path.

```powershell
$body = @{
  id = 1
  name = "Updated Mobile"
  description = "Updated phone device"
  price = 10999.99
  quantity = 8
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/products?id=1" `
  -Method Put `
  -ContentType "application/json" `
  -Body $body
```

### `DELETE /products?id={id}`

Deletes the product identified by the query-string `id`.

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/products?id=5" `
  -Method Delete
```

The same operations can be tried from Swagger UI at `/docs` without writing commands.

## Current Limitations

This project is a learning application and is not yet production-ready:
