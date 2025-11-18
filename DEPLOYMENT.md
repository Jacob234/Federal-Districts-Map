# Deployment Guide - Mini-Web Version

Complete guide for hosting the US Federal Districts Educational Map on various platforms.

## 📋 Prerequisites

You need only two files:
- `landing.html` (introduction page)
- `index.html` (interactive map, ~5.3 MB)

The `data/` folder is **not** required for deployment (data is embedded in `index.html`).

## 🌐 Current Deployment Status

**Status:** ⚠️ **Ready for deployment but not yet live**

The project is fully prepared for GitHub Pages deployment. Files are in the repository root and ready to serve.

**After you enable GitHub Pages (see instructions below), the URLs will be:**
- **Live URL:** `https://jacob234.github.io/Federal-Districts-Map/`
- **Landing Page:** `https://jacob234.github.io/Federal-Districts-Map/landing.html`
- **Direct to Map:** `https://jacob234.github.io/Federal-Districts-Map/index.html`

**Current branch:** `claude/evaluate-project-state-01HQZ5zq6QZCrhwwR5KPsm1M`
**Recommended:** Merge to `main` or create `gh-pages` branch for GitHub Pages

Files are served from the **repository root** (`/`).

## 📁 File Structure for GitHub Pages

```
Federal-Districts-Map/
├── index.html              # Interactive map (5.3 MB, served by GH Pages)
├── landing.html            # Landing page (11 KB, served by GH Pages)
├── README.md               # Project documentation
├── DEPLOYMENT.md           # This file
├── requirements.txt        # Python dependencies
├── validate.py             # Validation script
│
├── generate_map.py         # Map generator script
├── map_config.py           # Layer configurations
│
├── data/                   # Optimized GeoJSON files (3.9 MB total)
│   ├── Courts_of_Appeals_Circuits.geojson
│   ├── Bankruptcy_Courts.geojson
│   ├── FEMA_Regions.geojson
│   └── [7 more district files]
│
└── scripts/
    └── optimize_data.py    # Data optimization tool
```

**Note:** Only `index.html` and `landing.html` are served by GitHub Pages. The `data/` folder is embedded in the HTML files.

## 🚀 Initial GitHub Pages Setup

**First-time deployment? Follow these steps:**

### Step 1: Prepare Your Branch

**Option A: Merge to main** (Recommended)
```bash
# Ensure you're on your feature branch
git checkout claude/evaluate-project-state-01HQZ5zq6QZCrhwwR5KPsm1M

# Merge to main
git checkout main
git merge claude/evaluate-project-state-01HQZ5zq6QZCrhwwR5KPsm1M
git push origin main
```

**Option B: Deploy from current branch**
- Keep files on `claude/evaluate-project-state-01HQZ5zq6QZCrhwwR5KPsm1M`
- Configure GitHub Pages to use this branch (see Step 2)

### Step 2: Enable GitHub Pages (Manual - On GitHub.com)

1. **Go to repository on GitHub:**
   - Navigate to https://github.com/Jacob234/Federal-Districts-Map

2. **Open Settings:**
   - Click "Settings" tab at the top

3. **Navigate to Pages:**
   - In left sidebar, click "Pages" under "Code and automation"

4. **Configure Source:**
   - Under "Build and deployment"
   - Source: Select "Deploy from a branch"
   - Branch: Select your branch (e.g., `main` or current branch)
   - Folder: Select `/ (root)`
   - Click "Save"

5. **Wait for deployment:**
   - GitHub will display: "Your site is live at..."
   - Initial deployment takes 1-2 minutes
   - Refresh page to see status

6. **Verify deployment:**
   - Click the provided URL
   - Test landing page and map load correctly

### Step 3: Update Documentation

After deployment succeeds, update this file with your actual live URL.

---

## 🔄 Updating an Already-Deployed Map

Once GitHub Pages is configured, updating is easy:

1. **Make changes and regenerate** (if needed):
   ```bash
   # If you modified data or config
   python generate_map.py
   ```

2. **Commit and push**:
   ```bash
   git add index.html landing.html
   git commit -m "Update map with latest data"
   git push origin main  # or your deployment branch
   ```

3. **GitHub Pages auto-deploys** (takes 1-2 minutes)

## 🌐 Alternative Deployment Options

### Option 1: GitHub Pages (Recommended - Free)

**Best for**: Free hosting, version control, easy updates

**Current Status**: Not yet configured (see setup instructions above)

**After Setup**:
- Repository: https://github.com/Jacob234/Federal-Districts-Map
- Expected URL: https://jacob234.github.io/Federal-Districts-Map/
- Branch: `main` (recommended) or current branch
- Source: `/` (root folder)

