# Manual OASIS Test Instructions

## Server Status
✅ OASIS server is running on PID 1945837
✅ Process: `/usr/local/bin/python3 -m uvicorn open_webui.main:app --host 0.0.0.0 --port 8080`

## Test Account Creation

### Method 1: Web Interface
1. Open browser to: `http://localhost:8080/auth`
2. Fill form:
   - Name: `dqikst`
   - Email: `dqikst@gmail.com`
   - Password: `Havikz11`
3. Click "Initialize OASIS" or "Join OASIS"

### Method 2: Direct API Call
```bash
curl -X POST http://localhost:8080/api/v1/auths/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "dqikst",
    "email": "dqikst@gmail.com", 
    "password": "Havikz11"
  }'
```

### Method 3: Browser Console
```javascript
fetch('/api/v1/auths/signup', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    name: 'dqikst',
    email: 'dqikst@gmail.com',
    password: 'Havikz11'
  })
}).then(r => r.json()).then(console.log)
```

## Troubleshooting
- If inputs not clickable: Check browser console for CSS errors
- If server not responding: Restart with `docker-compose restart`
- If auth fails: Check server logs

## CSS Fixes Applied
✅ Emergency auth-fix.css loaded
✅ All inputs have `pointer-events: auto !important`
✅ Forms have highest z-index priority