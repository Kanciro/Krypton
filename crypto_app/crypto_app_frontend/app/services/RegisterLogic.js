import { useState } from 'react';
import { Alert } from 'react-native';

const registerLogic = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [date, setDate] = useState('');
  const [acceptTerms, setAcceptTerms] = useState(false);
  const [receiveEmails, setReceiveEmails] = useState(false);

  const handleRegistration = async () => {
    // Validar que se hayan aceptado los términos y condiciones
    if (!acceptTerms) {
      Alert.alert('Error', 'Debes aceptar los términos y condiciones.');
      return;
    }

    const userData = {
      nombre: username,
      contraseña: password,
      correo: email,
      fecha_nacimiento: date,
      recibir_correos: receiveEmails,
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/users/registrar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error en el registro');
      }

      const responseData = await response.json();
      console.log('¡Registro exitoso!', responseData);
      Alert.alert('Éxito', '¡Registro exitoso!');
      return true; // Retorna true si el registro fue exitoso
    } catch (error) {
      console.error('Hubo un error al registrar el usuario:', error);
      Alert.alert('Error', error.message || 'Hubo un error al registrar el usuario.');
      return false; // Retorna false si hubo un error
    }
  };

  return {
    username,
    setUsername,
    password,
    setPassword,
    email,
    setEmail,
    date,
    setDate,
    handleRegistration,
    acceptTerms,
    setAcceptTerms,
    receiveEmails,
    setReceiveEmails,
  };
};

export default registerLogic;