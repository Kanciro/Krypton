# modelo_criptomonedas.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from sqlalchemy.orm import relationship
from ..database.db import Base


class Criptomoneda(Base):
    __tablename__ = "criptomonedas"

    id_cripto = Column(Integer, primary_key=True, index=True)
    simbolo = Column(String(10), unique=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    id_api = Column(String(50), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Corrección: Asegura que todos los nombres de back_populates coincidan con las propiedades en otros modelos
    alertas_personalizadas = relationship("AlertaPersonalizada", back_populates="criptomoneda")
    calculadoras_de_divisas = relationship("CalculadoraDeDivisas", back_populates="criptomoneda")
    consultas_usuario = relationship("ConsultasUsuario", back_populates="criptomoneda")
    noticias = relationship("Noticia", back_populates="cripto") 
    valor_historico = relationship("ValorHistorico", back_populates="criptomoneda")
    interacciones_invitados = relationship("InteraccionInvitado", back_populates="criptomoneda")
