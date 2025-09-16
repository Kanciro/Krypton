import { router } from 'expo-router';
import React from 'react';
import {Text, TouchableOpacity, View } from 'react-native';
import Header from './components/header';
import styles from './styles/IndexStyles';

// Componente de la pantalla principal (Splash Screen)
const SplashScreen = () => {
  return (
    <View style={styles.container}>
      <Header/>
      <Text style={styles.title}>¡Bienvenido a KRYPTON!</Text>
        <TouchableOpacity style={styles.button} onPress={() => router.push('/screens/register')}>
          <Text style={styles.buttonText}>Ir a Registro</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={() => router.push('/screens/login')}>
          <Text style={styles.buttonText}>Ir a Login</Text>
        </TouchableOpacity>
        
    </View>
  );
};
export default SplashScreen;