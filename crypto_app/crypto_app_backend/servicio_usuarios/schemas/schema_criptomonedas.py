from pydantic import BaseModel
from datetime import datetime

class CriptomonedaSchema(BaseModel):
    id_cripto: int
    simbolo: str
    nombre: str
    id_api: str
    fecha_creacion: datetime

    class Config:
        from_attributes = True