import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
    main: {
        flex: 1, 
        backgroundColor: '#000042',
    },
    contentContainer: {
        flex: 1, 
        alignItems: 'center', 
        paddingHorizontal: 20, 
    },
    Container: {
        backgroundColor: '#7600a6',
        width: '80%', 
        marginTop: 20,
        padding: 20,
        alignItems: 'center', 
    },
    title: {
        fontSize: 17,
        color: '#fff',
        fontWeight: 'bold',
        marginBottom: 20, 
        alignSelf: 'center',
    },
    input: {
        width: '100%',
        backgroundColor: 'rgba(0, 0, 153, 0.69)',
        paddingHorizontal: 15,
        paddingVertical: 10,
        marginBottom: 10, 
        color: '#fff',
        borderRadius: 5,
    },
    button: {
        backgroundColor: '#00ffff',
        width: '100%',
        padding: 15,
        borderRadius: 5,
        alignItems: 'center',
        marginTop: 20,
    },
    buttonText: {
        color: '#000',
        fontSize: 18,
        fontWeight: 'bold',
    },
    checkboxContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 10,
    },
    label: {
        color: '#fff',
        fontSize: 14,
        marginLeft: 8,
    },
    eula: {
        color: '#00ffff',
        textDecorationLine: 'underline', 
    },
});

export default styles;