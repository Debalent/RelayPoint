/**
 * Post-build path fixer for GitHub Pages deployment.
 * Metro on Windows generates backslash paths and doesn't always apply baseUrl.
 * This script normalises dist/index.html before gh-pages deploys it.
 */
const fs = require('fs')
const path = require('path')

const distDir = path.join(__dirname, '..', 'dist')
const indexPath = path.join(distDir, 'index.html')
const BASE = '/RelayPoint'

let html = fs.readFileSync(indexPath, 'utf8')

// 1. Replace ALL backslashes in the file with forward slashes
html = html.replace(/\\/g, '/')

// 2. Ensure baseUrl prefix on all /_expo/ paths
//    (only add it if not already prefixed)
html = html.replace(/href="\/_expo\//g, `href="${BASE}/_expo/`)
html = html.replace(/src="\/_expo\//g,  `src="${BASE}/_expo/`)

// 3. Replace %PUBLIC_URL% placeholder
html = html.replace(/%PUBLIC_URL%/g, BASE)

fs.writeFileSync(indexPath, html, 'utf8')
console.log('✅  dist/index.html paths fixed for GitHub Pages.')
console.log('    Base URL:', BASE)
