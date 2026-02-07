# Week 22: Los Amigos (Friends) 🤝

**Theme:** February - El Amor (Love)  
**Topic:** Friendship and Kindness  
**Vocabulary:** amigo, jugar, compartir, ayudar, reír, abrazar, gentil (7 words)  
**Pages:** 10  
**Target Age:** 2-5 years  

---

## 📖 Book Overview

This interactive Spanish book teaches preschoolers essential friendship vocabulary through simple sentences, colorful illustrations, and Spanish audio pronunciation.

### Learning Objectives
- Recognize and pronounce 7 Spanish friendship words
- Understand basic friendship concepts (sharing, helping, kindness)
- Associate Spanish words with visual representations
- Develop social-emotional skills

### Vocabulary List
1. **amigo** - friend
2. **jugar** - to play
3. **compartir** - to share
4. **ayudar** - to help
5. **reír** - to laugh
6. **abrazar** - to hug
7. **gentil** - kind, gentle
8. **todos** - everyone (bonus word)

---

## 🚀 Quick Deploy (10-15 minutes)

### Step 1: Generate Images (if not done)
```bash
# Option A: Use AI (DALL-E, Midjourney, etc.)
# See images/prompts.txt for detailed prompts

# Option B: Use placeholder images (book works without real images)
# The HTML already has SVG fallbacks built in
```

### Step 2: Upload to WordPress
```bash
# Upload this entire folder to:
/wp-content/uploads/books/week-22-los-amigos/

# Or use FTP/cPanel File Manager
```

### Step 3: Create WordPress Page
1. Go to **Pages → Add New**
2. Title: "Los Amigos - Free Spanish Book for Preschool"
3. URL slug: `/spanish-books/week-22-los-amigos/`

### Step 4: Add SEO Meta Tags
1. Install plugin: "Insert Headers and Footers" or use Yoast SEO
2. Copy content from `seo-meta.html`
3. Paste into page `<head>` section

### Step 5: Embed Book
**Option A: iFrame Embed (Recommended)**
1. Add a **Divi Code Module** (or HTML block)
2. Copy content from `divi-embed-code.html`
3. Paste into module
4. Update the iframe `src` path if needed:
   ```html
   src="/wp-content/uploads/books/week-22-los-amigos/book-standalone.html"
   ```

**Option B: Direct Embed**
1. Copy entire `book-standalone.html` content
2. Paste into Divi Code Module
3. May need to adjust CSS if conflicts with theme

### Step 6: Test & Publish
- [ ] Preview page on desktop
- [ ] Preview page on mobile
- [ ] Click through all 10 pages
- [ ] Test audio on each page
- [ ] Verify CTAs work (tour link, review link)
- [ ] Check page load speed (<2 seconds)
- [ ] Validate schema markup: https://search.google.com/test/rich-results

### Step 7: Promote
- Share on social media (Facebook, Instagram)
- Email to parent list
- Add to homepage "Featured Books" section
- Create Google Ads campaign (if budget allows)

---

## 📁 File Structure

```
week-22-los-amigos/
├── README.md                    # This file
├── book-config.js               # Book data (for React integration)
├── book-standalone.html         # Full HTML (ready to deploy) ⭐
├── divi-embed-code.html         # WordPress Divi copy-paste
├── seo-meta.html                # Meta tags + schema markup
├── CHECKLIST.md                 # Pre-deployment QA
├── images/
│   ├── prompts.txt              # AI image generation prompts
│   ├── page-01-cover.webp       # (generate or add)
│   ├── page-02-amigo.webp       # (generate or add)
│   └── ... (10 images total)
```

---

## 🎨 Images Status

**Status:** ⏳ Prompts ready, images need generation

Generate using:
- **DALL-E 3** (recommended): https://openai.com/dall-e-3
- **Midjourney**: https://midjourney.com
- **Canva AI**: https://canva.com (free tier available)

All prompts provided in `images/prompts.txt`

---

## 📊 SEO Details

