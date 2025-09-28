from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session 
from sqlalchemy import and_
from servicio_usuarios.models.modelo_moneda_fiat import MonedaFiat
from servicio_usuarios.models.modelo_valor_fiat import ValorFiat
from servicio_usuarios.models.modelo_valor_historico import ValorHistorico 
from servicio_usuarios.models.modelo_criptomonedas import Criptomoneda 

def ObtenerValorFiatPorSimbolo(
    db: Session,
    simbolo_moneda: str,
    dias: int,
    simbolo_cripto: Optional[str] = None
) -> List[ValorFiat]:
    """
    Obtiene el valor histórico de una moneda fiat filtrando por fecha y,
    opcionalmente, por el símbolo de una criptomoneda.
    """
    # 1. Encontrar la moneda fiat por su símbolo
    fiat = db.query(MonedaFiat).filter(MonedaFiat.coi == simbolo_moneda).first()
    if not fiat:
        return []

    # 2. Calcular la fecha de inicio para el filtro
    fecha_limite = datetime.utcnow() - timedelta(days=dias)

    # 3. Construir la consulta base
    query = db.query(ValorFiat).filter(
        and_(
            ValorFiat.id_moneda == fiat.id_moneda,
            ValorFiat.fecha >= fecha_limite
        )
    )

    # 4. Añadir el filtro por criptomoneda si se proporciona
    if simbolo_cripto:
        query = query.join(ValorHistorico, ValorFiat.id_valor_historico == ValorHistorico.id_valor_historico)
        query = query.join(Criptomoneda, ValorHistorico.id_cripto == Criptomoneda.id_cripto)
        query = query.filter(Criptomoneda.simbolo == simbolo_cripto)

    # 5. Ejecutar la consulta
    valores = query.all()

    return valores