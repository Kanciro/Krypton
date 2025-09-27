# MODULO WEBSOCKET CONEXION
# test_smoke_existing_user.py
import pytest
import requests
import asyncio
import json
import websockets

@pytest.mark.asyncio
async def test_websocket_conexion():
    """Prueba que la conexión WebSocket se establece y recibe datos."""
    uri = f"ws://25.56.145.23:8000/ws/cryptocurrencies"
    try:
        async with websockets.connect(uri, ping_interval=None) as websocket:
            message = await asyncio.wait_for(websocket.recv(), timeout=10)
            data = json.loads(message)
            assert isinstance(data, list) and len(data) > 0, "No se recibieron datos válidos por WebSocket"
    except (websockets.exceptions.ConnectionClosedError, asyncio.TimeoutError) as e:
        pytest.fail(f"Falló la conexión WebSocket: {e}")