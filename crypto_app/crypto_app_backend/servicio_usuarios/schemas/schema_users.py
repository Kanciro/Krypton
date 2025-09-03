from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import date, datetime, timedelta


# Esquema base con nombres en español
class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    fecha_nacimiento: date
    ultimo_inicio_sesion: Optional[datetime] = None

    # Valida que los campos no estén vacíos
    @validator('nombre', 'correo', 'fecha_nacimiento', pre=True)
    def check_not_empty(cls, v):
        if not v:
            raise ValueError('El campo no puede estar vacío')
        return v
    
    @validator('fecha_nacimiento')
    def validate_age(cls, v):
        # Calcula la fecha que sería 18 años atrás
        hoy = datetime.now().date()
        fecha_hace_18_años = hoy - timedelta(days=365.25 * 18)
        
        # Compara si la fecha de nacimiento es anterior a la fecha de hace 18 años
        if v > fecha_hace_18_años:
            raise ValueError('Debes ser mayor de 18 años para registrarte')
        return v

# Esquema para crear un usuario (con contraseña)
class UsuarioCrear(UsuarioBase):
    contraseña: str

    # Valida que la contraseña tenga al menos 6 caracteres
    @validator('contraseña')
    def password_length(cls, v):
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        return v


# Esquema para la respuesta del usuario (sin contraseña)
class UsuarioSchema(UsuarioBase):
    id_usuario: int
    notificaciones: bool = True

    class Config:
        from_attributes = True


# Esquema para actualizar un usuario (todos los campos opcionales)
class UsuarioActualizar(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    fecha_nacimiento: Optional[date] = None
    contraseña: Optional[str] = None