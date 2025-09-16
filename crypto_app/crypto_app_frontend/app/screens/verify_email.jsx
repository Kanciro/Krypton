import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert } from 'react-native';
import { useRoute } from '@react-navigation/native';
import styles from '../styles/RegisterStyle'; // Reutiliza los estilos
import Header from '../components/header';

const VerifyScreen = ({ navigation }) => {
  const route = useRoute();
  const [code, setCode] = useState('');
  const { email } = route.params; // Captura el correo pasado desde la pantalla de registro

  const handleVerification = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/users/verify-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ correo: email, codigo: code }),
      });

      const responseData = await response.json();

      if (!response.ok) {
        throw new Error(responseData.detail || 'Error en la verificación del código');
      }

      Alert.alert('Éxito', responseData.mensaje);
      navigation.navigate('Login'); // Navega a la pantalla de inicio de sesión
    } catch (error) {
      Alert.alert('Error', error.message || 'Hubo un error al verificar el código.');
    }
  };

  return (
    <View style={styles.main}>
      <Header />
      <View style={styles.Container}>
        <Text style={styles.title}>Verifica tu cuenta</Text>
        <Text style={{ textAlign: 'center', marginBottom: 20 }}>
          Ingresa el código de 4 dígitos que enviamos a {email}
        </Text>
        <TextInput
          style={styles.input}
          placeholder="Código de verificación"
          placeholderTextColor="#aaa"
          keyboardType="numeric"
          maxLength={4}
          value={code}
          onChangeText={setCode}
        />
        <TouchableOpacity style={styles.button} onPress={handleVerification}>
          <Text style={styles.buttonText}>Verificar</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default VerifyScreen;