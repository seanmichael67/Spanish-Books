# 📷 IMAGE STYLE: REALISTIC PHOTOS

**IMPORTANT:** All books use **REALISTIC PHOTOGRAPHS**, not cartoons or illustrations!

---

## Why Realistic Photos

### **Educational Benefits:**
- **Real-world connection** — Kids see actual objects, animals, places
- **Vocabulary clarity** — "This is what a REAL llama looks like"
- **Cultural authenticity** — Actual places, traditions, people
- **Credibility** — Parents trust educational materials with real imagery
- **Montessori alignment** — Reality-based learning

### **Business Benefits:**
- **Professional appearance** — Premium quality
- **Differentiation** — Most preschool books use cartoons
- **Shareability** — Beautiful photos = social media gold
- **SEO** — "real photos" is a search keyword

---

## Image Specifications

### **Style:**
- ✅ **Realistic photography**
- ✅ High-quality, professional
- ✅ Natural lighting
- ✅ Vibrant colors
- ✅ Clean backgrounds (not cluttered)
- ✅ Child-friendly (safe, positive imagery)

### **Technical:**
- **Format:** WebP (with JPG fallback)
- **Size:** 800px width max
- **Quality:** 80-85% compression
- **File size:** <100KB per image
- **Aspect ratio:** 4:3 or 1:1 (square)

---

## Sources for Realistic Photos

### **Option 1: AI-Generated Photorealistic (DALL-E 3)**
```javascript
// Prompt structure for realistic photos
const prompt = `
  Professional photograph of ${subject},
  realistic photography,
  natural lighting,
  vibrant colors,
  clean background,
  high quality,
  suitable for children's educational book,
  sharp focus,
  ${culturalContext}
`;

// Example for Week 5: La Mariposa
const prompt = `
  Professional photograph of an orange monarch butterfly 
  on a bright flower,
  realistic nature photography,
  natural sunlight,
  vibrant orange and black wings,
  green background with soft bokeh,
  sharp focus on butterfly,
  macro photography style,
  suitable for children's educational book
`;
```

### **Option 2: Stock Photography (Free)**

**Unsplash** (free, high-quality)
- https://unsplash.com
- Commercial use allowed
- No attribution required (but nice to include)
- Search: "butterfly", "llama", "orange fruit", etc.

**Pexels** (free, high-quality)
- https://pexels.com
- Commercial use allowed
- Great for cultural/nature photos

**Pixabay** (free)
- https://pixabay.com
- Commercial use allowed
- Good for basic objects

### **Option 3: iStock/Shutterstock (Paid)**
- Premium quality
- More specific cultural imagery
- License needed (~$10-30 per image)
- Best for hero images or final polished books

---

## Prompt Templates by Category

### **Objects (Colors, Shapes, School Items)**
```
Professional photograph of a ${color} ${object},
realistic product photography,
clean white background,
natural lighting,
vibrant ${color} color,
sharp focus,
high resolution,
suitable for children's educational book
```

**Example:** "Professional photograph of a bright red apple, realistic product photography, clean white background, natural lighting, vibrant red color, sharp focus, suitable for children's book"

### **Animals**
```
Professional wildlife photograph of a ${animal},
realistic nature photography,
natural habitat,
${specific_location if cultural},
natural lighting,
animal in sharp focus,
${action - eating, walking, swimming},
beautiful natural background,
suitable for children's educational book
```

**Example:** "Professional wildlife photograph of a llama in the Andes mountains, realistic nature photography, mountainous background, natural sunlight, llama standing peacefully, soft wool visible, suitable for children's book"

### **Cultural Scenes**
```
Professional photograph of ${cultural_element},
authentic ${country/region},
realistic documentary photography,
vibrant colors,
people ${doing_activity},
natural setting,
culturally respectful,
suitable for educational book
```

**Example:** "Professional photograph of monarch butterflies on oyamel trees in Michoacán, Mexico, realistic nature documentary photography, thousands of orange butterflies, forest background, natural lighting, culturally significant, suitable for educational book"

### **Food**
```
Professional food photograph of ${food},
realistic food photography,
${presentation - on plate, in basket, growing},
natural lighting,
vibrant fresh colors,
${cultural context if relevant},
appetizing and inviting,
suitable for children's book
```

**Example:** "Professional food photograph of bright oranges in a basket, realistic food photography, Spanish orange grove background, natural sunlight, vibrant orange color, fresh and inviting, suitable for children's book"

