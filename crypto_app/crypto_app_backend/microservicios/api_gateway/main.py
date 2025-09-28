# main.py

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, Query, Path, Request, status
from typing import List, Optional
import asyncio
import logging
import json
from fastapi.middleware.cors import CORSMiddleware
# Tus imports existentes
from servicio_datos_cripto.services.crypto_data_service import traerTopCriptomonedas, traerCriptomonedas
from servicio_usuarios.schemas.schema_criptomonedas import CriptomonedaSchema  
from servicio_datos_cripto.services.crypto_data_id_service import ObtenerValorPorSimbolo
from servicio_datos_cripto.services.fiat_data_id_services import ObtenerValorFiatPorSimbolo
# Importa la función actualizada
from servicio_datos_cripto.services.crypto_sync_service import actualizar_criptomonedas_en_db
from servicio_datos_cripto.services.fiat_data_service import traerMonedasFiat 
from servicio_datos_cripto.services.valor_fiat_data_service import obtener_valores_historicos_por_cripto_y_fiats
from servicio_usuarios.services.user_data_services import RegistrarUsuario, hashContraseña
from servicio_usuarios.schemas.schema_valor_fiat import ValorFiatSchema
from servicio_usuarios.schemas.schema_users import (
    UsuarioCrear,
    UsuarioBase as UsuarioSchema, 
    UsuarioActualizar, 
    VerificacionCodigo
)
from servicio_usuarios.models.modelo_moneda_fiat import MonedaFiat
from jose import jwt, JWTError
from servicio_usuarios.services.auth.auth_utils import get_current_user
from servicio_usuarios.services.email_services.email_sender import send_verification_email, send_registration_email_with_code
from servicio_usuarios.schemas.schema_guest import InvitadoResponse
from servicio_datos_cripto.services.valor_fiat_sync_service import guardar_valores_fiat_en_db
import random
import string
from servicio_usuarios.services.user_enquiry_services import registrarConsultaUsuario
from servicio_usuarios.schemas.schema_valor_historico import ValorHistoricoSchema
from servicio_usuarios.models.modelo_usuario import Usuario
from servicio_usuarios.services.user_update_data_services import ActualizarUsuario
from servicio_usuarios.services.user_delete_services import DesactivarUsuario, ReactivarUsuario
from servicio_usuarios.services.guest_services import crear_sesion_invitado, registrar_interaccion_invitado, actualizar_estado_sesiones_inactivas, traerOCrearInvitado
from servicio_usuarios.schemas.schema_guest import InvitadoResponse, InteraccionInvitadoRequest
from sqlalchemy.orm import Session
from servicio_usuarios.schemas.schema_moneda_fiat import MonedaFiatSchema
from servicio_usuarios.schemas.schema_usuario_login import LoginSchema
from servicio_usuarios.database.db import get_db
from servicio_usuarios.services.password_services import solicitarRestablecimientoDeCredencial
from servicio_usuarios.schemas.schema_correo_update import CorreoActualizarSchema, CorreoVerificarSchema
from servicio_usuarios.services.auth.auth_utils import get_current_user
from servicio_usuarios.services.auth.auth_utils import create_access_token, get_current_user
from servicio_usuarios.schemas.schema_usuario_login import TokenSchema
from servicio_usuarios.services.user_enter_services import LoginUsuarioSeguro
from servicio_usuarios.services.auth.auth_utils import SECRET_KEY, ALGORITHM
from servicio_usuarios.schemas.schema_recuperar_contraseña import EmailRequest, PasswordReset  
from servicio_noticias.services.news_services import fetch_and_insert_news
from servicio_noticias.services.news_data_services import TraerNoticias 

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



"""@app.get("/api/v1/cryptocurrencies/popular")
async def leerCripto():
    cryptos = traerTopCriptomonedas()
    if cryptos is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los datos de las criptomonedas.",
        )
    return cryptos

"""

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
@app.get("/cryptos/todas", response_model=List[CriptomonedaSchema], status_code=200)
def obtener_todas_las_criptos(db: Session = Depends(get_db)):
    """
    Endpoint para obtener la lista completa de criptomonedas desde la base de datos.
    """
    try:
        all_cryptos = traerCriptomonedas(db=db)
        return all_cryptos
    except HTTPException as e:
        raise e
    
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

