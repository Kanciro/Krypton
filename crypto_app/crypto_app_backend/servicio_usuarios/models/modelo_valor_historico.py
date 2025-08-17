# modelo_valor.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from ..database.db import Base


class ValorHistorico(Base):
    __tablename__ = "valores_historicos"

    id_cripto = Column(Integer, ForeignKey("criptomonedas.id_cripto"), nullable=False)

    id_valor_historico = Column(Integer, primary_key=True, index=True)
    valor = Column(String(50), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relación con la tabla Criptomoneda
    criptomoneda = relationship("Criptomoneda", back_populates="valores_historicos")

    # Corrección: Agrega la relación con la tabla de valores fiat
    valores_fiat = relationship("ValorFiat", back_populates="valor_historico")
