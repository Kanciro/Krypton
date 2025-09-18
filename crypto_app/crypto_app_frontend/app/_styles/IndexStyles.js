import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    height:'100%',
    backgroundColor: '#000033',
  },
  title: {
    fontSize: 28,
    color: '#fff',
    marginBottom: 20,
    marginTop: '90%',
    fontWeight: 'bold',
  },
  button: {
    backgroundColor: '#00ffff',
    paddingVertical: 15,
    paddingHorizontal: 30,
    borderRadius: 5,
    marginBlockStart:10,
  },
  buttonText: {
    color: '#000',
    fontSize: 18,
    fontWeight: 'bold',
  },
  menubutton: {
    backgroundColor: '#00ffff',
    flexDirection: 'row',
    alignItems: 'center',
  },
  container: {
    flex: 1,
    backgroundColor: '#000033',
    alignItems: 'center',
    paddingTop: 50,
  },
  title: {
    fontSize: 24,
    color: '#fff',
    marginBottom: 20,
    fontWeight: 'bold',
  },
  pickerContainer: {
    width: '90%',
    marginBottom: 10,
  },
  pickerLabel: {
    color: '#fff',
    fontSize: 16,
    marginBottom: 5,
  },
  picker: {
    height: 50,
    width: '100%',
    color: '#fff',
    backgroundColor: '#1a1a4d',
    borderRadius: 5,
  },
  buttonGroup: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '90%',
    marginBottom: 20,
  },
  timeButton: {
    paddingVertical: 10,
    paddingHorizontal: 15,
    borderRadius: 5,
    backgroundColor: '#1a1a4d',
  },
  activeTimeButton: {
    backgroundColor: '#00ffff',
  },
  timeButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
});

export default styles;