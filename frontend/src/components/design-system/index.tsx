"""
Enterprise Design System - Material Design 3 Components
Polished, accessible, and production-ready UI components for RelayPoint
"""

import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Animated,
  Platform,
  Image,
} from 'react-native';
import LinearGradient from 'expo-linear-gradient';

// Enterprise Color Palette - Material Design 3
export const Colors = {
  // Primary Brand Colors
  primary: {
    50: '#E8F5E9',
    100: '#C8E6C9',
    200: '#A5D6A7',
    300: '#81C784',
    400: '#66BB6A',
    500: '#4CAF50',  // Main brand color
    600: '#43A047',
    700: '#388E3C',
    800: '#2E7D32',
    900: '#1B5E20',
  },
  
  // Secondary Colors
  secondary: {
    50: '#E3F2FD',
    100: '#BBDEFB',
    200: '#90CAF9',
    300: '#64B5F6',
    400: '#42A5F5',
    500: '#2196F3',
    600: '#1E88E5',
    700: '#1976D2',
    800: '#1565C0',
    900: '#0D47A1',
  },
  
  // Neutral/Grayscale
  neutral: {
    0: '#FFFFFF',
    50: '#FAFAFA',
    100: '#F5F5F5',
    200: '#EEEEEE',
    300: '#E0E0E0',
    400: '#BDBDBD',
    500: '#9E9E9E',
    600: '#757575',
    700: '#616161',
    800: '#424242',
    900: '#212121',
    1000: '#000000',
  },
  
  // Semantic Colors
  success: {
    light: '#81C784',
    main: '#4CAF50',
    dark: '#388E3C',
    contrast: '#FFFFFF',
  },
  
  error: {
    light: '#E57373',
    main: '#F44336',
    dark: '#D32F2F',
    contrast: '#FFFFFF',
  },
  
  warning: {
    light: '#FFB74D',
    main: '#FF9800',
    dark: '#F57C00',
    contrast: '#000000',
  },
  
  info: {
    light: '#64B5F6',
    main: '#2196F3',
    dark: '#1976D2',
    contrast: '#FFFFFF',
  },
  
  // Surface Colors
  surface: {
    base: '#FFFFFF',
    elevated: '#F5F5F5',
    overlay: 'rgba(0, 0, 0, 0.5)',
  },
  
  // Background Colors
  background: {
    default: '#FAFAFA',
    paper: '#FFFFFF',
  },
  
  // Text Colors
  text: {
    primary: 'rgba(0, 0, 0, 0.87)',
    secondary: 'rgba(0, 0, 0, 0.60)',
    disabled: 'rgba(0, 0, 0, 0.38)',
    hint: 'rgba(0, 0, 0, 0.38)',
  },
};

// Typography System
export const Typography = {
  // Display
  displayLarge: {
    fontSize: 57,
    lineHeight: 64,
    fontWeight: '400',
    letterSpacing: -0.25,
  },
  displayMedium: {
    fontSize: 45,
    lineHeight: 52,
    fontWeight: '400',
    letterSpacing: 0,
  },
  displaySmall: {
    fontSize: 36,
    lineHeight: 44,
    fontWeight: '400',
    letterSpacing: 0,
  },
  
  // Headline
  headlineLarge: {
    fontSize: 32,
    lineHeight: 40,
    fontWeight: '400',
    letterSpacing: 0,
  },
  headlineMedium: {
    fontSize: 28,
    lineHeight: 36,
    fontWeight: '400',
    letterSpacing: 0,
  },
  headlineSmall: {
    fontSize: 24,
    lineHeight: 32,
    fontWeight: '400',
    letterSpacing: 0,
  },
  
  // Title
  titleLarge: {
    fontSize: 22,
    lineHeight: 28,
    fontWeight: '500',
    letterSpacing: 0,
  },
  titleMedium: {
    fontSize: 16,
    lineHeight: 24,
    fontWeight: '500',
    letterSpacing: 0.15,
  },
  titleSmall: {
    fontSize: 14,
    lineHeight: 20,
    fontWeight: '500',
    letterSpacing: 0.1,
  },
  
  // Body
  bodyLarge: {
    fontSize: 16,
    lineHeight: 24,
    fontWeight: '400',
    letterSpacing: 0.5,
  },
  bodyMedium: {
    fontSize: 14,
    lineHeight: 20,
    fontWeight: '400',
    letterSpacing: 0.25,
  },
  bodySmall: {
    fontSize: 12,
    lineHeight: 16,
    fontWeight: '400',
    letterSpacing: 0.4,
  },
  
  // Label
  labelLarge: {
    fontSize: 14,
    lineHeight: 20,
    fontWeight: '500',
    letterSpacing: 0.1,
  },
  labelMedium: {
    fontSize: 12,
    lineHeight: 16,
    fontWeight: '500',
    letterSpacing: 0.5,
  },
  labelSmall: {
    fontSize: 11,
    lineHeight: 16,
    fontWeight: '500',
    letterSpacing: 0.5,
  },
};

