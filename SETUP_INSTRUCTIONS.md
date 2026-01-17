# Ghoztwoods LLC Website - Git Setup Instructions

## Current Status
✅ Clean website directory created at: `C:\Users\avery\ghoztwoods-website`
✅ All website files copied (HTML, CSS, JS, assets, backend, GitHub workflows)
✅ Git repository initialized

## Next Steps to Complete Setup

### Step 1: Open Terminal in Correct Directory
```powershell
cd C:\Users\avery\ghoztwoods-website
```

### Step 2: Verify You're in the Right Place
```powershell
pwd
# Should show: C:\Users\avery\ghoztwoods-website

dir
# Should show only website files (index.html, assets/, backend/, etc.)
```

### Step 3: Add All Files to Git
```powershell
git add .
```

### Step 4: Create Initial Commit
```powershell
git commit -m "Initial commit: Clean Ghoztwoods LLC website"
```

### Step 5: Rename Branch to main
```powershell
git branch -M main
```

### Step 6: Add Remote Repository
```powershell
git remote add origin https://github.com/Ghozta1320/ghoztwoods-llc-website.git
```

### Step 7: Push to GitHub (Force Push to Replace Old Content)
```powershell
git push origin main --force
```

## What This Accomplishes

1. **Clean Repository**: Only website files (no Python homework, no other projects)
2. **Proper Structure**:
   - `index.html` - Main landing page
   - `technician-tracker.html` - Technician tracking feature
   - `scam-detection.html` - Scam detection tools
   - `assets/` - CSS and JavaScript files
   - `backend/` - Python backend files
   - `.github/workflows/` - GitHub Actions for deployment

3. **GitHub Pages Deployment**: The workflow will automatically deploy your site

## Verification

After pushing, check:
1. Go to: https://github.com/Ghozta1320/ghoztwoods-llc-website
2. Verify only website files are there
3. Check Actions tab to see if deployment is running
4. Your site will be live at: https://ghozta1320.github.io/ghoztwoods-llc-website/

## Troubleshooting

If you get "remote origin already exists":
```powershell
git remote remove origin
git remote add origin https://github.com/Ghozta1320/ghoztwoods-llc-website.git
```

If push is rejected:
```powershell
git push origin main --force
```
(This will replace all content in the repository with your clean website files)

## Files in This Directory

- index.html
- technician-tracker.html  
- scam-detection.html
- README.md
- .gitignore
- .nojekyll
- assets/css/main.css
- assets/css/tracker.css
- assets/js/tracker.js
- backend/api.py
- backend/geo_tracker.py
- backend/osint_scanner.py
- backend/requirements.txt
- .github/workflows/deploy.yml
- .github/workflows/ruby.yml

Total: 15 files (clean website only!)
