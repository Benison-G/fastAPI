from fastapi import FastAPI
from models import Product

app = FastAPI()

@app.get("/")
def greet():
    return "Welcome to my first python project"

products = [
    Product(id= 1, name= "Mobile", description= "Phone device", price= 9999.99, quantity= 10),
        Product(id= 1, name= "Laptop", description= "A computer", price= 19999.99, quantity= 12),
            Product(id= 1, name= "Table", description= "An equipment for home", price= 999, quantity= 8),
                Product(id= 1, name= "Utensils", description= "A kit for kitchen", price= 999, quantity= 20)
]

@app.get("/products")
def get_all_products(): 
    return products