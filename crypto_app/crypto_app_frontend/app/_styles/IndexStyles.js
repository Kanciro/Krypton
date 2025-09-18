import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000042',
    alignItems: 'center',
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
    backgroundColor: '#000099',
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
    backgroundColor: '#000099',
  },
  activeTimeButton: {
    backgroundColor: '#00DBC3',
  },
  timeButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
});

export default styles;