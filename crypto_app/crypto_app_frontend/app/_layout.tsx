import { useEffect, useState } from 'react';
import { Stack } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { ActivityIndicator, View, StyleSheet } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';

export default function RootLayout() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [isGuest, setIsGuest] = useState<boolean | null>(null);

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const userToken = await AsyncStorage.getItem('access_token');
        const guestToken = await AsyncStorage.getItem('guest_token');

        if (userToken) {
          setIsAuthenticated(true);
          setIsGuest(false);
        } else if (guestToken) {
          setIsAuthenticated(true); // Considera la sesión como autenticada para la navegación.
          setIsGuest(true);
        } else {
          setIsAuthenticated(false);
          setIsGuest(false);
        }
      } catch (error) {
        console.error("Error checking authentication:", error);
        setIsAuthenticated(false);
        setIsGuest(false);
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
        <Stack.Screen
          name="index"
          options={{ headerShown: false }}
          redirect={!isAuthenticated ? true : undefined}
        />
        <Stack.Screen
          name="screens/login"
          options={{ headerShown: false }}
          redirect={isAuthenticated ? true : undefined}
        />
        <Stack.Screen
          name="screens/usuario"
          options={{ headerShown: false }}
          redirect={!isAuthenticated ? true : undefined}
        />
        <Stack.Screen
          name="screens/register"
          options={{ headerShown: false }}
          redirect={isAuthenticated ? true : undefined}
        />
        <Stack.Screen
          name="screens/user"
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="screens/news"
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="screens/newsDetail"
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="screens/conversion"
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