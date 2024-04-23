from fastapi import APIRouter, HTTPException
from models import Order

router = APIRouter()

@router.post("/add")
def add_order(order: Order):
    if len(order.items) == 0:
        raise HTTPException(status_code=400, detail="Order has no items")
    if not Order.are_all_items_valid(order.items):
        raise HTTPException(status_code=400, detail="There are invalid items in the order")
    for item in order.items:
        if item.amount <= 0:
            raise HTTPException(status_code=400, detail="There are items with invalid amount in the order")
    Order.objects.put(order)
    return order