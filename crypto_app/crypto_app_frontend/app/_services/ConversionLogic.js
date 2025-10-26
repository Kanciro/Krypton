import { useState, useEffect } from 'react';

const MOCK_RATES = {
    'BTC': { 'USD': 62000.00, 'EUR': 58000.00 },
    'ETH': { 'USD': 3500.00, 'EUR': 3300.00 }
};

export const CRYPTOS = ['BTC', 'ETH'];
export const FIATS = ['USD', 'EUR'];

const useCryptoConversion = () => {
    const [cryptoValue, setCryptoValue] = useState('');
    const [fiatValue, setFiatValue] = useState('');
    const [selectedCrypto, setSelectedCrypto] = useState(CRYPTOS[0]);
    const [selectedFiat, setSelectedFiat] = useState(FIATS[0]);
    const [conversionRate, setConversionRate] = useState(MOCK_RATES[CRYPTOS[0]][FIATS[0]]);

    // 1. Efecto para actualizar la tasa de conversión al cambiar las monedas
    // y recalcular el valor opuesto.
    useEffect(() => {
        const rate = MOCK_RATES[selectedCrypto]?.[selectedFiat] || 0;
        setConversionRate(rate);

        // Recalcular el valor opuesto manteniendo el valor ya escrito
        if (cryptoValue) {
            handleCryptoChange(cryptoValue, rate);
        } else if (fiatValue) {
            handleFiatChange(fiatValue, rate);
        }
    }, [selectedCrypto, selectedFiat]);

    // Función de limpieza de valor y conversión de Crypto a Fiat
    const handleCryptoChange = (value, currentRate = conversionRate) => {
        const cleanedValue = value.replace(/[^0-9.]/g, '');
        setCryptoValue(cleanedValue);

        if (cleanedValue && currentRate) {
            const cryptoAmount = parseFloat(cleanedValue);
            // Redondea a 2 decimales para la moneda fiat
            const newFiatValue = (cryptoAmount * currentRate).toFixed(2);
            setFiatValue(newFiatValue.toString());
        } else {
            setFiatValue('');
        }
    };

    // Función de limpieza de valor y conversión de Fiat a Crypto
    const handleFiatChange = (value, currentRate = conversionRate) => {
        const cleanedValue = value.replace(/[^0-9.]/g, '');
        setFiatValue(cleanedValue);

        if (cleanedValue && currentRate && currentRate !== 0) {
            const fiatAmount = parseFloat(cleanedValue);
            // Redondea a 8 decimales para la criptomoneda
            const newCryptoValue = (fiatAmount / currentRate).toFixed(8);
            setCryptoValue(newCryptoValue.toString());
        } else {
            setCryptoValue('');
        }
    };

    // Retorna todo el estado y las funciones que el componente necesita
    return {
        cryptoValue,
        fiatValue,
        selectedCrypto,
        selectedFiat,
        conversionRate,
        handleCryptoChange,
        handleFiatChange,
        setSelectedCrypto,
        setSelectedFiat,
    };
};

export default useCryptoConversion;