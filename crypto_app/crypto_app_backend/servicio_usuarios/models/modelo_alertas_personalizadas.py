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
)
from ..database.db import Base
from sqlalchemy.orm import relationship

class AlertaPersonalizada(Base):
    __tablename__ = "alertas_personalizadas"
    __table_args__ = (
        CheckConstraint(
            "(tipo_alerta = 'precio' AND precio_objetivo IS NOT NULL AND porcentaje_cambio_objetivo IS NULL) OR "
            "(tipo_alerta = 'porcentaje_cambio' AND porcentaje_cambio_objetivo IS NOT NULL AND precio_objetivo IS NULL)",
            name="chk_alerta_tipo",
        ),
    )

    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_cripto = Column(Integer, ForeignKey("criptomonedas.id_cripto"), nullable=False)

    id_alerta = Column(Integer, primary_key=True, index=True)
    # Corrección: Las columnas deben ser anulables para la lógica del CheckConstraint
    precio_objetivo = Column(Integer, nullable=True)
    porcentaje_cambio_objetivo = Column(Integer, nullable=True)
    tipo_alerta = Column(String(50), nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    ultima_activacion = Column(DateTime, nullable=True)

    # Las relaciones están bien definidas
    criptomoneda = relationship("Criptomoneda", back_populates="alertas_personalizadas")
    usuario = relationship("Usuario", back_populates="alertas_personalizadas")