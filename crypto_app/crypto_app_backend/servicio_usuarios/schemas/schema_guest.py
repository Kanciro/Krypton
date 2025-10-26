from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import date, datetime, timedelta

class InvitadoResponse(BaseModel):
    id_invitado: int
    mensaje: str = "Sesión de invitado creada con éxito."
    fecha_ingreso:  Optional[datetime]

class InteraccionInvitadoRequest(BaseModel):
    id_invitado: int
    id_cripto: Optional[int] = None
    id_moneda: Optional[int] = None