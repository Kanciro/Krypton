from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Verificar si la URL existe para evitar errores
if not DATABASE_URL:
    raise ValueError("No se encontró la variable de entorno DATABASE_URL.")

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crear una clase base para los modelos declarativos
Base = declarative_base()

# Configurar el SessionLocal para manejar las sesiones de la base de datos
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Función para obtener una sesión de la base de datos.
    """
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
