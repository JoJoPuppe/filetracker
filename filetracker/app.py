from fastapi import FastAPI
from filetracker.routes import project_home, item_file, item_folder
from fastapi.middleware.cors import CORSMiddleware
import motor.motor_asyncio

app = FastAPI()

origins = [
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(item_file.router, tags=["Item File"], prefix="/itemfile")
app.include_router(project_home.router, tags=["Project"])
app.include_router(item_folder.router, tags=["Item Folder"], prefix="/itemfolder")

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://localhost:27017"
    )
    app.database = app.mongodb_client["filetracker"]

@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "Welcome to your beanie"}
