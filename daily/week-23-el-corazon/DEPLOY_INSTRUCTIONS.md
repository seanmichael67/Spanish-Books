# Deployment Instructions - Week 23: El Corazón

**Target:** WordPress Divi site (beibeiamigos.com)  
**Est. Time:** 10-15 minutes  
**Difficulty:** Easy (copy-paste)

---

## Prerequisites

Before starting, make sure you have:
- [ ] WordPress admin access
- [ ] FTP/SFTP access (or File Manager in cPanel)
- [ ] Images generated (or ready to use SVG placeholders)
- [ ] Google My Business review link
- [ ] Email signup integration (optional - can skip for v1)

---

## Step 1: Generate Images (10-15 min)

### Option A: Use AI Image Generator (Recommended)

**Bing Image Creator (Free DALL-E 3):**
1. Go to: https://www.bing.com/create
2. Sign in with Microsoft account
3. Copy prompts from `images/prompts.txt`
4. Generate each image (10 total)
5. Download as PNG/JPG
6. Convert to WebP: https://squoosh.app/
7. Optimize to <100KB each
8. Name files correctly:
   - page-01-cover.webp
   - page-02-corazon.webp
   - ... etc.

**Alternative Tools:**
- Leonardo.ai (free tier): https://leonardo.ai/
- Playground AI: https://playgroundai.com/
- Stable Diffusion (local): https://github.com/AUTOMATIC1111/stable-diffusion-webui

### Option B: Skip for Now (Use SVG Placeholders)

The book has built-in SVG fallbacks. If images don't load, friendly placeholders will show instead. This is fine for testing or if you're in a hurry.

---

## Step 2: Upload Files to WordPress (5 min)

### Via FTP/SFTP:
1. Connect to your server
2. Navigate to: `/wp-content/books/`
3. Create folder: `week-23-el-corazon/`
4. Upload:
   - `book-standalone.html` → `/books/week-23-el-corazon/`
   - `images/` folder → `/books/week-23-el-corazon/images/`
5. Set permissions: 644 (files), 755 (folders)

### Via cPanel File Manager:
1. Log into cPanel
2. Open File Manager
3. Navigate to: `public_html/wp-content/books/`
4. Click "Upload"
5. Upload `book-standalone.html`
6. Create `week-23-el-corazon/` folder
7. Upload `images/` folder into it

