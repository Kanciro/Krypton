# servicio_usuarios/services/user_delete_services.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext

from ..models.modelo_usuario import Usuario
from ..schemas.schema_usuario_login import LoginSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def DesactivarUsuario(db: Session, credenciales: LoginSchema):

    usuario_encontrado = db.query(Usuario).filter(Usuario.nombre == credenciales.nombre).first()

    if not usuario_encontrado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


    if not pwd_context.verify(credenciales.contraseña, usuario_encontrado.contraseña): # type: ignore
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")


    usuario_encontrado.is_active = False # type: ignore
    db.commit()
    db.refresh(usuario_encontrado)

    return usuario_encontrado

def ReactivarUsuario(db: Session, credenciales: LoginSchema):

    usuario_encontrado = db.query(Usuario).filter(Usuario.nombre == credenciales.nombre).first()

    if not usuario_encontrado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not pwd_context.verify(credenciales.contraseña, usuario_encontrado.contraseña): # type: ignore
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    if usuario_encontrado.is_active: # type: ignore
        raise HTTPException(status_code=400, detail="La cuenta ya está activa")

    usuario_encontrado.is_active = True # type: ignore
    db.commit()
    db.refresh(usuario_encontrado)

    return usuario_encontrado