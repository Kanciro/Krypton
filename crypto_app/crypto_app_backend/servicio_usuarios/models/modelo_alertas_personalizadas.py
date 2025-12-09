# modelo_alertas.py

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    CheckConstraint,
    Numeric,
    func
)
from ..database.db import Base
from sqlalchemy.orm import relationship


class AlertaPersonalizada(Base):
    __tablename__ = "alertas_personalizadas"

    id_alerta = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False)
    id_cripto = Column(Integer, ForeignKey("criptomonedas.id_cripto", ondelete="CASCADE"), nullable=False)
    id_moneda = Column(Integer, ForeignKey("moneda_fiat.id_moneda", ondelete="CASCADE"), nullable=False)
    
    precio_subida_objetivo = Column(Numeric(18, 8), nullable=True)
    precio_bajada_objetivo = Column(Numeric(18, 8), nullable=True)
    
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=func.now())
    ultima_activacion = Column(DateTime, nullable=True)
    
    __table_args__ = (
        CheckConstraint(
            "(precio_subida_objetivo IS NOT NULL AND precio_bajada_objetivo IS NULL) OR "
            "(precio_subida_objetivo IS NULL AND precio_bajada_objetivo IS NOT NULL) OR "
            "(precio_subida_objetivo IS NULL AND precio_bajada_objetivo IS NULL)",
            name='chk_alerta_precio_orm'
        ),
    )
    # Las relaciones están bien definidas
    criptomoneda = relationship("Criptomoneda", back_populates="alertas_personalizadas")
    usuario = relationship("Usuario", back_populates="alertas_personalizadas")
    moneda_fiat = relationship("MonedaFiat", back_populates="alertas_personalizadas")