import requests
import logging
from datetime import datetime, timedelta

# TODO: Reemplaza con tu clave de API de ExchangeRate-API
API_KEY = "2c9506b4f77d85a2233fce27"
BASE_URL = "https://open.er-api.com/v6/historical"

# Configuración b\u00e1sica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def obtener_valores_fiat_historicos(moneda_base: str, moneda_target: str, dias: int) -> list:
    """
    Obtiene los valores hist\u00f3ricos de una moneda fiat en relaci\u00f3n a otra desde la API.

    Args:
        moneda_base (str): El c\u00f3digo de la moneda base (ej. 'USD').
        moneda_target (str): El c\u00f3digo de la moneda objetivo (ej. 'COP').
        dias (int): El n\u00famero de d\u00edas de datos hist\u00f3ricos a obtener.

    Returns:
        list: Una lista de diccionarios con los valores formateados, o una lista vac\u00eda si hay un error.
    """
    fechas_a_obtener = []
    fecha_fin = datetime.now().date()
    for i in range(dias + 1):
        fechas_a_obtener.append(fecha_fin - timedelta(days=i))
    
    # Invertimos la lista para obtener los datos en orden cronol\u00f3gico (de m\u00e1s antiguo a m\u00e1s reciente)
    fechas_a_obtener.reverse()

    datos_fiat = []

    for fecha in fechas_a_obtener:
        fecha_str = fecha.strftime("%Y-%m-%d")
        url = f"{BASE_URL}/{fecha_str}/{moneda_base}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data.get("result") == "success" and data["rates"].get(moneda_target):
                valor_cambio = data["rates"][moneda_target]
                
                # Preparamos el diccionario con los datos necesarios para la tabla valor_fiat
                datos_fiat.append({
                    "fecha": fecha_str,
                    "valor": str(valor_cambio), # Se guarda como string para coincidir con el modelo de DB
                    "moneda_target": moneda_target
                })
                logger.info(f"Datos obtenidos para {moneda_base}/{moneda_target} en la fecha {fecha_str}.")
            else:
                logger.warning(f"No se encontraron datos para {moneda_target} en la fecha {fecha_str}.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener datos hist\u00f3ricos para {fecha_str}: {e}")
            continue # Continuamos con la siguiente fecha incluso si una falla

    return datos_fiat

if __name__ == "__main__":
    logger.info("Iniciando la prueba del servicio de datos fiat...")
    
    moneda_base = "USD"
    moneda_target = "COP" # O cualquier otra moneda que desees probar
    dias = 7 
    
    datos_historicos = obtener_valores_fiat_historicos(moneda_base, moneda_target, dias)
    
    if datos_historicos:
        logger.info(f"Se obtuvieron {len(datos_historicos)} registros.")
        for dato in datos_historicos:
            print(f"Fecha: {dato['fecha']}, Valor: {dato['valor']} {moneda_target}")
    else:
        logger.warning("No se obtuvieron datos hist\u00f3ricos. Revisa la conexi\u00f3n o tu API Key.")