// Spacing System (8px base)
export const Spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 40,
  xxxl: 48,
};

// Border Radius
export const BorderRadius = {
  none: 0,
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  xxl: 24,
  full: 9999,
};

// Shadows (Material Design 3 Elevation)
export const Shadows = {
  none: {
    shadowColor: 'transparent',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0,
    shadowRadius: 0,
    elevation: 0,
  },
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.18,
    shadowRadius: 1.0,
    elevation: 1,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.20,
    shadowRadius: 2.62,
    elevation: 4,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.23,
    shadowRadius: 4.65,
    elevation: 8,
  },
  xl: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.27,
    shadowRadius: 6.27,
    elevation: 12,
  },
};

// Button Component (Enterprise-grade)
export const Button = ({
  variant = 'filled',
  size = 'medium',
  color = 'primary',
  onPress,
  disabled = false,
  loading = false,
  icon,
  children,
  style,
  ...props
}) => {
  const getButtonStyle = () => {
    const base = {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'center',
      borderRadius: BorderRadius.full,
      ...getSizeStyles(),
    };

    switch (variant) {
      case 'filled':
        return {
          ...base,
          backgroundColor: disabled ? Colors.neutral[300] : Colors[color].main,
          ...Shadows.sm,
        };
      case 'outlined':
        return {
          ...base,
          backgroundColor: 'transparent',
          borderWidth: 1,
          borderColor: disabled ? Colors.neutral[300] : Colors[color].main,
        };
      case 'text':
        return {
          ...base,
          backgroundColor: 'transparent',
        };
      case 'elevated':
        return {
          ...base,
          backgroundColor: Colors.surface.base,
          ...Shadows.md,
        };
      default:
        return base;
    }
  };

  const getSizeStyles = () => {
    switch (size) {
      case 'small':
        return {
          paddingHorizontal: Spacing.md,
          paddingVertical: Spacing.xs,
          minHeight: 32,
        };
      case 'medium':
        return {
          paddingHorizontal: Spacing.lg,
          paddingVertical: Spacing.sm,
          minHeight: 40,
        };
      case 'large':
        return {
          paddingHorizontal: Spacing.xl,
          paddingVertical: Spacing.md,
          minHeight: 48,
        };
      default:
        return {};
    }
  };

  const getTextStyle = () => {
    const base = {
      ...Typography.labelLarge,
      fontWeight: '600',
    };

    switch (variant) {
      case 'filled':
        return {
          ...base,
          color: Colors[color].contrast,
        };
      case 'outlined':
      case 'text':
        return {
          ...base,
          color: disabled ? Colors.text.disabled : Colors[color].main,
        };
      case 'elevated':
        return {
          ...base,
          color: Colors[color].main,
        };
      default:
        return base;
    }
  };

  return (
    <TouchableOpacity
      style={[getButtonStyle(), style]}
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.7}
      {...props}
    >
      {icon && <View style={{ marginRight: Spacing.xs }}>{icon}</View>}
      <Text style={getTextStyle()}>{loading ? 'Loading...' : children}</Text>
    </TouchableOpacity>
  );
};

// Card Component
export const Card = ({
  variant = 'elevated',
  children,
  onPress,
  style,
  ...props
}) => {
  const getCardStyle = () => {
    const base = {
      backgroundColor: Colors.surface.base,
      borderRadius: BorderRadius.lg,
      padding: Spacing.md,
    };

    switch (variant) {
      case 'elevated':
        return {
          ...base,
          ...Shadows.md,
        };
      case 'outlined':
        return {
          ...base,
          borderWidth: 1,
          borderColor: Colors.neutral[300],
        };
      case 'filled':
        return {
          ...base,
          backgroundColor: Colors.neutral[100],
        };
      default:
        return base;
    }
  };

  if (onPress) {
    return (
      <TouchableOpacity
        style={[getCardStyle(), style]}
        onPress={onPress}
        activeOpacity={0.8}
        {...props}
      >
        {children}
      </TouchableOpacity>
    );
  }

  return (
    <View style={[getCardStyle(), style]} {...props}>
      {children}
    </View>
  );
};

