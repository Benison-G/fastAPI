from fastapi import Depends, FastAPI
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

# DB creation

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Welcome to my first python project"

products = [
    Product(id= 1, name= "Mobile", description= "Phone device", price= 9999.99, quantity= 10),
        Product(id= 2, name= "Laptop", description= "A computer", price= 19999.99, quantity= 12),
            Product(id= 3, name= "Table", description= "An equipment for home", price= 999, quantity= 8),
                Product(id= 4, name= "Utensils", description= "A kit for kitchen", price= 999, quantity= 20)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Product).count()

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    return db.query(database_models.Product).all()

@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "Item not found"

@app.post("/products")
def add_product(product: Product):
    products.append(product)
    return product;

@app.put("/products")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if (products[i].id == id):
            products[i] = product;
            return "Product added"
    return "Product not found"

@app.delete("/products")
def delete_product(id: int):
    for i in range(len(products)):
        if (products[i].id == id):
            del products[i]
            return "Delete success"
    return "Product not found"    