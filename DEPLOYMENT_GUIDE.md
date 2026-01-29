# 🚀 Complete Deployment Guide

## Quick Deployment Checklist

### ✅ Pre-Deployment
- [ ] All files created and saved
- [ ] Dependencies listed in requirements.txt
- [ ] API tested locally
- [ ] GitHub repository created
- [ ] Code pushed to GitHub

### ✅ Render Deployment
- [ ] Render account created
- [ ] New Web Service created
- [ ] GitHub repository connected
- [ ] Build and start commands configured
- [ ] Environment variables set (if needed)
- [ ] Deployment successful

### ✅ Post-Deployment
- [ ] Health endpoint tested
- [ ] Detection endpoint tested with sample audio
- [ ] API key authentication verified
- [ ] Error handling verified
- [ ] API URL documented for submission

---

## Step-by-Step Deployment on Render

### Step 1: Prepare Your GitHub Repository

1. **Create a new repository on GitHub**
   - Go to https://github.com/new
   - Name: `voice-detection-api` (or any name)
   - Description: "AI Voice Detection API for Hackathon"
   - Public or Private (both work)
   - Don't initialize with README (we already have one)
   - Click "Create repository"

2. **Push your code to GitHub**
   ```bash
   cd voice-detection-api
   git init
   git add .
   git commit -m "Initial commit: AI Voice Detection API"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/voice-detection-api.git
   git push -u origin main
   ```

   Replace `YOUR_USERNAME` with your GitHub username.

### Step 2: Deploy on Render

1. **Sign up/Login to Render**
   - Go to https://render.com
   - Sign up with GitHub (recommended) or email
   - Verify your email if needed

2. **Create New Web Service**
   - Click "New +" in the top right
   - Select "Web Service"
   - Click "Connect account" if not connected to GitHub
   - Authorize Render to access your repositories

3. **Select Repository**
   - Find and click on your `voice-detection-api` repository
   - Click "Connect"

4. **Configure Web Service**
   
   Fill in these settings:
   
   - **Name**: `voice-detection-api` (or any unique name)
     - This will be your URL: `https://voice-detection-api.onrender.com`
   
   - **Region**: Choose closest to you (e.g., Singapore, Oregon)
   
   - **Branch**: `main`
   
   - **Root Directory**: Leave empty (unless repo is in subfolder)
   
   - **Runtime**: `Python 3`
   
   - **Build Command**: 
     ```
     pip install -r requirements.txt
     ```
   
   - **Start Command**:
     ```
     gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
     ```
   
   - **Instance Type**: 
     - **Free** (for testing, may be slower)
     - **Starter** ($7/month, recommended for hackathon)
   
   - **Environment Variables** (Advanced section):
     - Usually not needed, but you can add:
     - Key: `PYTHON_VERSION`, Value: `3.11.0`

5. **Create Web Service**
   - Click "Create Web Service" at the bottom
   - Wait for deployment (5-10 minutes first time)

6. **Monitor Deployment**
   - Watch the logs in the Render dashboard
   - Look for "Initializing AI Voice Detection API..."
   - Look for "Starting server..."
   - Deployment is complete when you see "Booting worker"

### Step 3: Test Your Deployed API

1. **Get Your API URL**
   - Your API URL will be: `https://YOUR-APP-NAME.onrender.com`
   - Find it at the top of your Render dashboard

2. **Test Health Endpoint**
   ```bash
   curl https://YOUR-APP-NAME.onrender.com/health
   ```
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "message": "AI Voice Detection API is running"
   }
   ```

3. **Test Detection Endpoint**
   Use the test script:
   ```bash
   python test_comprehensive.py
   # When prompted, enter: https://YOUR-APP-NAME.onrender.com
   ```

### Step 4: Submit to Hackathon

Submit these details:

1. **API Endpoint URL**: `https://YOUR-APP-NAME.onrender.com/detect`
2. **API Key**: `hackathon_api_key_2025`
3. **Method**: POST
4. **Authentication**: Include in header as `Authorization: hackathon_api_key_2025`

---

## Alternative: Deploy on Other Platforms

### Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Push: `git push heroku main`
5. Scale: `heroku ps:scale web=1`

### Railway

1. Go to https://railway.app
2. "New Project" → "Deploy from GitHub repo"
3. Select repository
4. Railway auto-detects Python and deploys
5. Get URL from Railway dashboard

