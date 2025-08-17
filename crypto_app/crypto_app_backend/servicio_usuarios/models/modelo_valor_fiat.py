# modelo_valor_fiat.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from ..database.db import Base
from sqlalchemy.orm import relationship

# Corrección: Elimina las importaciones de los modelos para evitar circularidad.
#from .modelo_moneda_fiat import MonedaFiat
#from .modelo_valor_historico import ValorHistorico

class ValorFiat(Base):
    __tablename__ = "valores_fiat"

    id_moneda_fiat = Column(Integer, ForeignKey("moneda_fiat.id_moneda"), nullable=False)
    id_valor_historico = Column(Integer, ForeignKey("valores_historicos.id_valor_historico"), nullable=False)

    id_valor_fiat = Column(Integer, primary_key=True, index=True)
    valor = Column(String(50), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    hora = Column(DateTime, default=datetime.utcnow)

    # Corrección: Las relaciones deben tener nombres de propiedades consistentes
    moneda_fiat = relationship("MonedaFiat", back_populates="valores_fiat")
    valor_historico = relationship("ValorHistorico", back_populates="valores_fiat")