from pydantic import BaseModel

class MonedaFiatSchema(BaseModel):
    id_moneda: int
    coi : str
    nombre: str

    class Config:
        from_attributes = True