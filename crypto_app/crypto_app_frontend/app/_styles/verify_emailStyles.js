import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
    main: {
        flex: 1, 
        backgroundColor: '#000042',
        alignItems: 'center',
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
        fontSize: 20,
        color: '#fff',
        fontWeight: 'bold',
        marginBottom: 20, 
        alignSelf: 'center',
    },
    label: {
        color: '#fff',
        fontSize: 20,
    },
    input: {
        width: '100%',
        backgroundColor: 'rgba(0, 0, 153, 0.69)',
        paddingHorizontal: 15,
        paddingVertical: 10,
        marginTop: 10,
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
});

export default styles;