// frontend/src/App.jsx
// Cross-platform React Native app for RelayPoint Elite

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { Platform, View, StyleSheet } from 'react-native';
import ThemeToggle from './components/ThemeToggle';
import Logo from './components/Logo';
import LoginForm from './components/LoginForm';
import Dashboard from './components/Dashboard';
import useAuth from './hooks/useAuth';

const Stack = createStackNavigator();

export default function App() {
  const { isAuthenticated } = useAuth();

  return (
    <NavigationContainer>
      <View style={styles.container}>
        <View style={styles.header}>
          <Logo style={styles.logo} />
          <ThemeToggle />
        </View>
        
        <Stack.Navigator
          screenOptions={{
            headerShown: false,
            cardStyle: { backgroundColor: 'transparent' },
          }}
        >
          {!isAuthenticated ? (
            <Stack.Screen name="Login" component={LoginForm} />
          ) : (
            <Stack.Screen name="Dashboard" component={Dashboard} />
          )}
        </Stack.Navigator>
      </View>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Platform.select({
      web: '#ffffff',
      default: '#f5f5f5',
    }),
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: Platform.select({
      web: '#ffffff',
      default: 'transparent',
    }),
  },
  logo: {
    height: 48,
    width: 'auto',
  },
});
