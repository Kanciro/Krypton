# crypto_data_service_gratuito.py
import requests
from typing import List
from fastapi import HTTPException
from servicio_usuarios.models.modelo_criptomonedas import Criptomoneda
from sqlalchemy.orm import Session
def traerTopCriptomonedas():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"

        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 20,
            "page": 1,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        if not isinstance(data, list):
            print("Respuesta inesperada de la API. Se esperaba una lista.")
            return None

        crypto_list = []
        for crypto in data:
            crypto_list.append(
                {
                    "id": crypto["id"],
                    "symbol": crypto["symbol"].upper(),
                    "name": crypto["name"],
                    "current_price": crypto["current_price"],
                    "market_cap": crypto["market_cap"],
                }
            )

        return crypto_list

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de CoinGecko: {e}")
        return None


if __name__ == "__main__":
    print("Obteniendo datos de la API gratuita de CoinGecko...")
    cryptos = traerTopCriptomonedas()
    if cryptos:
        for crypto in cryptos:
            print(
                f"Nombre: {crypto['name']}, Símbolo: {crypto['symbol']}, Precio: ${crypto['current_price']}"
            )
    else:
        print("No se pudieron obtener los datos de las criptomonedas.")

def traerCriptomonedas(db: Session) -> List[Criptomoneda]:
    
    try:
        criptos = db.query(Criptomoneda).all()
        if not criptos:
            raise HTTPException(status_code=404, detail="No se encontraron criptomonedas.")
        return criptos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las criptomonedas: {str(e)}")