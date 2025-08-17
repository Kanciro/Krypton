from fastapi import FastAPI, HTTPException, Depends
from servicio_datos_cripto.services.crypto_data_service import traerTopCriptomonedas
from servicio_datos_cripto.services.crypto_sync_service import (actualizar_criptomonedas_en_db)
from servicio_datos_cripto.services.fiat_data_service import traerTopMonedasFiat
from servicio_usuarios.services.user_data_services import RegistrarUsuario
from servicio_usuarios.schemas.schema_users import UsuarioCrear, UsuarioBase as UsuarioSchema
from sqlalchemy.orm import Session
from servicio_usuarios.database.db import get_db



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

    from servicio_usuarios.database.db import get_db

    db = next(get_db())
    cryptos = actualizar_criptomonedas_en_db(db)

    if cryptos is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los datos de las criptomonedas.",
        )
    return cryptos

@app.get("/api/v1/cryptocurrencies/popular/monedas_fiat/popular")
async def leerMonedasFiat():

    fiats = traerTopMonedasFiat()

    if fiats is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los datos de las monedas fiat.",
        )

    return fiats


@app.get("/api/v1/cryptocurrencies/popular/monedas_fiat/popular/base_de_datos")
async def leerMonedasFiatConBD():

    from servicio_usuarios.database.db import get_db

    db = next(get_db())
    fiats = traerTopMonedasFiat()

    if fiats is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los datos de las monedas fiat.",
        )
    
    return fiats


@app.post("/users/", response_model=UsuarioSchema, status_code=201)
def CrearUsuario(user_data: UsuarioCrear, db: Session = Depends(get_db)):
    try:

        new_user = RegistrarUsuario(db=db, datos_usuario=user_data)
        return new_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
