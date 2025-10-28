# servicio_alertas/schemas/schema_alerta.py

from pydantic import BaseModel, Field
from typing import Optional, Literal

# El tipo 'Literal' restringe el valor a 'subida' o 'bajada'
DireccionAlerta = Literal["subida", "bajada"]

class AlertaCreateSchema(BaseModel):
    # Usaremos símbolos para mayor comodidad del frontend/usuario
    simbolo_cripto: str = Field(default=..., min_length=2, max_length=10, example="BTC") # pyright: ignore[reportCallIssue]
    simbolo_moneda: str = Field(..., min_length=2, max_length=3, example="EUR") # pyright: ignore[reportCallIssue]
    
    # La dirección indica si el valor objetivo es para subida o bajada
    direccion: DireccionAlerta
    
    # El valor que activa la alerta
    valor_objetivo: float = Field(..., gt=0, description="El precio que activa la alerta")
    
    # Configuración de Pydantic
    class Config:
        from_attributes = True

class AlertaResponseSchema(BaseModel):
    id_alerta: int
    id_cripto: int
    id_moneda: int
    precio_subida_objetivo: Optional[float]
    precio_bajada_objetivo: Optional[float]
    estado: bool