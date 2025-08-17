# modelo_noticias.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from ..database.db import Base

# Corrección: Elimina las importaciones de los modelos para evitar circularidad.
#from .modelo_fuente import Fuente
#from .modelo_categoria_noticias import CategoriaNoticias

class Noticia(Base):
    __tablename__ = "noticias"

    id_cripto = Column(Integer, ForeignKey("criptomonedas.id_cripto"), nullable=True)
    id_fuente = Column(Integer, ForeignKey("fuentes.id_fuente"), nullable=False)
    id_categoria = Column(Integer, ForeignKey("categorias_noticias.id_categoria"), nullable=False)

    id_noticia = Column(Integer, primary_key=True, index=True)
    api_id = Column(String(50), nullable=False)
    titulo = Column(String(200), nullable=False)
    url = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Corrección: Usa el nombre de la clase, no de la tabla
    cripto = relationship("Criptomoneda", back_populates="noticias")
    fuente = relationship("Fuente", back_populates="noticias")
    categoria = relationship("CategoriaNoticias", back_populates="noticias")