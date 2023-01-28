from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str


class Camera(BaseModel):
    stream_mode: int
    name: str
    ip: str = None
    port: str = None
    typeof: str = None
    protocol: str = None
    local_path: str = None
    floor_id: int


class Floor(BaseModel):
    name: str
