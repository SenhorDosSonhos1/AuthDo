from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from sqlalchemy import select
from app.schemas.user import UserCreate, UserResponse, UserPatch
from app.core.security import get_password_hash
from app.core.security import get_current_user

router = APIRouter(
    tags=["Users"],
    prefix="/users",
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    if not data.password == data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="As senhas não coincidem."
        )
    user_exist = db.scalars(select(User).where(User.email == data.email)).first()
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O email já existe no nosso servidor.",
        )
    password_hashed = get_password_hash(data.password)
    user = User(username=data.username, email=data.email, password=password_hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("", status_code=200, response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.scalars(select(User)).all()


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.scalars(select(User).where(User.id == user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="O usuario não existe."
        )

    return user


@router.patch("", status_code=status.HTTP_200_OK, response_model=UserResponse)
def upgrade_user(
    data: UserPatch,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not data.password == data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="As senhas não coincidem."
        )

    password_hashed = get_password_hash(data.password)
    current_user.password = password_hashed

    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    db.delete(current_user)
    db.commit()
    return None
