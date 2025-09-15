import React from 'react';
import { View, Text, StyleSheet, SafeAreaView, TouchableOpacity, Image } from 'react-native';
import logo from '../assets/logo.png'; 
import krypton from '../assets/krypton.png';
import bell from '../assets/bell.png';

const Header = () => {
    return (
        <View style={styles.headerContainer}>
            <View style={styles.logo}>
              <Image 
                source={logo} 
                style={styles.logoImage} 
              />
            </View>
            <View>
              <Image 
                source={krypton} 
                style={styles.krypton} 
              />
            </View>
            <View>
              <TouchableOpacity style={styles.bell} >
                <Image 
                source={bell} 
                style={styles.bell} 
                />
              </TouchableOpacity>
            </View>
        </View> 
    );
};

const styles = StyleSheet.create({
    headerContainer: {
      alignItems: 'center',
      height: 100,
      width: '100%',
      backgroundColor: '#000099',
      flexDirection: 'row',
      justifyContent: 'space-between',
    },
    logoImage: {
      height:100,
      width:100,
      resizeMode: 'contain',
    },
    krypton: {
      width:300,
      resizeMode: 'contain',
    },
    bell: {
      width:120,
      resizeMode: 'contain',
    },
});

export default Header;