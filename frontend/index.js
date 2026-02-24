// Cross-platform entry point for RelayPoint Elite
import App from './src/App'

// On web (static export / browser), use ReactDOM directly.
// On native (iOS/Android), use Expo's registerRootComponent.
if (typeof document !== 'undefined') {
  const { createRoot } = require('react-dom/client')
  const React = require('react')
  const container = document.getElementById('root')
  const root = createRoot(container)
  root.render(React.createElement(App))
} else {
  const { registerRootComponent } = require('expo')
  registerRootComponent(App)
}
