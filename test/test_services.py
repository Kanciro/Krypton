from unittest.mock import Mock
from datetime import date
import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydantic import ValidationError

# Asegúrate de importar tus clases correctamente
from crypto_app.crypto_app_backend.servicio_usuarios.services.user_data_services import RegistrarUsuario
from crypto_app.crypto_app_backend.servicio_usuarios.schemas.schema_users import UsuarioCrear
from crypto_app.crypto_app_backend.servicio_usuarios.models.modelo_usuario import Usuario as UsuarioDBModel # Importa tu modelo de DB
from crypto_app.crypto_app_backend.servicio_usuarios.schemas.schema_users import UsuarioSchema # Importa tu esquema de respuesta

# Simula la base de datos
@pytest.fixture
def mock_db_session(mocker):
    # Crea un mock de la sesión de la base de datos
    session = Mock(spec=Session)
    
    # Simula el comportamiento de la base de datos para la consulta de usuarios
    session.query.return_value.filter_by.return_value.first.return_value = None
    
    # Simula el refresh. Esto es lo nuevo.
    # Cuando se llama a db.refresh(), se actualiza el objeto con el ID
    def mock_refresh(instance):
        instance.id_usuario = 1  # Simula un ID asignado por la BD
        instance.notificaciones = True # Simula el valor por defecto
    
    session.refresh = mock_refresh
    
    return session

def test_registrar_usuario_exitoso(mock_db_session):
    """Prueba que un usuario se registre correctamente."""
    datos_prueba = UsuarioCrear(
        nombre="Prueba Test",
        correo="prueba@test.com",
        fecha_nacimiento=date(1990, 1, 1),
        contraseña="password123"
    )

    # Llama a la función que quieres probar
    usuario_registrado = RegistrarUsuario(mock_db_session, datos_prueba)

    # Afirma que el usuario se ha creado y devuelto correctamente
    assert usuario_registrado.id_usuario == 1 # Ahora se espera un ID válido
    assert usuario_registrado.notificaciones == True # Ahora se espera un valor válido
    assert usuario_registrado.nombre == datos_prueba.nombre
    assert mock_db_session.add.assert_called_once()
    assert mock_db_session.commit.assert_called_once()
    
# Si la prueba pasa, ¡lo lograste! Ahora tu prueba es robusta y simula completamente el flujo.