import React, { useState } from 'react';
import { StyleSheet, Text, TouchableOpacity, View, Image} from 'react-native';
import Modal from 'react-native-modal';
import menu from '../assets/menu.png'; 
import flecha from '../assets/flecha.png';

interface MenuModalProps {
  // Ya no necesitamos isVisible y onClose aquí, el componente lo manejará
  options: { label: string; action: () => void }[];
}

const MenuModal = ({ options }: MenuModalProps) => {
  const [isModalVisible, setModalVisible] = useState(false);

  const toggleModal = () => {
    setModalVisible(!isModalVisible);
  };

  return (
    <>
      {/* Botón para abrir el menú, que ahora es parte del componente */}
      <TouchableOpacity style={styles.menuButton} onPress={toggleModal}>
        <View style={styles.titleMenu}>
            <Image 
              source={flecha} 
              style={styles.flechaImage} 
            />
            <Image 
              source={menu} 
              style={styles.menuImage} 
            />
              
            <Image 
              source={flecha} 
              style={styles.flechaImage} 
            />
          </View>
      </TouchableOpacity>

      {/* El modal se mostrará si isModalVisible es true */}
      <Modal
        isVisible={isModalVisible}
        onBackdropPress={toggleModal}
        onBackButtonPress={toggleModal}
        style={styles.modal}
        animationIn="slideInUp"
        animationOut="slideOutDown"
      >
        <View style={styles.menuContainer}>
          <View style={styles.titleMenu}>
            <Image 
              source={flecha} 
              style={styles.flechaImageMenu} 
            />
            <Image 
              source={menu} 
              style={styles.menuImage} 
            />
              
            <Image 
              source={flecha} 
              style={styles.flechaImageMenu} 
            />
          </View>
          {options.map((option, index) => (
            <TouchableOpacity
              key={index}
              style={styles.optionButton}
              onPress={() => {
                option.action();
                toggleModal(); // Cierra el modal después de la acción
              }}
            >
              <Text style={styles.optionText}>{option.label}</Text>
            </TouchableOpacity>
          ))}
          <TouchableOpacity style={styles.closeButton} onPress={toggleModal}>
            <Text style={styles.closeButtonText}>Cerrar</Text>
          </TouchableOpacity>
        </View>
      </Modal>
    </>
  );
};

const styles = StyleSheet.create({
  menuButton: {
    flexDirection: 'row',
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#0adbc3',
    marginBottom: 10,
    position: 'absolute',
    width: '100%',
    height: 60,
    paddingBottom: 80,
    bottom: 0, // A 10 píxeles de la parte inferior
  },
  menuButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  flechaImage: {
    height: '70%',
    width: '50%', 
    resizeMode: 'contain',
  },
  modal: {
    justifyContent: 'flex-end',
    margin: 0,
  },
  menuContainer: {
    backgroundColor: '#000099',
    paddingTop: 70,
    alignItems: 'center',
    width: '100%',
    bottom: 0,
    paddingBottom: 4,
  },
  titleMenu: {
    flexDirection: 'row',
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#0adbc3',
    marginBottom: 10,
    position: 'absolute',
    width: '100%',
    height: 60,
  },
  flechaImageMenu: {
    height: '70%',
    width: '50%', 
    resizeMode: 'contain',
    transform: [{ rotate: '180deg' }],
  },
  menuImage: {
    height: '100%',
    width: '30%', 
    resizeMode: 'contain',
    marginBottom: 10,
  },
  optionButton: {
    width: '100%',
    padding: 15,
    marginVertical: 5,
    backgroundColor: '#7600A9',
    borderRadius: 10,
    alignItems: 'center',
  },
  optionText: {
    fontSize: 18,
    color: '#fff',
  },
  closeButton: {
    marginTop: 20,
    width: '100%',
    padding: 15,
    backgroundColor: '#7600A9',
    borderRadius: 10,
    alignItems: 'center',
  },
  closeButtonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
});

export default MenuModal;