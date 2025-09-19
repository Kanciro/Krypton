import React from 'react';
import { Text, View, TouchableOpacity, } from 'react-native';
import Header from './_components/header';
import CandlestickChartComponent from './_components/CandlestickChart'; 
import { Picker } from '@react-native-picker/picker';
import styles from './_styles/IndexStyles';
import MenuModal from './_components/MenuModal';
import { router } from 'expo-router';
import useCryptoData from './_services/IndexLogic'; // Importa el hook personalizado

const SplashScreen = () => {
    // Usa el hook para obtener todos los datos y funciones necesarios
    const {
        selectedDays,
        setSelectedDays,
        selectedSymbol,
        setSelectedSymbol,
        cryptoOptions,
        timeOptions,
        menuOptions,
    } = useCryptoData();

    // Actualiza las acciones de los botones del menú para usar 'router'
    const updatedMenuOptions = menuOptions.map(option => {
        if (option.label === 'Ir a login') {
            return { ...option, action: () => router.push('/screens/login') };
        }
        if (option.label === 'Ir a Registro') {
            return { ...option, action: () => router.push('/screens/register') };
        }
        return option;
    });

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
                    {/* Renderiza las opciones obtenidas del hook */}
                    {cryptoOptions.map((option) => (
                        <Picker.Item key={option.value} label={option.label} value={option.value} color="#000000" />
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
            <MenuModal options={updatedMenuOptions} />
        </View>
    );
};

export default SplashScreen;