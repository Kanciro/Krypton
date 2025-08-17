from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


# Esquema base con nombres en español
class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    fecha_nacimiento: date


# Esquema para crear un usuario (con contraseña)
class UsuarioCrear(UsuarioBase):
    contraseña: str


# Esquema para la respuesta del usuario (sin contraseña)
class UsuarioSchema(UsuarioBase):
    id_usuario: int
    notificaciones: bool = True

    class Config:
        from_attributes = True
