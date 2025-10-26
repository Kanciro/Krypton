from pydantic import BaseModel
class EmailRequest(BaseModel):
    correo: str

class PasswordReset(BaseModel):
    token: str
    nueva_contraseña: str

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)