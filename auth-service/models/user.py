from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: EmailStr = Field(unique=True) # Validación estricta de correo en la BD
    hashed_password: str = Field(max_length=255) # Espacio suficiente para el hash largo de Argon2

class UserRegister(SQLModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(SQLModel):
    id: int
    username: str
    email: EmailStr