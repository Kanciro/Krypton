# servicio_usuarios/models/modelo_invitado.py

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.db import Base

class Invitado(Base):
    __tablename__ = "invitados"

    id_invitado = Column(Integer, primary_key=True, index=True)
    direccion_ip = Column(String(45), nullable=True)
    fecha_ingreso = Column(TIMESTAMP, default=datetime.utcnow)
    ultimo_acceso = Column(TIMESTAMP, nullable=True)
    sesion_activa = Column(Boolean, default=True)
    navegador_agente = Column(Text, nullable=True)
    
    # La clase 'InteraccionInvitado' se importa en el otro archivo, por eso se pone como string
    interacciones_invitados = relationship("InteraccionInvitado", back_populates="invitado")