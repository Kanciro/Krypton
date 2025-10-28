# servicio_alertas/services/servicio_alertas.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from servicio_usuarios.models.modelo_alertas_personalizadas import AlertaPersonalizada
from servicio_usuarios.schemas.schema_alerta import AlertaCreateSchema
from servicio_usuarios.models.modelo_criptomonedas import Criptomoneda # Asumiendo la ruta
from servicio_usuarios.models.modelo_moneda_fiat import MonedaFiat # Asumiendo la ruta
from servicio_usuarios.models.modelo_usuario import Usuario # Necesario para tipar el usuario

def crear_alerta_personalizada(db: Session, alerta_data: AlertaCreateSchema, usuario: Usuario):
    """
    Crea una nueva alerta personalizada en la base de datos.
    """
    
    # 1. Obtener ID de la Criptomoneda
    cripto = db.query(Criptomoneda).filter(Criptomoneda.simbolo == alerta_data.simbolo_cripto).first()
    if not cripto:
        raise HTTPException(status_code=404, detail=f"Criptomoneda '{alerta_data.simbolo_cripto}' no encontrada.")
    id_cripto = cripto.id_cripto

    # 2. Obtener ID de la Moneda Fiat
    moneda = db.query(MonedaFiat).filter(MonedaFiat.coi == alerta_data.simbolo_moneda).first()
    if not moneda:
        raise HTTPException(status_code=404, detail=f"Moneda Fiat '{alerta_data.simbolo_moneda}' no encontrada.")
    id_moneda = moneda.id_moneda
    
    # 3. Preparar los datos de precio
    precio_subida = None
    precio_bajada = None
    
    if alerta_data.direccion == "subida":
        precio_subida = alerta_data.valor_objetivo
    elif alerta_data.direccion == "bajada":
        precio_bajada = alerta_data.valor_objetivo
        
    # 4. Crear la instancia del modelo (AlertaPersonalizada)
    nueva_alerta = AlertaPersonalizada(
        id_usuario=usuario.id_usuario,
        id_cripto=id_cripto,
        id_moneda=id_moneda,
        precio_subida_objetivo=precio_subida,
        precio_bajada_objetivo=precio_bajada,
        estado=True # Por defecto activa
    )
    
    # 5. Guardar en la base de datos
    try:
        db.add(nueva_alerta)
        db.commit()
        db.refresh(nueva_alerta)
    except Exception as e:
        db.rollback()
        # En caso de un error de base de datos (ej. si falla la restricción CHECK por alguna razón)
        raise HTTPException(status_code=500, detail=f"Error al guardar la alerta: {str(e)}")
        
    return nueva_alerta