from random import choice
from starlette.templating import Jinja2Templates
from fastapi import APIRouter, Request
from HW6.dbmodels import database, products
from HW6.pymodels import Products, ProductsIn
from starlette.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory='./HW6/templates')


@router.get("/fake_products/")
async def create_fake_products():
    product_list = ['Апельсин', 'Банан', 'Кабачок', 'Арбуз', 'Мандарин']
    for item in product_list:
        query = products.insert().values(
            name=item,
            description=f"Крутой {item}",
            price=choice(range(100, 1000))
        )
        await database.execute(query)
    return {"message": f"created all fake products"}


@router.get('/products/', response_class=HTMLResponse, response_model=None)
async def get_tasks(request: Request):
    query = products.select()
    prod_list = await database.fetch_all(query)
    return templates.TemplateResponse('products.html',
                                      {'request': request,
                                       'Products': prod_list,
                                       'title': 'HomeWork 6. Shop'})


@router.post("/products", response_model=ProductsIn)
async def create_products(new_products: ProductsIn):
    query = products.insert().values(
        name=new_products.name,
        description=new_products.description, price=new_products.price)
    last_record_id = await database.execute(query)
    return {**new_products.model_dump(), "id": last_record_id}


@router.put("/products/{products_id}", response_model=Products)
async def update_products(products_id: int, new_products: ProductsIn):
    query = products.update().where(products.c.id == products_id).values(**new_products.model_dump())
    await database.execute(query)
    return {**new_products.model_dump(), "id": products_id}


@router.get("/products/{products_id}", response_model=Products)
async def read_products(products_id: int, request: Request):
    query = products.select().where(products.c.id == products_id)
    prod_list = await database.fetch_all(query)
    return templates.TemplateResponse('products.html',
                                      {'request': request,
                                       'Products': prod_list,
                                       'title': 'HomeWork 6. Shop'})


@router.delete("/products/{products_id}")
async def delete_products(products_id: int):
    query = products.delete().where(products.c.id == products_id)
    await database.execute(query)
    return {'message': 'Products deleted'}