import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  main: {
    backgroundColor: '#000042',
    paddingBottom: '50%',
    alignItems: 'center',
    position: 'absolute',
    height: '100%',
    width: '100%',
  },
  container: {
    backgroundColor: '#7600a6',
    marginTop: 20,
    paddingTop: 15,
    paddingLeft: 44,
    paddingRight: 44,
    paddingBottom: 20,
    width: 'auto',
    height: 'auto',
    alignItems: 'center',
  },
  SubContainer: {
    backgroundColor: '#7600a6',
    marginTop: 20,
    paddingTop: 15,
    paddingLeft: 70,
    paddingRight: 70,
    paddingBottom: 20,
    alignItems: 'center',
  },
  title: {
    fontWeight: 'bold',
    fontSize: 30,
    color: '#fff',
    marginBottom: 10,
  },
  inputText: {
    width: '130%',
    backgroundColor: 'rgba(0, 0, 153, 0.69)',
    height: 20,
    marginBottom: 5,
    justifyContent: 'center',
    padding: 20,
  },
  loginBtn: {
    width: '130%',
    backgroundColor: '#0adbc3',
    height: 50,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 5,
    marginBottom: 10,
  },
  loginText: {
    color: 'white',
    fontWeight: 'bold',
  },
  forgot: {
    color: 'white',
    fontSize: 12,
  },
  register: {
    color: '#0adbc3',
    marginTop: 0,
    fontSize: 14,
  },
  register_text: {
    color: 'white',
    marginTop: 0,
    fontSize: 14,
  },
});

export default styles;