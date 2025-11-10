import requests
import logging
from typing import List, Dict, Any

from fastapi import HTTPException

# URLs y configuración básica
BASE_URL = "https://api.coingecko.com/api/v3" 
logger = logging.getLogger(__name__)

# Lista de IDs de criptomonedas obtenidas de las imágenes
# Asegúrate de que estos IDs son correctos para la API de CoinGecko
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

def obtener_precio_actual_por_cripto_y_fiats(crypto_id: str, monedas_fiat: List[str]) -> Dict[str, Any]:
    """
    Obtiene el precio actual de una criptomoneda en relación a una lista de monedas fiat
    utilizando el endpoint /simple/price.
    
    Args:
        crypto_id (str): El ID de la criptomoneda (ej. 'bitcoin').
        monedas_fiat (List[str]): Una lista de códigos de monedas objetivo (ej. ['usd', 'eur']).
    
    Returns:
        Dict[str, Any]: Un diccionario con el precio actual.
                        Ejemplo: {"bitcoin": {"usd": 65000.50, "eur": 60000.25}}
    
    Raises:
        HTTPException: Si la criptomoneda no está permitida o hay un error en la conexión.
    """
    # 1. Validación de ID
    if crypto_id not in CRIPTOMONEDAS_IDS:
        raise HTTPException(status_code=404, detail="La criptomoneda no es válida o no se encuentra en la lista de IDs permitidos.")
    
    # 2. Construcción de la URL y Parámetros
    url = f"{BASE_URL}/simple/price"
    params = {
        "ids": crypto_id,
        "vs_currencies": ",".join(monedas_fiat)
    }

    # 3. Llamada a la API de CoinGecko
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Lanza excepción para errores HTTP
        data = response.json()

        if crypto_id in data:
            logger.info(f"Precio actual obtenido para {crypto_id} en {', '.join(monedas_fiat)}.")
            return {crypto_id: data[crypto_id]}
        else:
            logger.warning(f"No se encontraron datos de precio para {crypto_id}. La API devolvió: {data}")
            return {crypto_id: {}}

    except requests.exceptions.RequestException as e:
        logger.error(f"Error al obtener el precio actual desde CoinGecko: {e}")
        # Re-lanza como HTTPException
        raise HTTPException(status_code=503, detail=f"Error de conexión o API: No se pudo obtener el precio de CoinGecko. Detalle: {e}")