**For Your Own Fork**:

1. **Fork the repository on GitHub**
   - Click "Fork" on https://github.com/Jacob234/Federal-Districts-Map

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Federal-Districts-Map.git
   cd Federal-Districts-Map
   ```

3. **Enable GitHub Pages** (see "Initial GitHub Pages Setup" above)

4. **Access your site**:
   - URL: `https://YOUR-USERNAME.github.io/Federal-Districts-Map/`

**Cost**: Free

**Limitations**:
- Repository must be public (for free tier)
- 1 GB storage limit
- 100 GB bandwidth/month

---

### Option 2: Netlify

**Best for**: Automatic deployments, instant previews, custom domains

**Steps**:

1. **Via Drag & Drop** (easiest):
   - Go to [https://app.netlify.com/drop](https://app.netlify.com/drop)
   - Drag the mini-web folder into the drop zone
   - Your site is live!
   - URL: `random-name-123.netlify.app`

2. **Via Git** (recommended):
   - Push code to GitHub/GitLab/Bitbucket
   - Go to [Netlify](https://app.netlify.com)
   - Click "New site from Git"
   - Select your repository
   - Build settings: (leave empty for static site)
   - Publish directory: `/` (root) or `mini-web/`
   - Click "Deploy site"

3. **Configure**:
   - Custom domain: Site settings → Domain management
   - HTTPS: Enabled automatically
   - Redirects: Create `_redirects` file if needed:
     ```
     /  /landing.html  200
     ```

**Cost**: Free (100 GB bandwidth, unlimited sites)

**Advantages**:
- Instant deployments on git push
- Automatic HTTPS
- Form handling (if you add forms)
- Easy custom domains

---

### Option 3: Vercel

**Best for**: Developer-friendly, fast deployments, excellent performance

**Steps**:

1. **Install Vercel CLI** (optional):
   ```bash
   npm install -g vercel
   ```

2. **Deploy via CLI**:
   ```bash
   cd mini-web
   vercel
   # Follow prompts
   ```

3. **Or via Web Interface**:
   - Go to [Vercel](https://vercel.com)
   - Import Git repository
   - Framework preset: "Other"
   - Root directory: `mini-web/` (if in subdirectory)
   - No build command needed
   - Click "Deploy"

4. **Custom domain**:
   - Project settings → Domains
   - Add your domain
   - Configure DNS

**Cost**: Free (100 GB bandwidth, unlimited projects)

**Advantages**:
- Excellent CDN performance
- Automatic deployments
- Preview deployments for pull requests
- Built-in analytics

---

### Option 4: Your Own Web Server

**Best for**: Full control, existing hosting, custom setup

**Apache**:

1. Upload files to web directory:
   ```bash
   scp landing.html index.html user@yourserver.com:/var/www/html/federal-districts/
   ```

2. Configure `.htaccess` (optional):
   ```apache
   # Cache static files
   <FilesMatch "\.(html|js|css)$">
       Header set Cache-Control "max-age=7200, public"
   </FilesMatch>

   # Enable compression
   <IfModule mod_deflate.c>
       AddOutputFilterByType DEFLATE text/html text/css application/javascript
   </IfModule>
   ```

**Nginx**:

1. Upload files:
   ```bash
   scp landing.html index.html user@yourserver.com:/usr/share/nginx/html/federal-districts/
   ```

2. Configure nginx (optional):
   ```nginx
   location /federal-districts {
       root /usr/share/nginx/html;
       index landing.html;

       # Enable compression
       gzip on;
       gzip_types text/html text/css application/javascript;

       # Cache headers
       expires 2h;
   }
   ```

**Cost**: Depends on hosting provider

---

### Option 5: Personal Website Integration

If you already have a website, simply:

1. **Create a subdirectory**:
   ```
   yourwebsite.com/
   └── federal-districts/
       ├── landing.html
       └── index.html
   ```

2. **Upload files** via FTP, cPanel, or your hosting control panel

3. **Link to it** from your main site:
   ```html
   <a href="/federal-districts/landing.html">View Federal Districts Map</a>
   ```

---

## 🎨 Customization Before Deployment

### 1. Update GitHub Links

In `landing.html`, update:
```html
<a href="https://github.com/YOUR-USERNAME/Federal-Districts-Map">Federal Districts Map Project</a>
```

### 2. Add Analytics (Optional)

Add Google Analytics to track visitors:

In `landing.html` and `index.html`, add before `</head>`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### 3. Add Favicon

Create a simple favicon and add to both HTML files:
```html
<link rel="icon" href="favicon.ico" type="image/x-icon">
```

### 4. Update Meta Tags for SEO

In both HTML files, update `<head>` section:
```html
<meta name="description" content="Interactive educational map of US Federal administrative districts across the three branches of government">
<meta name="keywords" content="federal districts, civics education, US government, interactive map">
<meta name="author" content="Your Name">

<!-- Open Graph for social sharing -->
<meta property="og:title" content="US Federal Districts - Educational Map">
<meta property="og:description" content="Interactive map showing how the federal government divides America">
<meta property="og:type" content="website">
<meta property="og:url" content="https://yoursite.com/federal-districts/">
```

---

## ✅ Pre-Deployment Checklist

- [ ] Test `landing.html` locally in multiple browsers
- [ ] Test `index.html` locally in multiple browsers
- [ ] Test on mobile device
- [ ] Update all links (GitHub, social media, etc.)
- [ ] Add analytics code (if desired)
- [ ] Compress files if needed (though already optimized)
- [ ] Create custom domain DNS records (if using)
- [ ] Add `robots.txt` if you want search engine control
- [ ] Test all layer toggles work correctly
- [ ] Verify all popups display educational content
- [ ] Check fullscreen mode works

---

## 🔍 Testing After Deployment

1. **Functionality**:
   - All layers toggle on/off
   - Popups appear when clicking regions
   - Educational sidebar is visible
   - Layer control works
   - Fullscreen mode works

2. **Performance**:
   - Page loads in < 5 seconds on 3G
   - Map is responsive on mobile
   - No console errors

3. **Cross-browser**:
   - Chrome/Edge
   - Firefox
   - Safari
   - Mobile browsers

4. **SEO**:
   - Use [Google PageSpeed Insights](https://pagespeed.web.dev/)
   - Check mobile-friendliness
   - Validate HTML at [W3C Validator](https://validator.w3.org/)

---

## 🐛 Troubleshooting

### Issue: Map doesn't load
**Solution**:
- Check browser console for errors
- Ensure `index.html` is not corrupted
- Try clearing browser cache
- Verify file was uploaded completely (check file size)

### Issue: Layers don't toggle
**Solution**:
- Embedded data might be corrupted
- Regenerate `index.html` with `generate_map.py`
- Check for JavaScript errors in console

### Issue: Mobile display issues
**Solution**:
- Map is responsive by default
- Check viewport meta tag exists
- Test in mobile device simulator

### Issue: Slow loading
**Solution**:
- Enable gzip compression on server
- Use CDN if available
- File is already optimized, but ensure it's being served correctly
- Check server bandwidth

### Issue: Custom domain not working
**Solution**:
- DNS can take 24-48 hours to propagate
- Verify DNS records are correct
- Check CNAME file (for GitHub Pages)
- Ensure SSL certificate is configured

---

## 📊 Performance Optimization

The map is already optimized, but you can improve delivery:

### 1. Enable Compression

Most platforms do this automatically, but verify:
```bash
curl -H "Accept-Encoding: gzip,deflate" -I https://yoursite.com/index.html
# Look for: Content-Encoding: gzip
```

### 2. CDN (Optional)

For global audience, consider Cloudflare (free):
- Point your domain to Cloudflare
- Automatic CDN distribution
- Free SSL certificate
- DDoS protection

### 3. Caching Headers

Set appropriate cache headers:
```
Cache-Control: max-age=7200, public
```

---

## 📱 Mobile Optimization

The map is already mobile-friendly, but consider:

1. **Progressive Web App** (advanced):
   - Add `manifest.json`
   - Add service worker for offline access
   - Users can "install" to home screen

2. **App Stores** (advanced):
   - Wrap in Cordova/PhoneGap
   - Publish to app stores
   - Requires developer accounts

---

## 🔐 Security Considerations

For static sites, security is minimal, but:

1. **HTTPS**: Always use (automatic on GitHub Pages, Netlify, Vercel)
2. **Content Security Policy**: Add if needed
3. **No sensitive data**: Map has no user data, perfect for public hosting

---

## 📈 Monitoring

Track your deployment:

1. **Google Analytics**: See visitor counts, page views
2. **Netlify/Vercel Analytics**: Built-in metrics
3. **Server logs**: If self-hosting
4. **Uptime monitoring**: [UptimeRobot](https://uptimerobot.com/) (free)

---

## 🎉 You're Done!

Your educational map is now live and accessible to the world!

**Share it**:
- Twitter/X
- Facebook
- LinkedIn
- Educational forums
- With teachers and students

**Promote it**:
- Add to your resume/portfolio
- Submit to civics education resources
- Share with local schools
- Post on Reddit (r/dataisbeautiful, r/MapPorn)

---

**Questions?** Open an issue on the [main repository](https://github.com/Jacob234/Federal-Districts-Map/issues).
