from starlette.templating import Jinja2Templates
from werkzeug.security import generate_password_hash
from fastapi import APIRouter, Request
from HW6.dbmodels import database, users
from HW6.pymodels import User, UserIn
from starlette.responses import HTMLResponse


router = APIRouter()
templates = Jinja2Templates(directory='./HW6/templates')


@router.get("/fake_users/{count}")
async def create_note(count: int):
    for i in range(count):
        query = users.insert().values(
            name=f"user{i}",
            surname=f"surname{i}",
            email=f"user{i}@example.com",
            password_hash=generate_password_hash(f"password{i}")
        )
        await database.execute(query)
    return {"message": f"created {count} fake users"}


@router.get('/users/', response_class=HTMLResponse, response_model=None)
async def get_tasks(request: Request):
    query = users.select()
    user_list = await database.fetch_all(query)
    return templates.TemplateResponse('users.html',
                                      {'request': request,
                                       'Users': user_list,
                                       'title': 'HomeWork 6. Shop'})


@router.post("/user", response_model=UserIn)
async def create_user(user: UserIn):
    query = users.insert().values(**user.model_dump())
    last_record_id = await database.execute(query)
    return {**user.model_dump(), "id": last_record_id}


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@router.get("/users/{user_id}", response_class=HTMLResponse, response_model=None)
async def read_user(user_id: int, request: Request):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_all(query)
    return templates.TemplateResponse('users.html',
                                      {'request': request,
                                       'Users': user,
                                       'title': 'HomeWork 6. Shop'})


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}