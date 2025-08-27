import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

// Aquí iría la lógica para enviar los datos al backend
const LoginScreen = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [date, setDate] = useState('');

  const handleLogin = () => {
    console.log('Username:', username);
    console.log('Password:', password);
    console.log('Email:', email);
    console.log('Date:', date);
  };
//  Seccion fundamental del registro

  return (
    <LinearGradient
      colors={['#000042', '#7600A9']}
      style={styles.container}
    >
      <View style={styles.formContainer}>
        <Text style={styles.title}>Registro</Text>

        <TextInput
          style={styles.input}
          placeholder="Usuario"
          placeholderTextColor="#aaa"
          value={username}
          onChangeText={setUsername}
        />

        <TextInput
          style={styles.input}
          placeholder="Contraseña"
          placeholderTextColor="#aaa"
          secureTextEntry
          value={password}
          onChangeText={setPassword}
        />

        <TextInput
          style={styles.input}
          placeholder="Correo"
          placeholderTextColor="#aaa"
          keyboardType="email-address"
          value={email}
          onChangeText={setEmail}
        />

        <TextInput
          style={styles.input}
          placeholder="Fecha"
          placeholderTextColor="#aaa"
          value={date}
          onChangeText={setDate}
        />

        {/* Los checkboxes para aceptar términos y notificaciones irían aquí */}
        
        <TouchableOpacity style={styles.button} onPress={handleLogin}>
          <Text style={styles.buttonText}>Acceder</Text>
        </TouchableOpacity>
      </View>
    </LinearGradient>
  );
};

// Seccion de Styles

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  formContainer: {
    backgroundColor: 'rgba(0, 0, 0, 0.4)',
    padding: 20,
    borderRadius: 10,
    width: '85%',
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    color: '#fff',
    fontWeight: 'bold',
    marginBottom: 20,
  },
  input: {
    width: '100%',
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    color: '#fff',
    padding: 15,
    borderRadius: 5,
    marginBottom: 10,
  },
  button: {
    backgroundColor: '#00ffff',
    width: '100%',
    padding: 15,
    borderRadius: 5,
    alignItems: 'center',
    marginTop: 20,
  },
  buttonText: {
    color: '#000',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default LoginScreen;