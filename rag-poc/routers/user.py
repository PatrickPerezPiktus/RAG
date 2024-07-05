from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from dbs.database import SessionLocal, UserModel

router = APIRouter()

class UserCreate(BaseModel):
    name: str
    pw: str

@router.post("/user")
async def create_user(user: UserCreate):
    try:
        session = SessionLocal()
        existing_user = session.query(UserModel).filter(UserModel.name == user.name).first()
        if existing_user:
            return login(user)
        newUser = UserModel(name=user.name, pw=user.pw)
        session.add(newUser)
        session.commit()
        session.refresh(newUser)
        return newUser
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)
    finally:
        session.close()

@router.post("/user/delete")
async def delete_user(user: UserCreate):
    try:
        session = SessionLocal()
        oldUser = session.query(UserModel).filter(UserModel.name == user.name).first()
        session.delete(oldUser)
        session.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)
    finally:
        session.close()

@router.post("/login")
async def login(user: UserCreate):
    try:
        session = SessionLocal()
        dbUser = session.query(UserModel).filter(UserModel.name == user.name).first()
        if dbUser.pw == user.pw:
            return dbUser
        else:
            return False
    finally:
        session.close()

@router.get("/users")
async def get_users():
    try:
        session = SessionLocal()
        users = session.query(UserModel).all()
        return users
    finally:
        session.close()
