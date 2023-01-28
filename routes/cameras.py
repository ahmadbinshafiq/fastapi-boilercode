import asyncpg
from fastapi import APIRouter, status, HTTPException, Depends, Response

from sqlalchemy.future import select
from sqlalchemy import insert

from database.db import Database
from routes.schemas import Camera

db = Database()

router = APIRouter(
    prefix="/camera",
    tags=["Camera"],
    responses={404: {"description": "Not found"}},
)


@router.get('/all', tags=["Get all cameras"])
async def get_all_cameras(response: Response):
    await db.connect()
    query = select(db.cameras)
    result = await db.db.fetch_all(query)
    if result is None:
        raise HTTPException(status_code=404, detail="No cameras found")
    await db.disconnect()
    response.status_code = status.HTTP_200_OK
    return result


# TODO: check cam type and then add accordingly
@router.post('/add', tags=["Add camera"])
async def add_camera(camera: Camera, response: Response):
    await db.connect()
    # check if floor exists
    query = select(db.floors).where(db.floors.c.id == camera.floor_id)
    result = await db.db.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Floor not found")

    query = insert(db.cameras).values(
        name=camera.name,
        floor_id=camera.floor_id,
        stream_mode=camera.stream_mode,
    )
    try:
        await db.db.execute(query)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=404, detail="Camera already exists")

    await db.disconnect()
    response.status_code = status.HTTP_200_OK
    return {"message": "Camera added successfully"}
