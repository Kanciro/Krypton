from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import date, datetime, timedelta

class LoginSchema(BaseModel):
    nombre: str
    contraseña: str

# Nuevo esquema para la respuesta del token (opcional pero recomendado)
class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"