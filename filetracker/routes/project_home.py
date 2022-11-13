from fastapi import APIRouter, HTTPException, Body, status, Request
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from filetracker.models.project_home import ProjectHome

router = APIRouter()

@router.post("/", response_description="Project added to the database", response_model=ProjectHome)
async def add_project(request: Request, project: ProjectHome = Body(...)):
    project = jsonable_encoder(project)
    new_project = await request.app.database["project_home"].insert_one(project)
    created_project = await request.app.database["project_home"].find_one({"_id": new_project.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_project)


@router.get("/", response_description="get all project", response_model=List[ProjectHome])
async def list_projects(request: Request):
    project = await request.app.database["project_home"].find_one({"_id": id})
    return project


@router.get("/{id}", response_description="get project by id", response_model=ProjectHome)
async def find_project(id: str, request: Request):
    if (project := await request.app.database["project_home"].find_one({"_id": id})) is not None:
            return project

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with ID {id} not found")

