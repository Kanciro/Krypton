# servicio_usuarios/services/guest_services.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.modelo_invitados import Invitado
from datetime import datetime, timedelta

def crear_sesion_invitado(db: Session, ip_address: str, user_agent: str = None): # type: ignore

    try:
        nuevo_invitado = Invitado(
            direccion_ip=ip_address,
            navegador_agente=user_agent,
            fecha_ingreso=datetime.utcnow()
        )
        db.add(nuevo_invitado)
        db.commit()
        db.refresh(nuevo_invitado)
        return nuevo_invitado
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear la sesión de invitado: {e}")

def registrar_interaccion_invitado(db: Session, id_invitado: int, cripto_id: int = None, moneda_id: int = None): # type: ignore
    from ..models.modelo_interacciones_invitados import InteraccionInvitado
    
    try:
        invitado = db.query(Invitado).filter(Invitado.id_invitado == id_invitado).first()
        if not invitado:
            raise HTTPException(status_code=404, detail="Invitado no encontrado.")

        nueva_interaccion = InteraccionInvitado(
            id_invitado=id_invitado,
            id_cripto=cripto_id,
            id_moneda=moneda_id,
        )
        db.add(nueva_interaccion)
        
    
        invitado.ultimo_acceso = datetime.utcnow() # type: ignore
        db.add(invitado)

        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al registrar la interacción del invitado: {e}")


def actualizar_estado_sesiones_inactivas(db: Session, timeout_minutos: int = 30):

    # Calcula el tiempo límite para considerar una sesión inactiva
    tiempo_limite = datetime.utcnow() - timedelta(minutes=timeout_minutos)
    
    # Encuentra todas las sesiones activas cuya última actividad es anterior al tiempo límite
    sesiones_inactivas = db.query(Invitado).filter(
        Invitado.sesion_activa == True,
        Invitado.ultimo_acceso < tiempo_limite
    ).all()
    
    # Itera y actualiza el estado de cada sesión
    for invitado in sesiones_inactivas:
        invitado.sesion_activa = False # type: ignore
    
    db.commit()
    print(f"Se han actualizado {len(sesiones_inactivas)} sesiones a estado 'inactivo'.")
    return {"status": "success", "updated_count": len(sesiones_inactivas)}