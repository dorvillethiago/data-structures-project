from fastapi import APIRouter
from models import Purchases, Product

router = APIRouter()

@router.get("/list")
def list_purchases():
    return Purchases.objects

@router.put("/revert_last")
def revert_last_purchase():
    last_puchase = Purchases.objects.pop()
    for item in last_puchase.items:
        product = next((p for p in Product.objects if p.uuid == item.product_uuid), None)
        product.amount += item.amount
    return last_puchase