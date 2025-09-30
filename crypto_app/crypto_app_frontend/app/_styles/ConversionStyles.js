import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#000042', // Fondo Principal
    },
    scrollContainer: {
        paddingHorizontal: 20,
        paddingBottom: 40,
        alignItems: 'center',
    },
    title: {
        fontSize: 28, // Tamaño aumentado para el título de conversión
        color: '#00DBC3', // Color de acento para el título
        fontWeight: 'bold',
        marginVertical: 25,
        textAlign: 'center',
    },

    // --- Estilos Específicos para la Conversión ---

    inputGroup: {
        width: '100%',
        marginBottom: 25,
    },
    label: {
        fontSize: 16,
        color: '#fff',
        marginBottom: 8,
        fontWeight: '600',
    },
    inputRow: {
        flexDirection: 'row',
        backgroundColor: '#000099', // Fondo azul más oscuro para el campo
        borderRadius: 12,
        overflow: 'hidden',
        borderWidth: 1,
        borderColor: '#00DBC3', // Borde de acento
    },
    currencySelector: {
        justifyContent: 'center',
        alignItems: 'center',
        paddingHorizontal: 15,
        borderRightWidth: 1,
        borderRightColor: 'rgba(255, 255, 255, 0.2)', // Separador sutil
        backgroundColor: '#000066', // Un color ligeramente distinto para el selector
    },
    currencyText: {
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
    },
    input: {
        flex: 1, // Hace que el input tome el espacio restante
        height: 60,
        color: '#fff',
        fontSize: 24,
        paddingHorizontal: 15,
        textAlign: 'right', // Valor del input alineado a la derecha
        fontWeight: '700',
    },
    rateDisplay: {
        fontSize: 14,
        color: '#ccc',
        marginBottom: 30,
        paddingHorizontal: 10,
        backgroundColor: 'rgba(0, 220, 195, 0.1)', // Fondo sutil para la tasa
        paddingVertical: 5,
        borderRadius: 5,
    },
    
    // --- Estilos de Noticias (Mantenerlos para reuso) ---

    listContent: {
        paddingHorizontal: 10,
        paddingBottom: 20,
    },
    newsCard: {
        backgroundColor: '#000099',
        padding: 15,
        borderRadius: 10,
        marginBottom: 15,
        width: '100%',
        shadowColor: '#00DBC3',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
        elevation: 5,
        borderWidth: 1,
        borderColor: '#00DBC3',
    },
    newsCardTitle: {
        fontSize: 18,
        color: '#fff',
        fontWeight: 'bold',
        marginBottom: 8,
    },
    newsCardContent: {
        fontSize: 14,
        color: '#ccc',
        marginBottom: 10,
    },
    newsCardReadMore: {
        fontSize: 14,
        color: '#00DBC3',
        fontWeight: 'bold',
        textAlign: 'right',
    },
    emptyListText: {
        color: '#fff',
        textAlign: 'center',
        marginTop: 50,
        fontSize: 16,
    },
    // Añade esto a tu ConversionStyles.js
pickerStyle: {
    // Asegura que el Picker ocupe todo el espacio del contenedor
    width: '100%', 
    height: '100%', 
    // ¡CRUCIAL! Asegura que el texto visible del Picker sea blanco sobre tu fondo oscuro
    color: '#00DBC3', 
    // padding horizontal si es necesario, aunque el contenedor lo maneja
},
// Modifica currencySelector para que el Picker quepa bien:
currencySelector: {
    justifyContent: 'center',
    // IMPORTANTE: Flex 1 y altura definida para que el Picker se estire y sea clicable
    flex: 0.4, // Ocupa un poco más de espacio que el input si es necesario
    height: 60, 
    borderRightWidth: 1,
    borderRightColor: 'rgba(255, 255, 255, 0.2)',
    backgroundColor: '#000066',
    // Importante: Overflow hidden para que el Picker se recorte bien
    overflow: 'hidden', 
},
});

export default styles;