from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from ..database.db import Base

# Importar la clase necesaria para la relación
from .modelo_criptomonedas import Criptomoneda


class calculadoraDeDivisas(Base):
    __tablename__ = "calculadora_de_divisas"

    # foreing key para relacionar con la tabla criptomonedas
    id_cripto = Column(Integer, ForeignKey("criptomonedas.id_cripto"), nullable=False)

    # atributos de la tabla
    id_calculadora = Column(Integer, primary_key=True, index=True)
    api_valor_fiat = Column(String(100), nullable=False)
    cambio = Column(String(100), nullable=False)
    fecha_conversion = Column(DateTime, default=datetime.utcnow)

    # realción con la tabla Criptomoneda
    criptomoneda = relationship(
        "Criptomoneda", back_populates="calculadoras_de_divisas"
    )
