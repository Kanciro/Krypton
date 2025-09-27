import requests
import logging
from datetime import datetime
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from servicio_usuarios.database.db import get_db
from servicio_usuarios.models.modelo_criptomonedas import Criptomoneda
from servicio_usuarios.models.modelo_moneda_fiat import MonedaFiat
from servicio_usuarios.models.modelo_valor_historico import ValorHistorico
from servicio_usuarios.models.modelo_valor_fiat import ValorFiat

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


def guardar_valores_fiat_en_db(db: Session, crypto_id_api: str, datos_historicos: Dict[str, Any]):
    """
    Guarda los datos hist\u00f3ricos de una criptomoneda en la tabla de valores fiat.
    """
    try:
        # Obtener los objetos de la DB para las criptos y monedas fiat
        cripto_db = db.query(Criptomoneda).filter(Criptomoneda.id_api == crypto_id_api).first()
        if not cripto_db:
            raise ValueError(f"Criptomoneda con ID de API {crypto_id_api} no encontrada.")

        # Corregido: Usar 'acronimo' en lugar de 'codigo'
        moneda_fiat_map = {m.coi.lower(): m.id_moneda for m in db.query(MonedaFiat).all()}

        cripto_datos = datos_historicos.get(crypto_id_api)
        if not cripto_datos:
            logger.error(f"No se encontraron datos hist\u00f3ricos para {crypto_id_api}.")
            return {"mensaje": "No se encontraron datos hist\u00f3ricos para guardar."}

        fechas = cripto_datos.get("fechas", [])
        monedas = cripto_datos.get("monedas", {})

        for moneda_target, precios in monedas.items():
            moneda_target_lower = moneda_target.lower()
            if moneda_target_lower in moneda_fiat_map:
                id_moneda_fiat = moneda_fiat_map[moneda_target_lower]
                
                # Crear un solo ValorHistorico por d\u00eda
                for i in range(len(fechas)):
                    fecha_str = fechas[i]
                    precio_str = str(precios[i])
                    fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d")

                    # Verificar si el ValorHistorico ya existe para la cripto y la fecha
                    valor_historico_db = db.query(ValorHistorico).filter(
                        ValorHistorico.id_cripto == cripto_db.id_cripto,
                        ValorHistorico.fecha == fecha_dt
                    ).first()

                    if not valor_historico_db:
                        valor_historico_db = ValorHistorico(
                            id_cripto=cripto_db.id_cripto,
                            valor=precio_str, # Nota: Aqu\u00ed podr\u00edas decidir qu\u00e9 moneda fiat usar para este valor principal
                            fecha=fecha_dt
                        )
                        db.add(valor_historico_db)
                        db.flush() # Para obtener el ID del nuevo objeto

                    # Ahora, verificar si el ValorFiat ya existe
                    existe_valor_fiat = db.query(ValorFiat).filter(
                        ValorFiat.id_moneda == id_moneda_fiat,
                        ValorFiat.id_valor_historico == valor_historico_db.id_valor_historico
                    ).first()

                    if not existe_valor_fiat:
                        nuevo_valor_fiat = ValorFiat(
                            id_moneda=id_moneda_fiat,
                            id_valor_historico=valor_historico_db.id_valor_historico,
                            valor=precio_str,
                            fecha=fecha_dt,
                            hora=datetime.now()
                        )
                        db.add(nuevo_valor_fiat)
                        logger.info(f"Guardando valor para {crypto_id_api} en {moneda_target} ({precio_str}) para la fecha {fecha_str}.")
                    else:
                        logger.info(f"El valor ya existe para {crypto_id_api} en {moneda_target} en la fecha {fecha_str}. Se omite.")
        
        db.commit()
        logger.info("Datos guardados exitosamente en la tabla de valores fiat.")
        return {"mensaje": "Datos guardados exitosamente."}
    except Exception as e:
        db.rollback()
        logger.error(f"Error al guardar los datos en la tabla de valores fiat: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar los datos: {str(e)}",
        )
    
