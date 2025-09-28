import { useState, useEffect } from 'react';
import Constants from 'expo-constants';

// Define la interfaz de la noticia para tipado (mantenemos la interfaz aquí para que el hook sea autocontenido)
export interface Noticia {
    id_noticias: number;
    titulo: string;
    url: string;
    contenido: string;
}

// Define la interfaz del valor que devolverá el hook
interface UseNewsResult {
    noticias: Noticia[];
    loading: boolean;
    error: string | null;
    refetch: () => void; // Función para reintentar la carga si es necesario
}

const useNews = (): UseNewsResult => {
    const [noticias, setNoticias] = useState<Noticia[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Asume que la URL base de tu backend está configurada en expo-constants
    const API_URL = Constants.expoConfig?.extra?.API_URL;

    const fetchNoticias = async () => {
        setLoading(true); // Siempre empieza la carga
        setError(null); // Resetea el error
        
        if (!API_URL) {
            setError("Error: La URL de la API no está configurada.");
            setLoading(false);
            return;
        }

        try {
            // Reemplaza con el endpoint real de tu backend
            const response = await fetch(`${API_URL}/noticias/`); 
            
            if (!response.ok) {
                throw new Error(`Error en la respuesta: ${response.status} ${response.statusText}`);
            }
            
            const data: Noticia[] = await response.json();
            setNoticias(data);
        } catch (err) {
            console.error('Error al obtener las noticias:', err);
            // Cast 'err' a Error para acceder a 'message'
            setError(err instanceof Error ? err.message : 'Error desconocido al cargar noticias.');
            setNoticias([]); // Limpia las noticias en caso de error
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchNoticias();
    }, []); // Se ejecuta solo una vez al montar

    // Función que permite al componente llamar a la recarga manualmente
    const refetch = () => {
        fetchNoticias();
    };

    return { 
        noticias, 
        loading, 
        error, 
        refetch 
    };
};

export default useNews;