// Text Input Component
export const TextInput = ({
  label,
  value,
  onChangeText,
  error,
  helperText,
  leftIcon,
  rightIcon,
  variant = 'outlined',
  style,
  ...props
}) => {
  const [isFocused, setIsFocused] = React.useState(false);

  const getInputContainerStyle = () => {
    const base = {
      borderRadius: BorderRadius.sm,
      paddingHorizontal: Spacing.md,
      paddingVertical: Spacing.sm,
      minHeight: 56,
      justifyContent: 'center',
    };

    switch (variant) {
      case 'outlined':
        return {
          ...base,
          borderWidth: 2,
          borderColor: error
            ? Colors.error.main
            : isFocused
            ? Colors.primary.main
            : Colors.neutral[300],
          backgroundColor: 'transparent',
        };
      case 'filled':
        return {
          ...base,
          backgroundColor: Colors.neutral[100],
          borderWidth: 0,
          borderBottomWidth: 2,
          borderBottomColor: error
            ? Colors.error.main
            : isFocused
            ? Colors.primary.main
            : Colors.neutral[300],
          borderRadius: BorderRadius.sm,
          borderBottomLeftRadius: 0,
          borderBottomRightRadius: 0,
        };
      default:
        return base;
    }
  };

  return (
    <View style={style}>
      {label && (
        <Text
          style={{
            ...Typography.bodySmall,
            color: error ? Colors.error.main : Colors.text.secondary,
            marginBottom: Spacing.xs,
          }}
        >
          {label}
        </Text>
      )}
      <View style={getInputContainerStyle()}>
        <View style={{ flexDirection: 'row', alignItems: 'center' }}>
          {leftIcon && (
            <View style={{ marginRight: Spacing.sm }}>{leftIcon}</View>
          )}
          <Text
            style={{
              flex: 1,
              ...Typography.bodyLarge,
              color: Colors.text.primary,
            }}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            {...props}
          >
            {value}
          </Text>
          {rightIcon && (
            <View style={{ marginLeft: Spacing.sm }}>{rightIcon}</View>
          )}
        </View>
      </View>
      {(error || helperText) && (
        <Text
          style={{
            ...Typography.bodySmall,
            color: error ? Colors.error.main : Colors.text.secondary,
            marginTop: Spacing.xs,
            marginLeft: Spacing.md,
          }}
        >
          {error || helperText}
        </Text>
      )}
    </View>
  );
};

// Badge Component
export const Badge = ({
  variant = 'filled',
  color = 'primary',
  size = 'medium',
  children,
  style,
  ...props
}) => {
  const getBadgeStyle = () => {
    const base = {
      paddingHorizontal: size === 'small' ? Spacing.xs : Spacing.sm,
      paddingVertical: size === 'small' ? 2 : 4,
      borderRadius: BorderRadius.full,
      alignSelf: 'flex-start',
    };

    switch (variant) {
      case 'filled':
        return {
          ...base,
          backgroundColor: Colors[color].main,
        };
      case 'outlined':
        return {
          ...base,
          borderWidth: 1,
          borderColor: Colors[color].main,
          backgroundColor: 'transparent',
        };
      case 'soft':
        return {
          ...base,
          backgroundColor: Colors[color][50],
        };
      default:
        return base;
    }
  };

  const getTextStyle = () => {
    const base = size === 'small' ? Typography.labelSmall : Typography.labelMedium;

    switch (variant) {
      case 'filled':
        return {
          ...base,
          color: Colors[color].contrast,
          fontWeight: '600',
        };
      case 'outlined':
      case 'soft':
        return {
          ...base,
          color: Colors[color].dark,
          fontWeight: '600',
        };
      default:
        return base;
    }
  };

  return (
    <View style={[getBadgeStyle(), style]} {...props}>
      <Text style={getTextStyle()}>{children}</Text>
    </View>
  );
};

// Avatar Component
export const Avatar = ({
  size = 'medium',
  source,
  name,
  backgroundColor,
  style,
  ...props
}) => {
  const getSize = () => {
    switch (size) {
      case 'small':
        return 32;
      case 'medium':
        return 40;
      case 'large':
        return 56;
      case 'xlarge':
        return 72;
      default:
        return 40;
    }
  };

  const getInitials = (name) => {
    if (!name) return '?';
    const parts = name.split(' ');
    if (parts.length >= 2) {
      return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
    }
    return name[0].toUpperCase();
  };

  const avatarSize = getSize();

  return (
    <View
      style={[
        {
          width: avatarSize,
          height: avatarSize,
          borderRadius: avatarSize / 2,
          backgroundColor: backgroundColor || Colors.primary.main,
          justifyContent: 'center',
          alignItems: 'center',
          overflow: 'hidden',
        },
        style,
      ]}
      {...props}
    >
      {source ? (
        <Image
          source={source}
          style={{ width: '100%', height: '100%' }}
          resizeMode="cover"
        />
      ) : (
        <Text
          style={{
            color: Colors.neutral[0],
            fontSize: avatarSize * 0.4,
            fontWeight: '600',
          }}
        >
          {getInitials(name)}
        </Text>
      )}
    </View>
  );
};

// Divider Component
export const Divider = ({ orientation = 'horizontal', style, ...props }) => {
  return (
    <View
      style={[
        {
          backgroundColor: Colors.neutral[200],
          ...(orientation === 'horizontal'
            ? { height: 1, width: '100%' }
            : { width: 1, height: '100%' }),
        },
        style,
      ]}
      {...props}
    />
  );
};

export default {
  Colors,
  Typography,
  Spacing,
  BorderRadius,
  Shadows,
  Button,
  Card,
  TextInput,
  Badge,
  Avatar,
  Divider,
};
