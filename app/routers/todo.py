from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate

from app.database import get_db
from sqlalchemy.orm import Session
from app.models.todo import Todo
from app.core.security import get_current_user
from sqlalchemy import select

router = APIRouter(prefix="/todo", tags=["Todo"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TodoResponse)
def create_task(
    todo_data: TodoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    task = Todo(
        title=todo_data.title,
        description=todo_data.description,
        user_id=current_user.id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("", status_code=status.HTTP_200_OK, response_model=list[TodoResponse])
def list_my_tasks(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return db.scalars(select(Todo).where(Todo.user_id == current_user.id)).all()


@router.patch("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_status_task(
    task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    task = db.get(Todo, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="A task não foi encontrada"
        )

    if task.user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado"
        )
    task.status = Todo.StatusChoice.COMPLETED

    db.commit()
    db.refresh(task)
    return None


@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TodoResponse)
def update_task(
    task_id: int,
    data_task: TodoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    task = db.get(Todo, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="A task não foi encontrada"
        )
    if task.user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado"
        )

    task.title = data_task.title
    task.description = data_task.description

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    task = db.get(Todo, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="A task não foi encontrada"
        )
    if task.user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado"
        )

    db.delete(task)
    db.commit()
    return None