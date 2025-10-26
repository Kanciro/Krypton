# servicio_usuarios/services/guest_services.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from servicio_usuarios.models.modelo_invitados import Invitado
from servicio_usuarios.models.modelo_interacciones_invitados import InteraccionInvitado
from servicio_usuarios.models.modelo_criptomonedas import Criptomoneda
from datetime import datetime, timedelta
from servicio_usuarios.models.modelo_moneda_fiat import MonedaFiat

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

# servicio_usuarios/services/interaccion_invitados_services.py

# servicio_usuarios/services/invitados_services.py

from sqlalchemy.orm import Session
from datetime import datetime
from servicio_usuarios.models.modelo_invitados import Invitado

def traerOCrearInvitado(db: Session, direccion_ip: str):

    invitado = db.query(Invitado).filter(Invitado.direccion_ip == direccion_ip).first()

    if invitado:
        invitado.ultimo_acceso = datetime.utcnow() # pyright: ignore[reportAttributeAccessIssue]
    else:
        invitado = Invitado(direccion_ip=direccion_ip)
    
    db.add(invitado)
    db.commit()
    db.refresh(invitado)
    return invitado

def registrar_interaccion_invitado(
    db: Session,
    id_invitado: int,
    id_cripto: int = None, # type: ignore
    id_moneda: int = None # type: ignore
):
 
    try:
        # 1. Asegurarse de que el invitado exista
        invitado = db.query(Invitado).filter(Invitado.id_invitado == id_invitado).first()
        if not invitado:
            raise HTTPException(status_code=404, detail="Invitado no encontrado.")
            
        # 2. Validar que la criptomoneda y la moneda fiat existan si se proporcionan
        if id_cripto:
            cripto = db.query(Criptomoneda).filter(Criptomoneda.id_cripto == id_cripto).first()
            if not cripto:
                raise HTTPException(status_code=404, detail="Criptomoneda no encontrada.")
        
        if id_moneda:
            moneda = db.query(MonedaFiat).filter(MonedaFiat.id_moneda == id_moneda).first()
            if not moneda:
                raise HTTPException(status_code=404, detail="Moneda Fiat no encontrada.")

        # 3. Crear la nueva interacción
        nueva_interaccion = InteraccionInvitado(
            id_invitado=id_invitado,
            id_cripto=id_cripto,
            id_moneda=id_moneda
        )
        db.add(nueva_interaccion)
        
        # 4. Actualizar el último acceso del invitado
        invitado.ultimo_acceso = datetime.utcnow() # type: ignore
        db.add(invitado)

        db.commit()
        db.refresh(nueva_interaccion)
        return {"mensaje": "Interacción registrada con éxito."}

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al registrar la interacción: {str(e)}")

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