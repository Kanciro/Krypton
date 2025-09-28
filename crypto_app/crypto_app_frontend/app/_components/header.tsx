import React from 'react';
import { View, Text, StyleSheet, SafeAreaView, TouchableOpacity, Image } from 'react-native';
import { router } from 'expo-router';

import logo from '../assets/logo.png'; 
import krypton from '../assets/krypton.png';
import bell from '../assets/bell.png';

const Header = () => {
  return (
    <View style={styles.headerContainer}>
      {/* Se cambió la ruta de '../index' a '/' para asegurar una navegación confiable
        a la pantalla principal, sin importar dónde se utilice el componente Header.
      */}
      <TouchableOpacity 
        style={styles.bellButton} 
        onPress={() => router.push('/')}
      >
        <Image 
          source={logo} 
          style={styles.logoImage} 
        />
      </TouchableOpacity>
      <Image 
        source={krypton} 
        style={styles.krypton} 
      />
      <TouchableOpacity 
        style={styles.bellButton} 
        onPress={() => router.push('/screens/register')} 
      >
        <Image 
          source={bell} 
          style={styles.bellImage} 
        />
      </TouchableOpacity>
    </View> 
  );
};

const styles = StyleSheet.create({
  headerContainer: {
    alignItems: 'center',
    height: 80, 
    width: '100%',
    backgroundColor: '#000099',
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 10,
  },
  logoImage: {
    height: '100%',
    aspectRatio: 1, 
    resizeMode: 'contain',
  },
  krypton: {
    height: '170%',
    width: '50%', 
    resizeMode: 'contain',
  },
  bellButton: {
    height: '100%',
    aspectRatio: 1, 
    resizeMode: 'contain',
  },
  bellImage: {
    height: '100%',
    width: '100%',
    resizeMode: 'contain',
  }
});

export default Header;