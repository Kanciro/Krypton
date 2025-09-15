import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Linking } from 'react-native';
import styles from '../styles/RegisterStyle';
import registerLogic from '../services/RegisterLogic';
import { Checkbox } from 'expo-checkbox';
import DateTimePickerModal from 'react-native-modal-datetime-picker';
import Header from '../components/header';

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
    receiveEmails,
    setReceiveEmails,
  } = registerLogic();

  const [isDatePickerVisible, setDatePickerVisibility] = useState(false);

  const showDatePicker = () => {
    setDatePickerVisibility(true);
  };

  const hideDatePicker = () => {
    setDatePickerVisibility(false);
  };

  const handleConfirm = (selectedDate) => {
    const formattedDate = selectedDate.toISOString().split('T')[0];
    setDate(formattedDate);
    hideDatePicker();
  };

  const handleLinkPress = () => {
    Linking.openURL('https://www.google.com'); // Cambia esta URL por la que necesites
  };

  return (
    <View style={styles.main}>
      <Header/> 
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
        
        <TouchableOpacity onPress={showDatePicker} style={styles.input}>
          <Text style={{ color: date ? '#000' : '#aaa' }}>
            {date || "Fecha de Nacimiento"}
          </Text>
        </TouchableOpacity>

        <DateTimePickerModal
          isVisible={isDatePickerVisible}
          mode="date"
          onConfirm={handleConfirm}
          onCancel={hideDatePicker}
        />
        
        <View style={styles.checkboxContainer}>
          <Checkbox
            value={acceptTerms}
            onValueChange={setAcceptTerms}
            color={acceptTerms ? 'rgba(0, 0, 153, 0.62)' : 'rgba(0, 0, 153, 0.62)'}
          />
          <Text style={styles.label}>
            Acepto los <TouchableOpacity style={styles.eula} onPress={handleLinkPress}>
              <Text style={styles.eula}>Términos y condiciones</Text>
            </TouchableOpacity>
          </Text>
        </View>
        <View style={styles.checkboxContainer}>
          <Checkbox
            value={receiveEmails}
            onValueChange={setReceiveEmails}
            color={receiveEmails ? 'rgba(0, 0, 153, 0.62)' : 'rgba(0, 0, 153, 0.62)'}
          />
          <Text style={styles.label}>Deseo recibir correos de marketing</Text>
        </View>
        <TouchableOpacity style={styles.button} onPress={handleRegistration}>
          <Text style={styles.buttonText}>Acceder</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default RegisterScreen;