@app.get("/fiat/all", response_model=List[MonedaFiatSchema], status_code=200)
def obtener_todas_las_monedas_fiat(db: Session = Depends(get_db)):
    try:
        all_fiat = traerMonedasFiat(db=db)
        return all_fiat
    except HTTPException as e:
        raise e
    
@app.get(
    "/api/v1/moneda_fiat/history/by_symbol/{simbolo_moneda}",
    response_model=List[ValorFiatSchema],
    status_code=200
)
async def leer_historico_por_simbolo_fiat(
    simbolo_moneda: str = Path(..., description="Símbolo de la moneda fiat (ej. 'USD', 'EUR')", example="EUR"),
    dias: int = Query(30, ge=1, description="Número de días hacia atrás a filtrar", example=30),
    simbolo_cripto: Optional[str] = Query(None, description="Símbolo de la criptomoneda para filtrar (ej. 'BTC', 'ETH')", example="BTC"),
    db: Session = Depends(get_db)
):
    valores_historicos_fiat = ObtenerValorFiatPorSimbolo(db, simbolo_moneda, dias, simbolo_cripto)

    if not valores_historicos_fiat:
        raise HTTPException(status_code=404, detail="Moneda fiat no encontrada, o sin datos históricos para los filtros aplicados.")

    return valores_historicos_fiat
"""
@app.get("/api/v1/cryptocurrencies/{crypto_id}/historical-data")
async def leer_datos_historicos(
    crypto_id: str,
    monedas_fiat: List[str] = Query(..., description="Lista de c\u00f3digos de monedas fiat (ej. usd, eur, cop)", example=["usd", "eur"]),
    dias: int = Query(30, ge=1, description="N\u00famero de d\u00edas hist\u00f3ricos a obtener", example=30)
):

    datos = await obtener_valores_historicos_por_cripto_y_fiats(crypto_id, monedas_fiat, dias)
    if not datos or not datos.get(crypto_id):
        raise HTTPException(
            status_code=500,
            detail=f"No se pudieron obtener los datos hist\u00f3ricos para {crypto_id}.",
        )
    return datos

"""

@app.get("/api/v1/cryptocurrencies/{crypto_id}/historical-data")
async def leer_y_guardar_datos_historicos(
    crypto_id: str,
    monedas_fiat: List[str] = Query(..., description="Lista de c\u00f3digos de monedas fiat (ej. usd, eur, cop)", example=["usd", "eur"]),
    dias: int = Query(30, ge=1, description="N\u00famero de d\u00edas hist\u00f3ricos a obtener", example=30),
    db: Session = Depends(get_db)
):
    """
    Obtiene los datos hist\u00f3ricos de una criptomoneda y los guarda en la base de datos.
    """
    datos = await obtener_valores_historicos_por_cripto_y_fiats(crypto_id, monedas_fiat, dias)
    
    if not datos or not datos.get(crypto_id):
        raise HTTPException(
            status_code=500,
            detail=f"No se pudieron obtener los datos hist\u00f3ricos para {crypto_id}.",
        )
    
    guardado_exitoso = guardar_valores_fiat_en_db(db, crypto_id, datos)
    
    return {"datos_api": datos, "estado_guardado": guardado_exitoso["mensaje"]}





"""
@app.get("/api/v1/cryptocurrencies/popular/monedas_fiat/popular/base_de_datos")
async def leerMonedasFiatConBD(db: Session = Depends(get_db)):
    fiats = traerTopMonedasFiat()
    if fiats is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los datos de las monedas fiat.",
        )
    return fiats
"""

"""@app.get("/api/v1/cryptocurrencies/popular/valores_fiat")
async def leerValoresFiat():
    from servicio_datos_cripto.services.valor_fiat_data_service import traerValoresCripto
    precios = traerValoresCripto()
    if precios is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los datos de los valores fiat.",
        )
    return precios"""

@app.post("/users/login", response_model=TokenSchema)
def Login(credenciales: LoginSchema, db: Session = Depends(get_db)):
    try:
        usuario_logeado = LoginUsuarioSeguro(db=db, credenciales=credenciales)
        if not usuario_logeado:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        access_token = create_access_token(data={"sub": str(usuario_logeado.id_usuario)})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
        

