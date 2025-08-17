from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from sqlalchemy.orm import relationship
from ..database.db import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    correo = Column(String(100), unique=True, index=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    contraseña = Column(String(255), nullable=False)
    notificaciones = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    ultimo_inicio_sesion = Column(DateTime, default=datetime.utcnow)

    # Corrección: Se agrega la relación con ConsultasUsuario
    alertas_personalizadas = relationship(
        "AlertaPersonalizada", back_populates="usuario"
    )
    consultas_usuario = relationship("ConsultasUsuario", back_populates="usuario")
