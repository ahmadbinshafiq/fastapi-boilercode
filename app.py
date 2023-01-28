from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import users, cameras, floors

app = FastAPI(title="FYP", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World!", "status": 200}


app.include_router(users.router)
app.include_router(cameras.router)
app.include_router(floors.router)
