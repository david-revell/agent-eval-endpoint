# ngrok Setup Guide for test_callbacks.py

This guide will help you install ngrok and expose your local `test_callbacks.py` API publicly so it can receive webhooks from external services.

## Prerequisites

- Python environment with required dependencies (FastAPI, uvicorn, etc.)
- Internet connection
- A free ngrok account (recommended for persistent URLs)

---

## Step 1: Install ngrok

### Option A: Download ngrok (Recommended for Windows)

1. **Visit the ngrok website:**
   - Go to https://ngrok.com/download
   - Or directly: https://ngrok.com/download/windows

2. **Download ngrok:**
   - Download the Windows ZIP file
   - Extract it to a folder (e.g., `C:\ngrok` or `C:\Users\YourUsername\ngrok`)

3. **Add ngrok to PATH (Optional but recommended):**
   - Open System Properties → Environment Variables
   - Add the ngrok folder path to your `Path` environment variable
   - Or use ngrok with full path: `C:\ngrok\ngrok.exe`

### Option B: Install via Package Manager

**Using Chocolatey (if installed):**
```powershell
choco install ngrok
```

**Using Scoop (if installed):**
```powershell
scoop install ngrok
```

### Option C: Install via npm (if Node.js is installed)
```powershell
npm install -g ngrok
```

---

## Step 2: Create a Free ngrok Account (Recommended)

1. **Sign up for a free account:**
   - Visit https://dashboard.ngrok.com/signup
   - Create an account (free tier is sufficient)

2. **Get your authtoken:**
   - After signing up, go to https://dashboard.ngrok.com/get-started/your-authtoken
   - Copy your authtoken

3. **Configure ngrok with your authtoken:**
   ```powershell
   ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
   ```
   
   Replace `YOUR_AUTHTOKEN_HERE` with the token you copied.

**Why use an account?**
- Free accounts get persistent URLs (same URL each time)
- Better for production/testing
- Access to ngrok dashboard to inspect requests

---

## Step 3: Start Your Local API

1. **Open a terminal/PowerShell window**

2. **Navigate to your project directory:**
   ```powershell
   cd C:\Users\volti\OneDrive\Documents\Python_projects\palete-agent
   ```

3. **Start the callback API:**
   ```powershell
   python test_scripts/test_callbacks.py
   ```

4. **Verify it's running:**
   - You should see output indicating the server is running on port 8008
   - The API will be available at `http://127.0.0.1:8008`
   - Keep this terminal window open

---

## Step 4: Expose Your API with ngrok

1. **Open a NEW terminal/PowerShell window** (keep the API running in the first window)

2. **Start ngrok tunnel:**
   ```powershell
   ngrok http 8008
   ```
   
   If ngrok is not in your PATH, use the full path:
   ```powershell
   C:\ngrok\ngrok.exe http 8008
   ```

3. **ngrok will display:**
   ```
   Forwarding   https://xxxx-xx-xx-xx-xx.ngrok-free.app -> http://localhost:8008
   ```
   
   You'll see a public HTTPS URL (something like `https://abc123.ngrok-free.app`)

4. **Copy the public URL:**
   - The `Forwarding` URL is your public endpoint
   - Example: `https://abc123.ngrok-free.app`

---

## Step 5: Configure Your Webhook URL

Use the ngrok URL as your webhook endpoint:

**Full webhook URL format:**
```
https://YOUR-NGROK-URL.ngrok-free.app/api/v1/callback
```

**Example:**
```
https://abc123.ngrok-free.app/api/v1/callback
```

**Important Notes:**
- The URL uses `https://` (ngrok provides SSL automatically)
- Append `/api/v1/callback` to match your endpoint
- If you have `APP_KEY` configured, include it in the `X-API-Key` header

---

## Step 6: Test Your Setup

### Test 1: Health Check
Open in browser or use curl:
```powershell
curl https://YOUR-NGROK-URL.ngrok-free.app/
```

### Test 2: Send a Test Callback
```powershell
curl -X POST https://YOUR-NGROK-URL.ngrok-free.app/api/v1/callback `
  -H "Content-Type: application/json" `
  -d '{\"test\": \"data\", \"message\": \"Hello from webhook!\"}'
```

