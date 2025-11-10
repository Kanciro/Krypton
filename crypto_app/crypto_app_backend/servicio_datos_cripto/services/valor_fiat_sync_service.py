import requests
import logging
from datetime import datetime
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from servicio_usuarios.database.db import get_db
from servicio_usuarios.models.modelo_criptomonedas import Criptomoneda
from servicio_usuarios.models.modelo_moneda_fiat import MonedaFiat
from servicio_usuarios.models.modelo_valor_historico import ValorHistorico
from servicio_usuarios.models.modelo_valor_fiat import ValorFiat
from servicio_datos_cripto.services.valor_fiat_data_service import obtener_precio_actual_por_cripto_y_fiats

# URLs y configuraci\u00f3n b\u00e1sica de logging
BASE_URL = "https://api.coingecko.com/api/v3/coins"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Lista de IDs de criptomonedas obtenidas de las im\u00e1genes
# Aseg\u00farate de que estos IDs son correctos para la API de CoinGecko
CRIPTOMONEDAS_IDS = [
    "bitcoin", "ethereum", "ripple", "tether", "binancecoin",
    "solana", "usd-coin", "staked-ether", "dogecoin", "tron",
    "cardano", "wrapped-steth", "chainlink", "wrapped-beacon-eth",
    "hyperliquid", "wrapped-bitcoin", "wrapped-eeth", "sui", "stellar",
    "ethena-usde", "figure-heloc", "avalanche-2", "bitcoin-cash", "weth",
    "hedera-hashgraph", "leo-token", "usds", "litecoin", "binance-bridged-usdt-bnb-smart-chain",
    "shiba-inu", "the-open-network", "crypto-com-chain", "coinbase-wrapped-btc",
    "polkadot", "whitebit", "ethena-staked-usde", "mantle", "world-liberty-financial",
    "monero", "usdt0"
]


def obtener_precio_actual_y_guardar_en_db(db: Session, crypto_id: str, monedas_fiat: List[str]) -> Dict[str, Any]:
    """
    Obtiene el precio actual de una criptomoneda y lo guarda en la base de datos
    como el valor más reciente.
    
    Args:
        db (Session): Sesión de la base de datos.
        crypto_id (str): El ID de la criptomoneda (ej. 'bitcoin').
        monedas_fiat (List[str]): Una lista de códigos de monedas objetivo (ej. ['usd', 'eur']).
    
    Returns:
        Dict[str, Any]: Un diccionario con el precio actual y el estado del guardado.
        
    Raises:
        HTTPException: Si la criptomoneda no es válida o hay un error.
    """
    # 1. Obtener el precio actual de la API (usa la función que ya tienes)
    datos_api = obtener_precio_actual_por_cripto_y_fiats(crypto_id, monedas_fiat)
    
    precios_actuales = datos_api.get(crypto_id, {})
    
    if not precios_actuales:
        raise HTTPException(
            status_code=404, 
            detail=f"No se pudieron obtener datos de precio para {crypto_id} en las monedas especificadas."
        )

    # 2. Configuración de fecha y hora para el guardado
    ahora = datetime.now()
    fecha_dt = ahora.date() # Solo la fecha (para ValorHistorico)
    
    try:
        # **Asegúrate de que tus modelos (Criptomoneda, MonedaFiat, ValorHistorico, ValorFiat)
        # están disponibles en este contexto (importados).**
        
        # Obtener los objetos de la DB para la cripto
        # Aquí se asume que 'Criptomoneda' y 'MonedaFiat' están mapeadas en la DB
        cripto_db = db.query(Criptomoneda).filter(Criptomoneda.id_api == crypto_id).first()
        if not cripto_db:
            raise ValueError(f"Criptomoneda con ID de API {crypto_id} no encontrada en la DB.")

        # Mapear acrónimo (ej. 'usd') a ID de moneda de la DB
        moneda_fiat_map = {m.coi.lower(): m.id_moneda for m in db.query(MonedaFiat).all()}
        
        # 3. Guardar o actualizar ValorHistorico (por fecha)
        # El precio principal será el de la primera moneda fiat de la lista (o USD si está presente)
        moneda_principal_acronimo = monedas_fiat[0].lower() 
        precio_principal = precios_actuales.get(moneda_principal_acronimo, list(precios_actuales.values())[0])

        valor_historico_db = db.query(ValorHistorico).filter(
            ValorHistorico.id_cripto == cripto_db.id_cripto,
            ValorHistorico.fecha == fecha_dt
        ).first()

        if not valor_historico_db:
            # Crea un nuevo registro de ValorHistorico para hoy
            valor_historico_db = ValorHistorico(
                id_cripto=cripto_db.id_cripto,
                valor=str(precio_principal), # Se usa el precio principal para el valor principal
                fecha=fecha_dt
            )
            db.add(valor_historico_db)
            db.flush() # Para obtener el ID del nuevo objeto
            logger.info(f"Creado nuevo ValorHistorico para {crypto_id} en la fecha {fecha_dt}.")
        # Si ya existe, se mantiene el registro existente o se actualiza si fuera necesario

        # 4. Guardar o actualizar ValorFiat (para cada moneda vs la cripto)
        registros_actualizados = 0
        for moneda_target_acronimo, precio in precios_actuales.items():
            moneda_target_lower = moneda_target_acronimo.lower()
            if moneda_target_lower in moneda_fiat_map:
                id_moneda_fiat = moneda_fiat_map[moneda_target_lower]
                
                # Buscar ValorFiat para esta cripto, moneda y ValorHistorico
                existe_valor_fiat = db.query(ValorFiat).filter(
                    ValorFiat.id_moneda == id_moneda_fiat,
                    ValorFiat.id_valor_historico == valor_historico_db.id_valor_historico
                ).first()

                if not existe_valor_fiat:
                    # Insertar un nuevo ValorFiat
                    nuevo_valor_fiat = ValorFiat(
                        id_moneda=id_moneda_fiat,
                        id_valor_historico=valor_historico_db.id_valor_historico,
                        valor=str(precio),
                        fecha=fecha_dt,
                        hora=ahora # Usa la hora completa del momento
                    )
                    db.add(nuevo_valor_fiat)
                    registros_actualizados += 1
                    logger.info(f"Guardando nuevo ValorFiat para {crypto_id} en {moneda_target_acronimo} ({precio}).")
                else:
                    # Si ya existe, se puede optar por actualizar el 'valor' y la 'hora'
                    # para reflejar el precio actual más reciente.
                    if str(existe_valor_fiat.valor) != str(precio):
                        existe_valor_fiat.valor = str(precio)
                        existe_valor_fiat.hora = ahora
                        registros_actualizados += 1
                        logger.info(f"Actualizando ValorFiat para {crypto_id} en {moneda_target_acronimo} a {precio}.")
                    else:
                        logger.info(f"El valor de {crypto_id} en {moneda_target_acronimo} no ha cambiado. Se omite la actualización.")

        db.commit()
        return {
            "mensaje": f"Precio actual de {crypto_id} obtenido y {registros_actualizados} registro(s) guardado(s)/actualizado(s) exitosamente.",
            "precio_actual": precios_actuales
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error al guardar los datos del precio actual: {e}")
        # Re-lanza como HTTPException
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar los datos del precio actual: {str(e)}",
        )
    

