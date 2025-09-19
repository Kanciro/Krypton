import { useState, useEffect } from 'react';

const useCryptoData = () => {
    const [selectedDays, setSelectedDays] = useState('5');
    const [selectedSymbol, setSelectedSymbol] = useState('ETH');
    const [cryptoOptions, setCryptoOptions] = useState([]);

    useEffect(() => {
        const fetchCryptos = async () => {
            try {
                const response = await fetch('http://25.56.145.23:8000/cryptos/todas');
                if (!response.ok) {
                    throw new Error('Failed to fetch cryptocurrency list');
                }
                const json = await response.json();
                const formattedOptions = json.map(item => ({
                    label: item.symbol, 
                    value: item.symbol,
                }));
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

    const menuOptions = [
        { label: 'Ir a login', action: () => alert('Ir a login') },
        { label: 'Ir a Registro', action: () => alert('Ir a Registro') },
        { label: 'Acerca de', action: () => alert('Info sobre Krypton') },
        { label: 'Contacto', action: () => alert('Contacto de soporte') },
    ];

    return {
        selectedDays,
        setSelectedDays,
        selectedSymbol,
        setSelectedSymbol,
        cryptoOptions,
        timeOptions,
        menuOptions,
    };
};

export default useCryptoData;