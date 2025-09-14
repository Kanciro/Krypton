# servicio_usuarios/models/modelo_invitado.py

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database.db import Base


class InteraccionInvitado(Base):
    __tablename__ = "interacciones_invitados"

    id_interaccion = Column(Integer, primary_key=True, index=True)
    id_invitado = Column(Integer, ForeignKey('invitados.id_invitado', ondelete='CASCADE'), nullable=False)
    id_cripto = Column(Integer, ForeignKey('criptomonedas.id_cripto', ondelete='SET NULL'), nullable=True)
    id_moneda = Column(Integer, ForeignKey('moneda_fiat.id_moneda', ondelete='SET NULL'), nullable=True)
    fecha_consulta = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    
    invitado = relationship("Invitado", back_populates="interacciones_invitados")
    criptomoneda = relationship("Criptomoneda", back_populates="interacciones_invitados")
    moneda_fiat = relationship("MonedaFiat", back_populates="interacciones_invitados")
