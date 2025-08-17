# modelo_categorias_noticias.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from sqlalchemy.orm import relationship
from ..database.db import Base


# la clase categoria_noticias representa la tabla 'categorias_noticias' en la base de datos
class CategoriaNoticias(Base):
    __tablename__ = "categorias_noticias"

    # atributos de la tabla
    id_categoria = Column(Integer, primary_key=True, index=True)
    categoria = Column(String(100), unique=False, nullable=False)

    # Relación bidireccional con el modelo Noticia
    # Esta propiedad se usará en el back_populates del modelo Noticia
    noticias = relationship("Noticia", back_populates="categoria")
