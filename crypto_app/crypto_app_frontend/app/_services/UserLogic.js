import { useState, useEffect, useRef } from 'react'; 
import { router } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Alert } from 'react-native';

export function UserLogic() {
  const [nombreUsuario, setNombreUsuario] = useState('');
  const [formData, setFormData] = useState({
    nombre: '',
    correo: '',
    fecha_nacimiento: '',
    contrasena: '',
    nueva_contrasena: '',
    token: '',
    nuevo_correo: '',
    codigo: '',
  });
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const bottomSheetRef = useRef(null); // Referencia para controlar el MenuModal

  // URL base de la API, obtenida de app.json
  const API_URL = 'http://25.56.145.23:8000';

  useEffect(() => {
    const obtenerNombreUsuario = async () => {
      try {
        const nombreGuardado = await AsyncStorage.getItem('nombre_usuario');
        const isGuest = await AsyncStorage.getItem('guest_token');

        if (nombreGuardado || isGuest) { // Permite la navegación si es invitado o usuario registrado
          setNombreUsuario(nombreGuardado || 'Invitado'); // Muestra 'Invitado' si no hay nombre de usuario registrado
        } else {
          // Si no hay tokens, redirige al login inmediatamente
          router.replace('/screens/login');
        }
      } catch (error) {
        console.error("Error al obtener el nombre de usuario", error);
        router.replace('/screens/login');
      }
    };
    obtenerNombreUsuario();
  }, []);

  const handleChange = (name, value) => {
    setFormData({ ...formData, [name]: value });
  };

  // Función para manejar todas las llamadas a la API
  const handleFetch = async (endpoint, method, body) => {
    setIsLoading(true);
    setMessage('Procesando...');
    try {
      const accessToken = await AsyncStorage.getItem('access_token');
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify(body),
      });

    const data = await response.json();

      if (response.ok) {
        setMessage(data.mensaje || 'Acción completada con éxito.');
        Alert.alert('Éxito', data.mensaje || 'Acción completada con éxito.');
      } else {
        setMessage(data.detalle || 'Ocurrió un error. Inténtalo de nuevo.');
        Alert.alert('Error', data.detalle || 'Ocurrió un error.');
      }
    } catch (error) {
      console.error("Error en la petición:", error);
      setMessage('Error de conexión con el servidor.');
      Alert.alert('Error', 'Error de conexión con el servidor.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdateUser = () => {
    handleFetch('/users/actualizar', 'PUT', {
      nombre: formData.nombre,
      correo: formData.correo,
      fecha_nacimiento: formData.fecha_nacimiento,
      contrasena: formData.contrasena,
    });
  };

  const handleRequestUpdateEmail = () => {
    handleFetch('/users/request-update-email', 'POST', { nuevo_correo: formData.nuevo_correo });
  };

  const handleVerifyUpdateEmail = () => {
    handleFetch('/users/verify-update-email', 'POST', { codigo: formData.codigo, nuevo_correo: formData.nuevo_correo });
  };

  const handleActualizarPassword = () => {
    handleFetch('/users/actualizar-password', 'POST', { correo: formData.correo });
  };

  const handleResetPassword = () => {
    handleFetch('/users/reset-password', 'POST', { token: formData.token, nueva_contrasena: formData.nueva_contrasena });
  };

  const handleDesactivarUsuario = () => {
    handleFetch('/users/desactivar', 'POST', { nombre: formData.nombre, contrasena: formData.contrasena });
  };

  const handleReactivarUsuario = () => {
    handleFetch('/users/reactivar', 'POST', { nombre: formData.nombre, contrasena: formData.contrasena });
  };

  // FIX PRINCIPAL: Función de logout mejorada para borrar tokens de usuario e invitado.
  const handleLogout = async () => {
    Alert.alert(
      "Cerrar Sesión",
      "¿Estás seguro de que deseas cerrar tu sesión?",
      [
        {
          text: "Cancelar",
          style: "cancel"
        },
        {
          text: "Sí",
          onPress: async () => {
            try {
              // Limpiar los tokens de autenticación (usuario y invitado)
              await AsyncStorage.removeItem('access_token');
              await AsyncStorage.removeItem('nombre_usuario');
              await AsyncStorage.removeItem('guest_token'); // <--- FIX INVITADO

              // Redirigir al usuario a la pantalla de login.
              router.replace('/screens/login');
            } catch (error) {
              console.error("Error al cerrar sesión", error);
              Alert.alert('Error', 'Hubo un problema al cerrar la sesión.');
            }
          }
        }
      ],
      { cancelable: false }
    );
  };

  const handleOpenMenu = () => {
    bottomSheetRef.current?.expand();
  };

  return {
    nombreUsuario,
    formData,
    handleChange,
    handleUpdateUser,
    handleRequestUpdateEmail,
    handleVerifyUpdateEmail,
    handleActualizarPassword,
    handleResetPassword,
    handleDesactivarUsuario,
    handleReactivarUsuario,
    handleLogout,
    message,
    isLoading,
    bottomSheetRef,
    handleOpenMenu,
  };
}