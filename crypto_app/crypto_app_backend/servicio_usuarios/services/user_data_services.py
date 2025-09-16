# servicio_usuarios/services/user_enter_services.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
import secrets # Importa la librería secrets para generar el código de forma segura
# Otros imports existentes...

from servicio_usuarios.models.modelo_usuario import Usuario
from servicio_usuarios.schemas.schema_users import UsuarioCrear
from servicio_usuarios.services.email_services.email_sender import send_registration_email_with_code 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashContraseña(contraseña: str) -> str:
    return pwd_context.hash(contraseña)


def RegistrarUsuario(db: Session, datos_usuario: UsuarioCrear) -> dict:
    try:
        usuario_existente = (
            db.query(Usuario).filter_by(correo=datos_usuario.correo).first()
        )
        if usuario_existente:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")

        contraseña_hasheada = hashContraseña(datos_usuario.contraseña)

        # Generar un código de 4 dígitos seguro
        codigo_verificacion = str(secrets.randbelow(10000)).zfill(4)

        nuevo_usuario = Usuario(
            nombre=datos_usuario.nombre,
            correo=datos_usuario.correo,
            fecha_nacimiento=datos_usuario.fecha_nacimiento,
            contraseña=contraseña_hasheada,
            codigo_verificacion=codigo_verificacion, # Asigna el código al modelo
            is_verified=False,
            is_active=False
        )

        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        # Enviar el correo con el código en lugar del token
        email_sent = send_registration_email_with_code(str(nuevo_usuario.correo), codigo_verificacion)
        
        if not email_sent:
            db.rollback()
            raise HTTPException(status_code=500, detail="No se pudo enviar el correo de verificación. Inténtalo de nuevo.")

        return {
        "mensaje": "Usuario registrado. Por favor, ingresa el código de verificación enviado a tu correo electrónico.",
        "correo": nuevo_usuario.correo # <-- Retorna el correo del usuario
    }

    except Exception as e:
        db.rollback()
        if not isinstance(e, HTTPException):
            raise HTTPException(status_code=500, detail="Error interno del servidor") from e
        raise e