import { router } from 'expo-router';
import React from 'react';
import { Text, TouchableOpacity, View } from 'react-native';
import Header from './components/header';
import MenuModal from './components/MenuModal'; // Importa el componente modificado
import styles from './styles/IndexStyles';

const SplashScreen = () => {
  const menuOptions = [
    { label: 'Ir a Login', action: () => router.push('/screens/login') },
    { label: 'Ir a Registro', action: () => router.push('/screens/register') },
    { label: 'Acerca de', action: () => alert('Info sobre Krypton') },
    { label: 'Contacto', action: () => alert('Contacto de soporte') },
  ];

  return (
    <View style={styles.container}>
      <Header />
      <Text style={styles.title}>¡Bienvenido a KRYPTON!</Text>
  
      <MenuModal options={menuOptions} />
    </View>
  );
};

export default SplashScreen;