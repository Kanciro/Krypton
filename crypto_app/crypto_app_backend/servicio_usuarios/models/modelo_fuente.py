from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from ..database.db import Base


# la clase fuente representa la tabla 'fuentes' en la base de datos
class fuente(Base):
    __tablename__ = "fuentes"

    # atributos de la tabla
    id_fuente = Column(Integer, primary_key=True, index=True)
    fuente = Column(String(100), unique=True, nullable=False)
