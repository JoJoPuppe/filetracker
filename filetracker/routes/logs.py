import html
from json import dumps, loads
from typing import List

import bleach
from fastapi import APIRouter, Body, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from filetracker.models.item_log import ItemLog

router = APIRouter()


@router.post("/", response_description="added log message", response_model=ItemLog)
async def add_log(request: Request, log_message: ItemLog = Body(...)):
    log_message = jsonable_encoder(log_message)
    log_message["log_message"] = bleach.clean(log_message["log_message"])
    new_log = await request.app.database["item_log"].insert_one(log_message)
    created_log = await request.app.database["item_log"].find_one(
        {"_id": new_log.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_log)


@router.get("/{proj_id}", response_description="getting all log messages from project")
async def get_logs(request: Request, proj_id: str):
    cursor = (
        request.app.database["item_log"]
        .find({"project_id": proj_id})
        .sort("creation_date")
    )

    all_logs = await cursor.to_list(length=None)
    for log in all_logs:
        log["log_message"] = html.unescape(log["log_message"])
    return all_logs


@router.put(
    "/{log_id}", response_description="update log message", response_model=ItemLog
)
async def update_log(log_id: str, request: Request, log_message=Body(...)):
    log_message = jsonable_encoder(log_message)
    log_message["log_message"] = bleach.clean(log_message["log_message"])
    log_message_dict = {k: v for k, v in log_message.items() if v is not None}
    if len(log_message_dict) >= 1:
        await request.app.database["item_log"].update_one(
            {"_id": log_id}, {"$set": log_message_dict}
        )
        if (
            updated_item := await request.app.database["item_log"].find_one(
                {"_id": log_id}
            )
        ) is not None:
            return JSONResponse(
                status_code=status.HTTP_201_CREATED, content=updated_item
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"log with id {log_id} not found"
    )


@router.delete("/{log_id}", response_description="delete log message")
async def delete_log(log_id: str, request: Request, response: Response):
    delete_result = await request.app.database["item_log"].delete_one({"_id": log_id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"log with id {log_id} not found"
    )
