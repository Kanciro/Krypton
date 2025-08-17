# modelo_calculadora_de_divisas.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from ..database.db import Base

class CalculadoraDeDivisas(Base):
    __tablename__ = "calculadora_de_divisas"

    id_cripto = Column(Integer, ForeignKey("criptomonedas.id_cripto"), nullable=False)
    
    id_calculadora = Column(Integer, primary_key=True, index=True)
    api_valor_fiat = Column(String(100), nullable=False)
    cambio = Column(String(100), nullable=False)
    fecha_conversion = Column(DateTime, default=datetime.utcnow)

    # Corrección: El back_populates debe ser "calculadoras_de_divisas" (plural)
    # y la propiedad en Criptomoneda debe coincidir.
    criptomoneda = relationship("Criptomoneda", back_populates="calculadoras_de_divisas")