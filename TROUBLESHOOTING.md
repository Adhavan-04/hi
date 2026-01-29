# 🔧 Troubleshooting Guide

Complete guide to fixing common issues with the AI Voice Detection API.

---

## Table of Contents

1. [Local Development Issues](#local-development-issues)
2. [Deployment Issues](#deployment-issues)
3. [API Runtime Issues](#api-runtime-issues)
4. [Testing Issues](#testing-issues)
5. [Performance Issues](#performance-issues)

---

## Local Development Issues

### Issue: "pip: command not found" or "python: command not found"

**Cause**: Python not installed or not in PATH

**Solution**:
```bash
# Check if Python is installed
python --version
# or
python3 --version

# If not installed, download from:
# https://www.python.org/downloads/
```

---

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Cause**: Dependencies not installed

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# If still fails, install individually:
pip install flask flask-cors librosa numpy scikit-learn soundfile gunicorn pydub
```

---

### Issue: "Address already in use" / "Port 5000 is busy"

**Cause**: Port 5000 already occupied

**Solution 1 - Kill existing process**:
```bash
# Mac/Linux
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

**Solution 2 - Use different port**:
```python
# In app.py, change last line:
port = int(os.environ.get('PORT', 5001))  # Changed to 5001
app.run(host='0.0.0.0', port=port)
```

---

### Issue: Virtual environment activation fails

**Windows PowerShell**:
```powershell
# If you get execution policy error
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

**Mac/Linux**:
```bash
# If bash doesn't work, try
source venv/bin/activate

# Or
. venv/bin/activate

# Or use Python directly
./venv/bin/python app.py
```

---

## Deployment Issues

### Issue: Render build fails with "requirements.txt not found"

**Cause**: File not in repository or wrong directory

**Solution**:
```bash
# Verify file exists
ls -la requirements.txt

# If missing, create it
pip freeze > requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Add requirements.txt"
git push
```

---

### Issue: "Build failed" with dependency errors

**Cause**: Incompatible package versions or missing system dependencies

**Solution 1 - Simplify requirements**:
```txt
# Replace requirements.txt with:
flask==3.0.0
flask-cors==4.0.0
librosa==0.10.1
numpy==1.24.3
scikit-learn==1.3.2
soundfile==0.12.1
gunicorn==21.2.0
pydub==0.25.1
```

**Solution 2 - Add system dependencies**:
Create `apt-packages.txt`:
```txt
libsndfile1
ffmpeg
```

---

### Issue: "Application failed to start"

**Cause**: Startup timeout or crash on start

**Check Render logs for**:
1. Port binding issues
2. Import errors
3. Memory issues

**Solution**:
```python
# In Procfile, increase timeout:
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 180

# In app.py, ensure proper port binding:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

---

### Issue: "502 Bad Gateway" after deployment

**Cause**: App crashed or not listening on correct port

**Solution**:
1. Check Render logs for crash
2. Verify Procfile command
3. Ensure app.py binds to $PORT:
   ```python
   port = int(os.environ.get('PORT', 5000))
   ```

---

### Issue: Render deployment succeeds but API doesn't respond

**Cause**: App started but crashed quickly

**Solution**:
```bash
# Check Render logs (Live logs in dashboard)

# Common fixes:
# 1. Reduce workers
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 180

# 2. Add preload
web: gunicorn app:app --bind 0.0.0.0:$PORT --preload

# 3. Check memory usage
# Free tier has 512MB limit - reduce model complexity if needed
```

---

## API Runtime Issues

### Issue: 401 Unauthorized Error

**Cause**: Missing or incorrect API key

**Solution**:
```python
# Verify header name (try both):
headers = {
    "Authorization": "hackathon_api_key_2025",
    # OR
    "X-API-Key": "hackathon_api_key_2025",
}

# Test with curl:
curl -H "Authorization: hackathon_api_key_2025" \
     https://your-app.onrender.com/health
```

---

### Issue: 400 Bad Request - "Missing 'audio' field"

**Cause**: Request body incorrect

**Solution**:
```python
# Ensure request body has "audio" field:
data = {
    "audio": audio_base64  # Must be base64 string
}

# Not "file", not "audio_data", must be "audio"
```

---

### Issue: 400 Bad Request - "Invalid base64 encoding"

**Cause**: Audio not properly encoded

**Solution**:
```python
import base64

# CORRECT way:
with open("audio.mp3", "rb") as f:
    audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

# WRONG - don't do this:
# audio_base64 = base64.b64encode(audio_bytes)  # Missing .decode()
# audio_base64 = str(audio_bytes)  # This is wrong
```

---

### Issue: 400 Bad Request - "Invalid audio file"

**Cause**: Corrupted or unsupported audio format

**Solution**:
```python
# Try converting audio to WAV first:
from pydub import AudioSegment

audio = AudioSegment.from_mp3("input.mp3")
audio.export("output.wav", format="wav")

# Then encode WAV:
with open("output.wav", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode('utf-8')
```

---

### Issue: 500 Internal Server Error

**Cause**: Server-side processing error

**Check**:
1. Render logs for Python traceback
2. Audio file size (keep under 10MB)
3. Audio duration (keep under 30 seconds for fast response)

**Solution**:
```python
# Add error handling in app.py (already included)
# But you can add more detailed logging:

import logging
logging.basicConfig(level=logging.DEBUG)

# This will show detailed errors in Render logs
```

---

## Testing Issues

### Issue: test_api.py fails with "Connection refused"

**Cause**: API not running

**Solution**:
```bash
# Start API in separate terminal:
python app.py

# Then run test in another terminal:
python test_api.py
```

---

### Issue: test_comprehensive.py times out

**Cause**: Slow API response or network issues

**Solution**:
```python
# In test_comprehensive.py, increase timeout:
response = requests.post(url, headers=headers, json=payload, timeout=60)  # Increased to 60s
```

---

### Issue: Tests pass locally but fail on deployed API

**Cause**: Deployment environment differences

**Check**:
1. API URL is correct
2. API is actually running (check health endpoint)
3. Firewall/network not blocking
4. API key matches

**Solution**:
```bash
# Test health endpoint first:
curl https://your-app.onrender.com/health

# If health works but detect doesn't:
# - Check API key
# - Check request format
# - Check Render logs during request
```

---

## Performance Issues

### Issue: API responds very slowly (>10 seconds)

**Cause**: Free tier limitations or cold start

**Solutions**:

1. **Keep app warm**:
   ```bash
   # Use UptimeRobot to ping every 5 minutes
   # URL: https://uptimerobot.com
   # Monitor: https://your-app.onrender.com/health
   ```

2. **Optimize Procfile**:
   ```
   web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 180 --preload
   ```

3. **Upgrade to paid tier**: $7/month for instant responses

---

### Issue: API times out after 30 seconds

**Cause**: Render free tier has 30s timeout

**Solutions**:

1. **Upgrade to paid tier** (removes timeout)

2. **Optimize audio processing**:
   ```python
   # In app.py, reduce audio to max 10 seconds:
   if len(audio_data) > 10 * sample_rate:
       audio_data = audio_data[:10 * sample_rate]
   ```

3. **Increase Procfile timeout**:
   ```
   web: gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120
   ```

---

### Issue: Memory errors / Out of memory

**Cause**: Free tier has 512MB RAM limit

**Solutions**:

1. **Reduce workers**:
   ```
   web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1
   ```

2. **Upgrade to paid tier** (1GB+ RAM)

3. **Optimize model**:
   ```python
   # In app.py, reduce training samples:
   n_samples = 200  # Instead of 1000
   ```

---

## General Debugging Tips

### Enable Detailed Logging

Add to app.py:
```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add logging throughout your code:
logging.info(f"Received request from {request.remote_addr}")
logging.debug(f"Audio size: {len(audio_bytes)} bytes")
```

---

### Check Render Logs

1. Go to Render dashboard
2. Click on your service
3. Click "Logs" tab
4. View real-time logs
5. Look for Python tracebacks

---

### Test with Minimal Audio

```python
# Create tiny test audio:
import base64
import numpy as np
import soundfile as sf
import io

# 1 second of silence
audio = np.zeros(22050)
buffer = io.BytesIO()
sf.write(buffer, audio, 22050, format='WAV')
buffer.seek(0)
audio_base64 = base64.b64encode(buffer.read()).decode('utf-8')

# Test with this
```

---

### Verify Your Setup

```bash
# Checklist:
1. [ ] app.py exists and is correct
2. [ ] requirements.txt exists
3. [ ] Procfile exists with correct command
4. [ ] runtime.txt exists with Python version
5. [ ] All files pushed to GitHub
6. [ ] Render connected to correct repo
7. [ ] Render build completed successfully
8. [ ] Render logs show "Model initialized"
9. [ ] Health endpoint responds
10. [ ] API key is correct
```

---

## Emergency Fixes

### If nothing works - Nuclear option

1. **Delete and recreate Render service**
2. **Push fresh code to new GitHub repo**
3. **Reconnect everything**

```bash
# Steps:
git init
git add .
git commit -m "Fresh start"
git remote add origin https://github.com/username/new-repo.git
git push -u origin main

# Then create new Render service
```

---

### Alternative: Deploy to Heroku

```bash
heroku login
heroku create your-app-name
git push heroku main
heroku ps:scale web=1
heroku open
```

---

## Getting Help

If still stuck:

1. **Check logs** - 90% of issues show up in logs
2. **Test locally first** - Isolate if it's deployment or code
3. **Simplify** - Remove features until it works
4. **Google the error** - Include "render.com" or "gunicorn"
5. **Check Render docs** - https://render.com/docs

---

## Success Indicators

Your API is working correctly if:

✅ Health endpoint returns 200  
✅ Detection endpoint accepts requests  
✅ Returns proper JSON format  
✅ Authentication works  
✅ Responds in < 30 seconds  
✅ No errors in logs  
✅ Classification makes sense  
✅ Confidence scores are reasonable (0.5-0.99)  

---

## Final Checklist Before Panic

- [ ] Did you push all files to GitHub?
- [ ] Is Render connected to correct repo?
- [ ] Did build succeed on Render?
- [ ] Are logs showing any errors?
- [ ] Is health endpoint working?
- [ ] Did you use correct API key?
- [ ] Is request format exactly correct?
- [ ] Did you test with test_comprehensive.py?
- [ ] Is audio properly base64 encoded?
- [ ] Are you testing the right URL?

If all yes and still broken → Check Render status page → Try different cloud provider

---

**Remember**: Stay calm, read error messages carefully, check logs first! 🔍
