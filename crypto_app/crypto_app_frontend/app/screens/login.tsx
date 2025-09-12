import { Background } from '@react-navigation/elements';
import React, { useState } from 'react';
import { StyleSheet, View, Text, TextInput, TouchableOpacity, ImageBackground } from 'react-native';

export default function LoginScreen() {
  const [usuario, setUsuario] = useState('');
  const [contrasena, setContrasena] = useState('');

  const handleLogin = () => {
    // Aquí puedes agregar la lógica para autenticar al usuario
    // Por ejemplo, enviar 'usuario' y 'contrasena' a una API.
    console.log('Iniciando sesión con:', usuario, contrasena);
  };

  return (
      <View style={styles.container}>
        <Text style={styles.logo}>KRYPTON</Text>

        <View style={styles.inputView}>
          <TextInput
            style={styles.inputText}
            placeholder="Usuario"
            placeholderTextColor="#fff"
            onChangeText={text => setUsuario(text)}
          />
        </View>
        <View style={styles.inputView}>
          <TextInput
            secureTextEntry
            style={styles.inputText}
            placeholder="Contraseña"
            placeholderTextColor="#fff"
            onChangeText={text => setContrasena(text)}
          />
        </View>

        <TouchableOpacity style={styles.loginBtn} onPress={handleLogin}>
          <Text style={styles.loginText}>INICIAR SESIÓN</Text>
        </TouchableOpacity>

        <TouchableOpacity>
          <Text style={styles.forgot}>¿Olvidaste tu contraseña?</Text>
        </TouchableOpacity>
        
        <TouchableOpacity>
          <Text style={styles.register}>¿No tienes cuenta? Regístrate</Text>
        </TouchableOpacity>

      </View>

  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
    backgroundColor: 'rgba(0,0,0,0.5)', // Un fondo oscuro semi-transparente para que el texto resalte
  },
  logo: {
    fontWeight: 'bold',
    fontSize: 50,
    color: '#fff',
    marginBottom: 40,
  },
  inputView: {
    width: '80%',
    backgroundColor: 'rgba(255,255,255,0.2)',
    borderRadius: 25,
    height: 50,
    marginBottom: 20,
    justifyContent: 'center',
    padding: 20,
  },
  inputText: {
    height: 50,
    color: 'white',
  },
  loginBtn: {
    width: '80%',
    backgroundColor: '#008b8b', // Un color similar al verde aguamarina de la imagen
    borderRadius: 25,
    height: 50,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 40,
    marginBottom: 10,
  },
  loginText: {
    color: 'white',
    fontWeight: 'bold',
  },
  forgot: {
    color: 'white',
    fontSize: 12,
  },
  register: {
    color: 'white',
    marginTop: 15,
    fontSize: 14,
  },
});