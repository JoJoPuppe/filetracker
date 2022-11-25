from fastapi import APIRouter, HTTPException, Body, status, Request
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from filetracker.models.project_home import ProjectHome
from ..tree.tree import tree
from json import dumps

router = APIRouter()

@router.post("/", response_description="Project added to the database", response_model=ProjectHome)
async def add_project(request: Request, project: ProjectHome = Body(...)):
    project = jsonable_encoder(project)
    new_project = await request.app.database["project_home"].insert_one(project)
    created_project = await request.app.database["project_home"].find_one({"_id": new_project.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_project)


@router.get("/", response_description="get all project", response_model=List[ProjectHome])
async def list_projects(request: Request):
    project = await request.app.database["project_home"].find().to_list(length=100)

    return project


@router.get("/{id}", response_description="get project by id")
async def find_project(proj_id: str, request: Request):
    if (project := await request.app.database["items"].find({"project_id": proj_id}).to_list(length=300)) is not None:

        def id(node):
          return node['_id']

        def parent(node):
          return node['parent']

        def create_new_dict(node, children):
            n = node.update({"children": children(id(node))})
            return n


        A = project
        C = tree \
          ( A
          , parent
          , lambda node, children:
              dict([*list(node.items()), ("children", children(id(node)))])
          )

        return dumps(C)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with ID {proj_id} not found")

