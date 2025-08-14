from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime 
from sqlalchemy.orm import relationship
from ..database.db import Base

#importar la clase necesaria para la relacion
from .modelo_criptomonedas import Criptomoneda

# la clase ValorHistorico representa la tabla 'valores_historicos' en la base de datos
class ValorHistorico(Base):
    __tablenamme__ = "valores_historicos"

    #forign key para relacionar con la tabla criptomonedas
    id_cripto = Column(Integer, ForeignKey("criptomonedas.id_cripto"), nullable=False)

    # atributos de la tabla
    id_valor_historico = Column(Integer, primary_key=True, index=True)
    valor = Column(String(50), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relación con la tabla Criptomoneda
    criptomoneda = relationship("Criptomoneda", back_populates="valores_historicos")
