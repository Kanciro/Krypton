import React from 'react';
import { TouchableOpacity, Text, View, StyleSheet } from 'react-native';

interface Noticia {
    id_noticias: number;
    titulo: string;
    url: string;
    contenido: string;
}

interface NewsCardProps {
    noticia: Noticia;
    onPress: () => void;
}

// Función para obtener un fragmento del contenido
const getSnippet = (text: string, maxLength: number = 100): string => {
    if (text.length <= maxLength) {
        return text;
    }
    return text.substring(0, maxLength).trim() + '...';
};

const NewsCard: React.FC<NewsCardProps> = ({ noticia, onPress }) => {
    const snippet = getSnippet(noticia.contenido);

    return (
        <TouchableOpacity style={cardStyles.card} onPress={onPress}>
            <Text style={cardStyles.title}>{noticia.titulo}</Text>
            <Text style={cardStyles.content}>{snippet}</Text>
            <Text style={cardStyles.readMore}>Leer más »</Text>
        </TouchableOpacity>
    );
};

const cardStyles = StyleSheet.create({
    card: {
        backgroundColor: '#000099', // Color de fondo similar a los botones
        width: '90%',
        padding: 15,
        borderRadius: 8,
        marginBottom: 15,
        shadowColor: '#00DBC3', // Sombra para un efecto más *pop*
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.8,
        shadowRadius: 2,
        elevation: 5,
    },
    title: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#fff',
        marginBottom: 8,
    },
    content: {
        fontSize: 14,
        color: '#ccc',
        marginBottom: 10,
    },
    readMore: {
        fontSize: 12,
        color: '#00DBC3', // Color de acento
        fontWeight: 'bold',
        textAlign: 'right',
    }
});

export default NewsCard;