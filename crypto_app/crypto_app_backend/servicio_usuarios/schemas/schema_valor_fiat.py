from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ValorFiatSchema(BaseModel):
    """
    Esquema Pydantic para la respuesta del valor fiat.
    """
    valor: float
    fecha: datetime

    class Config:
        orm_mode = True