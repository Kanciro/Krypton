from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from ..database.db import Base


# la clase Usuario representa la tabla 'usuarios' en la base de datos
class Usuario(Base):
    __tablename__ = "usuarios"

    # atributos de la tabla
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    correo = Column(String(100), unique=True, index=True, nullable=False)
    fecha_nacimiento = Column(String(255), nullable=False)
    contraseña = Column(Date, nullable=True)
    notificaciones = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    ultimo_inicio_sesion = Column(DateTime, default=datetime.utcnow)