@app.post("/users/registrar", status_code=201)
def CrearUsuario(user_data: UsuarioCrear, db: Session = Depends(get_db)):
    try:
        response = RegistrarUsuario(db=db, datos_usuario=user_data)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@app.post("/verify-code", status_code=status.HTTP_200_OK)
def verificar_codigo(data: VerificacionCodigo, db: Session = Depends(get_db)):
    """
    Verifica un usuario con un código de 4 dígitos.
    """
    usuario = db.query(Usuario).filter(Usuario.correo == data.correo).first()
    
    # Check if user exists and the code matches
    if usuario is None or usuario.codigo_verificacion != data.codigo: # pyright: ignore[reportGeneralTypeIssues]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código o correo incorrecto.",
        )
    
    # Activate the user account
    usuario.is_verified = True # type: ignore
    usuario.is_active = True # type: ignore
    usuario.codigo_verificacion = None  # type: ignore # Clear the code after use
    db.commit()
    db.refresh(usuario)
    
    return {"mensaje": "Cuenta verificada exitosamente. Ahora puedes iniciar sesión."}



@app.put("/users/actualizar", response_model=UsuarioSchema, status_code=200)
def actualizar_usuario_endpoint(
    user_data: UsuarioActualizar, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) 
):
    try:
        updated_user = ActualizarUsuario(db=db, usuario_id=getattr(current_user, "id_usuario"), datos_usuario=user_data)
        return updated_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.put("/users/verify-update-email", status_code=200)
def verify_update_email(
    datos_verificacion: CorreoVerificarSchema,
    db: Session = Depends(get_db)
):

    usuario = db.query(Usuario).filter(
        Usuario.codigo_verificacion == datos_verificacion.codigo
    ).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Código de verificación inválido.")
  
    usuario.correo = datos_verificacion.nuevo_correo # type: ignore
    usuario.codigo_verificacion = None   # type: ignore
    db.commit()

    return {"mensaje": "Correo electrónico actualizado con éxito."}

@app.put("/users/request-update-email", status_code=200)
def request_update_email(
    
    correo_data: CorreoActualizarSchema,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):


    existing_user = db.query(Usuario).filter(Usuario.correo == correo_data.nuevo_correo).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado en otra cuenta.")

    verification_code = ''.join(random.choices(string.digits, k=6))

    current_user.codigo_verificacion = verification_code # type: ignore
    db.commit()


    email_sent = send_verification_email(correo_data.nuevo_correo, verification_code)

    if not email_sent:
        db.rollback()
        raise HTTPException(status_code=500, detail="No se pudo enviar el correo de verificación. Inténtalo de nuevo.")

    return {"mensaje": "Correo de verificación enviado. Revisa tu bandeja de entrada."}


@app.post("/users/actualizar-password", status_code=status.HTTP_200_OK)
def forgot_password(
    request: EmailRequest,
    db: Session = Depends(get_db)
):
    try:
        response = solicitarRestablecimientoDeCredencial(db, request.correo)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )
    
