import os
from argon2 import PasswordHasher
from dotenv import load_dotenv


load_dotenv()
PEPPER = os.getenv("PEPPER", "ClaveSeguraPorDefectoSiNoHayEnv")
ph = PasswordHasher()

def hash_password(password: str) -> str:
    password_peppered = password + PEPPER
    return ph.hash(password_peppered)

def verify_password(password: str, stored_hash: str) -> bool:
    password_peppered = password + PEPPER
    try:
        return ph.verify(stored_hash, password_peppered)
    except Exception:
        return False