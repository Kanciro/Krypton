import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  main: {
    flex: 1, // Ocupa toda la pantalla
    backgroundColor: '#000042',
  },
  contentContainer: {
    flex: 1, 
    marginTop: 50,
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  container: {
    backgroundColor: '#7600a6',
    width: '80%',
    padding: 20,
    alignItems: 'center',
    marginBottom: 20, 
  },
  SubContainer: {
    backgroundColor: '#7600a6',
    padding: 20,
    width: '80%',
    alignItems: 'center',
  },
  title: {
    fontWeight: 'bold',
    fontSize: 30,
    color: '#fff',
    marginBottom: 7,
  },
  inputText: {
    width: '100%',
    backgroundColor: 'rgba(0, 0, 153, 0.69)',
    paddingHorizontal: 15,
    paddingVertical: 10,
    marginBottom: 4,
    color: '#fff',
    borderRadius: 5,
  },
  loginBtn: {
    width: '100%',
    backgroundColor: '#0adbc3',
    height: 50,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 10,
    borderRadius: 5,
  },
  loginText: {
    color: 'white',
    fontWeight: 'bold',
  },
  forgot: {
    color: 'white',
    fontSize: 12,
    marginTop: 10,
  },
  register: {
    color: '#0adbc3',
    marginTop: 5,
    fontSize: 14,
  },
  register_text: {
    color: 'white',
    marginTop: 5,
    fontSize: 14,
  },
});

export default styles;