### Primary Keywords
- spanish preschool books
- learn friends spanish
- friendship vocabulary spanish
- free spanish books kids

### Secondary Keywords
- amigos español niños
- montessori spanish
- phoenix bilingual preschool
- spanish social skills

### Long-tail Keywords
- "how to teach friendship in spanish to preschoolers"
- "free spanish books for 2-5 year olds"
- "trilingual preschool resources phoenix"

### Schema Markup
✅ Book schema  
✅ Organization schema  
✅ BreadcrumbList schema  
✅ LearningResource schema  

---

## 💼 Business Integration

### CTAs Included
1. **Top Banner:** "Schedule a Tour of Our Preschool!"
2. **End Page - Review:** Google My Business review request
3. **End Page - Email:** Weekly book subscription signup
4. **End Page - Tour:** Enrollment page link

### Conversion Tracking
```javascript
// Google Analytics events tracked:
- book_page_view (initial load)
- page_view (each page flip)
- book_complete (reaches final page)
- email_signup (submits email)
```

### Update Required
⚠️ Replace placeholder Google review link in:
- `book-standalone.html` (line ~XXX)
- URL: `https://g.page/r/YOUR_GOOGLE_BUSINESS_ID/review`

---

## 🔊 Audio Configuration

**Method:** Web Speech API (built into browsers)  
**Language:** Spanish (es-ES)  
**Rate:** 0.85 (slightly slower for preschoolers)  
**Pitch:** 1.1 (slightly higher, friendly)

**Browser Support:**
- ✅ Chrome/Edge (excellent)
- ✅ Safari (good)
- ✅ Firefox (good)
- ❌ IE11 (not supported - graceful fallback)

**Alternative:** ElevenLabs API integration (if budget allows)

---

## 📱 Mobile Optimization

- Responsive design (adapts to all screen sizes)
- Touch-friendly buttons (large tap targets)
- Fast loading (<2 seconds target)
- Images: lazy loading + WebP format
- Works offline (once loaded)

---

## 🧪 Testing Checklist

See `CHECKLIST.md` for detailed QA checklist.

**Quick Test:**
```bash
# Open locally in browser
open book-standalone.html

# Or start simple server
python3 -m http.server 8000
# Visit: http://localhost:8000/book-standalone.html
```

---

## 📈 Success Metrics

**Week 1 Goals:**
- 50+ page views
- 10+ complete reads (all 10 pages)
- 2+ email signups
- 1+ Google review
- 0+ enrollment inquiries

**Month 1 Goals:**
- 200+ page views
- 50+ complete reads
- 10+ email signups
- 5+ Google reviews
- 2+ enrollment inquiries

---

## 🔄 Next Steps

After deploying this book:

1. **Monitor Analytics**
   - Track page views, completion rate
   - Identify drop-off points
   - A/B test CTAs if needed

2. **Gather Feedback**
   - Ask parents for reviews
   - Teacher feedback on vocabulary
   - Child engagement observations

3. **Iterate**
   - Improve weak pages
   - Add more interactive elements
   - Create companion materials (flashcards, activities)

4. **Build Week 23**
   - Theme: El Corazón (The Heart)
   - Vocabulary: corazón, amar, cuidar, familia, beso, abrazo, rojo

---

## 📞 Support

**Questions or issues?**
- Email: info@beibeiamigos.com
- Phone: XXX-XXX-XXXX
- Hours: Monday-Friday 8AM-5PM MST

---

## 📝 Version History

- **v1.0** (2026-01-29): Initial release
  - 10 pages, 7 vocabulary words
  - Standalone HTML with embedded CSS/JS
  - Web Speech API audio
  - Full SEO optimization
  - Business CTAs integrated

---

## 📄 License

© 2026 Beibei Amigos Language Preschool  
For internal use and distribution on Beibei Amigos websites.

---

**Build Time:** ~3 hours  
**Deploy Time:** ~15 minutes  
**Estimated Impact:** High (engaging content, SEO-optimized, lead generation)

🚀 **Ready to launch!**
