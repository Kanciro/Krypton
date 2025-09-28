import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  main: {
    flex: 1,
    backgroundColor: '#000042',
  },
  container: {
    flexGrow: 1,
    padding: 20,
    backgroundColor: '#000042',
    paddingBottom: 100,
  },
  greeting: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#ffffffff',
    textAlign: 'center',
    marginBottom: 10,
  },
  info: {
    fontSize: 16,
    color: '#ffffffff',
    textAlign: 'center',
    marginBottom: 20,
  },
  message: {
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
    padding: 10,
    backgroundColor: '#e0e0e0',
    borderRadius: 8,
  },
  loadingMessage: {
    color: '#0000ff',
  },
  section: {
    backgroundColor: '#7600A9',
    borderRadius: 10,
    padding: 20,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#ffffffff',
    marginBottom: 15,
  },
  input: {
    height: 50,
    borderColor: '#000099',
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 15,
    marginBottom: 15,
    backgroundColor: '#000099',
  },
  button: {
    backgroundColor: '#00DBC3',
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 10,
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  deactivateButton: {
    backgroundColor: '#ff0000e5',
    flex: 1,
    marginRight: 5,
  },
  reactivateButton: {
    backgroundColor: '#00DBC3',
    flex: 1,
    marginLeft: 5,
  },
  logoutBtn: {
    backgroundColor: '#00DBC3',
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  logoutText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
});

export default styles;