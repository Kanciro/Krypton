import React from 'react';
import { Text, View, ScrollView, TextInput, Alert } from 'react-native';
import { router } from 'expo-router';
import { Picker } from '@react-native-picker/picker';
import Header from '../_components/header';
import MenuModal from '../_components/MenuModal';
import styles from '../_styles/ConversionStyles';
import useCryptoConversion, { CRYPTOS, FIATS } from '../_services/ConversionLogic';


const ConversionScreen = () => {
    const {
        cryptoValue,
        fiatValue,
        selectedCrypto,
        selectedFiat,
        handleCryptoChange,
        handleFiatChange,
        setSelectedCrypto,
        setSelectedFiat,
    } = useCryptoConversion();

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
                
                {/* Bloque de Criptomoneda */}
                <View style={styles.inputGroup}>
                    <Text style={styles.label}>Criptomoneda</Text>
                    <View style={styles.inputRow}>
                        <View style={styles.currencySelector}>
                            <Picker
                                selectedValue={selectedCrypto}
                                style={styles.pickerStyle}
                                onValueChange={(itemValue) => setSelectedCrypto(itemValue)}
                                dropdownIconColor="#00ffff"
                            >
                                {CRYPTOS.map((option) => (
                                    <Picker.Item
                                        key={option}
                                        label={option}
                                        value={option}
                                        color="#ffffff"
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
                {/* Bloque de Moneda Fiat */}
                <View style={styles.inputGroup}>
                    <Text style={styles.label}>Moneda Fiat</Text>
                    <View style={styles.inputRow}>
                        <View style={styles.currencySelector}>
                            <Picker
                                selectedValue={selectedFiat}
                                style={styles.pickerStyle}
                                onValueChange={(itemValue) => setSelectedFiat(itemValue)}
                                dropdownIconColor="#00ffff"
                            >
                                {FIATS.map((option) => (
                                    <Picker.Item
                                        key={option}
                                        label={option}
                                        value={option}
                                        color="#ffffff"
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

            </ScrollView>
            <MenuModal options={menuOptions} />
        </View>
    );
};

export default ConversionScreen;