

from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from servicio_usuarios.models.modelo_criptomonedas import Criptomoneda
from servicio_usuarios.models.modelo_valor_historico import ValorHistorico

def ObtenerValorPorSimbolo(
    db: Session,
    simbolo_cripto: str,
    dias: int
) -> List[ValorHistorico]:

    # 1. Encontrar la criptomoneda por su símbolo
    cripto = db.query(Criptomoneda).filter(Criptomoneda.simbolo == simbolo_cripto).first()
    if not cripto:
        return None # Devuelve None si la criptomoneda no se encuentra

    # 2. Calcular la fecha de inicio para el filtro
    fecha_limite = datetime.utcnow() - timedelta(days=dias)

    # 3. Consultar los datos históricos
    valores = db.query(ValorHistorico).filter(
        and_(
            ValorHistorico.id_cripto == cripto.id_cripto,
            ValorHistorico.fecha >= fecha_limite
        )
    ).all()

    return valores