import { useState, useRef } from 'react';
import { Alert } from 'react-native';
import { router } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage'; 
import Constants from 'expo-constants';

export function useLogin() {
  const [usuario, setUsuario] = useState('');
  const [contrasena, setContrasena] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const bottomSheetRef = useRef(null);

  const API_URL = Constants.expoConfig.extra.API_URL;

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
    
        // Almacena el token de acceso y limpia el token de invitado
        await AsyncStorage.setItem('access_token', data.access_token);
        await AsyncStorage.setItem('nombre_usuario', usuario);
        await AsyncStorage.removeItem('guest_token'); // <-- Limpiar token de invitado
    
        router.replace('/'); // Estandarizado a ruta absoluta
      } else {
        Alert.alert('Error', data.detail || 'Credenciales incorrectas. Verifique su usuario y contraseña.');
      }
    } catch (error) {
      console.error('Error en la autenticación:', error);
      Alert.alert('Error', 'No se pudo conectar al servidor. Intente de nuevo más tarde.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGuestLogin = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/guests/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        Alert.alert('Éxito', '¡Has iniciado sesión como invitado!');
        // Almacena un token de invitado y limpia tokens de usuario.
        await AsyncStorage.setItem('guest_token', 'true'); 
        await AsyncStorage.removeItem('access_token');
        await AsyncStorage.removeItem('nombre_usuario');
    
        router.replace('/'); 
      } else {
        Alert.alert('Error', 'No se pudo iniciar sesión como invitado.');
      }
    } catch (error) {
      console.error('Error al iniciar sesión como invitado:', error);
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
    handleOpenMenu,
    handleGuestLogin,
  };
}