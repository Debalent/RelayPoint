// Web-specific entry point — bypasses Expo's AppRegistry for static export.
// Metro resolves index.web.js over index.js for --platform web builds.
import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './src/App'

const container = document.getElementById('root')
const root = createRoot(container)
root.render(<App />)
