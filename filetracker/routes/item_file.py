from fastapi import APIRouter, HTTPException, Body, status, Request
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from filetracker.models.item_file import ItemFile

router = APIRouter()

@router.post("/", response_description="Item added to Project", response_model=ItemFile)
async def add_item_file(request: Request, item_file: ItemFile = Body(...)):
    item_file = jsonable_encoder(item_file)
    if (await request.app.database["project_home"].find_one({"_id": item_file['project_id']})) is not None:
        new_item_file = await request.app.database["items"].insert_one(item_file)
        created_item_file = await request.app.database["items"].find_one({"_id": new_item_file.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_item_file)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with ID {item_file['project_id']} not found")




