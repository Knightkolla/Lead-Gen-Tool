from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

# Dummy in-memory database for users (for demonstration purposes only)
# In a real application, this would be replaced with a proper database
fake_users_db: Dict[str, Dict[str, str]] = {}

class UserRegistration(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register_user(user: UserRegistration):
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    # In a real application, you would hash the password before storing it
    fake_users_db[user.username] = {"password": user.password}
    return {"message": "User registered successfully"}

@router.post("/login")
async def login_user(user: UserLogin):
    stored_user = fake_users_db.get(user.username)
    if not stored_user or stored_user["password"] != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return {"message": "Login successful"} 