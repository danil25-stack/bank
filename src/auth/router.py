from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from src.configs import ACCESS_TOKEN_EXPIRE_MINUTES

from src.auth.services import get_user_by_email, hash_password, authenticate_user, create_access_token
from src.auth.models import User as UserModel
from src.database import get_db
# from src.auth import services
from src.auth.schemas import UserCreate, User, Token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/auth/register", response_model=User)
async def register(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    existing = await get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = UserModel(
        email=payload.email,
        hashed_password=hash_password(payload.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return User(email=user.email)


@router.post("/auth/login", response_model=Token)
async def login_for_access_token(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    form_data.username -> email
    form_data.password -> password
    """
    user = await authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )

    return Token(access_token=access_token, token_type="bearer")
