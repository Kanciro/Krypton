import logging
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from servicio_usuarios.models.modelo_valor_historico import ValorHistorico
from servicio_usuarios.models.modelo_criptomonedas import Criptomoneda
from servicio_datos_cripto.services.historical_crypto_data_services import LeerValorHistorico

logger = logging.getLogger(__name__)

def ActualizarValorHistoricoConDb(db: Session, crypto_id_api: str, days: int = 365):
    try:
        # Obtener la criptomoneda por su ID de API
        cripto = db.query(Criptomoneda).filter(Criptomoneda.id_api == crypto_id_api).first()
        
        if not cripto:
            logger.error(f"Criptomoneda con ID de API {crypto_id_api} no encontrada.")
            return {"mensaje": "Criptomoneda no encontrada."}

        # Ya no se necesita esta verificación global, ya que la validación por fecha se hace más abajo
        # if valores_existentes:
        #     ...

        datos_historicos = LeerValorHistorico(crypto_id_api, days)
        
        if not datos_historicos:
            logger.error(f"No se pudieron obtener datos históricos para {crypto_id_api}.")
            return {"mensaje": "No se pudieron obtener datos históricos."}

        # Guardar los nuevos valores históricos en la base de datos
        for dato in datos_historicos:
            fecha_dato = datetime.strptime(dato["date"], "%Y-%m-%d %H:%M:%S")
            
            # Verificar si ya existe un valor histórico para esa fecha
            # La verificación debe ser por 'id_cripto' y 'fecha'
            if not db.query(ValorHistorico).filter(
                ValorHistorico.id_cripto == cripto.id_cripto,
                ValorHistorico.fecha == fecha_dato
            ).first():
                # Si no existe un valor para esa fecha y cripto, lo creamos
                nuevo_valor = ValorHistorico(
                    criptomoneda=cripto,
                    valor=dato["price_usd"],
                    fecha=fecha_dato
                )
                db.add(nuevo_valor)
                logger.info(f"Agregando valor histórico para {cripto.nombre} en {fecha_dato}.")
            else:
                logger.info(f"Valor histórico ya existe para {cripto.nombre} en {fecha_dato}, no se agrega de nuevo.")
                
        db.commit()
        logger.info(f"Valores históricos actualizados para {cripto.nombre}.")
        return {"mensaje": "Valores históricos actualizados exitosamente."}
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar valores históricos: {e}")
        return {"mensaje": "Error al actualizar valores históricos."}

    
