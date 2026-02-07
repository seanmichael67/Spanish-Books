#!/usr/bin/env node

/**
 * Automatic Book Image Generator
 * Uses DALL-E 3 to generate images for preschool books
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const { execSync } = require('child_process');

// OpenAI API key from environment
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

if (!OPENAI_API_KEY) {
  console.error('❌ OPENAI_API_KEY not found in environment');
  process.exit(1);
}

// Configuration
const BOOK_DIR = process.argv[2];
const SIZE = '1024x1024'; // DALL-E 3 size
const QUALITY = 'standard'; // or 'hd' for higher quality ($0.080 vs $0.040)
const MODEL = 'dall-e-3';

if (!BOOK_DIR) {
  console.error('Usage: node generate-images.js <book-directory>');
  console.error('Example: node generate-images.js daily/week-22-los-amigos');
  process.exit(1);
}

const bookPath = path.join(__dirname, BOOK_DIR);
const imagesPath = path.join(bookPath, 'images');
const promptsFile = path.join(imagesPath, 'prompts.txt');

if (!fs.existsSync(promptsFile)) {
  console.error(`❌ prompts.txt not found at: ${promptsFile}`);
  process.exit(1);
}

console.log('🎨 Automatic Book Image Generator');
console.log('━'.repeat(50));
console.log(`📁 Book: ${BOOK_DIR}`);
console.log(`🔑 API Key: ${OPENAI_API_KEY.substring(0, 20)}...`);
console.log(`📏 Size: ${SIZE}`);
console.log(`💎 Quality: ${QUALITY}`);
console.log('━'.repeat(50));

// Parse prompts file
function parsePrompts(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const prompts = [];
  
  // Split by --- separators
  const sections = content.split('---').filter(s => s.trim().length > 0);
  
  for (const section of sections) {
    // Look for PAGE sections
    if (!section.includes('PAGE')) continue;
    
    // Extract prompt (between quotes after "Prompt:")
    const promptMatch = section.match(/Prompt: "(.+?)"/s);
    if (!promptMatch) continue;
    
    // Extract filename
    const filenameMatch = section.match(/Filename: (.+)/);
    if (!filenameMatch) continue;
    
    const prompt = promptMatch[1].trim();
    const filename = filenameMatch[1].trim();
    
    prompts.push({ prompt, filename });
  }
  
  return prompts;
}

// Generate image with DALL-E 3
async function generateImage(prompt, filename) {
  console.log(`\n🖼️  Generating: ${filename}`);
  console.log(`📝 Prompt: ${prompt.substring(0, 100)}...`);
  
  const requestBody = JSON.stringify({
    model: MODEL,
    prompt: prompt,
    n: 1,
    size: SIZE,
    quality: QUALITY,
    response_format: 'url'
  });
  
  return new Promise((resolve, reject) => {
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
    
    const req = https.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        if (res.statusCode === 200) {
          const response = JSON.parse(data);
          const imageUrl = response.data[0].url;
          console.log(`✅ Generated! URL: ${imageUrl.substring(0, 50)}...`);
          resolve(imageUrl);
        } else {
          console.error(`❌ API Error (${res.statusCode}): ${data}`);
          reject(new Error(`API returned ${res.statusCode}`));
        }
      });
    });
    
    req.on('error', (error) => {
      console.error(`❌ Request Error: ${error.message}`);
      reject(error);
    });
    
    req.write(requestBody);
    req.end();
  });
}

// Download image from URL
function downloadImage(url, filepath) {
  return new Promise((resolve, reject) => {
    console.log(`📥 Downloading to: ${filepath}`);
    
    const file = fs.createWriteStream(filepath);
    
    https.get(url, (response) => {
      response.pipe(file);
      
      file.on('finish', () => {
        file.close();
        console.log(`✅ Downloaded!`);
        resolve(filepath);
      });
    }).on('error', (error) => {
      fs.unlink(filepath, () => {});
      console.error(`❌ Download Error: ${error.message}`);
      reject(error);
    });
  });
}

// Convert to WebP
function convertToWebP(pngPath, webpPath) {
  console.log(`🔄 Converting to WebP...`);
  
  try {
    // Check if cwebp is installed
    execSync('which cwebp', { stdio: 'ignore' });
    
    // Convert with compression
    execSync(`cwebp -q 85 "${pngPath}" -o "${webpPath}"`, { stdio: 'inherit' });
    
    // Delete original PNG
    fs.unlinkSync(pngPath);
    
    console.log(`✅ Converted to WebP!`);
    return webpPath;
  } catch (error) {
    console.log(`⚠️  cwebp not found, keeping PNG format`);
    // Just rename to .png if cwebp isn't available
    const pngFilename = webpPath.replace('.webp', '.png');
    fs.renameSync(pngPath, pngFilename);
    return pngFilename;
  }
}

// Main generation loop
async function generateAllImages() {
  const prompts = parsePrompts(promptsFile);
  
  console.log(`\n📚 Found ${prompts.length} images to generate`);
  console.log('━'.repeat(50));
  
  const results = [];
  let successCount = 0;
  let errorCount = 0;
  
  for (let i = 0; i < prompts.length; i++) {
    const { prompt, filename } = prompts[i];
    
    try {
      console.log(`\n[${i + 1}/${prompts.length}]`);
      
      // Generate image
      const imageUrl = await generateImage(prompt, filename);
      
      // Download as PNG first
      const pngPath = path.join(imagesPath, filename.replace('.webp', '.png'));
      await downloadImage(imageUrl, pngPath);
      
      // Convert to WebP
      const webpPath = path.join(imagesPath, filename);
      const finalPath = convertToWebP(pngPath, webpPath);
      
      results.push({ filename, status: 'success', path: finalPath });
      successCount++;
      
      // Rate limiting - wait 2 seconds between requests
      if (i < prompts.length - 1) {
        console.log('⏳ Waiting 2 seconds before next generation...');
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
      
    } catch (error) {
      console.error(`❌ Failed to generate ${filename}: ${error.message}`);
      results.push({ filename, status: 'error', error: error.message });
      errorCount++;
    }
  }
  
  // Summary
  console.log('\n' + '━'.repeat(50));
  console.log('📊 GENERATION SUMMARY');
  console.log('━'.repeat(50));
  console.log(`✅ Success: ${successCount}`);
  console.log(`❌ Errors: ${errorCount}`);
  console.log(`💰 Estimated cost: $${(successCount * 0.04).toFixed(2)} (at $0.04/image)`);
  console.log('━'.repeat(50));
  
  // Save results
  const resultsFile = path.join(imagesPath, 'generation-results.json');
  fs.writeFileSync(resultsFile, JSON.stringify(results, null, 2));
  console.log(`\n📄 Results saved to: ${resultsFile}`);
  
  if (successCount > 0) {
    console.log('\n✅ Image generation complete!');
    console.log(`\n📂 Generated images are in: ${imagesPath}`);
    console.log(`\n🔧 Next step: Update book-standalone.html to use these images`);
  }
}

// Run it!
generateAllImages().catch(error => {
  console.error('❌ Fatal error:', error);
  process.exit(1);
});
