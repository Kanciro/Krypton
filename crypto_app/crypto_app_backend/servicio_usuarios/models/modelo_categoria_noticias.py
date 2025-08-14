from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from ..database.db import Base


# la clase categoria_noticias representa la tabla 'categorias_noticias' en la base de datos
class CategoriaNoticias(Base):
    __tablename__ = "categorias_noticias"

    # atributos de la tabla
    id_categoria = Column(Integer, primary_key=True, index=True)
    categoria = Column(String(100), unique=False, nullable=False)
