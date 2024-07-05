from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import config

app = FastAPI()

class User(BaseModel):
    name: str

class UserManager:
    def __init__(self):      
      db = config.db

    def get_user(self, user_id: int) -> User:
      
      try:
          session = SessionLocal()
          user = self.users.get(user_id)
          if not user:
              raise HTTPException(status_code=404, detail="User not found")
          return user
      except Exception as e:
          return {"error": str(e)}
      finally:
          session.close()

    def create_user(self, user: User) -> User:
        if user.id in self.users:
            raise HTTPException(status_code=400, detail="User already exists")
        self.users[user.id] = user
        return user

    def update_user(self, user_id: int, user: User) -> User:
        if user_id not in self.users:
            raise HTTPException(status_code=404, detail="User not found")
        self.users[user_id] = user
        return user

    def delete_user(self, user_id: int):
        if user_id not in self.users:
            raise HTTPException(status_code=404, detail="User not found")
        del self.users[user_id]
