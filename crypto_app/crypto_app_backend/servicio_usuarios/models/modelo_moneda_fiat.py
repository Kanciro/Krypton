from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from ..database.db import Base


# la clase moneda_fiat representa la tabla 'monedas_fiat' en la base de datos
class MonedaFiat(Base):
    __tablename__ = "monedas_fiat"

    # atributos de la tabla
    id_moneda = Column(Integer, primary_key=True, index=True)
    COI = Column(String(10), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
