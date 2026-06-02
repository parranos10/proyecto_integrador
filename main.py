import os
from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from models.user import UserRegister, UserResponse

load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME", "Image Management System"))

app.mount("/static", StaticFiles(directory="static"), name="static")

DB_USUARIOS = []
id_counter = 1

@app.get("/")
def home():
    return {"message": f"Bienvenido a {os.getenv('APP_NAME')}"}



@app.post("/users/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(user: UserRegister):
    global id_counter
    
    
    for u in DB_USUARIOS:
        if u["email"] == user.email:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
            
    
    nuevo_usuario = {
        "id": id_counter,
        "username": user.username,
        "email": user.email,
        "password": user.password, 
        "is_active": True
    }
    
    DB_USUARIOS.append(nuevo_usuario)
    id_counter += 1
    return nuevo_usuario

@app.get("/users", response_model=list[UserResponse])
def listar_usuarios():
    return DB_USUARIOS