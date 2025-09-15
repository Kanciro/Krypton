import React, { forwardRef, useMemo } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import BottomSheet from '@gorhom/bottom-sheet';

// Usamos forwardRef para permitir que el componente padre acceda a los métodos del BottomSheet
const Menu = forwardRef((props, ref) => {
  // Define los "puntos de anclaje" para el menú (qué tan alto se abrirá)
  const snapPoints = useMemo(() => ['10%', '50%', '90%'], []);

  return (
    <BottomSheet
      ref={ref}
      index={-1} // Comienza oculto
      snapPoints={snapPoints}
      enablePanDownToClose={true} // Permite deslizar hacia abajo para cerrar
      containerStyle={styles.container}
      backgroundStyle={styles.background}
    >
      <View style={styles.content}>
        <Text style={styles.menuTitle}>Menú</Text>
        {/* Aquí puedes agregar los elementos de tu menú */}
        <Text style={styles.menuItem}>Opción 1</Text>
        <Text style={styles.menuItem}>Opción 2</Text>
        <Text style={styles.menuItem}>Opción 3</Text>
      </View>
    </BottomSheet>
  );
});

const styles = StyleSheet.create({
  container: {
      
  },
  background: {
    backgroundColor: '#7600a6', 
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
  },
  content: {
    padding: 20,
  },
  menuTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 10,
  },
  menuItem: {
    fontSize: 18,
    color: 'white',
    paddingVertical: 10,
  },
});

export default Menu;