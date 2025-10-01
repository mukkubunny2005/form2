from fastapi import APIRouter, Depends, HTTPException, status, Form
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from database import SessionLocal3
from models import Users


router = APIRouter()

# Security Config
SECRET_KEY = "7c64a0170d214ab11e1c93508ed85c7606d64f6f88d829779b51080269b5d0db"
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/token")


# Dependency
def get_db():
    db = SessionLocal3()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# Authentication Helper
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return None
    if not bcrypt_context.verify(password, user.password):
        return None
    return user


def create_access_token(username: str, user_id: str, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# Token Verification
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/get_user', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.post("/")
async def create_user(
    db: db_dependency,
    username: str,
    email: str,
    first_name: str,
    last_name: str,
    password: str,
    ph_no: str,
):
    existing_user = db.query(Users).filter(Users.username == username).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Username already exists"
        )

    create_user_model = Users(
        email=email,
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=bcrypt_context.hash(password),  # bcrypt hashing
        ph_no=ph_no,
        is_active=True,
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)

    return {"msg": "User created successfully", "user_id": create_user_model.id}


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    user_id: str


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    user.token = token
    db.add(user)
    db.commit()

    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "user_id": user.id,
    }


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
    return 'password change succeessfully'


@router.delete('/logout')
async def logout(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.token = False
    db.add(user_model)
    return {'user logout successfully'}
