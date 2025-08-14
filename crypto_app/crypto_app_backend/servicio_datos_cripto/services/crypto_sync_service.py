    # servicio_datos_cripto/services/crypto_sync_service.py
from sqlalchemy.orm import Session
from .crypto_data_service import traerTopCriptomonedas
from servicio_usuarios.models.modelo_criptomonedas import Criptomoneda # Asegúrate de que esta sea la ruta correcta
from datetime import datetime
def actualizar_criptomonedas_en_db(db: Session):

        #Obtiene las criptomonedas populares de la API y actualiza la tabla
        #de criptomonedas en la base de datos.

    try:
            criptos_api = traerTopCriptomonedas()
            
            if not criptos_api:
                print("No se pudieron obtener datos de la API para actualizar la base de datos.")
                return

            for cripto_data in criptos_api:
                # Buscar si la criptomoneda ya existe en la base de datos por su ID de API
                cripto_existente = db.query(Criptomoneda).filter(Criptomoneda.id_api == cripto_data['id']).first()

                if cripto_existente:
                    # Si existe, actualizamos sus datos
                    cripto_existente.nombre = cripto_data['name']
                    cripto_existente.simbolo = cripto_data['symbol']
                else:
                    # Si no existe, creamos un nuevo registro en la base de datos
                    nueva_cripto = Criptomoneda(
                        simbolo=cripto_data['symbol'],
                        nombre=cripto_data['name'],
                        id_api=cripto_data['id']
                        fecha_creacion = datetime.utcnow()
                    )
                    db.add(nueva_cripto)

            db.commit()
            print("Base de datos de criptomonedas actualizada exitosamente.")
            
    except Exception as e:
            db.rollback()
            print(f"Error al actualizar la base de datos: {e}")