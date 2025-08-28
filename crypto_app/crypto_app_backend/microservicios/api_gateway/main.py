# main.py

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, Query
from typing import List
import asyncio
import logging
import json
from fastapi.middleware.cors import CORSMiddleware
# Tus imports existentes
from servicio_datos_cripto.services.crypto_data_service import traerTopCriptomonedas
# Importa la función actualizada
from servicio_datos_cripto.services.crypto_sync_service import actualizar_criptomonedas_en_db
from servicio_datos_cripto.services.fiat_data_service import traerTopMonedasFiat
from servicio_usuarios.services.user_data_services import RegistrarUsuario
from servicio_usuarios.schemas.schema_users import (
    UsuarioCrear,
    UsuarioBase as UsuarioSchema,
)
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

# Tu aplicación FastAPI
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

# Tus endpoints existentes (con pequeñas mejoras de logging y manejo de excepciones)
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
async def leerCriptoConBD(db: Session = Depends(get_db)):
    # Este endpoint ya no es necesario si la actualización se hace por WebSocket,
    # pero lo dejamos para no romper tu código.
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


@app.post("/login", response_model=UsuarioSchema)
def Login(credenciales: LoginSchema, db: Session = Depends(get_db)):
    from servicio_usuarios.services.user_enter_services import LoginUsuarioSeguro
    try:
        usuario_logeado = LoginUsuarioSeguro(db=db, credenciales=credenciales)
        return usuario_logeado
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@app.get("/api/v1/cryptocurrencies/history/{crypto_id_api}")
def LeerValorHistorico(crypto_id: str, days: int):

    from servicio_datos_cripto.services.historical_crypto_data_services import LeerValorHistorico
    result = LeerValorHistorico(crypto_id, days)
    if result is None:
        raise HTTPException(status_code=500, detail="Error al cargar los datos históricos.")
    return result

@app.get("/api/v1/cryptocurrencies/history/{crypto_id_api}/db")
def CargarHistoricoDesdeDb(crypto_id: str, days: int, db: Session = Depends(get_db)):
    from servicio_datos_cripto.services.historical_crypto_sync_services import ActualizarValorHistoricoConDb
    result = ActualizarValorHistoricoConDb(db, crypto_id, days)
    if result is None:
        raise HTTPException(status_code=500, detail="Error al cargar los datos históricos desde la base de datos.")
    return result

# --- Endpoint de WebSocket actualizado para sincronizar la BD ---
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
                # Sincronizar la base de datos con los datos recibidos
                actualizar_criptomonedas_en_db(db, crypto_prices)

                # Transmitir los datos a todos los clientes WebSocket conectados
                # Usamos json.dumps para enviar un string JSON válido al frontend
                await manager.broadcast(json.dumps(crypto_prices))

            await asyncio.sleep(3)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"Cliente desconectado de WebSocket.")
