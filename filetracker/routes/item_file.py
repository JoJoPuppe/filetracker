from typing import List

from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from filetracker.models.item_file import ItemFile

router = APIRouter()


@router.post("/", response_description="Item added to Project", response_model=ItemFile)
async def add_item_file(request: Request, item_file: ItemFile = Body(...)):
    item_file = jsonable_encoder(item_file)
    if (
        await request.app.database["project_home"].find_one(
            {"_id": item_file["project_id"]}
        )
    ) is not None:
        new_item_file = await request.app.database["items"].insert_one(item_file)
        created_item_file = await request.app.database["items"].find_one(
            {"_id": new_item_file.inserted_id}
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content=created_item_file
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Project with ID {item_file['project_id']} not found",
    )


@router.get(
    "/{item_id}", response_description="get item file by id", response_model=ItemFile
)
async def get_item_file(item_id: str, request: Request):
    if (
        item_file := await request.app.database["items"].find_one({"_id": item_id})
    ) is not None:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item_file)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item File with ID {item_id} not found",
    )

@router.put("/{item_id}", response_description="update item file", response_model=ItemFile)
async def update_item_file(item_id: str, request: Request, item_file = Body(...)):
    item_file = jsonable_encoder(item_file)
    item_file = {k: v for k, v in item_file.items() if v is not None}
    if len(item_file) >= 1:
        await request.app.database["items"].update_one(
            {"_id": item_id}, {"$set": item_file}
        )
        if (
                updated_item := await request.app.database["items"].find_one({"_id": item_id})
        ) is not None:
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=updated_item)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")


