from unittest.mock import Mock
from datetime import date
import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException

# Asegúrate de importar tu función y esquemas
from crypto_app.crypto_app_backend.servicio_usuarios.services.user_data_services import (
    RegistrarUsuario,
)
from crypto_app.crypto_app_backend.servicio_usuarios.schemas.schema_users import (
    UsuarioCrear,
    UsuarioSchema,
)


# Simula la base de datos
@pytest.fixture
def mock_db_session(mocker):
    session = Mock(spec=Session)
    return session


def test_registrar_usuario_exitoso(mock_db_session):
    """Prueba que un usuario se registre correctamente."""
    # Prepara los datos del usuario de prueba
    datos_prueba = UsuarioCrear(
        nombre="Prueba Test",
        correo="prueba@test.com",
        fecha_nacimiento=date(1990, 1, 1),
        contraseña="password123",
    )

    # Simula el comportamiento de la base de datos
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

    # Llama a la función que quieres probar
    usuario_registrado = RegistrarUsuario(mock_db_session, datos_prueba)

    # Afirma que el usuario se ha creado y devuelto correctamente
    assert usuario_registrado.nombre == datos_prueba.nombre
    assert usuario_registrado.correo == datos_prueba.correo
    assert usuario_registrado.id_usuario is not None
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
