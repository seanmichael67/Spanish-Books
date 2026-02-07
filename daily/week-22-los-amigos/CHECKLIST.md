# Pre-Deployment Checklist
## Los Amigos (Week 22)

Use this checklist before publishing the book to WordPress.

---

## ✅ Content Quality

### Vocabulary & Text
- [ ] All 7 vocabulary words present (amigo, jugar, compartir, ayudar, reír, abrazar, gentil)
- [ ] Spanish sentences grammatically correct
- [ ] English translations accurate
- [ ] Text appropriate for ages 2-5 (simple, short sentences)
- [ ] No typos or spelling errors
- [ ] Accent marks correct (español, gentil, etc.)

### Page Count
- [ ] Total 10 pages
- [ ] Page 1: Title page
- [ ] Pages 2-9: Vocabulary pages
- [ ] Page 10: End page with CTAs

---

## 🎨 Images

### Quality
- [ ] All 10 images present (or placeholder SVGs working)
- [ ] Images clear and colorful
- [ ] Age-appropriate (no scary/sad content)
- [ ] Diverse representation of children
- [ ] Consistent cartoon style across all pages

### Technical
- [ ] Format: WebP (with JPG fallback)
- [ ] File size: Each <100KB
- [ ] Dimensions: 800x600px or 1024x1024px
- [ ] Alt text present for accessibility
- [ ] Images lazy-load correctly
- [ ] Fallback SVGs display if image missing

---

## 🔊 Audio

### Functionality
- [ ] Audio button present on each page
- [ ] Audio plays in Spanish (es-ES)
- [ ] Pronunciation clear and correct
- [ ] Speed appropriate (0.85 rate = slightly slow)
- [ ] Works on desktop browsers (Chrome, Firefox, Safari)
- [ ] Works on mobile browsers
- [ ] Graceful fallback if Web Speech API not supported

### Content
- [ ] Audio text matches Spanish sentence on page
- [ ] No pronunciation errors (check accents)

---

## 🖥️ Technical Performance

### Page Load
- [ ] Total page load <2 seconds (test with slow 3G)
- [ ] No render-blocking resources
- [ ] CSS/JS minified or inline
- [ ] Images compressed and optimized
- [ ] Lazy loading enabled

### Browser Compatibility
- [ ] Works in Chrome (desktop + mobile)
- [ ] Works in Safari (desktop + mobile)
- [ ] Works in Firefox
- [ ] Works in Edge
- [ ] Graceful degradation in older browsers

### Responsive Design
- [ ] Looks good on desktop (1920x1080)
- [ ] Looks good on tablet (768x1024)
- [ ] Looks good on mobile (375x667)
- [ ] Buttons large enough to tap (44x44px minimum)
- [ ] Text readable on small screens
- [ ] Images scale properly

---

## 🧭 Navigation

### Functionality
- [ ] "Anterior" (previous) button works
- [ ] "Siguiente" (next) button works
- [ ] Buttons disabled on first/last page appropriately
- [ ] Page indicator shows correct page number
- [ ] Keyboard navigation works (arrow keys)
- [ ] No JavaScript errors in console

### UX
- [ ] Page transitions smooth
- [ ] No flickering or jumps
- [ ] Progress clear to user
- [ ] Easy to return to previous page

---

## 📊 SEO Optimization

### Meta Tags (seo-meta.html)
- [ ] Title tag present and accurate
- [ ] Meta description present (150-160 characters)
- [ ] Keywords relevant and not stuffed
- [ ] Canonical URL set correctly
- [ ] Open Graph tags complete (title, description, image, url)
- [ ] Twitter Card tags complete
- [ ] Image URLs absolute (not relative)

### Schema Markup
- [ ] Book schema present and valid
- [ ] Organization schema present
- [ ] BreadcrumbList schema present
- [ ] LearningResource schema present
- [ ] Validates in Google Rich Results Test
- [ ] No errors in structured data

### On-Page SEO
- [ ] H1 tag present on page ("Los Amigos")
- [ ] URL slug clean (/spanish-books/week-22-los-amigos/)
- [ ] Alt text on all images
- [ ] Internal links present (to enrollment, shop, etc.)
- [ ] Page title descriptive and keyword-rich

---

## 💼 Business CTAs

### Top Banner
- [ ] Banner visible and prominent
- [ ] Link to enrollment/tour page works
- [ ] Text clear and compelling
- [ ] Mobile-friendly

### End Page - Google Review
- [ ] Review request present
- [ ] Google My Business link correct (NOT placeholder)
- [ ] Text motivating ("unlock bonus book")
- [ ] Button styled and clickable

### End Page - Email Signup
- [ ] Form present and functional
- [ ] Email validation works
- [ ] Submit button works
- [ ] Success message shows
- [ ] Connected to email service (Mailchimp, ConvertKit, etc.)
- [ ] Or: Shows alert with confirmation (TODO: connect to service)

