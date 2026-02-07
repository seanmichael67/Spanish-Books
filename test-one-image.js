#!/usr/bin/env node

const https = require('https');
const fs = require('fs');
const path = require('path');

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

if (!OPENAI_API_KEY) {
  console.error('❌ OPENAI_API_KEY not set');
  process.exit(1);
}

console.log('🎨 Testing DALL-E 3 image generation...\n');

const prompt = "Two happy diverse preschool children holding hands and smiling, bright sunny background with soft clouds, cartoon illustration style, cheerful friendship theme, colorful clothing, simple clean design, suitable for ages 2-5, warm and inviting atmosphere, book cover quality";

console.log(`📝 Prompt: ${prompt.substring(0, 100)}...\n`);

const requestBody = JSON.stringify({
  model: 'dall-e-3',
  prompt: prompt,
  n: 1,
  size: '1024x1024',
  quality: 'standard'
});

const options = {
  hostname: 'api.openai.com',
  port: 443,
  path: '/v1/images/generations',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${OPENAI_API_KEY}`,
    'Content-Length': Buffer.byteLength(requestBody)
  }
};

console.log('⏳ Generating image...\n');

const req = https.request(options, (res) => {
  let data = '';
  
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    if (res.statusCode === 200) {
      const response = JSON.parse(data);
      const imageUrl = response.data[0].url;
      console.log(`✅ Success!\n`);
      console.log(`🖼️  Image URL: ${imageUrl}\n`);
      console.log(`💰 Cost: $0.04\n`);
      console.log(`\n🎉 DALL-E 3 is working! Ready to generate all 10 images.`);
    } else {
      console.error(`❌ API Error (${res.statusCode}):`);
      console.error(data);
    }
  });
});

req.on('error', (error) => {
  console.error(`❌ Request Error: ${error.message}`);
});

req.write(requestBody);
req.end();
