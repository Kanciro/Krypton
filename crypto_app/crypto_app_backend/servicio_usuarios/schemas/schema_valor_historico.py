
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ValorHistoricoSchema(BaseModel):
    """
    Esquema Pydantic para la respuesta del valor histórico.
    """
    valor: float
    fecha: datetime

    class Config:
        orm_mode = True