### Via WordPress Media Library (Alternative):
1. Go to: Media > Add New
2. Upload all images
3. Note the URLs (you'll update book-standalone.html paths)
4. Upload book-standalone.html via FTP

---

## Step 3: Create WordPress Page (5 min)

1. **Go to:** Pages > Add New
2. **Title:** `El Corazón - Free Spanish Book for Preschool`
3. **Permalink:** Edit to `/spanish-books/week-23-el-corazon/`
4. **Page Template:** Divi (or your theme's full-width template)
5. **Don't publish yet** - save as draft

---

## Step 4: Add SEO Meta Tags (3 min)

### Option A: Using Yoast SEO Plugin
1. Scroll down to "Yoast SEO" section
2. Click "Edit snippet"
3. Copy from `seo-meta.html`:
   - Title → Paste into "SEO title"
   - Description → Paste into "Meta description"
4. Scroll to "Advanced" tab
5. Paste schema markup JSON into "Schema" section

### Option B: Using Insert Headers and Footers Plugin
1. Install plugin: "Insert Headers and Footers"
2. Go to: Settings > Insert Headers and Footers
3. Paste content from `seo-meta.html` into "Scripts in Header"
4. Save changes

### Option C: Manual (Theme Header)
1. Go to: Appearance > Theme Editor
2. Open `header.php`
3. Find `</head>` tag
4. Paste content from `seo-meta.html` above it
5. Save

---

## Step 5: Embed Book (2 min)

1. **In your draft page**, add a **Code Module** (Divi)
   - OR use: "Custom HTML" block (Gutenberg)
2. **Copy entire content** from `divi-embed-code.html`
3. **Paste** into the code module
4. **Preview** the page
5. **Verify:**
   - Book loads
   - Navigation works
   - Audio plays

---

## Step 6: Update Links (2 min)

**IMPORTANT:** Update these links before publishing:

### 1. Google My Business Review Link
In `book-standalone.html`, find line ~573:
```html
<a href="https://g.page/r/YOUR_GOOGLE_BUSINESS_ID/review" ...>
```
Replace `YOUR_GOOGLE_BUSINESS_ID` with your actual Google Business ID.

**How to find your ID:**
- Go to: https://business.google.com/
- Select your business
- Click "Get reviews"
- Copy the review link
- Extract the ID from the URL

### 2. Email Signup Form Action (Optional)
In `book-standalone.html`, find line ~580:
```html
<form onsubmit="handleEmailSignup(event)">
```
Update `handleEmailSignup()` function to submit to your email service:
- Mailchimp
- ConvertKit
- ActiveCampaign
- Custom backend

**For now:** Leave as-is (will show alert confirmation).

---

## Step 7: Test Before Launch (5 min)

### Desktop Testing:
1. Preview the draft page
2. Click through all pages
3. Test audio on a few pages
4. Click all CTA buttons
5. Check for console errors (F12)

### Mobile Testing:
1. Open on phone (or use Chrome DevTools mobile view)
2. Test page navigation
3. Test audio
4. Verify no horizontal scroll
5. Check CTAs are clickable

### SEO Validation:
1. **Rich Results Test:** https://search.google.com/test/rich-results
   - Enter your page URL
   - Check for schema errors
2. **Mobile-Friendly Test:** https://search.google.com/test/mobile-friendly
   - Verify it passes
3. **PageSpeed Insights:** https://pagespeed.web.dev/
   - Target: >85 mobile, >90 desktop

---

## Step 8: Publish & Promote (10 min)

### Publish:
1. Click "Publish" button
2. Visit live URL: `https://beibeiamigos.com/spanish-books/week-23-el-corazon/`
3. Test again on live site
4. Fix any issues

### Submit to Google:
1. Go to: Google Search Console
2. URL Inspection: Paste your book URL
3. Click "Request Indexing"
4. Wait 1-3 days for indexing

### Promote:
1. **Social Media:**
   - Facebook post with cover image
   - Instagram story/post
   - Pinterest pin (all 10 images)
   - Twitter thread (page-by-page)

2. **Email Newsletter:**
   - Subject: "❤️ NEW Spanish Book: El Corazón (Love & Family)"
   - Include link and preview images
   - CTA: "Read Now Free"

3. **Google My Business:**
   - Create a post
   - Share book link
   - Add cover image

4. **Update Books Index:**
   - Add Week 23 to your main books page
   - Link to new book
   - Update "Latest Books" section

---

## Step 9: Monitor Performance (Ongoing)

### First Week:
- [ ] Check Google Analytics daily
- [ ] Monitor page views
- [ ] Track email signups
- [ ] Watch for Google reviews
- [ ] Note any errors/feedback

### First Month:
- [ ] Organic search traffic
- [ ] Keyword rankings
- [ ] Conversion rate (emails/reviews)
- [ ] Bounce rate
- [ ] Avg. time on page

---

## Troubleshooting

### Images Not Loading?
- Check file paths in book-standalone.html
- Verify images uploaded to correct folder
- Check file permissions (644)
- Use SVG placeholders (already built-in)

### Audio Not Working?
- Check browser compatibility (Web Speech API)
- Test in different browsers
- Fallback: Add note "Audio works in Chrome/Edge"

### Schema Errors?
- Validate JSON at: https://validator.schema.org/
- Check for missing commas, brackets
- Update URLs to match your domain

### Mobile Layout Broken?
- Clear cache
- Check CSS media queries
- Test in Chrome DevTools mobile view
- Verify viewport meta tag present

---

## Rollback Plan

If something goes wrong:
1. **Unpublish page** (revert to draft)
2. **Fix issues** locally
3. **Re-upload** corrected files
4. **Test again** before republishing

---

## Success Metrics

After 1 week, you should see:
- ✅ 50+ page views
- ✅ 5+ email signups
- ✅ 2+ Google reviews
- ✅ Indexed by Google
- ✅ No technical errors

After 1 month:
- ✅ 200+ organic page views
- ✅ 20+ email signups
- ✅ 10+ Google reviews
- ✅ 1+ enrollment inquiry

---

## Next Steps

After this book is live:
1. Monitor analytics for 1 week
2. Gather user feedback
3. Share widely on social media
4. Build Week 24 (Los Ayudantes - Community Helpers)
5. Consider adding:
   - Downloadable PDF version
   - Print-at-home worksheets
   - Interactive quiz module

---

## Need Help?

- **Technical issues:** Check TECHNICAL_SPECS.md
- **SEO questions:** Review seo-meta.html comments
- **Agent workflow:** Read BOOKS_AGENT_SOUL.md
- **Calendar:** See 52-WEEK-SPANISH-THEMES.md

---

**Deployment Checklist:**
- [ ] Images generated/uploaded
- [ ] Files uploaded to WordPress
- [ ] Page created with SEO tags
- [ ] Book embedded via Divi
- [ ] Links updated (GMB review, etc.)
- [ ] Tested on desktop & mobile
- [ ] SEO validated (Rich Results, Mobile-Friendly)
- [ ] Published & live
- [ ] Submitted to Google Search Console
- [ ] Promoted on social media
- [ ] Added to books index page

---

**Ready to go live? 🚀**
