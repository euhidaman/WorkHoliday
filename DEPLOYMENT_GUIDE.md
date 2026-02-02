# 🚀 Netlify Deployment Guide for WorkHoliday Visa Guide

## Prerequisites
- A GitHub account (free)
- A Netlify account (free - sign up at netlify.com)

---

## Method 1: Deploy via GitHub (Recommended - Auto-deploys on updates)

### Step 1: Push to GitHub

1. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Repository name: `workholiday-visa-guide` (or any name you prefer)
   - Description: "Comprehensive visa guide for work and holiday visas"
   - Choose: **Public** or **Private** (both work with Netlify free tier)
   - **DO NOT** initialize with README, .gitignore, or license
   - Click "Create repository"

2. **Push your local code to GitHub:**
   Open PowerShell in the WorkHoliday directory and run:

```powershell
# Check current git status
git status

# Add all files (respects .gitignore)
git add .

# Commit the changes
git commit -m "Initial commit - WorkHoliday Visa Guide ready for deployment"

# Add GitHub as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/workholiday-visa-guide.git

# Push to GitHub
git push -u origin main
```

If you get an error about "main" vs "master", try:
```powershell
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Netlify

1. **Sign up/Login to Netlify:**
   - Go to https://app.netlify.com/
   - Click "Sign up" and choose "Sign up with GitHub"
   - Authorize Netlify to access your GitHub account

2. **Create a new site:**
   - Click "Add new site" → "Import an existing project"
   - Click "Deploy with GitHub"
   - Authorize Netlify if prompted
   - Select your `workholiday-visa-guide` repository

3. **Configure build settings:**
   - **Site name**: Choose a custom name (e.g., `workholiday-guides`)
     Your site will be at: `workholiday-guides.netlify.app`
   - **Branch to deploy**: `main`
   - **Build command**: Leave empty (static site)
   - **Publish directory**: `.` (or leave empty)
   - Click "Deploy site"

4. **Wait for deployment:**
   - Netlify will deploy your site (takes 30-60 seconds)
   - Once complete, you'll see "Site is live" ✅
   - Your site URL: `https://your-site-name.netlify.app`

### Step 3: Custom Domain (Optional)

If you have a custom domain:
1. Go to "Domain settings" in Netlify
2. Click "Add custom domain"
3. Follow the DNS configuration instructions
4. Netlify provides free SSL automatically!

---

## Method 2: Quick Deploy via Drag & Drop (Fastest)

### Step 1: Prepare a deployment folder

1. **Copy your project to a new folder:**
   - Create a new folder: `C:\WorkHoliday-Deploy`
   - Copy these files/folders from your WorkHoliday directory:
     - `index.html` and all other `.html` files
     - `css/` folder
     - `js/` folder
     - `img/` folder
     - `lib/` folder
     - `countries/` folder
     - `mail/` folder
     - `netlify.toml`
     - `LICENSE.txt`
   - **EXCLUDE**: 
     - `backend/` folder
     - `.git/` folder
     - All `.ps1` files
     - PDF and MD documentation files

### Step 2: Deploy to Netlify

1. **Go to Netlify:**
   - Visit https://app.netlify.com/drop
   - Sign up/login if needed

2. **Drag and drop:**
   - Open File Explorer
   - Navigate to `C:\WorkHoliday-Deploy`
   - Select ALL files and folders
   - Drag them to the Netlify drop zone
   - Drop!

3. **Wait for deployment:**
   - Netlify uploads and deploys (30-60 seconds)
   - You'll get a random URL like: `random-name-123.netlify.app`
   - Click "Site settings" → "Change site name" to customize it

---

## Post-Deployment Checklist

✅ Visit your site URL and test:
- [ ] Homepage loads correctly
- [ ] Country picker works (select origin → destination → submit)
- [ ] Navigation menu works (Home and Contact visible)
- [ ] Individual country pages load (e.g., `/countries/USA-to-Canada.html`)
- [ ] All images load
- [ ] Mobile responsive design works (use browser DevTools or phone)
- [ ] Contact form works

✅ Configure site settings in Netlify:
- [ ] Custom domain (if you have one)
- [ ] HTTPS is enabled (automatic)
- [ ] Set site name to something memorable

---

## Updating Your Site (Method 1 - GitHub)

To update your live site after making changes:

```powershell
cd C:\Users\User\Desktop\Freelancing\WorkHoliday

# Make your changes to files...

# Add and commit changes
git add .
git commit -m "Updated visa information for Germany"

# Push to GitHub
git push

# Netlify auto-deploys within 1 minute! ✨
```

## Updating Your Site (Method 2 - Drag & Drop)

1. Make changes to your local files
2. Go to Netlify dashboard → Your site → "Deploys"
3. Drag the updated folder to the deploy zone
4. New version goes live in ~30 seconds!

---

## Troubleshooting

### Images not loading?
- Check that `img/` folder was deployed
- Verify image paths are relative (start with `img/` not `/img/`)

### CSS not applying?
- Check that `css/style.css` file exists in deployment
- Clear browser cache (Ctrl + Shift + R)

### Country pages showing 404?
- Ensure `countries/` folder with all HTML files was deployed
- Check that file names match exactly (case-sensitive on some systems)

### Custom domain not working?
- DNS changes can take 24-48 hours
- Verify you added the correct DNS records in your domain registrar

---

## Your Site Information

After deployment, save these details:

- **Site Name**: ___________________________
- **URL**: https://_________________.netlify.app
- **Custom Domain** (if any): ___________________________
- **GitHub Repo** (if Method 1): ___________________________
- **Deployment Method**: □ GitHub (Auto) □ Manual (Drag & Drop)
- **Deployed Date**: ___________________________

---

## Need Help?

- Netlify Docs: https://docs.netlify.com/
- Netlify Community: https://answers.netlify.com/
- Your site's deploy logs: Netlify Dashboard → Your Site → Deploys

🎉 **Congratulations! Your visa guide is now live and accessible worldwide!**
