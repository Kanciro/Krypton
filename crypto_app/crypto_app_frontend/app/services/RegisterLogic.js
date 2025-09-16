import { useState } from 'react';
import { Alert } from 'react-native';

const registerLogic = (router) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [date, setDate] = useState('');
    const [acceptTerms, setAcceptTerms] = useState(false); // Mantener el estado aquí
    const [receiveEmails, setReceiveEmails] = useState(false); // Y aquí

    const handleRegistration = async () => {
        // Validación en el front-end para evitar 400 Bad Request
        if (!username || !password || !email || !date) {
            Alert.alert('Error de validación', 'Por favor, completa todos los campos.');
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
            const response = await fetch('http://127.0.0.1:8000/users/registrar', {
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
        acceptTerms, // Asegúrate de que este estado se devuelva
        setAcceptTerms, // Y su función actualizadora también
        //receiveEmails, // Si lo necesitas en el componente, también devuélvelo
        //setReceiveEmails,
    };
};

export default registerLogic;