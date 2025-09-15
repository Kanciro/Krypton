import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
    main:{
        backgroundColor: '#000042',
        paddingBottom: '50%',
        alignItems: 'center',
        position: 'absolute',
        height: '100%',
        width: '100%',
    },
    Container: {
        backgroundColor: '#7600a6',
        marginTop: 20,
        paddingTop: 15,
        paddingLeft: 25,
        paddingRight: 25,
        paddingBottom: 20,
        width: 'auto',
        height: 'auto',
    },
    title: {
        fontSize: 17,
        color: '#fff',
        fontWeight: 'bold',
        marginBottom: 10,
        alignSelf:'center',
    },
    input: {
        width: '100%',
        backgroundColor: 'rgba(0, 0, 153, 0.62)',
        color: '#fff',
        padding: 7,
        marginBottom: 3,
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
        marginTop: 2,
        marginBottom: 3,
    },
    label: {
        color: '#fff',
        fontSize: 14,
        marginLeft: 8,
    },
    eula: {
        color:'#00ffff'
    }
});

export default styles;