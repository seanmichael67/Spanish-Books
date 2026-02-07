# Deployment Instructions
## Los Amigos - Week 22

**Estimated Time:** 15-20 minutes  
**Difficulty:** Easy (no coding required)

---

## 📋 Prerequisites

Before you start:
- [ ] WordPress admin access
- [ ] FTP/cPanel access (for file upload)
- [ ] Google My Business admin (for review link)

---

## Step-by-Step Deployment

### 🗂️ STEP 1: Prepare Files (5 minutes)

1. **Check that you have all files:**
   ```
   week-22-los-amigos/
   ├── book-standalone.html  ← Main file
   ├── images/               ← Image folder
   │   ├── prompts.txt       ← Generate images from here
   │   └── (image files)
   └── (other docs)
   ```

2. **Generate images (if not done yet):**
   - Open `images/prompts.txt`
   - Use DALL-E, Midjourney, or Canva to generate
   - Save as: `page-01-cover.webp`, `page-02-amigo.webp`, etc.
   - Place in `images/` folder

   **OR:** Skip this step - the book has placeholder images built-in!

---

### 📤 STEP 2: Upload Files to WordPress (5 minutes)

#### Option A: Using cPanel File Manager

1. Log into your hosting cPanel
2. Open **File Manager**
3. Navigate to: `/public_html/wp-content/uploads/`
4. Create folder: `books/` (if doesn't exist)
5. Inside `books/`, create: `week-22-los-amigos/`
6. Upload entire folder contents:
   - `book-standalone.html`
   - `images/` folder with all images
7. **Important:** Check file permissions (should be 644 for files, 755 for folders)

#### Option B: Using FTP (FileZilla)

1. Open FileZilla
2. Connect to your site:
   - Host: `ftp.yoursite.com`
   - Username: (your FTP username)
   - Password: (your FTP password)
3. Navigate to: `/public_html/wp-content/uploads/books/`
4. Drag and drop the `week-22-los-amigos/` folder
5. Wait for upload to complete

#### Option C: Using WordPress Media Library

1. In WordPress, go to **Media → Add New**
2. Upload `book-standalone.html` and all images
3. Note the URLs (you'll need them for the iframe)

---

### 📄 STEP 3: Create WordPress Page (3 minutes)

1. **Log into WordPress Admin**

2. **Go to:** Pages → Add New

3. **Page Setup:**
   - **Title:** `Los Amigos - Free Spanish Book for Preschool`
   - **URL slug:** Click "Edit" next to title → Change to `los-amigos`
   - **Parent page:** Spanish Books (if you have a parent page)

4. **Add Content:**
   
   **Option A: If using Divi Builder**
   - Click "Use Divi Builder"
   - Add a new section
   - Add a **Code Module**
   - Open `divi-embed-code.html` file
   - Copy all contents
   - Paste into Code Module
   - **Update the path** in line 15:
     ```html
     src="/wp-content/uploads/books/week-22-los-amigos/book-standalone.html"
     ```
   - Save module

   **Option B: If using Block Editor (Gutenberg)**
   - Add a **Custom HTML** block
   - Copy contents of `divi-embed-code.html`
   - Paste into block
   - Update the iframe path (same as above)

5. **Don't publish yet!** Click "Save Draft"

---

### 🔍 STEP 4: Add SEO Meta Tags (3 minutes)

#### Option A: Using Yoast SEO Plugin

1. Scroll down to **Yoast SEO** section on the page editor
2. **SEO Title:**
   ```
   Los Amigos - Free Spanish Book for Preschool | Beibei Amigos
   ```
3. **Meta Description:**
   ```
   Free interactive Spanish book teaching friendship vocabulary to preschoolers ages 2-5. Learn amigo, jugar, compartir, ayudar with audio!
   ```
4. **Focus Keyphrase:** `spanish preschool books`
5. Click **Advanced** tab
6. **Canonical URL:**
   ```
   https://beibeiamigos.com/spanish-books/los-amigos/
   ```

#### Option B: Using "Insert Headers and Footers" Plugin

1. Install plugin: **WPCode** or **Insert Headers and Footers**
2. Go to: Settings → Insert Headers and Footers (or WPCode)
3. Open `seo-meta.html` file
4. Copy all contents
5. Paste into **"Scripts in Header"** section
6. **Important:** Change URLs to match your site:
   - Replace `beibeiamigos.com` with your domain
   - Update image URLs
   - Update page URLs
7. Save changes

#### Option C: Manual (Theme Customizer)

1. Go to: Appearance → Theme Editor
2. Open `header.php`
3. Find `</head>` tag
4. Paste contents of `seo-meta.html` just before `</head>`
5. **Update all URLs** to match your site
6. Save

---

### 🔗 STEP 5: Update Google Review Link (2 minutes)

**Important:** The book has a placeholder Google review link. Update it!

1. **Get your Google My Business review link:**
   - Go to: https://business.google.com/
   - Select your location (Beibei Amigos)
   - Go to "Home" → "Get more reviews"
   - Copy the review link
   - Example: `https://g.page/r/CX1234567890/review`

2. **Update the link in the book:**
   - Open `book-standalone.html` in text editor
   - Find (Ctrl+F): `YOUR_GOOGLE_BUSINESS_ID`
   - Replace with your actual review link
   - Save file
   - Re-upload to server (overwrite existing)

---

### 🧪 STEP 6: Test the Page (5 minutes)

1. **Preview the draft page**
   - Click "Preview" in WordPress editor
   - Page opens in new tab

2. **Desktop Tests:**
   - [ ] Book displays correctly
   - [ ] Click through all 10 pages
   - [ ] Test audio on 2-3 pages (click 🔊 button)
   - [ ] Click "Schedule Tour" link (top banner)
   - [ ] Click "Leave Review" button (last page)
   - [ ] Try email signup form (use test email)
   - [ ] Check for any broken images

3. **Mobile Test:**
   - [ ] Open preview on phone
   - [ ] Tap through pages
   - [ ] Test audio
   - [ ] Check all buttons work
   - [ ] Verify text is readable

4. **Speed Test:**
   - Go to: https://pagespeed.web.dev/
   - Enter your preview URL
   - Check score (should be >85)

5. **Schema Test:**
   - Go to: https://search.google.com/test/rich-results
   - Enter your preview URL
   - Verify "Book" schema detected
   - Fix any errors

---

### 🚀 STEP 7: Publish! (1 minute)

1. **Final checks:**
   - [ ] All tests passed
   - [ ] Google review link updated
   - [ ] SEO meta tags added
   - [ ] Images displaying (or placeholders working)

2. **Click "Publish"** button in WordPress

3. **Get the URL:**
   - Copy the page URL
   - Example: `https://beibeiamigos.com/spanish-books/los-amigos/`

---

### 📣 STEP 8: Promote (15 minutes)

#### Immediate Actions

1. **Facebook Post**
   ```
   📚 NEW FREE BOOK! 📚
   
   Los Amigos (Friends) - Our latest Spanish book for preschoolers!
   
   🤝 Learn friendship vocabulary:
   • amigo (friend)
   • compartir (to share)
   • ayudar (to help)
   • And more!
   
   🔊 Interactive with Spanish audio
   👶 Perfect for ages 2-5
   
   Read now: [LINK]
   
   #SpanishForKids #BilingualEducation #PhoenixPreschool
   ```

2. **Instagram Post**
   - Screenshot of book cover
   - Same caption as above
   - Stories: Swipe-up link (if you have 10K followers)

3. **Email to Parents**
   ```
   Subject: 🤝 New Spanish Book: Los Amigos (Friends)
   
   Dear [Parent Name],
   
   We just released a brand new Spanish book for preschoolers!
   
   "Los Amigos" teaches essential friendship vocabulary through colorful 
   illustrations and Spanish audio pronunciation.
   
   📖 Read it now (free!): [LINK]
   
   Your child will learn:
   • amigo (friend)
   • jugar (to play)
   • compartir (to share)
   • ayudar (to help)
   • And more!
   
   Perfect for ages 2-5. Enjoy!
   
   Warmly,
   [Your Name]
   Beibei Amigos
   ```

4. **Google My Business Post**
   - Log into GMB
   - Create "What's New" post
   - Link to book
   - Add image (book cover)

---

### 📊 STEP 9: Monitor & Track (Ongoing)

#### Week 1: Check Daily

1. **Google Analytics:**
   - Go to: Analytics → Reports → Engagement → Pages
   - Find your book page
   - Check: Views, average time, completion rate

2. **Check for Issues:**
   - Review browser console errors (ask someone if needed)
   - Check WordPress error logs
   - Monitor parent feedback

3. **Respond to Comments:**
   - Facebook comments
   - Email replies
   - Google reviews (hopefully some come in!)

#### Week 2-4: Weekly Review

1. **SEO Performance:**
   - Google Search Console
   - Check impressions, clicks
   - See which keywords driving traffic

2. **Conversion Tracking:**
   - How many email signups?
   - How many review clicks?
   - How many tour clicks?

3. **Adjustments:**
   - Change CTAs if not converting
   - Fix any bugs reported
   - Improve low-performing pages

---

## 🆘 Troubleshooting

### Book doesn't display
- Check file path in iframe `src`
- Verify file uploaded correctly
- Check file permissions (644)
- Try opening HTML file directly in browser

### Images don't load
- Check `images/` folder uploaded
- Verify image paths in HTML
- Check file extensions (.webp vs .jpg)
- Placeholder SVGs should display if images missing

### Audio doesn't work
- Requires modern browser (Chrome, Safari, Firefox)
- Check browser console for errors
- Verify user clicked audio button (autoplay blocked by most browsers)
- Try different browser/device

### Page loads slowly
- Compress images (<100KB each)
- Use WebP format
- Enable lazy loading (already in code)
- Check server response time

### Schema errors
- Validate at: https://search.google.com/test/rich-results
- Check for missing required fields
- Update URLs to absolute paths
- Fix JSON-LD syntax errors

---

## 📞 Need Help?

**Can't figure something out?**

1. Check `CHECKLIST.md` for detailed testing
2. Review `README.md` for overview
3. Contact:
   - Email: info@beibeiamigos.com
   - Text: XXX-XXX-XXXX

---

## ✅ Deployment Complete!

Congratulations! Your book is live. 🎉

**Next steps:**
1. Share on social media
2. Email parents
3. Monitor analytics
4. Collect feedback
5. Start planning Week 23 book!

---

**Time Invested:** ~20 minutes  
**Potential Impact:** High (SEO traffic, parent engagement, lead generation)

**Deployment Date:** _____________  
**Deployed By:** _____________  
**Page URL:** _____________
