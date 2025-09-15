# servicio_datos_cripto/services/crypto_sync_service.py
from sqlalchemy.orm import Session
from .crypto_data_service import traerTopCriptomonedas
from servicio_usuarios.models.modelo_criptomonedas import Criptomoneda
from datetime import datetime
from servicio_usuarios.models.modelo_valor_historico import ValorHistorico
from typing import List
from fastapi import HTTPException

def actualizar_criptomonedas_en_db(db: Session, criptos_api: list):

    try:
        if not criptos_api:
            print("No se recibieron datos de la API para actualizar la base de datos.")
            return None

        for cripto_data in criptos_api:
            cripto_existente = (
                db.query(Criptomoneda)
                .filter(Criptomoneda.id_api == cripto_data["id"])
                .first()
            )

            if cripto_existente:
                # Si existe, buscamos el valor histórico más reciente para comparación
                valor_historico_actual = (
                    db.query(ValorHistorico)
                    .filter(ValorHistorico.id_cripto == cripto_existente.id_cripto)
                    .order_by(ValorHistorico.fecha.desc())
                    .first()
                )
                
                # Comparamos el precio actual de la API con el último precio registrado
                # para evitar duplicados si el valor no cambia
                precio_api = cripto_data["current_price"]
                
                # Para la primera inserción, el valor_historico_actual será None
                # Por eso también se debe guardar si no hay un valor histórico aún
                if (
                    valor_historico_actual is None or
                    precio_api != valor_historico_actual.valor
                ):
                    # El precio ha cambiado o es la primera vez, así que se crea un nuevo registro
                    nuevo_valor_historico = ValorHistorico(
                        id_cripto=cripto_existente.id_cripto,
                        valor=precio_api,
                        fecha=datetime.utcnow(),
                    )
                    db.add(nuevo_valor_historico)
                    print(
                        f"¡Cambio detectado! Guardando valor histórico para {cripto_existente.nombre}."
                    )
                else:
                    print(
                        f"Valor de {cripto_existente.nombre} sin cambios. No se guarda un nuevo registro histórico."
                    )

                # Siempre actualizamos el registro principal de la criptomoneda en caso de que
                # otros campos como 'nombre' o 'simbolo' cambien en la API.
                cripto_existente.nombre = cripto_data["name"]
                cripto_existente.simbolo = cripto_data["symbol"]
            else:
                # Si no existe, primero creamos la criptomoneda en la tabla "criptomonedas"
                nueva_cripto = Criptomoneda(
                    simbolo=cripto_data["symbol"],
                    nombre=cripto_data["name"],
                    id_api=cripto_data["id"],
                    fecha_creacion=datetime.utcnow(),
                )
                db.add(nueva_cripto)
                db.commit() # Se debe hacer un commit para obtener el id_cripto
                db.refresh(nueva_cripto)
                
                # Luego, creamos el primer registro de su valor histórico
                nuevo_valor_historico = ValorHistorico(
                    id_cripto=nueva_cripto.id_cripto,
                    valor=cripto_data["current_price"],
                    fecha=datetime.utcnow(),
                )
                db.add(nuevo_valor_historico)
                print(f"Nueva criptomoneda añadida: {nueva_cripto.nombre}.")

        db.commit()
        print("Base de datos de criptomonedas y valores históricos actualizada exitosamente.")

        return {"mensaje": "Base de datos de criptomonedas actualizada exitosamente."}
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar la base de datos: {e}")
        return None

