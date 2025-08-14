from fastapi import FastAPI, HTTPException
from servicio_datos_cripto.services.crypto_data_service import traerTopCriptomonedas
from servicio_datos_cripto.services.crypto_sync_service import (
    actualizar_criptomonedas_en_db,
)

app = FastAPI(
    title="Krypton API Gateway",
    description="API Gateway para la aplicación móvil de gestión de criptomonedas.",
    version="1.0.0",
)


@app.get("/api/v1/cryptocurrencies/popular")
async def leerCripto():

    cryptos = traerTopCriptomonedas()

    if cryptos is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los datos de las criptomonedas.",
        )

    return cryptos


@app.get("/api/v1/cryptocurrencies/popular/base_de_datos")
async def leerCriptoConBD():

    from ...servicio_usuarios.database.db import get_db

    db = next(get_db())
    cryptos = actualizar_criptomonedas_en_db(db)

    if cryptos is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los datos de las criptomonedas.",
        )
    return cryptos
