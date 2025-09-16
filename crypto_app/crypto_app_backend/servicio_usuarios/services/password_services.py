# servicio_usuarios/services/password_services.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
from servicio_usuarios.models.modelo_usuario import Usuario
from servicio_usuarios.services.auth.auth_utils import create_access_token
from servicio_usuarios.services.email_services.email_sender import send_registration_email_with_code

def solicitarRestablecimientoDeCredencial(db: Session, correo: str):
    """
    Busca al usuario por correo, genera un token y envía un correo de restablecimiento.
    """
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()

    if not usuario:
        
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Si el correo está registrado, recibirás un enlace para restablecer la contraseña."
        )
    
    
    reset_token = create_access_token(
        data={"sub": str(usuario.id_usuario)},
        expires_delta=timedelta(minutes=15)
    )

    
    email_sent = send_registration_email_with_code(usuario.correo, reset_token) # type: ignore

    if not email_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo enviar el correo de restablecimiento. Inténtalo de nuevo."
        )

    return {"mensaje": "Si el correo está registrado, recibirás un enlace para restablecer la contraseña."}