# Pre-Deployment Quality Checklist

**Book:** El Corazón (Week 23)  
**Date:** January 30, 2026

---

## ✅ Content Quality

### Vocabulary
- [ ] 7 core vocabulary words included
- [ ] Age-appropriate (2-5 years)
- [ ] Spanish spelling correct
- [ ] English translations accurate
- [ ] Word highlighting implemented (`<span class='word-highlight'>`)

### Sentences
- [ ] Simple structure (3-7 words max per sentence)
- [ ] Grammatically correct Spanish
- [ ] Pronunciation-friendly for TTS
- [ ] Repetitive patterns (good for learning)
- [ ] English translations provided

### Images
- [ ] 10 images total (or SVG placeholders ready)
- [ ] Child-friendly, cartoon style
- [ ] Bright, high contrast colors
- [ ] No scary/sad/inappropriate content
- [ ] Diverse representation
- [ ] WebP format, <100KB each
- [ ] Alt tags descriptive

---

## ✅ Technical Implementation

### HTML/JavaScript
- [ ] Book data structure complete
- [ ] Page navigation works (prev/next buttons)
- [ ] Page indicator shows current page correctly
- [ ] Keyboard navigation works (arrow keys)
- [ ] Audio button on every page
- [ ] Web Speech API configured (Spanish TTS)
- [ ] No console errors
- [ ] SVG fallbacks for missing images

### Responsive Design
- [ ] Desktop (1920px+) - looks good
- [ ] Laptop (1366px) - looks good
- [ ] Tablet (768px) - looks good
- [ ] Mobile (375px) - looks good
- [ ] Touch-friendly buttons (min 44px)
- [ ] No horizontal scrolling

### Performance
- [ ] Page loads in <2 seconds
- [ ] Images lazy-loaded (except first page)
- [ ] No render-blocking resources
- [ ] CSS/JS minified (inline, so OK)
- [ ] Total file size <1.5MB

---

## ✅ SEO Optimization

### Meta Tags
- [ ] Title tag present (<60 chars)
- [ ] Meta description present (<160 chars)
- [ ] Keywords meta tag included
- [ ] Canonical URL set
- [ ] Open Graph tags (Facebook)
- [ ] Twitter Card tags
- [ ] Language tags (es, en)
- [ ] Robots tag (index, follow)

### Schema Markup
- [ ] Book schema complete
- [ ] Organization schema included
- [ ] WebPage schema present
- [ ] Breadcrumb schema added
- [ ] LearningResource schema included
- [ ] Validates at schema.org validator
- [ ] Passes Google Rich Results Test

### Content SEO
- [ ] H1 tag on title page
- [ ] Alt tags on all images
- [ ] Keyword density appropriate
- [ ] Internal links work
- [ ] External links open in new tab
- [ ] URL slug SEO-friendly

---

## ✅ Business Integration

### CTAs (Call-to-Actions)
- [ ] Top banner: Tour scheduling link
- [ ] End of book: Google review request
- [ ] End of book: Email signup form
- [ ] End of book: Tour scheduling link
- [ ] All links working
- [ ] Links open in new tabs

### Tracking
- [ ] Google Analytics event tracking present
- [ ] Page view tracking configured
- [ ] Book completion event tracked
- [ ] Email signup conversion tracked
- [ ] Review click tracked

### Links to Update
- [ ] Google My Business review link (replace YOUR_GOOGLE_BUSINESS_ID)
- [ ] Tour scheduling link (beibeiamigos.com/enroll)
- [ ] Email signup form action
- [ ] Social share URLs

---

## ✅ Divi Integration

### Embed Code
- [ ] iFrame embed code ready
- [ ] Height set appropriately (700px desktop)
- [ ] Width 100%, max-width 800px
- [ ] Mobile responsive CSS included
- [ ] Loading="lazy" attribute
- [ ] Title attribute for accessibility
- [ ] Allow="autoplay" for audio

### WordPress Files
- [ ] book-standalone.html ready
- [ ] All images uploaded to /books/week-23-el-corazon/images/
- [ ] File permissions correct (readable)
- [ ] Path references match file structure

---

## ✅ Testing (Manual)

### Desktop Testing
- [ ] Open in Chrome
- [ ] Open in Firefox
- [ ] Open in Safari
- [ ] Open in Edge
- [ ] Audio plays correctly
- [ ] Navigation smooth
- [ ] Images load (or fallbacks show)
- [ ] CTAs clickable

### Mobile Testing
- [ ] Test on iOS (iPhone)
- [ ] Test on Android
- [ ] Portrait orientation
- [ ] Landscape orientation
- [ ] Touch gestures work
- [ ] Audio plays
- [ ] No layout breaks

### Functionality Testing
- [ ] Click "Anterior" button (goes to previous page)
- [ ] Click "Siguiente" button (goes to next page)
- [ ] Buttons disabled at start/end appropriately
- [ ] Audio button plays Spanish TTS
- [ ] Audio stops when navigating pages
- [ ] Email form submission works
- [ ] Review link opens in new tab
- [ ] Tour link opens in new tab

---

## ✅ SEO Validation

### Tools to Use
- [ ] Google Rich Results Test: https://search.google.com/test/rich-results
- [ ] Schema.org Validator: https://validator.schema.org/
- [ ] Google PageSpeed Insights: https://pagespeed.web.dev/
- [ ] Google Mobile-Friendly Test: https://search.google.com/test/mobile-friendly

### Expected Results
- [ ] Schema validates with no errors
- [ ] PageSpeed score >90 (desktop)
- [ ] PageSpeed score >80 (mobile)
- [ ] Mobile-friendly test passes
- [ ] No console errors in browser

---

## ✅ Accessibility

### WCAG 2.1 AA Compliance
- [ ] Keyboard navigation works (Tab, Arrow keys)
- [ ] Focus indicators visible
- [ ] Color contrast ratio >4.5:1 (text/background)
- [ ] Alt text on all images
- [ ] ARIA labels on buttons
- [ ] Screen reader compatible
- [ ] No flashing/strobing content

---

## ✅ Final Pre-Launch

### WordPress Setup
- [ ] Page created: "El Corazón - Free Spanish Book"
- [ ] URL slug: `/spanish-books/week-23-el-corazon/`
- [ ] SEO meta tags added to page head
- [ ] Divi embed code pasted into Code Module
- [ ] Page saved as draft (not published yet)

### Pre-Publish Review
- [ ] Maestro reviewed content
- [ ] Images approved (or placeholders acceptable)
- [ ] All links tested
- [ ] Mobile preview looks good
- [ ] Analytics tracking confirmed

### Launch Checklist
- [ ] Publish page
- [ ] Test live URL
- [ ] Submit to Google Search Console
- [ ] Share on social media
- [ ] Send to email list
- [ ] Add to books index page
- [ ] Monitor analytics first 24h

---

## 🐛 Known Issues / Notes

- If images aren't generated yet, SVG placeholders will show (✅ OK)
- Google My Business link needs to be updated before launch (❗ REQUIRED)
- Email signup form action needs backend integration (optional for v1)

---

## 📝 Notes from Build

- Built: January 30, 2026, 10:00 PM MST
- Agent: Books Agent (automated)
- Theme: Love & Family (February)
- Next book: Week 24 - Los Ayudantes (Community Helpers)

---

**Ready to deploy?** ✅  
**Blockers?** ⬜ List here

---

**Signed off by:**
- [ ] Books Agent (automated QA passed)
- [ ] Maestro (human review)
- [ ] Technical review (links tested)
