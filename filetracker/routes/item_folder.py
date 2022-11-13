from fastapi import APIRouter, HTTPException, Body, status, Request
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from filetracker.models.item_folder import ItemFolder

router = APIRouter()

@router.post("/", response_description="Folder added to Project", response_model=ItemFolder)
async def add_folder(request: Request, item_folder: ItemFolder = Body(...)):
    item_folder = jsonable_encoder(item_folder)
    if (await request.app.database["project_home"].find_one({"_id": item_folder['project_id']})) is not None:
        new_item_folder = await request.app.database["items"].insert_one(item_folder)
        created_item_folder = await request.app.database["items"].find_one({"_id": new_item_folder.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_item_folder)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with ID {item_folder['project_id']} not found")




