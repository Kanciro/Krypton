import React from 'react';
import { router } from 'expo-router';
import { View, Text, TextInput, TouchableOpacity, ActivityIndicator } from 'react-native';
import styles from '../styles/LoginStyles';
import Header from '../components/header';
import Menu from '../components/menu';
import { useLogin } from '../services/LoginLogic';

export default function LoginScreen() {
  const { 
    usuario, 
    setUsuario, 
    contrasena, 
    setContrasena, 
    handleLogin, 
    isLoading, 
    bottomSheetRef, 
    handleOpenMenu 
  } = useLogin();

  return (
    <View style={styles.main}>
      <Header />
      <View style={styles.container}>
        <Text style={styles.title}>Login</Text>
        <TextInput
          style={styles.inputText}
          placeholder="Usuario"
          placeholderTextColor="#fff"
          onChangeText={setUsuario}
          value={usuario}
        />
        <TextInput
          secureTextEntry
          style={styles.inputText}
          placeholder="Contraseña"
          placeholderTextColor="#fff"
          onChangeText={setContrasena}
          value={contrasena}
        />
        <TouchableOpacity style={styles.loginBtn} onPress={handleLogin} disabled={isLoading}>
          {isLoading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.loginText}>INICIAR SESIÓN</Text>
          )}
        </TouchableOpacity>
        <TouchableOpacity onPress={handleOpenMenu}>
          <Text style={styles.forgot}>¿Olvidaste tu contraseña?</Text>
        </TouchableOpacity>
      </View>
      <View style={styles.SubContainer}>
        <Text style={styles.register_text}>¿No tienes cuenta?</Text>
        <TouchableOpacity onPress={() => router.push('/screens/register')}>
          <Text style={styles.register} >Regístrate</Text>
        </TouchableOpacity>
        <Text style={styles.register_text}>o</Text>
        <TouchableOpacity>
          <Text style={styles.register}>continua como invitado</Text>
        </TouchableOpacity>
      </View>
      <Menu ref={bottomSheetRef} />
    </View>
  );
}