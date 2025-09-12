# main.py

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, Query, Path
from typing import List
import asyncio
import logging
import json
from fastapi.middleware.cors import CORSMiddleware
# Tus imports existentes
from servicio_datos_cripto.services.crypto_data_service import traerTopCriptomonedas
from servicio_datos_cripto.services.crypto_data_id_service import ObtenerValorPorSimbolo
# Importa la función actualizada
from servicio_datos_cripto.services.crypto_sync_service import actualizar_criptomonedas_en_db
from servicio_datos_cripto.services.fiat_data_service import traerTopMonedasFiat
from servicio_usuarios.services.user_data_services import RegistrarUsuario
from servicio_usuarios.schemas.schema_users import (
    UsuarioCrear,
    UsuarioBase as UsuarioSchema, 
    UsuarioActualizar
)
from servicio_usuarios.schemas.schema_valor_historico import ValorHistoricoSchema
from servicio_usuarios.models.modelo_usuario import Usuario
from servicio_usuarios.services.user_update_data_services import ActualizarUsuario
from sqlalchemy.orm import Session
from servicio_usuarios.schemas.schema_usuario_login import LoginSchema
from servicio_usuarios.database.db import get_db

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Gestor de conexiones para WebSockets
class ConnectionManager:
    #Clase para gestionar las conexiones de clientes por WebSocket.
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # Acepta una nueva conexión WebSocket y la agrega a la lista de conexiones activas.
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Nuevo cliente conectado. Total de conexiones: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        # Desconecta un cliente WebSocket y lo elimina de la lista de conexiones activas.
        self.active_connections.remove(websocket)
        logger.info(f"Cliente desconectado. Total de conexiones: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        # Envía un mensaje a un cliente WebSocket específico.
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        # Envía un mensaje a todos los clientes WebSocket conectados.
        for connection in self.active_connections:
            await connection.send_text(message)
        logger.info("Mensaje transmitido a todos los clientes.")


manager = ConnectionManager()

app = FastAPI(
    title="Krypton API Gateway",
    description="API Gateway para la aplicación móvil de gestión de criptomonedas.",
    version="1.0.0",
)



origins = [
    "http://localhost",
    "http://localhost:3000", 
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
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



"""
@app.get("/api/v1/cryptocurrencies/popular/base_de_datos")
async def leerCriptoConBD(db: Session = Depends(get_db)):
    criptos_api = traerTopCriptomonedas()
    if criptos_api is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los datos de las criptomonedas.",
        )
    result = actualizar_criptomonedas_en_db(db, criptos_api)
    if result is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los datos de las criptomonedas.",
        )
    return result 
"""

@app.get(
    "/api/v1/cryptocurrencies/history/by_symbol/{simbolo_cripto}",
    response_model=List[ValorHistoricoSchema],
    status_code=200
)
async def leer_historico_por_simbolo(
    simbolo_cripto: str = Path(..., description="Símbolo de la criptomoneda (ej. 'BTC', 'ETH')", example="BTC"),
    dias: int = Query(30, ge=1, description="Número de días hacia atrás a filtrar", example=30),
    db: Session = Depends(get_db)
):
    valores_historicos = ObtenerValorPorSimbolo(db, simbolo_cripto, dias)

    if valores_historicos is None:
        raise HTTPException(status_code=404, detail="Criptomoneda no encontrada.")

    return valores_historicos


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
async def leerMonedasFiatConBD(db: Session = Depends(get_db)):
    fiats = traerTopMonedasFiat()
    if fiats is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los datos de las monedas fiat.",
        )
    return fiats


@app.post("/users/registrar", response_model=UsuarioSchema, status_code=201)
def CrearUsuario(user_data: UsuarioCrear, db: Session = Depends(get_db)):
    try:
        new_user = RegistrarUsuario(db=db, datos_usuario=user_data)
        return new_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
# Nuevo endpoint para actualizar usuario por ID
@app.put("/users/actualizar/{user_id}", response_model=UsuarioSchema, status_code=200)
def actualizar_usuario_endpoint(
    user_id: int = Path(..., description="ID del usuario a actualizar", gt=0),
    user_data: UsuarioActualizar = ...,
    db: Session = Depends(get_db)
):
    try:
        updated_user = ActualizarUsuario(db=db, usuario_id=user_id, datos_usuario=user_data)
        return updated_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# Nuevo endpoint para actualizar usuario por correo
@app.put("/users/actualizar/by-email/{email}", response_model=UsuarioSchema, status_code=200)
def actualizar_usuario_por_correo_endpoint(
    email: str = Path(..., description="Correo del usuario a actualizar"),
    user_data: UsuarioActualizar = ...,
    db: Session = Depends(get_db)
):
    try:
        usuario_encontrado = db.query(Usuario).filter(Usuario.correo == email).first()
        
        if not usuario_encontrado:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        updated_user = ActualizarUsuario(db=db, usuario_id=usuario_encontrado.id_usuario, datos_usuario=user_data)
        return updated_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.post("/users/login", response_model=UsuarioSchema)
def Login(credenciales: LoginSchema, db: Session = Depends(get_db)):
    from servicio_usuarios.services.user_enter_services import LoginUsuarioSeguro
    try:
        usuario_logeado = LoginUsuarioSeguro(db=db, credenciales=credenciales)
        return usuario_logeado
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    


"""
@app.get("/api/v1/cryptocurrencies/history/{crypto_id_api}")
def LeerValorHistorico(crypto_id: str, days: int):

    from servicio_datos_cripto.services.historical_crypto_data_services import LeerValorHistorico
    result = LeerValorHistorico(crypto_id, days)
    if result is None:
        raise HTTPException(status_code=500, detail="Error al cargar los datos históricos.")
    return result
"""

"""
@app.get("/api/v1/cryptocurrencies/history/{crypto_id_api}/db")
def CargarHistoricoDesdeDb(crypto_id: str, days: int, db: Session = Depends(get_db)):
    from servicio_datos_cripto.services.historical_crypto_sync_services import ActualizarValorHistoricoConDb
    result = ActualizarValorHistoricoConDb(db, crypto_id, days)
    if result is None:
        raise HTTPException(status_code=500, detail="Error al cargar los datos históricos desde la base de datos.")
    return result
"""

@app.websocket("/ws/cryptocurrencies")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):

    await manager.connect(websocket)
    try:
        while True:
            retries = 3
            crypto_prices = None
            for i in range(retries):
                crypto_prices = traerTopCriptomonedas()
                if crypto_prices:
                    break
                else:
                    logger.warning(f"Intento {i+1} de {retries} fallido. Esperando antes de reintentar...")
                    await asyncio.sleep(2 ** i)

            if not crypto_prices:
                logger.error("No se pudieron obtener los datos después de varios intentos. Deteniendo la transmisión.")
            else:

                actualizar_criptomonedas_en_db(db, crypto_prices)

                await manager.broadcast(json.dumps(crypto_prices))

            await asyncio.sleep(3)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"Cliente desconectado de WebSocket.")
