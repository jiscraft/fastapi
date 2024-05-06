from database.conection import get_db
from database.orm import ToDo
from database.repository import get_todos, get_todo_by_todo_id
from fastapi import FastAPI, Body, HTTPException, Depends
from pydantic import BaseModel
from schema.response import ListToDoResponse, ToDoSchema
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World232"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

todo_data = {
    1: {
        "id": 1,
        "contents": "실전 api",
        "is_done": True
    },
    2: {
        "id": 2,
        "contents": "실전 api2",
        "is_done": True
    },
    3: {
        "id": 3,
        "contents": "실전 api3",
        "is_done": True
    }
}

@app.get("/todos")
def get_todos_handler(
    order: str | None = None,
    session: Session = Depends(get_db),
):
    todos: List[ToDo] = get_todos(session=session)
    return todos

# @app.get("/todos/{todo_id}", status_code=200)
# def get_todo_handler(
#     todo_id: int,
#     session: Session = Depends(get_db())
# ) -> ToDoSchema:
#     todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
#     if todo:
#         return ToDoSchema.from_orm(todo)
#     raise HTTPException(status_code=404, detail="조회할 데이타가 없습니다")

class CreateToDoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool

@app.post("/todos" )
def create_todo_handler(request: CreateToDoRequest):
    todo_data[request.id] = request.dict()
    return todo_data

@app.patch("/todoos/{todo_id}")
def update_todo_handler(
    todo_id:int ,
    is_done: bool = Body(...,embed= True),
):
    todo= todo_data.get(todo_id)
    if todo:
        todo["is_done"] = is_done
        return todo
    return {}


@app.delete("/todos/{todo_id}" , status_code=204)
def deleteTodoHandler(todo_id: int):
    todo = todo_data.pop(todo_id , None)
    if todo:
        return

    raise HTTPException(status_code=404, detail= "삭재할 데이타가 없습니다")