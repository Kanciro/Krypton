from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import date, datetime, timedelta

class CorreoVerificarSchema(BaseModel):
    codigo: str
    nuevo_correo: EmailStr

class CorreoActualizarSchema(BaseModel):
    nuevo_correo: EmailStr