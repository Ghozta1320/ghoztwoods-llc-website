# 🚀 RENDER.COM DEPLOYMENT GUIDE - GHOZTWOODS LLC

## **Step-by-Step Instructions**

### **Step 1: Push Code to GitHub (Remove API Key First)**

Before we can deploy, we need to remove the API key from scam-detection.html and push to GitHub.

**I'll do this for you in the next step.**

---

### **Step 2: Create New Web Service on Render**

1. Go to https://dashboard.render.com
2. Click **"New +"** button (top right)
3. Select **"Web Service"**
4. Click **"Build and deploy from a Git repository"**
5. Click **"Connect account"** if needed, then select your GitHub account
6. Find and select: **`ghoztwoods-llc-website`** repository
7. Click **"Connect"**

---

### **Step 3: Configure the Service**

Fill in these settings:

**Name:** `ghoztwoods-scam-intel-api`

**Region:** `Oregon (US West)`

**Branch:** `main`

**Root Directory:** Leave blank (or enter `backend` if it asks)

**Runtime:** `Python 3`

**Build Command:**
```
pip install -r backend/requirements.txt
```

**Start Command:**
```
cd backend && gunicorn scam_intel_api:app
```

**Instance Type:** `Free`

---

### **Step 4: Add Environment Variables**

Scroll down to **"Environment Variables"** section:

Click **"Add Environment Variable"** and add:

**Key:** `HF_API_KEY`  
**Value:** `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`

Click **"Add Environment Variable"** again:

**Key:** `FLASK_ENV`  
**Value:** `production`

---

### **Step 5: Deploy**

1. Click **"Create Web Service"** button at the bottom
2. Render will start building your API
3. Wait 3-5 minutes for deployment to complete
4. You'll see logs showing the build progress

---

### **Step 6: Get Your API URL**

Once deployed, you'll see your API URL at the top:

**Example:** `https://ghoztwoods-scam-intel-api.onrender.com`

**Copy this URL** - you'll need it!

---

### **Step 7: Test Your API**

Open this URL in your browser:
```
https://ghoztwoods-scam-intel-api.onrender.com/api/health
```

You should see:
```json
{
  "status": "online",
  "service": "GHOZTWOODS Scam Intelligence API",
  "version": "1.0.0"
}
```

✅ **If you see this, your API is LIVE!**

---

### **Step 8: Update Frontend (I'll do this)**

Once you have your Render URL, I'll update `scam-detection.html` to use it.

---

## **What Happens Next:**

1. ✅ Your API is deployed on Render (free, secure, professional)
2. ✅ API key is safe in environment variables (not in code)
3. ✅ No CORS errors (Render handles this)
4. ✅ HTTPS automatically enabled
5. ✅ AI chat will work perfectly
6. ✅ All scan tools will work
7. ✅ Fortune 500 ready!

---

## **Important Notes:**

- **Free tier limitations:** API may sleep after 15 minutes of inactivity (first request takes ~30 seconds to wake up)
- **Upgrade to paid:** $7/month for always-on service (recommended for production)
- **Monitoring:** Render dashboard shows logs, metrics, and uptime

---

## **Need Help?**

If you get stuck at any step, let me know which step and I'll guide you through it!
