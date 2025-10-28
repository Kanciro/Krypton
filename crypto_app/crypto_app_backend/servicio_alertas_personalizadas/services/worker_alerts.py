# worker_alertas.py

from sqlalchemy.orm import Session
from sqlalchemy import func, text
from datetime import datetime
from servicio_usuarios.database.db import engine, sessionLocal # Asumiendo rutas correctas
from servicio_usuarios.models.modelo_alertas_personalizadas import AlertaPersonalizada
# Importa también los modelos Criptomoneda, MonedaFiat, ValorHistorico, ValorFiat

def get_latest_price(db: Session, id_cripto: int, id_moneda: int) -> float | None:
    """Consulta tu DB para obtener el precio más reciente de una cripto/fiat."""
    
    # Esta consulta busca el valor de la cripto en la moneda fiat específica, 
    # obteniendo el registro de valor_historico más reciente.
    query = text("""
        SELECT
            vf.valor
        FROM
            valor_historico vh
        JOIN
            valor_fiat vf ON vh.id_valor_historico = vf.id_valor_historico
        WHERE
            vh.id_cripto = :cripto_id AND vf.id_moneda = :moneda_id
        ORDER BY
            vh.fecha DESC
        LIMIT 1
    """)
    resultado = db.execute(query, {"cripto_id": id_cripto, "moneda_id": id_moneda}).fetchone()

    return float(resultado[0]) if resultado else None


def verificar_y_disparar_alertas():
    db: Session = sessionLocal()
    try:
        # 1. Obtener todas las alertas activas (estado = True)
        alertas_activas = db.query(AlertaPersonalizada).filter(AlertaPersonalizada.estado == True).all()
        
        for alerta in alertas_activas:
            # 2. Obtener el precio actual (de tu DB)
            precio_actual = get_latest_price(db, alerta.id_cripto, alerta.id_moneda)
            
            if precio_actual is None:
                print(f"Advertencia: No se encontró precio para alerta {alerta.id_alerta}")
                continue

            alerta_disparada = False
            
            # 3. Lógica de Comparación
            
            # Alerta de Subida
            if alerta.precio_subida_objetivo is not None:
                if precio_actual >= alerta.precio_subida_objetivo:
                    alerta_disparada = True
                    print(f"Alerta {alerta.id_alerta} DISPARADA: {precio_actual} >= {alerta.precio_subida_objetivo}")

            # Alerta de Bajada
            elif alerta.precio_bajada_objetivo is not None:
                if precio_actual <= alerta.precio_bajada_objetivo:
                    alerta_disparada = True
                    print(f"Alerta {alerta.id_alerta} DISPARADA: {precio_actual} <= {alerta.precio_bajada_objetivo}")
            
            # 4. Disparo y Actualización (solo si se cumplió la condición)
            if alerta_disparada:
                # 4a. Notificación (Aquí llamarías a tu servicio de Email/Push)
                # enviar_notificacion(alerta, precio_actual) 
                
                # 4b. Actualizar el estado en la DB
                alerta.estado = False  # Desactivar
                alerta.ultima_activacion = datetime.utcnow()
                
        db.commit()
    except Exception as e:
        print(f"Error en el worker de alertas: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    verificar_y_disparar_alertas()