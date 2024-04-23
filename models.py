import queue
from pydantic import BaseModel
from typing import ClassVar, List
from structures import Stack
from queue import Queue
from datetime import datetime
import uuid

class Product(BaseModel):
    uuid: str = str(uuid.uuid4())
    name: str
    price: float
    amount: int = 1

    objects: ClassVar[List['Product']] = []

class OrderItem(BaseModel):
    product_uuid: str
    amount: int

class Order(BaseModel):
    uuid: str = str(uuid.uuid4())
    items: List[OrderItem]

    objects: ClassVar[Queue] = Queue()

    @staticmethod
    def are_all_items_valid(items):
        for item in items:
            if not next((p for p in Product.objects if p.uuid == item.product_uuid), None):
                return False
        return True

    @staticmethod
    def process_last_order():
        if Order.objects.empty():
            return
        order = Order.objects.get_nowait()
        """ treating possible exceptions """
        for item in order.items:
            product = next((p for p in Product.objects if p.uuid == item.product_uuid), None)
            if not product:
                print("There was an unknown product in the order, order has been cancelled")
                raise RuntimeError("Unknown product")
            if product.amount < item.amount:
                print("There was not enough stock for the product, order has been cancelled")
                raise RuntimeError("Not enough stock")
            if len(order.items) == 0:
                print ("There are no items in the order, order has been cancelled")
                raise RuntimeError("Empty order")
        """ processing order """
        for item in order.items:
            product = next((p for p in Product.objects if p.uuid == item.product_uuid), None)
            product.amount -= item.amount
        Purchases.objects.push(order)
        print(f"Order of uuid ${order.uuid} processed")

class Purchases(BaseModel):

    objects: ClassVar[Stack] = Stack()

