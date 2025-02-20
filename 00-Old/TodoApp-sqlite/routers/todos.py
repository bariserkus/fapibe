from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todos
from database import SessionLocal
from .auth import get_current_user


router = APIRouter(
    prefix="",
    tags=["todo"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=30)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=1, le=5)
    completed: bool = Field(default=False)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Task Title",
                "description": "Description of the Task",
                "priority": 1,
                "completed": False,
            }
        }
    }

#GET Requests
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentiction Failed")
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency,
                    db: db_dependency,
                    todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentiction Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).\
        filter(Todos.owner_id == user.get("id")).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo Not Found")

#POST Requests
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,
                      db: db_dependency,
                      todo_request: TodoRequest):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentiction Failed")

    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))

    db.add(todo_model)
    db.commit()

#PUT Requests
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency,
                      db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0),):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentiction Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id). \
        filter(Todos.owner_id == user.get("id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo Not Found!")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.completed = todo_request.completed

    db.add(todo_model)
    db.commit()

#DELETE Requests
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency,
        db: db_dependency,
        todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentiction Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id). \
        filter(Todos.owner_id == user.get("id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo Not Found!")

    db.query(Todos).filter(Todos.id == todo_id).\
        filter(Todos.owner_id == user.get("id")).delete()
    db.commit()