### End Page - Tour/Enrollment
- [ ] Link to enrollment page present
- [ ] Button styled prominently
- [ ] Opens in new tab or same tab (consistent)

---

## 📈 Analytics Tracking

### Google Analytics
- [ ] GA4 tracking code installed (on WordPress site)
- [ ] Custom events fire correctly:
  - `book_page_view` (on initial load)
  - `page_view` (on each page flip)
  - `book_complete` (on reaching last page)
  - `email_signup` (on form submission)
- [ ] Test events in GA4 DebugView

### Conversion Tracking
- [ ] Email signup tracked
- [ ] Review button clicks tracked
- [ ] Tour button clicks tracked

---

## 🔗 WordPress Integration

### File Upload
- [ ] Entire folder uploaded to correct path
- [ ] Path: `/wp-content/uploads/books/week-22-los-amigos/`
- [ ] All files present (HTML, images, etc.)
- [ ] Permissions correct (readable by web server)

### Page Creation
- [ ] WordPress page created
- [ ] Title: "Los Amigos - Free Spanish Book for Preschool"
- [ ] URL slug: `/spanish-books/week-22-los-amigos/`
- [ ] Parent page (if applicable): "Spanish Books"

### Divi Embed
- [ ] Divi Code Module added to page
- [ ] `divi-embed-code.html` pasted correctly
- [ ] iFrame src path correct (absolute or relative)
- [ ] iFrame height appropriate (700px desktop, 600px mobile)
- [ ] No CSS conflicts with theme

### SEO Settings
- [ ] Meta tags added to page head (via plugin or Yoast)
- [ ] Social preview looks good (Facebook, Twitter)
- [ ] Canonical URL matches page URL
- [ ] Robots: index, follow

---

## 🧪 Final Testing

### Desktop Test
- [ ] Open in Chrome
- [ ] Click through all 10 pages
- [ ] Play audio on 3+ random pages
- [ ] Click all CTA buttons
- [ ] Check browser console (no errors)
- [ ] Test keyboard navigation

### Mobile Test
- [ ] Open on iPhone/Android
- [ ] Tap through all 10 pages
- [ ] Play audio on 3+ random pages
- [ ] Tap all CTA buttons
- [ ] Portrait and landscape orientation
- [ ] Text readable without zooming

### Speed Test
- [ ] Run Google PageSpeed Insights
- [ ] Score: >90 on mobile
- [ ] Score: >95 on desktop
- [ ] Largest Contentful Paint (LCP) <2.5s
- [ ] First Input Delay (FID) <100ms

### Accessibility Test
- [ ] Run WAVE or aXe accessibility checker
- [ ] No errors or critical issues
- [ ] Alt text on all images
- [ ] Keyboard navigable
- [ ] Color contrast sufficient (WCAG AA)

### Cross-Browser Test
- [ ] Chrome (latest)
- [ ] Safari (latest)
- [ ] Firefox (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

---

## 📱 Social Media Preview

### Facebook
- [ ] Share link on Facebook
- [ ] Preview image displays correctly
- [ ] Title and description accurate
- [ ] No broken images

### Twitter
- [ ] Tweet link
- [ ] Twitter Card displays correctly
- [ ] Image and text look good

### Email
- [ ] Send test email with link
- [ ] Link works when clicked
- [ ] Looks good in mobile email apps

---

## 🚨 Pre-Launch Final Checks

- [ ] All above sections completed ✅
- [ ] No console errors in browser
- [ ] No broken links (404s)
- [ ] Google review link updated (not placeholder)
- [ ] Email signup connected (or TODO noted)
- [ ] Contact info updated (phone, email)
- [ ] Stakeholders notified (Maestro, teachers, staff)
- [ ] Backup of site made (before publishing)

---

## 🎉 Post-Launch

### Immediate (Day 1)
- [ ] Share on Facebook page
- [ ] Share on Instagram
- [ ] Email to parent mailing list
- [ ] Post in Facebook parent group
- [ ] Add to homepage "Featured Books" section

### Week 1
- [ ] Check analytics (views, completion rate)
- [ ] Monitor for bugs/issues (check error logs)
- [ ] Respond to parent feedback
- [ ] Adjust CTAs if low conversion

### Week 2-4
- [ ] Review SEO performance (Google Search Console)
- [ ] Collect and respond to Google reviews
- [ ] A/B test different CTAs (if needed)
- [ ] Plan improvements for future books

---

## 📝 Notes & Issues

_Record any issues found during testing:_

**Issue 1:**
- Description:
- Severity: (Critical / High / Medium / Low)
- Status: (Open / Fixed)
- Fix:

**Issue 2:**
- ...

---

## ✅ Final Approval

**QA Completed By:** _______________  
**Date:** _______________  
**Approved for Launch:** ☐ Yes  ☐ No (issues noted above)

**Maestro Approval:** ☐ Approved  
**Date:** _______________

---

**Ready to Launch! 🚀**

Once all boxes checked and approved, proceed with publishing to WordPress.
