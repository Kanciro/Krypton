import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, TextInput, ScrollView, Alert, ActivityIndicator } from 'react-native';
import { UserLogic } from '../_services/UserLogic'; // Ajusta la ruta a tu estructura de proyecto
import styles from '../_styles/UserStyles'; // Ajusta la ruta
import { router } from 'expo-router';
import Header from '../_components/header';
import MenuModal from '../_components/MenuModal';

export default function UsuarioScreen() {
  const {
    nombreUsuario,
    formData,
    handleChange,
    handleUpdateUser,
    handleRequestUpdateEmail,
    handleVerifyUpdateEmail,
    handleActualizarPassword,
    handleResetPassword,
    handleDesactivarUsuario,
    handleReactivarUsuario,
    handleLogout,
    message,
    isLoading,
    bottomSheetRef, // <-- Desestructurado del hook
    handleOpenMenu, // <-- Desestructurado del hook
  } = UserLogic();

  // Cerrar el menú después de navegar
  const menuOptions = [
    { label: 'Ir a Inicio', action: () =>  router.push('/')},
    { label: 'Noticias', action: () =>  router.push('/screens/news')},
    { label: 'Conversión de Monedas', action: () =>  router.push('/screens/conversion')},
    { label: 'Acerca de', action: () => Alert.alert('Info', 'Información sobre Krypton')},
    { label: 'Contacto', action: () => Alert.alert('Contacto', 'Contacto de soporte')},
  ];

return (
  <View style={styles.main}> 
  <Header onMenuPress={handleOpenMenu} /> {/* <-- Se pasa el handler para abrir el menú */}
    <ScrollView contentContainerStyle={styles.container}>
  
      <Text style={styles.greeting}>
        ¡Bienvenido, {nombreUsuario}! 👋
      </Text>
      <Text style={styles.info}>
        Gestiona tu perfil de usuario.
      </Text>

      {/* Mensajes de estado */}
      {message && (
        <Text style={[styles.message, isLoading && styles.loadingMessage]}>
          {message}
        </Text>
      )}

      {isLoading && <ActivityIndicator size="large" color="#0000ff" />}

        {/* Sección de Actualizar Usuario */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Actualizar Perfil</Text>
          <TextInput
            style={styles.input}
            placeholder="Nuevo nombre"
            placeholderTextColor="#ffffff"
            value={formData.nombre}
            onChangeText={(text) => handleChange('nombre', text)}
          />
          <TextInput
            style={styles.input}
            placeholder="Nuevo correo"
            placeholderTextColor="#ffffff"
            value={formData.correo}
            onChangeText={(text) => handleChange('correo', text)}
            keyboardType="email-address"
          />
          <TextInput
            style={styles.input}
            placeholder="Fecha de nacimiento (YYYY-MM-DD)"
            placeholderTextColor="#ffffff"
            value={formData.fecha_nacimiento}
            onChangeText={(text) => handleChange('fecha_nacimiento', text)}
          />
          <TextInput
            style={styles.input}
            placeholder="Contraseña actual"
            placeholderTextColor="#ffffff"
            value={formData.contrasena}
            onChangeText={(text) => handleChange('contrasena', text)}
            secureTextEntry
          />
          <TouchableOpacity style={styles.button} onPress={handleUpdateUser} disabled={isLoading}>
            <Text style={styles.buttonText}>Actualizar Perfil</Text>
          </TouchableOpacity>
        </View>

        {/* Sección de Cambio de Correo */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Cambiar Correo Electrónico</Text>
          <TextInput
            style={styles.input}
            placeholder="Nuevo correo electrónico"
            placeholderTextColor="#ffffff"
            value={formData.nuevo_correo}
            onChangeText={(text) => handleChange('nuevo_correo', text)}
            keyboardType="email-address"
          />
          <TouchableOpacity style={styles.button} onPress={handleRequestUpdateEmail} disabled={isLoading}>
            <Text style={styles.buttonText}>Solicitar Código</Text>
          </TouchableOpacity>
          <TextInput
            style={styles.input}
            placeholder="Código de verificación"
            placeholderTextColor="#ffffff"
            value={formData.codigo}
            onChangeText={(text) => handleChange('codigo', text)}
          />
          <TouchableOpacity style={styles.button} onPress={handleVerifyUpdateEmail} disabled={isLoading}>
            <Text style={styles.buttonText}>Verificar Código</Text>
          </TouchableOpacity>
        </View>

        {/* Sección de Cambio de Contraseña */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Restablecer Contraseña</Text>
          <TextInput
            style={styles.input}
            placeholder="Tu correo para restablecer"
            placeholderTextColor="#ffffff"
            value={formData.correo}
            onChangeText={(text) => handleChange('correo', text)}
            keyboardType="email-address"
          />
          <TouchableOpacity style={styles.button} onPress={handleActualizarPassword} disabled={isLoading}>
            <Text style={styles.buttonText}>Solicitar Restablecimiento</Text>
          </TouchableOpacity>
          <TextInput
            style={styles.input}
            placeholder="Token de restablecimiento"
            placeholderTextColor="#ffffff"
            value={formData.token}
            onChangeText={(text) => handleChange('token', text)}
          />
          <TextInput
            style={styles.input}
            placeholder="Nueva contraseña"
            placeholderTextColor="#ffffff"
            value={formData.nueva_contrasena}
            onChangeText={(text) => handleChange('nueva_contrasena', text)}
            secureTextEntry
          />
          <TouchableOpacity style={styles.button} onPress={handleResetPassword} disabled={isLoading}>
            <Text style={styles.buttonText}>Restablecer Contraseña</Text>
          </TouchableOpacity>
        </View>

        {/* Botones de Desactivar y Reactivar */}
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={[styles.button, styles.deactivateButton]} onPress={handleDesactivarUsuario} disabled={isLoading}>
            <Text style={styles.buttonText}>Desactivar Usuario</Text>
          </TouchableOpacity>
          <TouchableOpacity style={[styles.button, styles.reactivateButton]} onPress={handleReactivarUsuario} disabled={isLoading}>
            <Text style={styles.buttonText}>Reactivar Usuario</Text>
          </TouchableOpacity>
        </View>

        <TouchableOpacity style={[styles.logoutBtn, { marginTop: 20 }]} onPress={handleLogout} disabled={isLoading}>
          <Text style={styles.logoutText}>Cerrar Sesión</Text>
        </TouchableOpacity>
      </ScrollView>
      <MenuModal options={menuOptions} bottomSheetRef={bottomSheetRef}/> {/* <-- Se pasa la ref al MenuModal */}
    </View>
  );
}