#!/usr/bin/env node
/**
 * Generate config.json from .env.local for static hosting
 * This allows Firebase Hosting to read the NEXT_PUBLIC_MODE setting
 */

const fs = require('fs');
const path = require('path');

const envPath = path.join(__dirname, '.env.local');
const configPath = path.join(__dirname, 'public', 'config.json');

// Default values
let mode = 'waitlist';
let appUrl = 'https://mobile--morningbuddies.us-central1.hosted.app/';

// Read .env.local if it exists
if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf8');
  
  const modeMatch = envContent.match(/NEXT_PUBLIC_MODE=(.+)/);
  if (modeMatch) {
    mode = modeMatch[1].trim();
  }
  
  const appUrlMatch = envContent.match(/NEXT_PUBLIC_APP_URL=(.+)/);
  if (appUrlMatch) {
    appUrl = appUrlMatch[1].trim();
  }
  
  console.log('📖 Read from .env.local:');
  console.log(`   NEXT_PUBLIC_MODE=${mode}`);
  console.log(`   NEXT_PUBLIC_APP_URL=${appUrl}`);
} else {
  console.warn('⚠️  .env.local not found, using defaults');
}

// Create config object
const config = {
  mode,
  appUrl
};

// Ensure public directory exists
const publicDir = path.dirname(configPath);
if (!fs.existsSync(publicDir)) {
  fs.mkdirSync(publicDir, { recursive: true });
}

// Write config.json
fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
console.log(`✅ Created ${configPath}`);
console.log(`   Mode: ${mode}`);
console.log(`   App URL: ${appUrl}`);


