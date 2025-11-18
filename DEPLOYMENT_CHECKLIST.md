# GitHub Pages Deployment Checklist

Quick reference guide for deploying the Federal Districts Map to GitHub Pages.

## ✅ Pre-Deployment Checklist

- [ ] All changes committed and pushed to branch
- [ ] Validation script passes (`python validate.py`)
- [ ] `index.html` and `landing.html` in repository root
- [ ] Files tested locally in browser
- [ ] README.md and DEPLOYMENT.md up to date

## 🚀 Initial Deployment Steps

### Step 1: Choose Deployment Branch ⏱️ 2 minutes

**Option A: Merge to Main (Recommended)**
```bash
git checkout main
git pull origin main
git merge claude/evaluate-project-state-01HQZ5zq6QZCrhwwR5KPsm1M
git push origin main
```

**Option B: Deploy from Feature Branch**
- Use current branch: `claude/evaluate-project-state-01HQZ5zq6QZCrhwwR5KPsm1M`
- Configure in GitHub Pages settings (Step 2)

---

### Step 2: Enable GitHub Pages on GitHub.com ⏱️ 3 minutes

**URL:** https://github.com/Jacob234/Federal-Districts-Map/settings/pages

**Instructions:**

1. ✅ Navigate to repository on GitHub
   - Go to: https://github.com/Jacob234/Federal-Districts-Map

2. ✅ Click **"Settings"** tab (top of page)

3. ✅ In left sidebar, click **"Pages"** under "Code and automation"

4. ✅ Configure source:
   - **Source:** Deploy from a branch
   - **Branch:** Select `main` (or your branch)
   - **Folder:** Select `/ (root)`
   - Click **"Save"**

5. ✅ Wait for deployment
   - Page will refresh and show: "Your site is live at..."
   - URL will be: `https://jacob234.github.io/Federal-Districts-Map/`
   - **Wait time:** 1-2 minutes for first deployment

6. ✅ Click the URL to verify deployment

---

### Step 3: Verify Deployment ⏱️ 2 minutes

Test these URLs in your browser:

- [ ] **Landing page:** `https://jacob234.github.io/Federal-Districts-Map/landing.html`
  - Should show introduction with statistics
  - "View Interactive Map" button should work

- [ ] **Interactive map:** `https://jacob234.github.io/Federal-Districts-Map/index.html`
  - Map should load within 5 seconds
  - All 10 layers should be in layer control (top right)
  - Educational sidebar should be visible (left side)
  - Address search box should be present

- [ ] **Test interactivity:**
  - Toggle 2-3 layers on/off
  - Click on a district (popup should appear)
  - Try address search (e.g., "White House, DC")
  - Test fullscreen mode button

---

### Step 4: Update Documentation ⏱️ 3 minutes

Once deployment succeeds:

1. ✅ Update `DEPLOYMENT.md`:
   ```markdown
   ## 🌐 Current Deployment Status

   **Status:** ✅ **Live and Deployed**

   - **Live URL:** https://jacob234.github.io/Federal-Districts-Map/
   - **Landing Page:** https://jacob234.github.io/Federal-Districts-Map/landing.html
   - **Direct to Map:** https://jacob234.github.io/Federal-Districts-Map/index.html
   - **Deployed from:** `main` branch
   ```

2. ✅ Commit documentation update:
   ```bash
   git add DEPLOYMENT.md
   git commit -m "Update deployment documentation with live URL"
   git push origin main
   ```

---

## 🔄 Future Updates Workflow

After initial setup, updating is simple:

```bash
# 1. Make changes (regenerate map if needed)
python generate_map.py

# 2. Commit and push
git add index.html landing.html
git commit -m "Update map with latest data"
git push origin main

# 3. Wait 1-2 minutes for auto-deploy
# 4. Verify changes at live URL
```

---

## 🐛 Troubleshooting

### "Your site is having trouble building"
- Check GitHub Actions tab for error details
- Ensure `index.html` and `landing.html` are in root
- Verify files are valid HTML (run `python validate.py`)

### "404 Page Not Found"
- Wait 2-3 minutes and refresh
- Check GitHub Pages settings are correct
- Ensure branch has latest changes
- Clear browser cache

### Map doesn't load
- Check browser console for errors (F12)
- Verify file size isn't too large (should be ~5MB)
- Test on different browser
- Check internet connection (map uses external tiles)

### Slow loading
- Normal for first load (~5MB file)
- Enable gzip compression (automatic on GitHub Pages)
- Consider CDN for high traffic (see DEPLOYMENT.md)

---

## 📊 Deployment Verification Checklist

After deployment, verify:

- [ ] Landing page loads correctly
- [ ] "View Interactive Map" button works
- [ ] Map loads and displays correctly
- [ ] All 10 layers are available in layer control
- [ ] Layer toggle works (try 2-3 layers)
- [ ] Click on district shows popup with educational content
- [ ] Educational sidebar is visible and readable
- [ ] Address search box is present
- [ ] Address search works (test: "Times Square, NY")
- [ ] Results panel appears with correct districts
- [ ] Fullscreen button works
- [ ] Mobile responsive (test on phone or DevTools)
- [ ] No console errors (press F12 to check)

---

## 🎯 Success Criteria

Your deployment is successful when:

✅ All checklist items above pass
✅ Map loads in under 5 seconds on good connection
✅ Address search returns results
✅ Educational content is readable
✅ No JavaScript errors in console
✅ Works on mobile and desktop

---

## 📞 Need Help?

- **GitHub Pages Docs:** https://docs.github.com/en/pages
- **Repository Issues:** https://github.com/Jacob234/Federal-Districts-Map/issues
- **Validation Script:** Run `python validate.py` to check files

---

**Estimated total time:** 10 minutes for first-time setup

**Last updated:** November 2025
