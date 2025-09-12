import { router } from 'expo-router';
import React from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';

// Componente de la pantalla principal (Splash Screen)
const SplashScreen = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>¡Bienvenido a KRYPTON!</Text>
        <TouchableOpacity style={styles.button} onPress={() => router.push('/../screens/register')}>
          <Text style={styles.buttonText}>Ir a Registro</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={() => router.push('/../screens/login')}>
          <Text style={styles.buttonText}>Ir a Login</Text>
        </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#000033',
  },
  title: {
    fontSize: 28,
    color: '#fff',
    marginBottom: 20,
    fontWeight: 'bold',
  },
  button: {
    backgroundColor: '#00ffff',
    paddingVertical: 15,
    paddingHorizontal: 30,
    borderRadius: 5,
    marginBlockStart:10,
  },
  buttonText: {
    color: '#000',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default SplashScreen;