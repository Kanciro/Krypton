# modelo_fuente.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from sqlalchemy.orm import relationship
from ..database.db import Base


class Fuente(Base):
    # Corrección: Nombre de la tabla en minúsculas
    __tablename__ = "fuente"

    id_fuente = Column(Integer, primary_key=True, index=True)
    fuente = Column(String(100), unique=True, nullable=False)

    # Agrega la relación que se usará en el modelo de Noticias
    noticias = relationship("Noticia", back_populates="fuente")
