# test_smoke_existing_user.py
import pytest
import requests
import asyncio
import json
import websockets

# URL base de tu API
API_URL = "http://25.56.145.23:8000"


# MODULO API Y CRYPTOS
def test_api_is_activa():
    """Prueba que el endpoint simple de criptomonedas responde correctamente."""
    response = requests.get(f"{API_URL}/cryptos/todas")
    assert response.status_code == 200, "El endpoint /cryptos/todas no devolvió un 200 OK"
    data = response.json()
    assert isinstance(data, list) and len(data) > 0, "No se recibieron datos de criptomonedas válidos"