### **Landscapes/Nature**
```
Professional landscape photograph of ${location},
realistic travel photography,
${specific_region},
natural lighting,
vibrant natural colors,
${time_of_day},
beautiful composition,
suitable for educational book
```

**Example:** "Professional landscape photograph of Patagonian glaciers, realistic travel photography, icy blue and white colors, penguins in foreground, natural daylight, majestic and beautiful, suitable for children's book"

---

## DO's and DON'Ts

### ✅ DO:
- Use real, authentic photos
- Choose vibrant, colorful images
- Select clear, focused subjects
- Use natural lighting
- Show cultural elements authentically
- Choose child-appropriate imagery (happy, safe, positive)
- Credit sources when required

### ❌ DON'T:
- Use cartoons or illustrations
- Use AI-generated "art" style (only photorealistic)
- Use dark/scary imagery
- Use cluttered backgrounds
- Use low-resolution images
- Use watermarked stock photos
- Appropriate cultural sacred symbols

---

## Quality Checklist (Per Image)

Before using an image, verify:
- ✅ Photorealistic (not illustrated/cartoon)
- ✅ High resolution (at least 1024px width)
- ✅ Clear subject in focus
- ✅ Vibrant, appealing colors
- ✅ Clean or natural background
- ✅ Child-appropriate
- ✅ Culturally authentic (for cultural books)
- ✅ Properly licensed (commercial use allowed)
- ✅ Optimized for web (WebP, <100KB)

---

## Example: Week 1 - Los Colores (The Colors)

### Cartoon Style (❌ OLD WAY):
- Red apple cartoon illustration
- Blue sky with cartoon clouds
- Yellow sun with smiley face

### Realistic Photos (✅ NEW WAY):
- Professional photo of a bright red apple on white background
- Real photograph of a clear blue sky
- Real photograph of a yellow flower or lemon

**Impact:** Parents see professional, educational quality. Kids connect words to REAL objects.

---

## Example: Week 5 - La Mariposa (Mexico)

### Image 1: Monarch Butterfly
```
Professional macro photograph of an orange monarch butterfly,
perched on a bright purple flower,
realistic nature photography,
natural sunlight,
vibrant orange, black, and white wing pattern visible,
soft green background,
sharp focus on butterfly,
suitable for children's educational book
```

**OR** Find on Unsplash: Search "monarch butterfly flower"

### Image 2: Mexican Forest
```
Professional landscape photograph of oyamel fir trees 
covered with thousands of monarch butterflies,
Michoacán, Mexico,
realistic nature documentary photography,
orange butterflies clustered on branches,
natural forest setting,
warm natural light,
culturally significant location,
suitable for educational book
```

---

## Workflow for Books Agent

### Nightly Process:

1. **Generate Realistic Photo Prompts:**
   - Each page needs 1 realistic photo
   - Write photorealistic prompt
   - Save to `images/prompts.txt`

2. **Option A: Auto-generate (DALL-E 3)**
   ```javascript
   // Add "realistic photograph" to every prompt
   const image = await openai.images.generate({
     model: "dall-e-3",
     prompt: `${basePrompt}, realistic photograph, professional photography, natural lighting, high quality`,
     size: "1024x1024",
     quality: "standard"
   });
   ```

3. **Option B: Stock Photo Links**
   ```markdown
   # Image Sources (Manual)
   - Page 1: https://unsplash.com/photos/red-apple-xyz
   - Page 2: https://unsplash.com/photos/blue-sky-abc
   - Page 3: https://unsplash.com/photos/yellow-flower-def
   ```

4. **Save Original + Optimized:**
   ```
   images/
   ├── originals/
   │   ├── page-01.jpg (high-res original)
   │   └── ...
   └── optimized/
       ├── page-01.webp (<100KB for web)
       └── ...
   ```

---

## Benefits Summary

### **Educational:**
- ✅ Reality-based learning (Montessori principle)
- ✅ Clear vocabulary association
- ✅ Cultural authenticity

### **Business:**
- ✅ Professional appearance
- ✅ Premium positioning
- ✅ Parent trust
- ✅ Social media appeal
- ✅ Differentiation from competitors

### **Technical:**
- ✅ SEO-friendly (real photos keyword)
- ✅ Fast loading (optimized)
- ✅ Accessible (clear subjects)

---

**BOTTOM LINE:** 

Every book image should look like it came from a **National Geographic kids' magazine** or **high-quality educational publisher**, not a coloring book.

Real photos = Professional = Premium = Parents choose YOUR school.

---

**Created:** 2026-01-28  
**For:** Books Agent — Use realistic photography ONLY  
**Reference:** Read before generating ANY images
