from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from ..database.db import Base

# Importar modelos necesarios
from .modelo_criptomonedas import Criptomoneda
from .modelo_fuente import fuente
from .modelo_categoria_noticias import CategoriaNoticias


# la clase noticia representa la tabla 'noticias' en la base de datos
class Noticia(Base):
    __tablename__ = "noticias"

    # foreign keys
    id_cripto = Column(Integer, ForeignKey("criptomonedas.id_cripto", nullable=True))
    id_fuente = Column(Integer, ForeignKey("fuentes.id_fuente", nullable=False))
    id_categoria = Column(
        Integer, ForeignKey("categorias_noticias.id_categoria", nullable=False)
    )
    # atributos de la tabla
    id_noticia = Column(Integer, primary_key=True, index=True)
    api_id = Column(String(50), nullable=False)
    titulo = Column(String(200), nullable=False)
    url = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relaciones
    cripto = relationship("Criptomoneda", back_populates="noticias")
    fuente = relationship("Fuente", back_populates="noticias")
    categoria = relationship("CategoriaNoticias", back_populates="noticias")