If you have `APP_KEY` configured:
```powershell
curl -X POST https://YOUR-NGROK-URL.ngrok-free.app/api/v1/callback `
  -H "Content-Type: application/json" `
  -H "X-API-Key: YOUR_APP_KEY" `
  -d '{\"test\": \"data\", \"message\": \"Hello from webhook!\"}'
```

You should see the callback logged in your API terminal window.

---

## Step 7: View ngrok Dashboard (Optional)

1. **Open ngrok web interface:**
   - While ngrok is running, visit: http://localhost:4040
   - This shows all incoming requests, headers, and responses

2. **Or use ngrok dashboard:**
   - Visit https://dashboard.ngrok.com/
   - View your active tunnels and request history

---

## Troubleshooting

### Issue: "ngrok: command not found"
**Solution:** 
- Use full path: `C:\ngrok\ngrok.exe http 8008`
- Or add ngrok to your PATH environment variable

### Issue: "ERR_NGROK_108" or "authtoken required"
**Solution:**
- Sign up for a free ngrok account
- Run: `ngrok config add-authtoken YOUR_AUTHTOKEN`

### Issue: "Port 8008 is already in use"
**Solution:**
- Check if another process is using port 8008
- Change the port in your `.env` file: `CALLBACK_PORT=8009`
- Update ngrok command: `ngrok http 8009`

### Issue: "ngrok session expired"
**Solution:**
- Free tier has session limits
- Restart ngrok: Stop (Ctrl+C) and run `ngrok http 8008` again
- Consider upgrading to a paid plan for longer sessions

### Issue: "Connection refused" from webhook service
**Solution:**
- Ensure your local API is running
- Verify ngrok is forwarding to the correct port (8008)
- Check firewall settings

### Issue: "ngrok-free.app" shows warning page
**Solution:**
- This is normal for free ngrok accounts
- The webhook service needs to click through the warning
- Consider upgrading to a paid plan to remove the warning

---

## Advanced Configuration

### Use a Custom Domain (Paid Plans)
```powershell
ngrok http 8008 --domain=your-custom-domain.ngrok.io
```

### Set a Static URL (Paid Plans)
```powershell
ngrok http 8008 --domain=static-url.ngrok-free.app
```

### Run ngrok in Background
```powershell
Start-Process ngrok -ArgumentList "http 8008"
```

### Save ngrok Configuration
Create `%USERPROFILE%\.ngrok2\ngrok.yml`:
```yaml
authtoken: YOUR_AUTHTOKEN
tunnels:
  callback:
    addr: 8008
    proto: http
```

Then run:
```powershell
ngrok start callback
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `ngrok http 8008` | Start tunnel to port 8008 |
| `ngrok config add-authtoken TOKEN` | Configure authtoken |
| `ngrok http 8008 --region us` | Use US region |
| `ngrok http 8008 --hostname custom.ngrok.io` | Use custom domain (paid) |

---

## Security Notes

1. **API Key Protection:**
   - Set `APP_KEY` in your `.env` file for production use
   - The callback endpoint will require `X-API-Key` header if `APP_KEY` is set

2. **Temporary URLs:**
   - Free ngrok URLs change each time you restart (unless using authtoken)
   - Update your webhook configuration when the URL changes

3. **HTTPS:**
   - ngrok automatically provides HTTPS
   - Always use the `https://` URL for webhooks

4. **Exposure:**
   - Your local API is now publicly accessible
   - Only expose it when needed for testing
   - Stop ngrok when not in use

---

## Next Steps

1. ✅ Install ngrok
2. ✅ Configure authtoken
3. ✅ Start your API (`python test_scripts/test_callbacks.py`)
4. ✅ Start ngrok tunnel (`ngrok http 8008`)
5. ✅ Use the public URL in your webhook configuration
6. ✅ Test with a sample request
7. ✅ Monitor requests via ngrok dashboard (http://localhost:4040)

---

## Support

- **ngrok Documentation:** https://ngrok.com/docs
- **ngrok Status:** https://status.ngrok.com/
- **ngrok Community:** https://ngrok.com/community

