from fastapi import APIRouter, status, HTTPException, Depends, Response

from sqlalchemy.future import select
from sqlalchemy import insert

from database.db import Database
from routes.schemas import User

db = Database()

router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.post('/login', tags=["Login"])
async def login(user: User, response: Response):
    await db.connect()
    query = select(db.users).where(db.users.c.email == user.email)
    result = await db.db.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    if result['password'] != user.password:
        raise HTTPException(status_code=404, detail="Incorrect password")
    await db.disconnect()
    response.status_code = status.HTTP_200_OK
    return {"message": "Login successful"}


@router.post('/signup', tags=["Signup"])
async def signup(user: User, response: Response):
    await db.connect()
    query = select(db.users).where(db.users.c.email == user.email)
    result = await db.db.fetch_one(query)
    if result is not None:
        raise HTTPException(status_code=404, detail="User already exists")
    query = insert(db.users).values(email=user.email, password=user.password)
    await db.db.execute(query)
    await db.disconnect()
    response.status_code = status.HTTP_200_OK
    return {"message": "Signup successful"}
