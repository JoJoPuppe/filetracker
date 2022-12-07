from fastapi import FastAPI
from filetracker.routes import project_home, item_file, item_folder, logs
from fastapi.middleware.cors import CORSMiddleware
import motor.motor_asyncio

app = FastAPI()

origins = [ "*" ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(item_file.router, tags=["Item File"], prefix="/api/itemfile")
app.include_router(project_home.router, tags=["Project"], prefix="/api/project")
app.include_router(item_folder.router, tags=["Item Folder"], prefix="/api/itemfolder")
app.include_router(logs.router, tags=["Logs"], prefix="/api/logs")

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://localhost:27017"
    )
    app.database = app.mongodb_client["filetracker"]

# @app.get("/api", tags=["Root"])
# async def read_root() -> dict:
#     return {"message": "Welcome to your beanie"}
