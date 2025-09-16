import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const Validacion = () => {
    return (
        <View style={styles.overlay}>
            <View style={styles.contentBox}>
                <Text style={styles.title}>Valide su correo</Text>
            </View>
        </View> 
    );
};

const styles = StyleSheet.create({
    overlay: {
        // Ocupa toda la pantalla y se superpone
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(255, 255, 255, 0.8)', // Blanco con 80% de opacidad
        justifyContent: 'center', // Centra el contenido verticalmente
        alignItems: 'center', // Centra el contenido horizontalmente
    },
    contentBox: {
        backgroundColor: 'white', // El cuadro blanco que contiene el texto
        padding: 20,
        borderRadius: 10, // Bordes redondeados para un mejor aspecto
        elevation: 5, // Sombra para Android
        shadowColor: '#000', // Sombra para iOS
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
    },
    title: {
        color: '#000',
        fontSize: 16,
        fontWeight: 'bold',
    },
});

export default Validacion;