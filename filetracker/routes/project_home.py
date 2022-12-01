from fastapi import APIRouter, HTTPException, Body, status, Request
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from filetracker.models.project_home import ProjectHome
from ..tree.tree import tree
from json import dumps, loads

router = APIRouter()


def build_flat_order(arr, no_parent):
    x = {}
    for i_idx, i in enumerate(arr):
        if 'children' in i:
            for j_idx, j in enumerate(i['children']):
                x[j['_id']] = {"parent": i['_id'], "order": j_idx}

                if 'children' in j:
                    x = {**x, **build_flat_order(i['children'], False)}
        if no_parent:
            x[i['_id']] = {"parent": None, "order": i_idx}
    return x

@router.post("/", response_description="Project added to the database", response_model=ProjectHome)
async def add_project(request: Request, project: ProjectHome = Body(...)):
    project = jsonable_encoder(project)
    new_project = await request.app.database["project_home"].insert_one(project)
    created_project = await request.app.database["project_home"].find_one({"_id": new_project.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_project)


@router.get("/", response_description="get all project", response_model=List[ProjectHome])
async def list_projects(request: Request):
    project = await request.app.database["project_home"].find().to_list(length=300)

    return project

@router.put("/reorder", response_description="reorder items")
async def reorder_project(request: Request, all_items = Body(...)):
    all_items = loads(all_items)
    order_dict = build_flat_order(all_items, True)

    get_project = await request.app.database['items'].find({"project_id": all_items[0]["project_id"]}).to_list(length=300)
    if get_project is not None:
        for item in get_project:
            if order_dict[item['_id']]['parent'] != item['parent'] or order_dict[item['_id']]['order'] != item['order_index']:
                item_file = {"parent": order_dict[item['_id']]['parent'],
                    "order_index": order_dict[item['_id']]['order']}
                await request.app.database["items"].update_one(
                    {"_id": item['_id']}, {"$set": item_file})


@router.get("/{proj_id}", response_description="get project by id")
async def find_project(proj_id: str, request: Request):
    cursor = request.app.database['items'].aggregate([
        {"$match": { "project_id": proj_id }},
        {"$sort": { "version": -1 }},
        {"$group": {"_id": "$item_id",
            "doc": { "$first": "$$ROOT" }}},
        {"$replaceRoot": { "newRoot": "$doc"}},
    ])
    project = await cursor.to_list(length=None)
    #if (project := await request.app.database["items"].find({"project_id": proj_id }).to_list(length=300)) is not None:
    if project is not None:

        def id(node):
          return node['_id']

        def parent(node):
          return node['parent']

        def create_new_dict(node, children):
            n = node.update({"children": children(id(node))})
            return n

        if len(project) > 0:
            A = project
            C = tree \
              ( A
              , parent
              , lambda node, children:
                dict([*list(node.items()), ("children", children(id(node)))])
              )

            print(C)

            return dumps({"tree": C, "flat": project})
        else:
            return dumps({"tree": [], "flat": []})

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with ID {proj_id} not found")

