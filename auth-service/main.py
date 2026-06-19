import os
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from sqlmodel import SQLModel, Field, create_engine, Session, select
from models.user import User, UserRegister, UserResponse
from auth_py.auth import hash_password, verify_password  

load_dotenv()

DATABASE_URL = "sqlite:///./usuarios.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="Sistema de Autenticación Seguro")

@app.on_event("startup")
def on_startup():
    init_db()

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def home():
    return {"message": "API de Autenticación con SQLModel y Argon2 activa"}

@app.post("/users/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(user_data: UserRegister, session: Session = Depends(get_session)):
    statement = select(User).where((User.email == user_data.email) | (User.username == user_data.username))
    usuario_existente = session.exec(statement).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo o usuario ya está registrado")
    
    password_hash = hash_password(user_data.password)
    
    nuevo_usuario = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=password_hash  
    )
    
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)
    
    return nuevo_usuario

@app.post("/users/login", status_code=status.HTTP_200_OK)
def login_usuario(user_data: UserRegister, session: Session = Depends(get_session)):
    # Buscamos al usuario por su correo
    statement = select(User).where(User.email == user_data.email)
    usuario = session.exec(statement).first()
    
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    
    es_valida = verify_password(user_data.password, usuario.hashed_password)
    if not es_valida:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    
    return {
        "message": "Inicio de sesión exitoso",
        "username": usuario.username
    }
