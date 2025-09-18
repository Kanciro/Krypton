import { View, Text, TextInput, TouchableOpacity } from 'react-native';
import styles from '../_styles/verify_emailStyles';
import Header from '../_components/header';
import MenuModal from '../_components/MenuModal';
import useVerifyLogic from '../_services/VerifyLogic';
import { router } from 'expo-router';

const VerifyScreen = ({ navigation }) => {
  const { code, setCode, email, handleVerification } = useVerifyLogic();

  // 👉 Mueve las opciones del menú aquí, dentro del componente
  const menuOptions = [
    { label: 'Ir a Login', action: () => router.push('/screens/Login') },
    { label: 'Ir a Registro', action: () => router.push('/screens/Register') },
    { label: 'Acerca de', action: () => alert('Info sobre Krypton') },
    { label: 'Contacto', action: () => alert('Contacto de soporte') },
  ];

  return (
    <View style={styles.main}>
      <Header />
      <View style={styles.Container}>
        <Text style={styles.title}>Verifica tu cuenta</Text>
        <Text style={styles.label}>
          Ingresa el código de 4 dígitos que enviamos a {email}
        </Text>
        <TextInput
          style={styles.input}
          placeholder="Código de verificación"
          placeholderTextColor="#aaa"
          keyboardType="numeric"
          maxLength={4}
          value={code}
          onChangeText={setCode}
        />
        <TouchableOpacity
          style={styles.button}
          onPress={() => handleVerification(navigation)}>
          <Text style={styles.buttonText}>Verificar</Text>
        </TouchableOpacity>
      </View>
      <MenuModal options={menuOptions} />
    </View>
  );
};

export default VerifyScreen;