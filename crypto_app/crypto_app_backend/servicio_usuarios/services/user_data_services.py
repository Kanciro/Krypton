# Importaciones
from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext

from servicio_usuarios.models.modelo_usuario import Usuario
from servicio_usuarios.schemas.schema_users import UsuarioCrear, UsuarioSchema
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashContraseña(contraseña: str) -> str:
    return pwd_context.hash(contraseña)

def RegistrarUsuario(db: Session, datos_usuario: UsuarioCrear) -> UsuarioSchema:
    try:
        # Verificar si el correo ya existe
        usuario_existente = db.query(Usuario).filter_by(correo=datos_usuario.correo).first()
        if usuario_existente:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")

        # Hashear la contraseña
        contraseña_hasheada = hashContraseña(datos_usuario.contraseña)

        # Mapear los datos a los campos del modelo de SQLAlchemy
        nuevo_usuario = Usuario(
            nombre=datos_usuario.nombre,
            correo=datos_usuario.correo,
            fecha_nacimiento=datos_usuario.fecha_nacimiento,
            contraseña=contraseña_hasheada
        )
        
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        
        return UsuarioSchema.model_validate(nuevo_usuario)
    except Exception as e:
        db.rollback() 
        if not isinstance(e, HTTPException):
            raise HTTPException(status_code=500, detail="Error interno del servidor") from e
        raise e