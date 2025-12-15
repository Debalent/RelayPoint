# RelayPoint Elite Frontend - Cross-Platform

## Architecture

This frontend is built with **React Native** and **Expo**, providing a unified codebase that runs on:

- **iOS** (iPhone & iPad)
- **Android** (phones & tablets)
- **Web** (desktop & mobile browsers via React Native Web)
- **Desktop** (Windows, macOS, Linux via Electron - planned)

## Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn
- For iOS development: macOS with Xcode
- For Android development: Android Studio
- Expo CLI (installed automatically with dependencies)

### Installation

```bash
cd frontend
npm install
```

### Development

#### Web Development
```bash
npm run start:web
```
Launches the web app at `http://localhost:19006`

#### iOS Development
```bash
npm run start:ios
```
Launches in iOS Simulator (requires macOS and Xcode)

#### Android Development
```bash
npm run start:android
```
Launches in Android Emulator (requires Android Studio)

#### Universal Development Server
```bash
npm start
```
Opens Expo DevTools - scan QR code with Expo Go app for testing on physical devices

## Key Dependencies

- **React Native** - Core cross-platform framework
- **Expo** - Development toolchain and native modules
- **React Native Web** - Web support
- **React Navigation** - Cross-platform navigation
- **Redux Toolkit** - Global state management
- **React Native Paper** - Material Design components
- **Axios** - HTTP client

## Building for Production

### Web
```bash
npm run build:web
```
Outputs to `web-build/` directory - deploy to any static hosting

### iOS/Android
```bash
npm run build:ios
npm run build:android
```
Requires EAS Build setup (Expo Application Services)

## Learn More

- [React Native Documentation](https://reactnative.dev/)
- [Expo Documentation](https://docs.expo.dev/)
- [React Navigation](https://reactnavigation.org/)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
