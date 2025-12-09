import React from 'react';
import { Text, View, ScrollView, TextInput, Alert, ActivityIndicator } from 'react-native';
import { router } from 'expo-router';
import { Picker } from '@react-native-picker/picker';
import Header from '../_components/header';
import MenuModal from '../_components/MenuModal';
import styles from '../_styles/ConversionStyles';
import useCryptoConversion from '../_services/ConversionLogic'; 


const ConversionScreen = () => {
    const {
        cryptoValue,
        fiatValue,
        selectedCrypto,
        selectedFiat,
        conversionRate, // Tasa para mostrar, si se desea
        cryptoOptions, // Nueva lista de opciones
        fiatOptions,   // Nueva lista de opciones
        isLoading,     // Indicador de carga
        handleCryptoChange,
        handleFiatChange,
        setSelectedCrypto, // Ahora toma el id_api
        setSelectedFiat,   // Ahora toma el coi
    } = useCryptoConversion();

// Opciones del menú
    const menuOptions = [
        { label: 'Gestionar Usuario', action: () => router.push('/screens/user') },
        { label: 'Noticias', action: () => router.push('/screens/news') },
        { label: 'Inicio', action: () => router.push('/') },
        { label: 'Acerca de', action: () => Alert.alert('Información', 'Info sobre Krypton') },
        { label: 'Contacto', action: () => Alert.alert('Soporte', 'Contacto de soporte') },
    ];

    return (
        <View style={styles.container}>
            <Header />
            <ScrollView contentContainerStyle={styles.scrollContainer}>
                <Text style={styles.title}>Conversión de Monedas</Text>

                {/* Mostrar indicador de carga */}
                {isLoading ? (
                    <ActivityIndicator size="large" color="#00ffff" style={{ marginTop: 50 }} />
                ) : (
                    <>
                        {/* Bloque de Criptomoneda */}
                        <View style={styles.inputGroup}>
                            <Text style={styles.label}>Criptomoneda</Text>
                            <View style={styles.inputRow}>
                                <View style={styles.currencySelector}>
                                    <Picker
                                        // selectedValue ahora usa el símbolo para coincidir con la UI
                                        selectedValue={selectedCrypto}
                                        style={styles.pickerStyle}
                                        // onValueChange recibe el 'id_api' y lo pasa a setSelectedCrypto
                                        onValueChange={(itemValue) => setSelectedCrypto(itemValue)} 
                                        dropdownIconColor="#00ffff"
                                    >
                                        {/* Mapea sobre cryptoOptions, usando 'id_api' como valor y 'simbolo' como etiqueta */}
                                        {cryptoOptions.map((option) => (
                                            <Picker.Item
                                                key={option.id_cripto}
                                                label={option.simbolo} // BTC, ETH
                                                value={option.id_api}  // bitcoin, ethereum
                                                color="#000000ff"
                                            />
                                        ))}
                                    </Picker>
                                </View>
                                <TextInput
                                    style={styles.input}
                                    value={cryptoValue}
                                    onChangeText={handleCryptoChange}
                                    keyboardType="numeric"
                                    placeholder="0.0"
                                />
                            </View>
                        </View>
                        
                        {/* Muestra la Tasa de Conversión Actual (Opcional, pero útil) */}
                        <Text style={styles.rateText}>
                            Tasa: 1 {selectedCrypto} = {conversionRate.toFixed(2)} {selectedFiat}
                        </Text>
                        
                        {/* Bloque de Moneda Fiat */}
                        <View style={styles.inputGroup}>
                            <Text style={styles.label}>Moneda Fiat</Text>
                            <View style={styles.inputRow}>
                                <View style={styles.currencySelector}>
                                    <Picker
                                        // selectedValue ahora usa el símbolo (coi.toUpperCase())
                                        selectedValue={selectedFiat}
                                        style={styles.pickerStyle}
                                        // onValueChange recibe el 'coi' en minúsculas y lo pasa a setSelectedFiat
                                        onValueChange={(itemValue) => setSelectedFiat(itemValue)}
                                        dropdownIconColor="#00ffff"
                                    >
                                        {/* Mapea sobre fiatOptions, usando 'coi' como valor y 'coi.toUpperCase()' como etiqueta */}
                                        {fiatOptions.map((option) => (
                                            <Picker.Item
                                                key={option.id_moneda}
                                                label={option.coi.toUpperCase()} // USD, EUR
                                                value={option.coi}               // usd, eur
                                                color="#000000ff"
                                            />
                                        ))}
                                    </Picker>
                                </View>
                                <TextInput
                                    style={styles.input}
                                    value={fiatValue}
                                    onChangeText={handleFiatChange}
                                    keyboardType="numeric"
                                    placeholder="0.00"
                                />
                            </View>
                        </View>
                    </>
                )}
            </ScrollView>
            <MenuModal options={menuOptions} />
        </View>
    );
};

export default ConversionScreen;