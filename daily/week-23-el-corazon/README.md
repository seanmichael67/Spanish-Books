# Week 23: El Corazón (The Heart)

**Theme:** February - El Amor (Love)  
**Vocabulary:** corazón, amar, cuidar, familia, beso, abrazo, rojo  
**Pages:** 10  
**Target Age:** 2-5  
**Built:** January 30, 2026

---

## 📖 Book Overview

Interactive Spanish vocabulary book teaching love, family, and caring concepts to preschoolers. Perfect for Valentine's Day, family discussions, or social-emotional learning.

### Vocabulary Words (7):
1. **corazón** - heart
2. **amar** - to love
3. **cuidar** - to care for
4. **familia** - family
5. **beso** - kiss
6. **abrazo** - hug
7. **rojo** - red

### Bonus Word:
- **amor** - love (review page)

---

## 🚀 Quick Deploy (10-15 minutes)

### Prerequisites:
- [ ] WordPress admin access
- [ ] Images generated (or use SVG placeholders)
- [ ] Google My Business review link ready
- [ ] Analytics tracking configured

### Steps:

1. **Generate Images** (if not auto-generated)
   - Use prompts from `images/prompts.txt`
   - Generate via Bing Image Creator, DALL-E 3, or similar
   - Save as WebP format in `images/` folder
   - Optimize: <100KB per image

2. **Upload Files to WordPress**
   ```
   /wp-content/books/week-23-el-corazon/
   ├── book-standalone.html
   └── images/
       ├── page-01-cover.webp
       ├── page-02-corazon.webp
       └── ... (all 10 images)
   ```

3. **Create WordPress Page**
   - Title: "El Corazón - Free Spanish Book for Preschool"
   - URL slug: `/spanish-books/week-23-el-corazon/`
   - Template: Divi or your theme

4. **Add SEO Meta Tags**
   - Copy content from `seo-meta.html`
   - Paste into page `<head>` section
   - Use plugin: "Insert Headers and Footers" or Yoast SEO

5. **Embed Book**
   - Add Divi Code Module (or HTML block)
   - Copy-paste content from `divi-embed-code.html`
   - Save draft

6. **Test Before Publishing**
   - [ ] Desktop view works
   - [ ] Mobile responsive (test on phone)
   - [ ] Audio plays correctly
   - [ ] Navigation buttons work
   - [ ] Images load (or SVG placeholders show)
   - [ ] CTAs link correctly

7. **Validate SEO**
   - Google Rich Results Test: https://search.google.com/test/rich-results
   - Check schema markup validates
   - Verify meta tags present

8. **Publish & Promote**
   - Click "Publish"
   - Share on social media
   - Send to email list
   - Add to books index page

---

## 📊 SEO Keywords

### Primary:
- "free spanish books for preschool"
- "learn love spanish kids"
- "spanish family vocabulary"
- "corazón español niños"

### Secondary:
- "valentine spanish preschool"
- "montessori spanish materials"
- "phoenix bilingual preschool"
- "interactive spanish books free"
- "spanish emotions preschool"

### Long-tail:
- "how to teach love in spanish to preschoolers"
- "free spanish valentine book for kids"
- "best spanish family vocabulary books 2-5"
- "spanish love vocabulary preschool"

---

## 💼 Business Integration

### CTAs Included:
1. **Top Banner:** Schedule a preschool tour
2. **End of Book:**
   - Google review request (unlock bonus book)
   - Email signup (weekly books)
   - Tour scheduling link

### Conversion Goals:
- [ ] 10+ email signups/month
- [ ] 5+ Google reviews generated
- [ ] 2+ enrollment inquiries
- [ ] 100+ organic visitors/month

---

## 📁 File Structure

```
week-23-el-corazon/
├── README.md                   # This file
├── book-config.js              # JavaScript book data
├── book-standalone.html        # Full HTML book (ready to deploy)
├── divi-embed-code.html        # WordPress copy-paste embed
├── seo-meta.html               # Meta tags + schema markup
├── images/
│   ├── prompts.txt             # AI image generation prompts
│   ├── page-01-cover.webp      # (Generate these)
│   ├── page-02-corazon.webp
│   └── ... (10 images total)
├── CHECKLIST.md                # Pre-deployment QA
└── DEPLOY_INSTRUCTIONS.md      # Detailed deployment guide
```

---

## 🎨 Design Notes

- **Color Scheme:** Red, pink, warm tones (love/heart theme)
- **Font:** System fonts (fast loading)
- **Audio:** Web Speech API (Spanish TTS)
- **Images:** SVG fallbacks if images not loaded
- **Mobile:** Fully responsive, tested on iOS/Android

---

## 📈 Analytics Tracking

Events tracked:
- `book_page_view` - Page loaded
- `page_view` - Each book page viewed
- `book_complete` - User reaches last page
- `email_signup` - Email captured
- `review_click` - Google review link clicked

Make sure Google Tag Manager or GA4 is configured in WordPress.

---

## 🔧 Technical Specs

- **Load Time:** <2 seconds (target)
- **File Size:** <1.5MB total (all assets)
- **Browser Support:** Chrome, Safari, Firefox, Edge (latest 2 versions)
- **Mobile:** iOS 13+, Android 8+
- **Accessibility:** WCAG 2.1 AA (keyboard navigation, screen readers)

---

## 📝 Notes for Maestro

### Next Steps After Deployment:
1. Monitor analytics for first week
2. Share on Beibei Amigos social media
3. Email to current parents list
4. Add to Google My Business post
5. Cross-link from other book pages

### Future Improvements:
- [ ] Add ElevenLabs premium TTS (optional)
- [ ] Create downloadable PDF version
- [ ] Add print-at-home worksheets
- [ ] Build quiz/game module
- [ ] Translate to Mandarin (Amici)

### Marketing Ideas:
- **Valentine's Week:** Feature prominently on homepage
- **Parent Newsletter:** Include in February edition
- **Social Media:** Post page-by-page teasers
- **Google Ads:** Target "valentine spanish preschool"
- **Pinterest:** Pin all images with book link

---

## ❓ Questions?

Contact the Books Agent (nightly builds) or check:
- `BOOKS_AGENT_SOUL.md` - Mission & workflow
- `TECHNICAL_SPECS.md` - Implementation details
- `52-WEEK-SPANISH-THEMES.md` - Full calendar

---

**Built with ❤️ by Books Agent**  
**For:** Beibei Amigos & Amici Trilingual Montessori  
**Date:** January 30, 2026, 10:00 PM MST
