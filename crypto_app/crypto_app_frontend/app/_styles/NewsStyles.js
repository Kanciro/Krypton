import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000042',
    alignItems: 'center',
  },
  listContent: {
    paddingHorizontal: 10,
    paddingBottom: 20, // Espacio al final de la lista
  },
  newsCard: {
    backgroundColor: '#000099', // Color de fondo de la tarjeta
    padding: 15,
    borderRadius: 10,
    marginBottom: 15,
    width: '100%',
    shadowColor: '#00DBC3', // Sombra suave para darle relieve
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
    borderWidth: 1,
    borderColor: '#00DBC3', // Borde para resaltar
  },
  newsCardTitle: {
    fontSize: 18,
    color: '#fff',
    fontWeight: 'bold',
    marginBottom: 8,
  },
  newsCardContent: {
    fontSize: 14,
    color: '#ccc', // Texto de contenido más claro
    marginBottom: 10,
  },
  newsCardReadMore: {
    fontSize: 14,
    color: '#00DBC3', // Color de acento para el "Leer más"
    fontWeight: 'bold',
    textAlign: 'right',
  },
  emptyListText: {
    color: '#fff',
    textAlign: 'center',
    marginTop: 50,
    fontSize: 16,
  }
});

export default styles;