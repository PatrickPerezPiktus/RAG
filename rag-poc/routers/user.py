from fastapi import APIRouter, Depends, HTTPException, status, Request, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, ValidationError
from dbs.database import get_db, UserModel
import bcrypt
import config
from datetime import datetime, timedelta
import jwt

router = APIRouter()

SECRET_KEY = config.jwt_secret_key
ALGORITHM = config.hash_algo
ACCESS_TOKEN_EXPIRE_MINUTES = config.token_expire_minutes


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str

class UserCreate(BaseModel):
    name: str
    pw: str

def hashPassword(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verifyPassword(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def createAccessToken(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def getCurrentUser(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = getUserFromDB(db, username)
    if user is None:
        raise credentials_exception
    return user

def getUserFromDB(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.name == username).first()

@router.post("/token")
async def loginForAccessToken(request: Request, db: Session = Depends(get_db)):
    try:
        form_data = await request.json()
        user = UserCreate(**form_data)
        dbUser = getUserFromDB(db, user.name)
        if not dbUser or not verifyPassword(user.pw, dbUser.pw):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (ValidationError, ValueError):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            dbUser = getUserFromDB(db, username)
            if dbUser is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = createAccessToken(data={"sub": dbUser.name}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "id": dbUser.id, "username": dbUser.name}

@router.post("/user")
async def createUser(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = getUserFromDB(db, user.name)
        if existing_user:
            raise HTTPException(status_code=400, detail="Nutzer bereits vorhanden")
        hashed_pw = hashPassword(user.pw)
        newUser = UserModel(name=user.name, pw=hashed_pw)
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        return newUser
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@router.post("/user/delete")
async def deleteUser(user: User = Depends(getCurrentUser), db: Session = Depends(get_db)):
    try:
        oldUser = getUserFromDB(db, user.name)
        if not oldUser:
            raise HTTPException(status_code=404, detail="Kein Nutzer gefunden")
        db.delete(oldUser)
        db.commit()
        return {"message": "Nutzer erfolgreich gelöscht"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim löschen eines Nutzers: {str(e)}")

@router.get("/users")
async def getUsers(user: User = Depends(getCurrentUser), db: Session = Depends(get_db)):
    try:
        users = db.query(UserModel).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim laden der Nutzer: {str(e)}")

@router.get("/users/me")
async def readUsersMe(user: User = Depends(getCurrentUser), db: Session = Depends(get_db)):
    return user
