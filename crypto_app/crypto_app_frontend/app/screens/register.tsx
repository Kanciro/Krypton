import React from 'react';
import { View, Text, TextInput, TouchableOpacity, Linking } from 'react-native';
import { router } from 'expo-router';
import { Checkbox } from 'expo-checkbox';
import styles from '../styles/RegisterStyle';
import registerLogic from '../services/RegisterLogic';
import Header from '../components/header';

const RegisterScreen = () => {
    // Pasa el objeto `router` a tu hook `registerLogic`
    const {
        username,
        setUsername,
        password,
        setPassword,
        email,
        setEmail,
        date,
        setDate,
        handleRegistration,
        // Añade estas dos propiedades aquí
        acceptTerms,
        setAcceptTerms,
    } = registerLogic(router);

    const handleLinkPress = () => {
        Linking.openURL('https://www.google.com');
    };

    return (
        <View style={styles.main}>
            <Header />
            <View style={styles.Container}>
                <Text style={styles.title}>Registro</Text>
                <TextInput
                    style={styles.input}
                    placeholder="Usuario"
                    placeholderTextColor="#aaa"
                    value={username}
                    onChangeText={setUsername}
                />
                <TextInput
                    style={styles.input}
                    placeholder="Contraseña"
                    placeholderTextColor="#aaa"
                    secureTextEntry
                    value={password}
                    onChangeText={setPassword}
                />
                <TextInput
                    style={styles.input}
                    placeholder="Correo"
                    placeholderTextColor="#aaa"
                    keyboardType="email-address"
                    value={email}
                    onChangeText={setEmail}
                />
                <TextInput
                    style={styles.input}
                    placeholder="FECHA DE NACIMIENTO (YYYY-MM-DD)"
                    placeholderTextColor="#aaa"
                    value={date}
                    onChangeText={setDate}
                />
                {/* Asegúrate de que este bloque de código no esté comentado */}
                <View style={styles.checkboxContainer}>
                    <Checkbox
                        value={acceptTerms}
                        onValueChange={setAcceptTerms}
                        color={acceptTerms ? 'rgba(0, 0, 153, 0.62)' : 'rgba(0, 0, 153, 0.62)'}
                    />
                    <Text style={styles.label}>
                        Acepto los <TouchableOpacity onPress={handleLinkPress}>
                            <Text style={styles.eula}>Términos y condiciones</Text>
                        </TouchableOpacity>
                    </Text>
                </View>
                {/* Si tienes un checkbox para los correos de marketing, también deberías añadirlo */}
                {/* <View style={styles.checkboxContainer}>
                    <Checkbox
                        value={receiveEmails}
                        onValueChange={setReceiveEmails}
                        color={receiveEmails ? 'rgba(0, 0, 153, 0.62)' : 'rgba(0, 0, 153, 0.62)'}
                    />
                    <Text style={styles.label}>Deseo recibir correos de marketing</Text>
                </View> */}
                <TouchableOpacity style={styles.button} onPress={handleRegistration}>
                    <Text style={styles.buttonText}>Acceder</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
};

export default RegisterScreen;