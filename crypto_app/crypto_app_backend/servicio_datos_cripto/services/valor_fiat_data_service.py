import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

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

app = FastAPI()

async def obtener_valores_historicos_por_cripto_y_fiats(crypto_id: str, monedas_fiat: List[str], dias: int) -> Dict[str, Any]:
    """
    Obtiene los valores hist\u00f3ricos de una criptomoneda en relaci\u00f3n a una lista de monedas fiat.
    
    Args:
        crypto_id (str): El ID de la criptomoneda (ej. 'bitcoin').
        monedas_fiat (List[str]): Una lista de c\u00f3digos de monedas objetivo (ej. ['usd', 'eur']).
        dias (int): El n\u00famero de d\u00edas de datos hist\u00f3ricos a obtener.
    
    Returns:
        Dict[str, Any]: Un diccionario con los datos formateados.
    """
    if crypto_id not in CRIPTOMONEDAS_IDS:
        raise HTTPException(status_code=404, detail="La criptomoneda no es v\u00e1lida o no se encuentra en la lista.")
    
    datos_historicos_completos = {crypto_id: {}}
    
    for moneda_target in monedas_fiat:
        url = f"{BASE_URL}/{crypto_id}/market_chart"
        params = {
            "vs_currency": moneda_target,
            "days": dias
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "prices" in data:
                # Si es la primera moneda fiat, inicializamos la estructura
                if moneda_target == monedas_fiat[0]:
                    datos_historicos_completos[crypto_id] = {
                        "monedas": {},
                        "fechas": []
                    }
                    for timestamp, _ in data["prices"]:
                        fecha = datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d")
                        datos_historicos_completos[crypto_id]["fechas"].append(fecha)

                # Guardamos los precios para la moneda actual
                precios_actuales = [precio for _, precio in data["prices"]]
                datos_historicos_completos[crypto_id]["monedas"][moneda_target] = precios_actuales
                
                logger.info(f"Datos obtenidos para {crypto_id} en {moneda_target} para {dias} d\u00edas.")
            else:
                logger.warning(f"No se encontraron datos de precios para {crypto_id} en {moneda_target}.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener datos hist\u00f3ricos: {e}")
            continue
            
    return datos_historicos_completos
