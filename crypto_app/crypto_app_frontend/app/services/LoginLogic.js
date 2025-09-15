import { useState, useRef } from 'react';
import { Alert } from 'react-native';

export function useLogin() {
  const [usuario, setUsuario] = useState('');
  const [contrasena, setContrasena] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const bottomSheetRef = useRef(null);

  const handleLogin = async () => {
    if (!usuario || !contrasena) {
      Alert.alert('Error', 'Por favor, ingrese su usuario y contraseña.');
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/users/');
      if (!response.ok) {
        throw new Error('Error al obtener los datos de usuarios.');
      }
      const users = await response.json();

      const userFound = users.find(
        (user) => user.email === usuario && user.password === contrasena
      );

      if (userFound) {
        Alert.alert('Éxito', '¡Inicio de sesión exitoso!');
        //añadir la lógica para guardar el token de sesión y navegar

        console.log('Usuario autenticado:', userFound.email);
      } else {
        Alert.alert('Error', 'Credenciales incorrectas. Verifique su usuario y contraseña.');
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