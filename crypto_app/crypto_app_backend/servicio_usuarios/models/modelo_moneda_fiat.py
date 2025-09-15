# modelo_moneda_fiat.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from sqlalchemy.orm import relationship
from ..database.db import Base


class MonedaFiat(Base):
    __tablename__ = "moneda_fiat"

    id_moneda = Column(Integer, primary_key=True, index=True)
    coi  = Column( String(3), unique=False, nullable=False)
    nombre = Column(String(100), nullable=False)

    valores_fiat = relationship("ValorFiat", back_populates="moneda_fiat")
    consultas_usuario = relationship("ConsultasUsuario", back_populates="moneda_fiat")
    interacciones_invitados = relationship("InteraccionInvitado", back_populates="moneda_fiat")