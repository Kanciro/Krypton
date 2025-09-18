import { useState, useRef } from 'react';
import { Alert } from 'react-native';
import { router } from 'expo-router';
// Importa AsyncStorage si lo vas a usar para guardar los datos del usuario
import AsyncStorage from '@react-native-async-storage/async-storage'; 

export function useLogin() {
  const [usuario, setUsuario] = useState('');
  const [contrasena, setContrasena] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const bottomSheetRef = useRef(null);
  
  const API_URL = 'http://25.56.145.23:8000'; 

  const handleLogin = async () => {
    if (!usuario || !contrasena) {
      Alert.alert('Error', 'Por favor, ingrese su usuario y contraseña.');
      return;
    }
    
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/users/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nombre: usuario,
          contraseña: contrasena,
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        Alert.alert('Éxito', '¡Inicio de sesión exitoso!');
        
        // Guardar el token y el nombre del usuario
        await AsyncStorage.setItem('access_token', data.access_token);
        await AsyncStorage.setItem('nombre_usuario', usuario);
        
        console.log('Token de acceso:', data.access_token);
        console.log('Usuario logeado:', usuario);
        
        // Redirige al usuario al dashboard.
        // Asegúrate de que esta ruta sea correcta para tu proyecto.
        // Si tu archivo se llama `dashboard.js` y está en la carpeta `screens`, la ruta es `/screens/dashboard`.
        router.replace('../screens/usuario'); 
      } else {
        // Muestra el error que viene del backend
        Alert.alert('Error', data.detail ||  'Credenciales incorrectas. Verifique su usuario y contraseña.');
      }
    } catch (error) {
      console.error('Error en la autenticación:', error);
      Alert.alert('Error', 'No se pudo conectar al servidor. Intente de nuevo más tarde.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpenMenu = () => {
    bottomSheetRef.current?.expand();
  };

  return {
    usuario,
    setUsuario,
    contrasena,
    setContrasena,
    handleLogin,
    isLoading,
    bottomSheetRef,
    handleOpenMenu
  };
}