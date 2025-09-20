import { useState, useEffect } from 'react';
import Constants from 'expo-constants';

const useCryptoData = () => {
    const [selectedDays, setSelectedDays] = useState('5');
    const [selectedSymbol, setSelectedSymbol] = useState('ETH');
    const [cryptoOptions, setCryptoOptions] = useState([]);

    const API_URL = Constants.expoConfig.extra.API_URL;

    useEffect(() => {
        const fetchCryptos = async () => {
            try {
                const response = await fetch(`${API_URL}/cryptos/todas`);
                if (!response.ok) {
                    throw new Error('Failed to fetch cryptocurrency list');
                }
                const json = await response.json();
                
                // --- CAMBIO CLAVE AQUÍ ---
                const formattedOptions = json.map(item => ({
                    label: `${item.nombre} (${item.simbolo})`, // Muestra el nombre ("Bitcoin")
                    value: item.simbolo, // Usa el símbolo como valor ("BTC")
                }));
                // -------------------------
                
                setCryptoOptions(formattedOptions);
                // Si la lista de criptos se carga, establece el primer símbolo como el seleccionado por defecto
                if (formattedOptions.length > 0) {
                    setSelectedSymbol(formattedOptions[0].value);
                }
            } catch (error) {
                console.error("Error fetching cryptos:", error);
            }
        };

        fetchCryptos();
    }, []);

    const timeOptions = [
        { label: '1 Día', value: '1' },
        { label: '5 Días', value: '5' },
        { label: '1 Mes', value: '30' },
        { label: '5 Meses', value: '150' },
    ];

    return {
        selectedDays,
        setSelectedDays,
        selectedSymbol,
        setSelectedSymbol,
        cryptoOptions,
        timeOptions,
    };
};

export default useCryptoData;