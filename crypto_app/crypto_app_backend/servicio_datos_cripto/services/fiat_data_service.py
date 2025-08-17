import requests

def traerTopMonedasFiat():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        
        # Diccionario para mapear los símbolos de las monedas fiat a sus nombres
        fiat_names = {
            "usd": "Dólar estadounidense",
            "eur": "Euro",
            "gbp": "Libra esterlina",
            "jpy": "Yen japonés",
            "cad": "Dólar canadiense",
            "aud": "Dólar australiano",
            "chf": "Franco suizo",
            "cny": "Yuan chino",
            "inr": "Rupia india",
            "brl": "Real brasileño",
            "rub": "Rublo ruso",
            "mxn": "Peso mexicano",
            "sgd": "Dólar de Singapur",
            "hkd": "Dólar de Hong Kong",
            "nzd": "Dólar neozelandés",
            "sek": "Corona sueca",
            "nok": "Corona noruega", 
            "dkk": "Corona danesa",
            "zar": "Rand sudafricano",
            "try": "Lira turca", 
            "krw": "Won surcoreano",
            "idr": "Rupia indonesia",
            "pln": "Zloty polaco",
            "thb": "Baht tailandés",
            "myr": "Ringgit malayo",
            "php": "Peso filipino",
            "clp": "Peso chileno",
            "cop": "Peso colombiano",
            "ars": "Peso argentino",
            "egp": "Libra egipcia",
            "ils": "Nuevo shekel israelí",
            "aed": "Dírham de los Emiratos Árabes Unidos",
            "sar": "Riyal saudí",
            "qar": "Riyal qatarí",
            "kwd": "Dinar kuwaití",
            "bhd": "Dinar bahreín",
            "omr": "Rial omaní",
            "pkr": "Rupia pakistaní",
            "bdt": "Taka de Bangladesh",
            "npr": "Rupia nepalí"
        }

        vs_currencies_str = ",".join(fiat_names.keys())

        params = {
            "ids": "bitcoin,ethereum",
            "vs_currencies": vs_currencies_str
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Devuelve tanto los datos de precios como el diccionario de nombres
        return data, fiat_names

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de CoinGecko: {e}")
        return None, None

if __name__ == "__main__":
    print("Obteniendo precios de criptomonedas en múltiples monedas fiat...")
    precios, fiat_names = traerTopMonedasFiat()
    if precios and fiat_names:
        print("Precios obtenidos:")
        for crypto, valor in precios.items():
            print(f"\nCriptomoneda: {crypto.capitalize()}")
            for fiat_symbol, precio in valor.items():
                fiat_name = fiat_names.get(fiat_symbol, "Nombre Desconocido")
                print(f"  Símbolo: {fiat_symbol.upper()}, Nombre: {fiat_name}, Precio: {precio}")
    else:
        print("No se pudieron obtener los precios.")
