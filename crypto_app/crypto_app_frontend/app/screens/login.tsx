import React from 'react';
import { router } from 'expo-router';
import { View, Text, TextInput, TouchableOpacity, ActivityIndicator, KeyboardAvoidingView, Platform } from 'react-native';
import styles from '../styles/LoginStyles';
import Header from '../components/header';
import MenuModal from '../components/MenuModal';
import { useLogin } from '../services/LoginLogic';

export default function LoginScreen() {
  const {
    usuario,
    setUsuario,
    contrasena,
    setContrasena,
    handleLogin,
    isLoading,
  } = useLogin();

  const menuOptions = [
    { label: 'Ir a Inicio', action: () => router.push('/') },
    { label: 'Ir a Registro', action: () => router.push('/screens/register') },
    { label: 'Acerca de', action: () => alert('Info sobre Krypton') },
    { label: 'Contacto', action: () => alert('Contacto de soporte') },
  ];

  return (
    <View style={styles.main}>
      <Header />
      <KeyboardAvoidingView
        style={styles.contentContainer}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <View style={styles.container}>
          <Text style={styles.title}>Login</Text>
          <TextInput
            style={styles.inputText}
            placeholder="Usuario"
            placeholderTextColor="#fff"
            onChangeText={setUsuario}
            value={usuario}
            autoCapitalize="none"
            autoFocus={true}
          />
          <TextInput
            secureTextEntry
            style={styles.inputText}
            placeholder="Contraseña"
            placeholderTextColor="#fff"
            onChangeText={setContrasena}
            value={contrasena}
            autoCapitalize="none"
          />
          <TouchableOpacity style={styles.loginBtn} onPress={handleLogin} disabled={isLoading}>
            {isLoading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.loginText}>INICIAR SESIÓN</Text>
            )}
          </TouchableOpacity>
          <TouchableOpacity onPress={() => console.log('Olvidó su contraseña sjsjsjsjsjs pinche pendejo XD')}>
            <Text style={styles.forgot}>¿Olvidaste tu contraseña?</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.SubContainer}>
          <Text style={styles.register_text}>¿No tienes cuenta?</Text>
          <TouchableOpacity onPress={() => router.push('/screens/register')}>
            <Text style={styles.register}>Regístrate</Text>
          </TouchableOpacity>
          <Text style={styles.register_text}>o</Text>
          <TouchableOpacity onPress={() => console.log('Continua como invitado')}>
            <Text style={styles.register}>continua como invitado</Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
      <MenuModal options={menuOptions} />
    </View>
  );
}