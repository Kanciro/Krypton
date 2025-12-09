import { useState, useEffect } from 'react';
import Constants from 'expo-constants';

const API_URL = Constants.expoConfig.extra.API_URL;
const INITIAL_CRYPTO_LIST = [];
const INITIAL_FIAT_LIST = [];

// Función para obtener los datos de la API
const fetchApiData = async (endpoint) => {
    try {
        const response = await fetch(`${API_URL}${endpoint}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching data:", error);
        return null;
    }
};

const useCryptoConversion = () => {
    const [cryptoValue, setCryptoValue] = useState('');
    const [fiatValue, setFiatValue] = useState('');
    
    // Estado para las listas de monedas
    const [cryptoOptions, setCryptoOptions] = useState(INITIAL_CRYPTO_LIST);
    const [fiatOptions, setFiatOptions] = useState(INITIAL_FIAT_LIST);

    // Estado para las monedas seleccionadas (almacenan el 'id_api' y 'coi')
    const [selectedCryptoId, setSelectedCryptoId] = useState(''); // ej: 'bitcoin'
    const [selectedFiatId, setSelectedFiatId] = useState('');       // ej: 'usd'
    
    // Almacenamos el símbolo/coi para mostrar en el componente (ej: 'BTC', 'USD')
    const [selectedCryptoSymbol, setSelectedCryptoSymbol] = useState('');
    const [selectedFiatSymbol, setSelectedFiatSymbol] = useState('');

    const [conversionRate, setConversionRate] = useState(0);
    const [isLoading, setIsLoading] = useState(true);

    // --- 1. Efecto inicial para cargar listas de cryptos y fiats ---
    useEffect(() => {
        const loadInitialData = async () => {
            setIsLoading(true);
            
            const [cryptos, fiats] = await Promise.all([
                fetchApiData('/cryptos/todas'),
                fetchApiData('/fiat/all')
            ]);

            if (cryptos && cryptos.length > 0 && fiats && fiats.length > 0) {
                setCryptoOptions(cryptos);
                setFiatOptions(fiats);
                
                // Establecer las selecciones iniciales (primer elemento de cada lista)
                setSelectedCryptoId(cryptos[0].id_api);
                setSelectedCryptoSymbol(cryptos[0].simbolo);
                setSelectedFiatId(fiats[0].coi);
                setSelectedFiatSymbol(fiats[0].coi.toUpperCase());
            } else {
                console.warn("No se pudieron cargar las listas de monedas.");
            }
            setIsLoading(false);
        };

        loadInitialData();
    }, []);

    // --- 2. Efecto para actualizar la tasa de conversión al cambiar las monedas ---
    useEffect(() => {
        // Ejecutar solo si ya se seleccionaron las monedas
        if (selectedCryptoId && selectedFiatId) {
            const fetchRate = async () => {
                const endpoint = `/cripto/valor-actual-db?crypto_id=${selectedCryptoId}&monedas_fiat=${selectedFiatId}`;
                const data = await fetchApiData(endpoint);
                
                let rate = 0;
                
                // Extraer la tasa del objeto de respuesta anidado
                if (data) {
                    const cryptoKey = Object.keys(data)[0]; // 'bitcoin'
                    const fiatKey = Object.keys(data[cryptoKey])[0]; // 'usd'
                    rate = data[cryptoKey]?.[fiatKey]?.valor || 0;
                }

                setConversionRate(rate);

                // Recalcular el valor opuesto manteniendo el valor ya escrito
                if (cryptoValue) {
                    handleCryptoChange(cryptoValue, rate);
                } else if (fiatValue) {
                    handleFiatChange(fiatValue, rate);
                }
            };

            fetchRate();
        }
    }, [selectedCryptoId, selectedFiatId]); // Depende de los IDs de las monedas seleccionadas

    // --- Funciones de Manejo de Cambio de Valores ---
    
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

    // --- Funciones para cambiar las monedas ---
    const handleSelectCrypto = (id_api) => {
        const newCrypto = cryptoOptions.find(c => c.id_api === id_api);
        if (newCrypto) {
            setSelectedCryptoId(id_api);
            setSelectedCryptoSymbol(newCrypto.simbolo);
        }
    };

    const handleSelectFiat = (coi) => {
        const newFiat = fiatOptions.find(f => f.coi === coi);
        if (newFiat) {
            setSelectedFiatId(coi);
            setSelectedFiatSymbol(coi.toUpperCase());
        }
    };

    // Retorna todo el estado y las funciones que el componente necesita
    return {
        cryptoValue,
        fiatValue,
        selectedCrypto: selectedCryptoSymbol, 
        selectedFiat: selectedFiatSymbol,
        conversionRate,
        cryptoOptions,
        fiatOptions,   
        isLoading,
        handleCryptoChange,
        handleFiatChange,
        setSelectedCrypto: handleSelectCrypto,
        setSelectedFiat: handleSelectFiat,
    };
};

export default useCryptoConversion;