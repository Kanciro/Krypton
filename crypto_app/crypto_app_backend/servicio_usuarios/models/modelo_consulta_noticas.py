# modelo_consulta_noticias.py
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database.db import Base

class ConsultaNoticias(Base):
    __tablename__ = "consulta_noticias"

    id_consulta_noticia = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_noticia = Column(Integer, ForeignKey("noticias.id_noticias"), nullable=False)
    fecha_consulta = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Definir las relaciones con los modelos de Usuario y Noticia
    usuario = relationship("Usuario", back_populates="consultas_noticias")
    noticias = relationship("Noticia", back_populates="consultas_noticias")