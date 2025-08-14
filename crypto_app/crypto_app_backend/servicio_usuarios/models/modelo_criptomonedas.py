from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from ..database.db import Base


# la clase criptomoneda representa la tabla 'criptomonedas' en la base de datos
class Criptomoneda(Base):
    __tablename__ = "criptomonedas"

    # atributos de la tabla
    id_cripto = Column(Integer, primary_key=True, index=True)
    simbolo = Column(String(10), unique=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    id_api = Column(String(50), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
