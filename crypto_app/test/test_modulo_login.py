
# test_smoke_existing_user.py
import pytest
import requests
import asyncio
import json
import websockets

API_URL = "http://25.56.145.23:8000"
#MODULO ENDPOINT PROTEGIDO

USUARIO_EXISTENTE = {
    "nombre": "Juan",
    "contraseña": "Ac123456.."
} 


@pytest.fixture(scope="session")
def auth_token_existente():
    """Fixture que usa un usuario existente para obtener un token de autenticación."""
    login_data = {
        "nombre": USUARIO_EXISTENTE["nombre"],
        "contraseña": USUARIO_EXISTENTE["contraseña"]
    }
    response = requests.post(f"{API_URL}/users/login", json=login_data)
    response.raise_for_status()
    token = response.json().get("access_token")
    assert token, "No se pudo obtener el token de autenticación del usuario existente"
    return token
@pytest.mark.usefixtures("auth_token_existente")
def test_autenticacion_endpoint(auth_token_existente):
    """Prueba que un endpoint protegido es accesible con un token válido del usuario existente."""
    headers = {"Authorization": f"Bearer {auth_token_existente}"}
    params = {"id_cripto": 1, "id_moneda": 1}
    response = requests.post(f"{API_URL}/users/consultas", params=params, headers=headers)
    assert response.status_code == 201, f"El endpoint protegido no devolvió un 201. Status: {response.status_code}, Detalle: {response.text}"
