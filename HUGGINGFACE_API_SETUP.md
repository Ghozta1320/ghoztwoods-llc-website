# 🤖 HUGGING FACE API SETUP GUIDE
## For GHOZTWOODS LLC Scam Intelligence Center

---

## 📋 OVERVIEW

The Scam Intelligence Center uses **Hugging Face's Mistral-7B-Instruct** model for conversational AI analysis. This is a FREE, open-source AI with LOW MODERATION, perfect for IC-level scam investigation.

---

## 🚀 QUICK START (5 MINUTES)

### Step 1: Get Your FREE API Key

1. Go to: **https://huggingface.co/join**
2. Create a free account (no credit card required)
3. Go to: **https://huggingface.co/settings/tokens**
4. Click **"New token"**
5. Name it: `GHOZTWOODS_SCAM_INTEL`
6. Select: **Read** access
7. Click **"Generate token"**
8. **COPY THE TOKEN** (you'll need it in Step 2)

### Step 2: Add API Key to Website

1. Open: `scam-detection.html`
2. Find line ~235: `const HF_API_KEY = 'hf_demo';`
3. Replace `'hf_demo'` with your token:
   ```javascript
   const HF_API_KEY = 'hf_YOUR_TOKEN_HERE';
   ```
4. Save the file
5. Commit and push to GitHub

### Step 3: Test It!

1. Go to your live site: `https://ghozta1320.github.io/ghoztwoods-llc-website/scam-detection.html`
2. Type a question like: "Analyze this phone scam: Someone called claiming to be from the IRS demanding payment"
3. The AI should respond with detailed IC-level analysis

---

## 🎯 WHY MISTRAL-7B-INSTRUCT?

✅ **FREE** - No usage limits on Hugging Face Inference API  
✅ **LOW MODERATION** - Allows investigation of scam tactics  
✅ **POWERFUL** - 7 billion parameters, trained on diverse data  
✅ **FAST** - Responses in 2-5 seconds  
✅ **NO CENSORSHIP** - Can discuss scam methodologies openly  

---

## 🔧 ADVANCED CONFIGURATION

### Rate Limits (Free Tier)
- **Requests:** Unlimited
- **Tokens per request:** 500 (configurable)
- **Concurrent requests:** 1

### Upgrade to Pro (Optional - $9/month)
- Faster inference
- Higher rate limits
- Priority access
- Go to: https://huggingface.co/pricing

### Alternative Models (If Needed)

If Mistral-7B is slow, try these alternatives:

1. **Llama-2-7B-Chat** (Meta)
   ```javascript
   const HF_API_URL = 'https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf';
   ```

2. **Falcon-7B-Instruct** (TII)
   ```javascript
   const HF_API_URL = 'https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct';
   ```

3. **GPT-J-6B** (EleutherAI)
   ```javascript
   const HF_API_URL = 'https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6b';
   ```

---

## 🛡️ SECURITY BEST PRACTICES

### ⚠️ IMPORTANT: Protect Your API Key

**NEVER commit your API key to public repositories!**

### Option 1: Environment Variables (Recommended for Production)

1. Create a backend API endpoint
2. Store API key in environment variables
3. Frontend calls your backend, backend calls Hugging Face

### Option 2: GitHub Secrets (For GitHub Pages)

1. Go to: Repository Settings > Secrets and variables > Actions
2. Add secret: `HF_API_KEY`
3. Use GitHub Actions to inject it during build

### Option 3: Client-Side (Current - OK for Demo)

- Users can see the API key in browser DevTools
- Fine for free tier with rate limits
- Upgrade to backend solution for production

---

## 📊 MONITORING USAGE

### Check Your Usage
1. Go to: https://huggingface.co/settings/tokens
2. Click on your token
3. View usage statistics

### Set Up Alerts
- Hugging Face doesn't charge for free tier
- No risk of unexpected bills
- Upgrade to Pro only if you need faster speeds

---

## 🐛 TROUBLESHOOTING

### Error: "Model is loading"
**Solution:** Wait 20 seconds and try again. Free tier models "cold start"

### Error: "Rate limit exceeded"
**Solution:** Wait 1 minute between requests on free tier

### Error: "Invalid API key"
**Solution:** 
1. Check you copied the full token (starts with `hf_`)
2. Regenerate token if needed
3. Make sure token has "Read" access

### Error: "CORS policy"
**Solution:** This is normal for client-side requests. Hugging Face allows CORS.

### AI Responses Are Generic
**Solution:** 
1. Make your prompts more specific
2. Include more context in the system prompt
3. Try a different model (see alternatives above)

---

## 🎓 CUSTOMIZATION

### Adjust Response Length
In `scam-detection.html`, find:
```javascript
parameters: {
    max_new_tokens: 500,  // Increase for longer responses
    temperature: 0.7,     // Lower = more focused, Higher = more creative
    top_p: 0.95          // Nucleus sampling
}
```

### Modify System Prompt
Edit the `SYSTEM_PROMPT` variable to change AI behavior:
```javascript
const SYSTEM_PROMPT = `You are an elite intelligence analyst...`;
```

---

## 📞 SUPPORT

### Hugging Face Support
- Docs: https://huggingface.co/docs/api-inference
- Forum: https://discuss.huggingface.co
- Discord: https://hf.co/join/discord

### GHOZTWOODS Support
- Phone: +1 (934) 667-0073
- Email: AVERYAD59@GHOZTWOODS.COM

---

## ✅ DEPLOYMENT CHECKLIST

- [ ] Created Hugging Face account
- [ ] Generated API token
- [ ] Added token to `scam-detection.html`
- [ ] Tested locally (open HTML file in browser)
- [ ] Committed changes to Git
- [ ] Pushed to GitHub
- [ ] Verified on live site
- [ ] Tested AI conversation
- [ ] Checked all navigation links work

---

## 🚀 NEXT STEPS

1. **Enable GitHub Pages** (if not already done)
2. **Test all features** on live site
3. **Share with Fortune 500 clients**
4. **Monitor usage** and upgrade if needed
5. **Consider backend API** for production security

---

**POWERED BY VETERAN EXCELLENCE**  
© 2025 GHOZTWOODS LLC | IC-LEVEL INTELLIGENCE
