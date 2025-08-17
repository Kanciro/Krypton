# modelo_consulta_usuario.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from ..database.db import Base

# Corrección: No importes los modelos aquí para evitar importaciones circulares.
# SQLAlchemy resolverá las cadenas de texto.


class ConsultasUsuario(Base):
    __tablename__ = "consultas_usuario"

    id_cripto = Column(Integer, ForeignKey("criptomonedas.id_cripto"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_moneda_fiat = Column(
        Integer, ForeignKey("moneda_fiat.id_moneda"), nullable=False
    )

    id_consulta = Column(Integer, primary_key=True, index=True)
    fecha_consulta = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Corrección: El back_populates debe coincidir con el nombre de la propiedad en los otros modelos.
    criptomoneda = relationship("Criptomoneda", back_populates="consultas_usuario")
    usuario = relationship("Usuario", back_populates="consultas_usuario")
    moneda_fiat = relationship("MonedaFiat", back_populates="consultas_usuario")