### PythonAnywhere

1. Sign up at https://www.pythonanywhere.com
2. Upload files via Files tab
3. Create new web app
4. Configure WSGI file
5. Reload web app

---

## Troubleshooting Deployment Issues

### Issue: Build Failed

**Check:**
- Are all files committed to GitHub?
- Is `requirements.txt` correct?
- Check build logs for specific error

**Fix:**
```bash
# Update requirements if needed
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Issue: Application Error / Not Starting

**Check:**
- Render logs for error messages
- Is `Procfile` correct?
- Is port binding correct in app.py?

**Fix in app.py:**
```python
# Ensure this line exists at the end
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### Issue: 502 Bad Gateway

**Cause:** App crashed or didn't start

**Check:**
- Render logs
- Memory usage (Free tier has 512MB limit)
- Startup time (must start in 5 minutes)

**Fix:**
- Reduce workers in Procfile: `--workers 1`
- Increase timeout: `--timeout 180`

### Issue: API Returns 401 Unauthorized

**Check:**
- API key in request header
- Header name: `Authorization` or `X-API-Key`
- API key value: `hackathon_api_key_2025`

**Test:**
```bash
curl -X POST https://YOUR-APP.onrender.com/detect \
  -H "Authorization: hackathon_api_key_2025" \
  -H "Content-Type: application/json" \
  -d '{"audio": "test"}'
```

### Issue: API Returns 400 Bad Request

**Check:**
- Request body is valid JSON
- "audio" field is present
- Audio is properly base64 encoded

### Issue: Slow Response / Timeout

**Cause:** Free tier limitations

**Solutions:**
1. Upgrade to Starter plan ($7/month)
2. Reduce audio processing complexity
3. Increase timeout in Procfile
4. Keep app warm with uptime monitor

---

## Keeping Your Free Render App Alive

Render free tier apps sleep after 15 minutes of inactivity.

**Solutions:**

1. **UptimeRobot** (Recommended)
   - Sign up at https://uptimerobot.com
   - Add new monitor
   - Type: HTTP(s)
   - URL: `https://YOUR-APP.onrender.com/health`
   - Interval: 5 minutes
   - This pings your app to keep it awake

2. **Cron Job**
   - Set up a cron job on your computer
   - Pings your API every 10 minutes

3. **Upgrade to Paid Plan**
   - Starter plan: $7/month
   - Apps never sleep
   - Better performance

---

## Performance Optimization

### For Free Tier
```python
# In Procfile
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 180 --preload
```

### For Paid Tier
```python
# In Procfile
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --worker-class gthread --threads 2
```

---

## Security Considerations

### Change API Key
In `app.py`, change:
```python
API_KEY = "your_secure_api_key_here"
```

### Use Environment Variables (Production)
```python
import os
API_KEY = os.environ.get('API_KEY', 'default_key')
```

Then in Render:
- Go to Environment
- Add: `API_KEY` = `your_secure_key`

---

## Monitoring Your API

### Render Dashboard
- View logs in real-time
- Monitor CPU and memory usage
- Check request counts
- View error rates

### Health Check Monitoring
Set up automated health checks:
```bash
# Check every 5 minutes
*/5 * * * * curl https://YOUR-APP.onrender.com/health
```

---

## Final Checklist Before Submission

- [ ] API is deployed and accessible
- [ ] Health endpoint returns 200
- [ ] Detection endpoint works with test audio
- [ ] Authentication is working
- [ ] Response format matches requirements
- [ ] API URL is noted down
- [ ] API key is noted down
- [ ] API has been tested multiple times
- [ ] Logs show no errors
- [ ] App is not sleeping (pinged recently)

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Flask Docs**: https://flask.palletsprojects.com
- **Gunicorn Docs**: https://docs.gunicorn.org

---

## Emergency Backup Plan

If Render deployment fails:

1. **Use Replit**
   - Fork repl from GitHub
   - Click "Run"
   - Get URL instantly

2. **Use ngrok (Local)**
   - Run API locally
   - Use ngrok to expose: `ngrok http 5000`
   - Use ngrok URL for submission

3. **Use Vercel**
   - Deploy as serverless function
   - Quick deployment from GitHub

---

**Remember**: Test everything before submission! Good luck! 🍀
