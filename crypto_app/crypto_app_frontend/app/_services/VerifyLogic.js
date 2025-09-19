import { useState } from 'react';
import { useRoute } from '@react-navigation/native';
import { Alert } from 'react-native';
import Constants from 'expo-constants';

const useVerifyLogic = () => {
  // Obtiene los parámetros de la ruta, como el email
  const route = useRoute();
  const { email } = route.params; 

  // Estado para el código de verificación
  const [code, setCode] = useState('');

  const API_URL = Constants.expoConfig.extra.API_URL;

  const handleVerification = async (navigation) => {
    try {
      // Validar que el código no esté vacío
      if (!code) {
        Alert.alert('Error', 'Por favor, ingresa el código de verificación.');
        return;
      }

      const response = await fetch(`${API_URL}/verify-code`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ correo: email, codigo: code }),
      });

      const responseData = await response.json();

      if (!response.ok) {
        throw new Error(responseData.detail || 'Error en la verificación del código');
      }

      Alert.alert('Éxito', responseData.mensaje);
      // Navega a la pantalla de inicio de sesión
      navigation.navigate('Login'); 
    } catch (error) {
      Alert.alert('Error', error.message || 'Hubo un error al verificar el código.');
    }
  };

  // Retorna el estado y la función para que el componente los use
  return {
    code,
    setCode,
    email,
    handleVerification,
  };
};

export default useVerifyLogic;