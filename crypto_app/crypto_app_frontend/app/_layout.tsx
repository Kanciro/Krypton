import { useEffect, useState } from 'react';
import { Stack, router } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { ActivityIndicator, View, StyleSheet } from 'react-native';


export default function RootLayout() {
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const token = await AsyncStorage.getItem('access_token');
        if (token) {
          // If a token exists, the user is considered authenticated
          setIsAuthenticated(true);
        } else {
          // No token means not authenticated
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
    // Show a loading screen while the authentication state is being checked
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  // Use the redirect prop on the Stack.Screen components
  return (
    <Stack>
      <Stack.Screen 
        name="screens/login" 
        options={{ headerShown: false }} 
        redirect={isAuthenticated ? true : undefined}
      />
      <Stack.Screen 
        name="screens/usuario" 
        options={{ headerShown: false }} 
        redirect={isAuthenticated === false ? true : undefined}
      />
      {/* Add other protected screens here */}
    </Stack>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});