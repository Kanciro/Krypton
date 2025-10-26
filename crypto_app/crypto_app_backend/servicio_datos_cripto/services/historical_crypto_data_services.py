import datetime
import requests
import logging
import json

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def LeerValorHistorico(crypto_id_api: str, days: int):

    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id_api}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "precision": 8  # Opcional: precisión de los precios a dos decimales
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        prices = data.get("prices", [])
        
        # Lista para almacenar los datos formateados
        formatted_prices = []
        
        # Iteramos sobre la lista de precios que contiene la marca de tiempo y el valor
        for timestamp_ms, price in prices:
            # Convertimos los milisegundos a segundos (dividiendo por 1000)
            timestamp_s = timestamp_ms / 1000
            
            # Usamos datetime para convertir la marca de tiempo a un objeto de fecha y hora
            date_time_obj = datetime.datetime.fromtimestamp(timestamp_s)
            
            # Formateamos la fecha y hora a un string más legible
            formatted_date = date_time_obj.strftime("%Y-%m-%d %H:%M:%S")
            
            formatted_prices.append({
                "date": formatted_date,
                "price_usd": price
            })
            
        return formatted_prices

    except requests.exceptions.RequestException as e:
        logging.error(f"Error al obtener historial para {crypto_id_api} desde la API: {e}")
        return None

if __name__ == "__main__":
    print("Obteniendo el valor histórico de Bitcoin y convirtiendo a fechas...")
    crypto_id = "chainlink "
    days = 365 # Obtiene los datos de los últimos 7 días
    
    historical_data = LeerValorHistorico(crypto_id, days)

    if historical_data:
        print(json.dumps(historical_data, indent=2))
    else:
        print(f"No se pudieron obtener los datos históricos para {crypto_id}.")
