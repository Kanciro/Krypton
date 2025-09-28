import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Linking, KeyboardAvoidingView, Platform } from 'react-native';
import { router } from 'expo-router';
import { Checkbox } from 'expo-checkbox';
import styles from '../_styles/RegisterStyle';
import registerLogic from '../_services/RegisterLogic';
import Header from '../_components/header';
import DateTimePickerModal from 'react-native-modal-datetime-picker';
import MenuModal from '../_components/MenuModal';

const menuOptions = [
    { label: 'Ir a Inicio', action: () => router.push('/') },
    { label: 'Ir a Login', action: () => router.push('/screens/login') }, 
    { label: 'Acerca de', action: () => alert('Info sobre Krypton') },
    { label: 'Contacto', action: () => alert('Contacto de soporte') },
];

const RegisterScreen = () => {
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
        acceptTerms,
        setAcceptTerms,
    } = registerLogic(router);

    const [isDatePickerVisible, setDatePickerVisibility] = useState(false);

    const showDatePicker = () => {
        setDatePickerVisibility(true);
    };
    const hideDatePicker = () => {
        setDatePickerVisibility(false);
    };
    const handleConfirm = (selectedDate: Date) => {
        const formattedDate = selectedDate.toISOString().split('T')[0];
        setDate(formattedDate);
        hideDatePicker();
    };
    const handleLinkPress = () => {
        Linking.openURL('https://www.google.com');
    };
    return (
        <View style={styles.main}>
            <Header />
            <KeyboardAvoidingView
                style={styles.contentContainer}
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            >
                <View style={styles.Container}>
                    <Text style={styles.title}>Registro</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="Usuario"
                        placeholderTextColor="#aaa"
                        value={username}
                        onChangeText={setUsername}
                        autoCapitalize="none"
                        autoFocus={true}
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
                    <TouchableOpacity onPress={showDatePicker} style={styles.input}>
                        <Text style={{ color: date ? '#fff' : '#aaa' }}>
                            {date || "FECHA DE NACIMIENTO"}
                        </Text>
                    </TouchableOpacity>
                    <DateTimePickerModal
                        isVisible={isDatePickerVisible}
                        mode="date"
                        onConfirm={handleConfirm}
                        onCancel={hideDatePicker}
                        date={date ? new Date(date) : new Date()}
                    />
                    <View style={styles.checkboxContainer}>
                        <Checkbox
                            value={acceptTerms}
                            onValueChange={setAcceptTerms}
                            color={acceptTerms ? 'rgba(0, 0, 153, 0.62)' : 'rgba(0, 0, 153, 0.62)'}
                        />
                        <Text style={styles.label}>
                            Acepto los <Text style={styles.eula} onPress={handleLinkPress}>Términos y condiciones</Text>
                        </Text>
                    </View>
                    <TouchableOpacity style={styles.button} onPress={handleRegistration}>
                        <Text style={styles.buttonText}>Acceder</Text>
                    </TouchableOpacity>
                </View>
            </KeyboardAvoidingView>
            <MenuModal options={menuOptions} />
        </View>
    );
};

export default RegisterScreen;