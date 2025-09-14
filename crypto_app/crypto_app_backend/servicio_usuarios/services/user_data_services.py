# servicio_usuarios/services/user_enter_services.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import timedelta

from servicio_usuarios.models.modelo_usuario import Usuario
from servicio_usuarios.schemas.schema_users import UsuarioCrear, UsuarioSchema
from servicio_usuarios.services.auth.auth_utils import create_access_token
from servicio_usuarios.services.email_services.email_sender import send_registration_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashContraseña(contraseña: str) -> str:
    return pwd_context.hash(contraseña)


def RegistrarUsuario(db: Session, datos_usuario: UsuarioCrear) -> dict:
    try:
        # Verificar si el correo ya existe
        usuario_existente = (
            db.query(Usuario).filter_by(correo=datos_usuario.correo).first()
        )
        if usuario_existente:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")

        # Hashear la contraseña
        contraseña_hasheada = hashContraseña(datos_usuario.contraseña)

        # Mapear los datos a los campos del modelo de SQLAlchemy
        nuevo_usuario = Usuario(
            nombre=datos_usuario.nombre,
            correo=datos_usuario.correo,
            fecha_nacimiento=datos_usuario.fecha_nacimiento,
            contraseña=contraseña_hasheada,
            is_verified=False,  
            is_active=False  
        )

        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        # Generar un token de verificación (con una duración corta, por ejemplo 24 horas)
        verification_token = create_access_token(
            data={"sub": str(nuevo_usuario.id_usuario)},
            expires_delta=timedelta(hours=24)
        )

        # Enviar el correo de verificación
        if verification_token is None:
            db.rollback()
            raise HTTPException(status_code=500, detail="No se pudo generar el token de verificación.")
        email_sent = send_registration_email(str(nuevo_usuario.correo), str(verification_token))
        
        if not email_sent:
            db.rollback()
            raise HTTPException(status_code=500, detail="No se pudo enviar el correo de verificación. Inténtalo de nuevo.")

        return {"mensaje": "Usuario registrado. Por favor, verifica tu correo electrónico para activar tu cuenta."}

    except Exception as e:
        db.rollback()
        if not isinstance(e, HTTPException):
            raise HTTPException(status_code=500, detail="Error interno del servidor") from e
        raise e