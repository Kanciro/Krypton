import { useState } from 'react';
import { Alert } from 'react-native';
import Constants from 'expo-constants';

// Función para validar el formato del correo electrónico
const validateEmail = (email) => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
};

// Función para validar la fortaleza de la contraseña
const validatePassword = (password) => {
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}\[\]|:;"'<>,.?/~`]).{6,}$/;
    return regex.test(password);
};

// Función para validar que el usuario es mayor de 18 años
const validateAge = (dateString) => {
    const today = new Date();
    const birthDate = new Date(dateString);
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDifference = today.getMonth() - birthDate.getMonth();

    if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    return age >= 18;
};

// Lógica de registro encapsulada en un hook personalizado
const registerLogic = (router) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [date, setDate] = useState('');
    const [acceptTerms, setAcceptTerms] = useState(false);

    const API_URL = Constants.expoConfig.extra.API_URL;

    const handleRegistration = async () => {
        if (!username || !password || !email || !date) {
            Alert.alert('Error de validación', 'Por favor, completa todos los campos.');
            return;
        }

        if (!validateEmail(email)) {
            Alert.alert('Error de validación', 'Por favor, introduce un correo electrónico válido.');
            return;
        }

        if (!validatePassword(password)) {
            Alert.alert(
                'Error de validación',
                'La contraseña debe tener al menos 6 caracteres, incluyendo una letra mayúscula, una minúscula, un número y un carácter especial.'
            );
            return;
        }

        if (!validateAge(date)) {
            Alert.alert('Error de edad', 'Debes ser mayor de 18 años para registrarte.');
            return;
        }

        if (!acceptTerms) {
            Alert.alert('Error', 'Debes aceptar los términos y condiciones.');
            return;
        }

        const userData = {
            nombre: username,
            contraseña: password,
            correo: email,
            fecha_nacimiento: date,
        };

        try {
            const response = await fetch(`${API_URL}/users/registrar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error en el registro');
            }

            const responseData = await response.json();
            Alert.alert('Éxito', '¡Registro exitoso! Por favor, ingresa el código de verificación que enviamos a tu correo.');

            const userEmailFromBackend = responseData.correo;

            router.push({ pathname: '/screens/verify_email', params: { email: userEmailFromBackend } });

            return true;
        } catch (error) {
            Alert.alert('Error', (error instanceof Error ? error.message : String(error)) || 'Hubo un error al registrar el usuario.');
            return false;
        }
    };

    return {
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
    };
};

export default registerLogic;