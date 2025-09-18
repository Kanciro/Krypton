import React, { useState } from 'react';
import { Text, View, TouchableOpacity, } from 'react-native';
import Header from './_components/header';
import CandlestickChartComponent from './_components/CandlestickChart'; // Importa el nuevo componente
import { Picker } from '@react-native-picker/picker';
import styles from './_styles/IndexStyles';
import MenuModal from './_components/MenuModal';
import { router } from 'expo-router';



const SplashScreen = () => {
  const [selectedDays, setSelectedDays] = useState('1'); // Estado para los días
  const [selectedSymbol, setSelectedSymbol] = useState('BTC'); // Estado para el símbolo

  const menuOptions = [
    { label: 'Ir a Inicio', action: () => router.push('/screens/login') },
    { label: 'Ir a Registro', action: () => router.push('/screens/register') },
    { label: 'Acerca de', action: () => alert('Info sobre Krypton') },
    { label: 'Contacto', action: () => alert('Contacto de soporte') },
  ];  

  const timeOptions = [
    { label: '1 Día', value: '1' },
    { label: '5 Días', value: '5' },
    { label: '1 Mes', value: '30' },
    { label: '5 Meses', value: '150' },
  ];

  const symbolOptions = [
    { label: 'Bitcoin (BTC)', value: 'BTC' },
    { label: 'Ethereum (ETH)', value: 'ETH' },
    { label: 'Solana (SOL)', value: 'SOL' },
  ];

  return (
    <View style={styles.container}>
      <Header />
      <Text style={styles.title}>Gráfico de Criptomonedas</Text>
      
      {/* Contenedor para la selección de símbolos */}
      <View style={styles.pickerContainer}>
        <Text style={styles.pickerLabel}>Seleccionar Criptomoneda:</Text>
        <Picker
          selectedValue={selectedSymbol}
          style={styles.picker}
          onValueChange={(itemValue) => setSelectedSymbol(itemValue)}
          dropdownIconColor="#00ffff"
        >
          {symbolOptions.map((option) => (
            <Picker.Item key={option.value} label={option.label} value={option.value} color="#fff" />
          ))}
        </Picker>
      </View>

      {/* Contenedor de botones para los días */}
      <View style={styles.buttonGroup}>
        {timeOptions.map((option) => (
          <TouchableOpacity
            key={option.value}
            style={[
              styles.timeButton,
              selectedDays === option.value && styles.activeTimeButton,
            ]}
            onPress={() => setSelectedDays(option.value)}
          >
            <Text style={styles.timeButtonText}>{option.label}</Text>
          </TouchableOpacity>
        ))}
      </View>
      
      {/* Componente del gráfico */}
      <CandlestickChartComponent symbol={selectedSymbol} days={selectedDays} />
      <MenuModal options={menuOptions} />
    </View>
  );
};

export default SplashScreen;