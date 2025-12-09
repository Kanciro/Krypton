# worker_alertas.py

from sqlalchemy.orm import Session
from sqlalchemy import func, text
from datetime import datetime
from typing import cast
from servicio_usuarios.database.db import engine, sessionLocal # Asumiendo rutas correctas
from servicio_usuarios.models.modelo_alertas_personalizadas import AlertaPersonalizada
# Importa también los modelos Criptomoneda, MonedaFiat, ValorHistorico, ValorFiat

def get_latest_price(db: Session, id_cripto: int, id_moneda: int) -> float | None:
    """Consulta tu DB para obtener el precio más reciente de una cripto/fiat."""
    
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
            # Convert SQLAlchemy Column values to plain ints for the typed helper
            precio_actual = get_latest_price(db, cast(int, alerta.id_cripto), cast(int, alerta.id_moneda))
            
            if precio_actual is None:
                print(f"Advertencia: No se encontró precio para alerta {alerta.id_alerta}")
                continue

            alerta_disparada = False
            
            # 3. Lógica de Comparación
            # Asegurarse de trabajar con valores Python (floats) y no con ColumnElement de SQLAlchemy.
            precio_subida = getattr(alerta, "precio_subida_objetivo", None)
            precio_bajada = getattr(alerta, "precio_bajada_objetivo", None)

            def _coerce_scalar(val, field_name: str):
                if val is None:
                    return None
                # Primer intento: convertir directamente (útil si es Decimal/str/float)
                try:
                    return float(val)
                except Exception:
                    # Si falla (por ejemplo es un ColumnElement), obtener el valor desde la BD por id de alerta
                    try:
                        return db.query(getattr(AlertaPersonalizada, field_name)).filter(AlertaPersonalizada.id_alerta == alerta.id_alerta).scalar()
                    except Exception:
                        return None

            precio_subida = _coerce_scalar(precio_subida, "precio_subida_objetivo")
            precio_bajada = _coerce_scalar(precio_bajada, "precio_bajada_objetivo")

            # Alerta de Subida
            if precio_subida is not None:
                if precio_actual >= precio_subida:
                    alerta_disparada = True
                    print(f"Alerta {alerta.id_alerta} DISPARADA: {precio_actual} >= {precio_subida}")

            # Alerta de Bajada
            elif precio_bajada is not None:
                if precio_actual <= precio_bajada:
                    alerta_disparada = True
                    print(f"Alerta {alerta.id_alerta} DISPARADA: {precio_actual} <= {precio_bajada}")
            
            # 4. Disparo y Actualización (solo si se cumplió la condición)
            if alerta_disparada:
                # 4a. Notificación (Aquí llamarías a tu servicio de Email/Push)
                # enviar_notificacion(alerta, precio_actual) 
                
                # 4b. Actualizar el estado en la DB (usar update para evitar errores de tipado)
                db.query(AlertaPersonalizada).filter(
                    AlertaPersonalizada.id_alerta == alerta.id_alerta
                ).update(
                    {"estado": False, "ultima_activacion": datetime.utcnow()},
                    synchronize_session=False
                )
                
        db.commit()
    except Exception as e:
        print(f"Error en el worker de alertas: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    verificar_y_disparar_alertas()