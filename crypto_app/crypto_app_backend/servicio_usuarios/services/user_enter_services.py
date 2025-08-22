# Importaciones
from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime


from servicio_usuarios.models.modelo_usuario import Usuario
from servicio_usuarios.schemas.schema_users import UsuarioSchema
from servicio_usuarios.schemas.schema_usuario_login import LoginSchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def LoginUsuarioSeguro(db: Session, credenciales: LoginSchema):

    
    usuario_encontrado = db.query(Usuario).filter_by(nombre=credenciales.nombre).first()

    if not usuario_encontrado:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

   
    if not pwd_context.verify(credenciales.contraseña, usuario_encontrado.contraseña):  # type: ignore
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    
    usuario_encontrado.ultimo_inicio_sesion = datetime.utcnow()  # type: ignore
    db.refresh(usuario_encontrado)

    return UsuarioSchema.model_validate(usuario_encontrado)
