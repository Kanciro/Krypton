from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime
from typing import Optional

from servicio_usuarios.models.modelo_usuario import Usuario
from servicio_usuarios.schemas.schema_users import UsuarioSchema, UsuarioCrear
from servicio_usuarios.schemas.schema_users import UsuarioActualizar

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashContraseña(password: str) -> str:
    return pwd_context.hash(password)


def ActualizarUsuario(db: Session, usuario_id: int, datos_usuario: UsuarioActualizar) -> UsuarioSchema:
    try:
        print(f"Actualizando usuario ID: {usuario_id}")  # Debug
        print(f"Datos recibidos: {datos_usuario}")  # Debug
        
        # Buscar el usuario por ID
        usuario_encontrado = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
        
        # Si se quiere actualizar el correo, verificar que no exista otro usuario con ese correo
        if datos_usuario.correo and datos_usuario.correo != usuario_encontrado.correo:  # type: ignore
            correo_existente = (
                db.query(Usuario)
                .filter(Usuario.correo == datos_usuario.correo, Usuario.id_usuario != usuario_id)
                .first()
            )
            if correo_existente:
                raise HTTPException(status_code=400, detail="El correo ya está registrado por otro usuario")
        
        # Actualizar solo los campos que se enviaron (no None)
        if datos_usuario.nombre is not None:
            print(f"Actualizando nombre: {datos_usuario.nombre}")
            usuario_encontrado.nombre = datos_usuario.nombre # type: ignore
        
        if datos_usuario.correo is not None:
            print(f"Actualizando correo: {datos_usuario.correo}")
            usuario_encontrado.correo = datos_usuario.correo # type: ignore
        
        if datos_usuario.fecha_nacimiento is not None:
            print(f"Actualizando fecha_nacimiento: {datos_usuario.fecha_nacimiento}")
            usuario_encontrado.fecha_nacimiento = datos_usuario.fecha_nacimiento # type: ignore
        
        if datos_usuario.contraseña is not None:
            print("Actualizando contraseña")
            usuario_encontrado.contraseña = hashContraseña(datos_usuario.contraseña) # type: ignore
        
        print("Guardando cambios en la base de datos...")
        db.commit()
        db.refresh(usuario_encontrado)
        
        print("Usuario actualizado exitosamente")
        return UsuarioSchema.model_validate(usuario_encontrado)
        
    except Exception as e:
        print(f"Error en ActualizarUsuario: {str(e)}")  # Debug
        db.rollback()
        if not isinstance(e, HTTPException):
            raise HTTPException(
                status_code=500, detail=f"Error interno: {str(e)}"
            ) from e
        raise e