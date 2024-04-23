from fastapi import FastAPI
from contextlib import asynccontextmanager
from models import Product, Order, Purchases
from apscheduler.schedulers.background import BackgroundScheduler
import json

from routes.product import router as product_router
from routes.order import router as order_router
from routes.purchase import router as purchase_router

""" scheduler """

def scheduled_task():
    Order.process_last_order()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_task, 'interval', seconds=5)  # Executa a cada 60 segundos
    scheduler.start()

""" startup """

def populate_memory():
    products = json.load(open("products.json"))
    for product in products:
        Product.objects.append(Product(**product))

@asynccontextmanager
async def lifespan(app: FastAPI):
    populate_memory()
    start_scheduler()
    yield

app = FastAPI(lifespan=lifespan)

""" routes """

app.include_router(product_router, prefix="/product")
app.include_router(order_router, prefix="/order")
app.include_router(purchase_router, prefix="/purchase")

@app.get("/")
def root():
    total_products_ammount = sum([product.amount for product in Product.objects])
    total_purchases_made = Purchases.objects.size()
    return {"total_products_ammount": total_products_ammount, "total_purchases_made": total_purchases_made}