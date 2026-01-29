# 🚀 Quick Start Guide

## For Hackathon Participants - Start Here!

This guide will get you from zero to deployed API in under 30 minutes.

---

## What You Need

- Python 3.8+ installed
- Git installed
- GitHub account
- Render account (free) at https://render.com

---

## 5-Minute Local Setup

### Step 1: Navigate to Project
```bash
cd voice-detection-api
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the API
```bash
python app.py
```

You should see:
```
Initializing AI Voice Detection API...
Model initialized successfully
Starting server...
 * Running on http://0.0.0.0:5000
```

### Step 5: Test It (in new terminal)
```bash
python test_comprehensive.py
```

When prompted, just press Enter to use `http://localhost:5000`

---

## 10-Minute GitHub Setup

### Step 1: Create Repository on GitHub
1. Go to https://github.com/new
2. Name: `voice-detection-api`
3. Click "Create repository" (don't initialize with anything)

### Step 2: Push Code
```bash
git init
git add .
git commit -m "AI Voice Detection API for Hackathon"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/voice-detection-api.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## 15-Minute Render Deployment

### Step 1: Sign Up
- Go to https://render.com
- Sign up with GitHub (easiest)

### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Click "Connect account" to link GitHub
3. Find and select `voice-detection-api`
4. Click "Connect"

### Step 3: Configure (Copy These Exactly)

| Setting | Value |
|---------|-------|
| Name | `voice-detection-api` (or any name) |
| Region | Singapore / Oregon (choose closest) |
| Branch | `main` |
| Runtime | `Python 3` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120` |
| Instance Type | Free (or Starter for better performance) |

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for first deployment
3. Watch the logs - look for "Model initialized successfully"

### Step 5: Get Your URL
Your API will be at: `https://YOUR-APP-NAME.onrender.com`

---

## 5-Minute Testing

### Test 1: Health Check
```bash
curl https://YOUR-APP-NAME.onrender.com/health
```

Expected:
```json
{"status": "healthy", "message": "AI Voice Detection API is running"}
```

### Test 2: With Python Script
```bash
python test_comprehensive.py
# Enter: https://YOUR-APP-NAME.onrender.com
```

### Test 3: With Real Audio (Python)
```python
import base64
import requests

# Your MP3 file
with open("sample.mp3", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode('utf-8')

response = requests.post(
    "https://YOUR-APP-NAME.onrender.com/detect",
    headers={
        "Authorization": "hackathon_api_key_2025",
        "Content-Type": "application/json"
    },
    json={"audio": audio_base64}
)

print(response.json())
```

---

## Example API Requests

### cURL Example
```bash
# Health check
curl https://your-app.onrender.com/health

# Detection (with base64 audio)
curl -X POST https://your-app.onrender.com/detect \
  -H "Authorization: hackathon_api_key_2025" \
  -H "Content-Type: application/json" \
  -d '{"audio": "BASE64_ENCODED_AUDIO_HERE"}'
```

### Python Example
```python
import requests
import base64

url = "https://your-app.onrender.com/detect"
headers = {
    "Authorization": "hackathon_api_key_2025",
    "Content-Type": "application/json"
}

# Encode your audio file
with open("audio.mp3", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode('utf-8')

data = {"audio": audio_base64}
response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### JavaScript Example
```javascript
const fs = require('fs');

const audioBuffer = fs.readFileSync('audio.mp3');
const audioBase64 = audioBuffer.toString('base64');

fetch('https://your-app.onrender.com/detect', {
  method: 'POST',
  headers: {
    'Authorization': 'hackathon_api_key_2025',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ audio: audioBase64 })
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## Expected Response Format

### Success (200)
```json
{
  "classification": "AI_GENERATED",
  "confidence": 0.87,
  "language": "English",
  "explanation": "The voice sample in English shows characteristics typical of AI-generated speech, including consistent pitch patterns and spectral uniformity. Confidence: 87%"
}
```

or

```json
{
  "classification": "HUMAN",
  "confidence": 0.82,
  "language": "Tamil",
  "explanation": "The voice sample in Tamil exhibits natural human speech patterns, including pitch variation and natural prosody. Confidence: 82%"
}
```

### Authentication Error (401)
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing API key"
}
```

### Bad Request (400)
```json
{
  "error": "Bad Request",
  "message": "Missing 'audio' field in request body"
}
```

---

## Hackathon Submission Format

When submitting to the hackathon, provide:

```
API Endpoint: https://YOUR-APP-NAME.onrender.com/detect
API Key: hackathon_api_key_2025
Method: POST
Content-Type: application/json

Request Format:
{
  "audio": "<base64_encoded_mp3_audio>"
}

Response Format:
{
  "classification": "AI_GENERATED" or "HUMAN",
  "confidence": 0.0 to 1.0,
  "language": "Tamil/English/Hindi/Malayalam/Telugu",
  "explanation": "Human-readable explanation"
}
```

---

## Common Issues & Quick Fixes

### Issue: "Module not found"
```bash
pip install -r requirements.txt
```

### Issue: "Address already in use"
```bash
# Change port in app.py
port = int(os.environ.get('PORT', 5001))  # Changed to 5001
```

### Issue: Render build fails
- Check you pushed all files to GitHub
- Verify requirements.txt is correct
- Check Render logs for specific error

### Issue: API returns 500
- Check Render logs
- Verify audio is valid base64
- Test with test_comprehensive.py first

### Issue: Slow responses on free tier
- Upgrade to Starter plan ($7/month)
- Or keep app warm with UptimeRobot

---

## Emergency Support

If you're stuck:

1. **Check the logs** (Render dashboard → Logs tab)
2. **Test locally first** with test_comprehensive.py
3. **Verify your GitHub repo** has all files
4. **Check these files exist:**
   - app.py
   - requirements.txt
   - Procfile
   - runtime.txt

5. **Common file issues:**
   ```bash
   # Verify files
   ls -la
   
   # Should see:
   # app.py
   # requirements.txt
   # Procfile
   # runtime.txt
   # README.md
   # test_comprehensive.py
   ```

---

## Pre-Submission Checklist

Before submitting to hackathon:

- [ ] API is deployed and accessible
- [ ] Health endpoint works: `curl https://your-app.onrender.com/health`
- [ ] Detection endpoint tested with sample audio
- [ ] Returns correct JSON format
- [ ] Authentication works with API key
- [ ] Tested with all 5 languages (or at least varied audio)
- [ ] No errors in Render logs
- [ ] Response time is acceptable (< 30 seconds)
- [ ] API URL written down
- [ ] API key written down: `hackathon_api_key_2025`

---

## Tips for Success

1. **Test early and often** - Don't wait until last minute
2. **Keep it simple** - The current solution works well
3. **Monitor your API** - Set up UptimeRobot for free tier
4. **Have backups** - Know your API URL and keep logs
5. **Document everything** - Take screenshots of successful tests

---

## Next Steps After Deployment

1. **Test with hackathon's sample audio** (if provided)
2. **Keep your app awake** during evaluation period
3. **Monitor Render logs** during evaluation
4. **Don't make changes** after submission unless necessary
5. **Keep your computer on** if using free tier during evaluation

---

## Good Luck! 🍀

You've got everything you need. The API works, it's deployable, and it meets all requirements. Just follow the steps carefully and you'll be fine!

**Remember**: Test → Deploy → Test Again → Submit → Monitor

---

## Quick Reference

**Your API Details:**
- Endpoint: `https://YOUR-APP-NAME.onrender.com/detect`
- Method: `POST`
- Auth Header: `Authorization: hackathon_api_key_2025`
- Content-Type: `application/json`
- Body: `{"audio": "base64_string"}`

**Supported Languages:**
- Tamil
- English  
- Hindi
- Malayalam
- Telugu

**Response:**
- classification: "AI_GENERATED" or "HUMAN"
- confidence: 0.0 to 1.0
- language: detected language
- explanation: detailed explanation

---

**You're ready to win this hackathon! 🏆**
