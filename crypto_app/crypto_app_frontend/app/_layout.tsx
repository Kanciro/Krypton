import { useEffect, useState } from 'react';
import { Stack } from 'expo-router'; 
import AsyncStorage from '@react-native-async-storage/async-storage';
import { ActivityIndicator, View, StyleSheet } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';

export default function RootLayout() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const token = await AsyncStorage.getItem('access_token');
        if (token) {
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.error("Error checking authentication:", error);
        setIsAuthenticated(false);
      }
    };

    checkAuthentication();
  }, []);

  if (isAuthenticated === null) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <Stack>
        {/*
          1. La pantalla de "index" debe ir primero.
          2. Su lógica de redirección se encarga de dirigir a los usuarios autenticados a la pantalla de "usuario".
        */}
        <Stack.Screen
          name="index"
          options={{ headerShown: false }}
          redirect={isAuthenticated ? true : undefined}
        />

        {/*
          3. La pantalla de "login" se muestra si el usuario NO está autenticado.
          4. No necesita redirección, ya que el index ya maneja la lógica.
        */}
        <Stack.Screen
          name="screens/login"
          options={{ headerShown: false }}
        />

        {/*
          5. La pantalla de "usuario" es una ruta protegida.
          6. La redirección se activa si el usuario NO está autenticado.
        */}
        <Stack.Screen
          name="screens/usuario"
          options={{ headerShown: false }}
          redirect={!isAuthenticated ? true : undefined}
        />
        {/* Agrega otras pantallas protegidas aquí */}
        <Stack.Screen
        name="screens/register"
        options={{ headerShown: false }}
        />
        <Stack.Screen
        name="screens/"
        options={{ headerShown: false }}
        />
      </Stack>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});