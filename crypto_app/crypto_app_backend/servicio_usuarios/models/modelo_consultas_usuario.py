from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from ..database.db import Base

# importar la clases necesarias para la relación
from .modelo_criptomonedas import Criptomoneda
from .modelo_usuario import Usuario
from .modelo_moneda_fiat import MonedaFiat


class ConsultasUsuario(Base):
    __tablename__ = "consultas_usuario"

    # foreign key para relacionar con la tabla criptomonedas
    id_cripto = Column(Integer, ForeignKey("criptomonedas.id_cripto"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_moneda_fiat = Column(Integer, ForeignKey("monedas_fiat.id_moneda"), nullable=False)

    # Atributos de la tabla
    id_consulta = Column(Integer, primary_key=True, index=True)
    fecha_consulta = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones con las tablas Criptomoneda, Usuario y MonedaFiat
    criptomoneda = relationship("Criptomoneda", back_populates="consultas_usuario")
    usuario = relationship("Usuario", back_populates="consultas_usuario") 
    moneda_fiat = relationship("MonedaFiat", back_populates="consultas_usuario") 
