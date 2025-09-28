import React from 'react';
import { View, Text, ScrollView, Linking, Button, StyleSheet } from 'react-native';
import { useLocalSearchParams, router } from 'expo-router';
import Header from '../_components/header';

const NewsDetailScreen = () => {
    // Obtiene los parámetros pasados desde la tarjeta
    const params = useLocalSearchParams();
    const { titulo, contenido, url } = params;

    // Puedes manejar la navegación de regreso
    const handleGoBack = () => {
        router.back();
    };

    return (
        <View style={detailStyles.container}>
            <Header showBackButton={true} onBackPress={handleGoBack} />
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