from fastapi import APIRouter, status, HTTPException, Depends, Response

from sqlalchemy.future import select
from sqlalchemy import insert

from database.db import Database
from routes.schemas import Floor

db = Database()

router = APIRouter(
    prefix="/floor",
    tags=["Floor"],
    responses={404: {"description": "Not found"}},
)


@router.get('/all', tags=["Get all floors"])
async def get_all_floors(response: Response):
    await db.connect()
    query = select(db.floors)
    result = await db.db.fetch_all(query)
    if result is None:
        raise HTTPException(status_code=404, detail="No floors found")
    await db.disconnect()
    response.status_code = status.HTTP_200_OK
    return result


@router.post('/add', tags=["Add floor"])
async def add_floor(floor: Floor, response: Response):
    await db.connect()
    query = insert(db.floors).values(name=floor.name)
    await db.db.execute(query)
    await db.disconnect()
    response.status_code = status.HTTP_200_OK
    return {"message": "Floor added successfully"}


@router.get('/all/deep', tags=["Get all floors with cameras"])
async def get_all_floors_deep(response: Response):
    await db.connect()
    query = select(db.floors)
    dat = {}
    result = await db.db.fetch_all(query)
    if result is None:
        raise HTTPException(status_code=404, detail="No floors found")
    for floor in result:
        query = select(db.cameras).where(db.cameras.c.floor_id == floor['id'])
        camera = await db.db.fetch_all(query)
        dat[floor['name']] = camera

    await db.disconnect()
    response.status_code = status.HTTP_200_OK
    return dat
