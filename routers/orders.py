import datetime
import random

from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from HW6.dbmodels import products, database, orders, users
from HW6.pymodels import Order, OrderIn

router = APIRouter()
templates = Jinja2Templates(directory='./HW6/templates')


@router.get("/fake_orders/{count}")
async def create_fake_order(count: int):
    for i in range(count):
        users_query = users.select()
        users_list = await database.fetch_all(users_query)
        products_query = products.select()
        products_list = await database.fetch_all(products_query)

        query = orders.insert().values(
            user_id=random.choice([user_id[0] for user_id in users_list]),
            product_id=random.choice([products_id[0] for products_id in products_list]),
            order_date=datetime.datetime.now().strftime("%d/%m/%y, %H:%M:%S"),
            status=random.choice(['new', 'in_progress', 'done'])
        )
        await database.execute(query)
    return {'message': f'{count} fake orders create'}


@router.post("/order/{user_id}/{products_id}", response_model=OrderIn)
async def create_order(user_id: int, products_id: int, new_order: OrderIn):\

    query = orders.insert().values(
        user_id=user_id,
        product_id=products_id,
        order_date=datetime.datetime.now().strftime("%d/%m/%y, %H:%M:%S"),
        status=new_order.status
    )
    last_record_id = await database.execute(query)
    return {**new_order.model_dump(), "id": last_record_id}


@router.put("/order/{order_id}", response_model=OrderIn)
async def update_order(order_id, new_goods: OrderIn):

    query = orders.update().where(orders.c.id == order_id).values(
        status=new_goods.status,
        order_date=datetime.datetime.now().strftime("%d/%m/%y, %H:%M:%S")
    )
    await database.execute(query)
    return {**new_goods.model_dump(), "id": order_id}


@router.get("/orders/", response_class=HTMLResponse, response_model=None)
async def read_orders(request: Request):
    query = orders.select()
    order_list = await database.fetch_all(query)
    return templates.TemplateResponse('orders.html',
                                      {'request': request,
                                       'Orders': order_list,
                                       'title': 'HomeWork 6. Shop'})


@router.get("/orders/{order_id}", response_model=None, response_class=HTMLResponse)
async def read_order(order_id: int, request: Request):
    query = orders.select().where(orders.c.id == order_id)
    order_list = await database.fetch_all(query)
    return templates.TemplateResponse('orders.html',
                                      {'request': request,
                                       'Orders': order_list,
                                       'title': 'HomeWork 6. Shop'})


@router.delete("/order/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)

    await database.execute(query)
    return {'message': 'Заказ удален'}