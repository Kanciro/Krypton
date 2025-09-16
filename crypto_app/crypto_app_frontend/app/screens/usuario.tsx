// crypto_app_frontend/app/screens/DashboardScreen.js

import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { router } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function DashboardScreen() {
    const [nombreUsuario, setNombreUsuario] = useState('');

    useEffect(() => {
        const obtenerNombreUsuario = async () => {
            try {
                const nombreGuardado = await AsyncStorage.getItem('nombre_usuario');
                
                if (nombreGuardado) {
                    setNombreUsuario(nombreGuardado);
                } else {
                    router.replace('/screens/login');
                }
            } catch (error) {
                console.error("Error al obtener el nombre de usuario", error);
                router.replace('/screens/login');
            }
        };

        obtenerNombreUsuario();
    }, []);

    const handleLogout = async () => {
        try {
            await AsyncStorage.removeItem('access_token');
            await AsyncStorage.removeItem('nombre_usuario');
            console.log("Sesión cerrada. Token y nombre de usuario eliminados.");
            router.replace('../screens/login');
        } catch (error) {
            console.error("Error al cerrar sesión", error);
        }
    };

    return (
        <View style={styles.container}>
            <Text style={styles.greeting}>
                ¡Bienvenido, {nombreUsuario}! 👋
            </Text>
            <Text style={styles.info}>
                Este es tu dashboard personalizado.
            </Text>
            <TouchableOpacity style={styles.logoutBtn} onPress={handleLogout}>
                <Text style={styles.logoutText}>Cerrar Sesión</Text>
            </TouchableOpacity>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#1E1E1E',
        padding: 20,
    },
    greeting: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#fff',
        marginBottom: 10,
    },
    info: {
        fontSize: 16,
        color: '#ccc',
        marginBottom: 40,
        textAlign: 'center',
    },
    logoutBtn: {
        width: "80%",
        backgroundColor: "#FF6347",
        borderRadius: 25,
        height: 50,
        alignItems: "center",
        justifyContent: "center",
        marginTop: 20,
    },
    logoutText: {
        color: "white",
        fontWeight: 'bold',
    },
});