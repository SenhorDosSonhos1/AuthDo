from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.token import Token
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.core.security import verify_password

from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Users"])


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha ou email incorretos"
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha ou email incorretos"
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "Bearer"}
