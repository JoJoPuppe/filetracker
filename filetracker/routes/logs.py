
from fastapi import APIRouter, HTTPException, Body, status, Request
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from filetracker.models.item_log import ItemLog
from json import dumps, loads
import bleach

router = APIRouter()

@router.post("/", response_description="added log message", response_model=ItemLog)
async def add_log(request: Request, log_message: ItemLog = Body(...)):
    log_message = jsonable_encoder(log_message)
    log_message["log_message"] = bleach.clean(log_message['log_message'])
    new_log = await request.app.database["item_log"].insert_one(log_message)
    created_log = await request.app.database["item_log"].find_one({"_id": new_log.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_log)


@router.get("/{proj_id}", response_description="getting all log messages from project", response_model=ItemLog)
async def get_logs(request: Request,  proj_id: str):
    all_logs = await request.app.database["item_log"].find({"project_id": proj_id}).sort({"creation_date": 1}).to_list(length=300)
    return all_logs