@app.post("/users/reset-password", status_code=status.HTTP_200_OK)
def reset_password(
    request: PasswordReset,
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:

        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
      
        raise credentials_exception
   
    usuario = db.query(Usuario).filter(Usuario.id_usuario == int(user_id)).first()
    if not usuario:
        raise credentials_exception
    contraseña_hasheada = hashContraseña(request.nueva_contraseña)
    
    usuario.contraseña = contraseña_hasheada # type: ignore
    db.commit()
    db.refresh(usuario)
    return {"mensaje": "Contraseña actualizada con éxito."}

@app.delete("/users/desactivar", status_code=200)
def desactivar_usuario_endpoint(
    credenciales: LoginSchema,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.nombre != credenciales.nombre: # type: ignore
        raise HTTPException(status_code=403, detail="No tienes permiso para realizar esta acción")

    try:
        DesactivarUsuario(db=db, credenciales=credenciales)
        return {"mensaje": "Cuenta desactivada con éxito."}
    except HTTPException as e:
        raise e
    
@app.post("/users/reactivar", status_code=200)
def reactivar_usuario_endpoint(
    credenciales: LoginSchema,
    db: Session = Depends(get_db)
):

    try:
        ReactivarUsuario(db=db, credenciales=credenciales)
        return {"mensaje": "Cuenta reactivada con éxito. Ya puedes iniciar sesión."}
    except HTTPException as e:
        raise e
    

@app.post("/guests/login", response_model=InvitadoResponse, status_code=201)
def crear_sesion_invitado_endpoint(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        ip_address = request.client.host # type: ignore
        user_agent = request.headers.get("user-agent")
        nuevo_invitado = crear_sesion_invitado(db, ip_address, user_agent) # type: ignore
        return nuevo_invitado
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    



@app.post("/guests/cleanup")
def limpiar_sesiones_inactivas_endpoint(db: Session = Depends(get_db)):
    try:
        resultado = actualizar_estado_sesiones_inactivas(db)
        return resultado
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")




"""
@app.get("/api/v1/cryptocurrencies/history/{crypto_id_api}")
def LeerValorHistorico(crypto_id: str, days: int):

    from servicio_datos_cripto.services.historical_crypto_data_services import LeerValorHistorico
    result = LeerValorHistorico(crypto_id, days)
    if result is None:
        raise HTTPException(status_code=500, detail="Error al cargar los datos históricos.")
    return result
"""


@app.get("/api/v1/cryptocurrencies/history/{crypto_id_api}/db")
def CargarHistoricoDesdeDb(crypto_id: str, days: int, db: Session = Depends(get_db)):
    from servicio_datos_cripto.services.historical_crypto_sync_services import ActualizarValorHistoricoConDb
    result = ActualizarValorHistoricoConDb(db, crypto_id, days)
    if result is None:
        raise HTTPException(status_code=500, detail="Error al cargar los datos históricos desde la base de datos.")
    return result

@app.post("/guests/interact", status_code=status.HTTP_201_CREATED)
def registrar_interaccion_invitado_endpoint(
    request: Request,
    id_cripto: int = None, # type: ignore
    id_moneda: int = None, # type: ignore
    db: Session = Depends(get_db)
):

    try:
        
        direccion_ip = request.client.host if request.client else None
        if not direccion_ip:
            raise HTTPException(status_code=400, detail="No se pudo obtener la dirección IP del cliente.")
        invitado = traerOCrearInvitado(db, direccion_ip)
        response = registrar_interaccion_invitado(
            db=db,
            id_invitado=invitado.id_invitado, # type: ignore
            id_cripto=id_cripto,
            id_moneda=id_moneda,
        )
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    

@app.get("/noticias/", response_model=list[dict])  # Puedes usar un Pydantic model para tipado
def read_all_news(db: Session = Depends(get_db)):
    """
    Endpoint que devuelve una lista de todas las noticias de la base de datos.
    """
    news_list = TraerNoticias(db)
    # Convertir los objetos de SQLAlchemy a diccionarios para que sean serializables
    return [{"id_noticias": n.id_noticias, "titulo": n.titulo, "url": n.url, "contenido": n.contenido} for n in news_list]


@app.post("/users/consultas", status_code=status.HTTP_201_CREATED)
def registrar_consulta(
    id_cripto: int,
    id_moneda: int,  
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    
    try:
        # Llama al servicio para registrar la consulta
        response = registrarConsultaUsuario(
            db=db,
            id_usuario=current_user.id_usuario, # type: ignore
            id_cripto=id_cripto,
            id_moneda=id_moneda 
        )
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor al registrar la consulta: {str(e)}"
        )
    


@app.get("/fetch_and_insert_news")
def trigger_news_update(db: Session = Depends(get_db)):
    """
    Endpoint que obtiene noticias de criptomonedas y las guarda en la base de datos.
    
    Este endpoint se encarga de:
    1. Conectar con la API de CryptoCompare.
    2. Procesar las noticias obtenidas.
    3. Insertar las noticias nuevas en la base de datos.
    """
    try:
        # Llamar a la función que ya creamos.
        # Le pasamos la sesión de la base de datos y el idioma.
        fetch_and_insert_news(db=db, lang='ES') 
        return {"message": "Las noticias se han actualizado correctamente."}
    except Exception as e:
        return {"error": f"Ocurrió un error al actualizar las noticias: {e}"}

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