def obtener_valor_actual_fiat_desde_db(
    db: Session, 
    crypto_id_api: str, 
    monedas_fiat: List[str]
) -> Dict[str, Any]:
    """
    Consulta el valor más reciente ("actual") de una criptomoneda 
    en relación a las monedas fiat, directamente desde la DB.
    
    Args:
        db (Session): Sesión de la base de datos.
        crypto_id_api (str): El ID de la criptomoneda (ej. 'bitcoin').
        monedas_fiat (List[str]): Una lista de códigos de monedas objetivo (ej. ['usd', 'eur']).
        
    Returns:
        Dict[str, Any]: Un diccionario con el valor actual.
    """
    
    # 1. Obtener el ID interno de la criptomoneda
    cripto_db = db.query(Criptomoneda).filter(Criptomoneda.id_api == crypto_id_api.lower()).first()
    if not cripto_db:
        raise HTTPException(status_code=404, detail=f"Criptomoneda '{crypto_id_api}' no encontrada en la base de datos.")

    id_cripto = cripto_db.id_cripto
    resultados = {crypto_id_api: {}}
    
    # 2. Iterar sobre cada moneda fiat solicitada
    for acronimo_fiat in monedas_fiat:
        acronimo_fiat_lower = acronimo_fiat.lower()
        
        # 2a. Obtener el ID interno de la moneda fiat
        moneda_fiat_db = db.query(MonedaFiat).filter(MonedaFiat.coi == acronimo_fiat_lower).first()
        if not moneda_fiat_db:
            logger.warning(f"Moneda fiat '{acronimo_fiat}' no encontrada en la base de datos. Omitiendo.")
            continue

        id_moneda_fiat = moneda_fiat_db.id_moneda
        
        # 2b. Consultar los datos en ValorHistorico y ValorFiat, LIMITADO A 1
        consulta = (
            db.query(ValorFiat)
            .join(ValorHistorico, ValorFiat.id_valor_historico == ValorHistorico.id_valor_historico)
            .filter(
                ValorHistorico.id_cripto == id_cripto,
                ValorFiat.id_moneda == id_moneda_fiat
            )
            .order_by(desc(ValorFiat.fecha), desc(ValorFiat.hora))
            .limit(1)  # <<--- Aquí está la clave: siempre se limita a 1
            .first()   # <<--- Usamos .first() para obtener el objeto en lugar de una lista
        )
        
        # 3. Formatear el resultado
        if consulta:
            resultados[crypto_id_api][acronimo_fiat] = {
                "valor": float(consulta.valor),
                "fecha": consulta.fecha.strftime("%Y-%m-%d"),
                "hora": consulta.hora.strftime("%H:%M:%S")
            }
        else:
             resultados[crypto_id_api][acronimo_fiat] = None

    return resultados