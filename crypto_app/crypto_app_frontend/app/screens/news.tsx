import React from 'react';
import { Text, View, ScrollView, ActivityIndicator, Alert } from 'react-native';
import { router } from 'expo-router'; 
import Header from '../_components/header';
import MenuModal from '../_components/MenuModal';
import NewsCard from '../_components/NewsCard';
import styles from '../_styles/NewsStyles';
import useNews, { Noticia } from '../_services/NewsLogic'; // Asegúrate de la ruta correcta

const NewsScreen = () => {
    const { 
        noticias, 
        loading, 
        error, 
        refetch 
    } = useNews();

    const handleCardPress = (noticia: Noticia) => {
        router.push({
            pathname: '/screens/newsDetail', 
            params: { 
                id: noticia.id_noticias.toString(),
                titulo: noticia.titulo,
                contenido: noticia.contenido,
                url: noticia.url,
            }
        });
    };

    const menuOptions = [
        { label: 'Gestionar Usuario', action: () => router.push('/screens/user') },
        { label: 'Conversión de Monedas', action: () => router.push('/screens/conversion') },
        { label: 'Inicio', action: () => router.push('/') },
        { label: 'Acerca de', action: () => alert('Info sobre Krypton') },
        { label: 'Contacto', action: () => alert('Contacto de soporte') },
    ];
    
    // Opcionalmente, puedes mostrar el error usando una alerta si el hook lo retorna
    if (error) {
        Alert.alert(
            "Error de Carga",
            `No pudimos obtener las noticias. ¿Quieres reintentar?\nDetalle: ${error}`,
            [
                { text: "Cancelar", style: "cancel" },
                { text: "Reintentar", onPress: refetch }
            ]
        );
    }

    return (
        <View style={styles.container}>
            <Header />
            <Text style={styles.title}>Últimas Noticias</Text>
            
            {loading ? (
                <ActivityIndicator size="large" color="#00DBC3" style={{ marginTop: 50 }} />
            ) : (
                <ScrollView contentContainerStyle={{ paddingBottom: 20, width: '100%', alignItems: 'center' }}>
                    {/* Se muestran noticias solo si no hay error y hay datos */}
                    {noticias.map((noticia) => (
                        <NewsCard 
                            key={noticia.id_noticias}
                            noticia={noticia}
                            onPress={() => handleCardPress(noticia)}
                        />
                    ))}
                    
                    {/* Mensaje si no hay noticias (y no hay error) */}
                    {noticias.length === 0 && !error && (
                        <Text style={styles.emptyListText}>No se encontraron noticias.</Text>
                    )}
                </ScrollView>
            )}
            
            <MenuModal options={menuOptions} />
        </View>
    );
};

export default NewsScreen;