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

# importar las clases necesarias para la relación
from .modelo_criptomonedas import Criptomoneda
from .modelo_usuario import Usuario


class AlertaPersonalizada(Base):
    __tablename__ = "alertas_personalizadas"
    __table_args__ = (
        CheckConstraint(
            "(tipo_alerta = 'precio' AND precio_objetivo IS NOT NULL AND porcentaje_cambio_objetivo IS NULL) OR "
            "(tipo_alerta = 'porcentaje_cambio' AND porcentaje_cambio_objetivo IS NOT NULL AND precio_objetivo IS NULL)",
            name="chk_alerta_tipo",
        ),
    )

    # foreign key para relacionar con las tablas necesarias
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_cripto = Column(Integer, ForeignKey("criptomonedas.id_cripto"), nullable=False)

    # Atributos de la tabla
    id_alerta = Column(Integer, primary_key=True, index=True)
    precio_objetivo = Column(Integer, nullable=False)
    porcentaje_cambio_objetivo = Column(Integer, nullable=False)
    tipo_alerta = Column(
        String(50), nullable=False
    )  # Ejemplo: "precio", "porcentaje_cambio"
    estado = Column(Boolean, default=True)  # Estado de la alerta (activa/inactiva)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    ultima_activacion = Column(DateTime, nullable=True)

    # Relaciones con las tablas Criptomoneda y Usuario
    criptomoneda = relationship("Criptomoneda", back_populates="alertas_personalizadas")
    usuario = relationship("Usuario", back_populates="alertas_personalizadas")
