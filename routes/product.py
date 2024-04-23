from fastapi import APIRouter, HTTPException
from models import Product

router = APIRouter()

@router.post("/register")
def register_product(product: Product):
    Product.objects.append(product)
    return product

@router.put("/increase")
def increase_product(product_uuid: str):
    product = next((p for p in Product.objects if p.uuid == product_uuid), None)
    if product:
        product.amount += 1
        return product
    raise HTTPException(status_code=404, detail="Product not found")

@router.put("/reduce")
def reduce_product(product_uuid: str):
    product = next((p for p in Product.objects if p.uuid == product_uuid), None)
    if product:
        if product.amount == 0:
            raise HTTPException(status_code=400, detail="Product out of stock")
        product.amount -= 1
        return product
    raise HTTPException(status_code=404, detail="Product not found")

@router.get("/list")
def list_products():
    return Product.objects