import requests


def traerValoresfiat():
    try:

        url = "https://api.coingecko.com/api/v3/simple/price"

        fiat_currencies = [
            "usd",
            "cop",
            "eur",
            "jpy",
            "gbp",
            "aud",
            "cad",
            "chf",
            "cny",
            "hkd",
            "nzd",
            "sgd",
            "inr",
            "rub",
            "brl",
            "ars",
            "mxn",
            "clp",
            "per",
            "krw",
        ]

        vs_currencies_str = ",".join(fiat_currencies)

        params = {"ids": "bitcoin,ethereum", "vs_currencies": vs_currencies_str}

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return data

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de CoinGecko: {e}")
        return None


if __name__ == "__main__":
    print("Obteniendo precios de criptomonedas en múltiples monedas fiat...")
    precios = traerValoresfiat()
    if precios:
        print("Precios obtenidos:")
        for crypto, valor in precios.items():
            print(f"\nCriptomoneda: {crypto.capitalize()}")
            for fiat, precio in valor.items():
                print(f"  Precio en {fiat.upper()}: {precio}")
    else:
        print("No se pudieron obtener los precios.")
