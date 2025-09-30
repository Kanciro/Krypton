import React from 'react';
import { View, Text, ScrollView, Linking, Button, StyleSheet } from 'react-native';
import { useLocalSearchParams, router } from 'expo-router';
import Header from '../_components/header';
import MenuModal from '../_components/MenuModal';

const NewsDetailScreen = () => {
    const params = useLocalSearchParams();
    const { titulo, contenido, url } = params;

    const menuOptions = [
        { label: 'Gestionar Usuario', action: () => router.push('/screens/user') },
        { label: 'Conversión de Monedas', action: () => router.push('/screens/conversion') },
        { label: 'Inicio', action: () => router.push('/') },
        { label: 'Acerca de', action: () => alert('Info sobre Krypton') },
        { label: 'Contacto', action: () => alert('Contacto de soporte') },
    ];

    return (
        <View style={detailStyles.container}>
            <Header/>
                <ScrollView style={detailStyles.scrollView}>
                    <Text style={detailStyles.title}>{titulo}</Text>
                    <Text style={detailStyles.content}>{contenido}</Text>
        
                    {url && (
                        <Button 
                            title="Ver Fuente Original" 
                            onPress={() => Linking.openURL(url as string)} 
                            color="#00DBC3"
                        />
                    )}
                </ScrollView>
            <MenuModal options={menuOptions} />
        </View>
    );
};

const detailStyles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#000042',
    },
    scrollView: {
        padding: 20,
    },
    title: {
        fontSize: 26,
        fontWeight: 'bold',
        color: '#fff',
        marginBottom: 20,
    },
    content: {
        fontSize: 16,
        color: '#ccc',
        lineHeight: 24,
        marginBottom: 30,
    },
});

export default NewsDetailScreen;