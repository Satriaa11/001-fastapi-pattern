# 🔐 Swagger Authentication Guide

## How to Test Authentication in Swagger UI

### Step 1: Start the Server

```bash
uv run python run.py
```

### Step 2: Open Swagger UI

Navigate to: http://localhost:8000/docs

### Step 3: Register a New User

1. Find the **POST /auth/register** endpoint
2. Click "Try it out"
3. Enter user data:

```json
{
  "email": "test@example.com",
  "username": "testuser",
  "password": "testpass123"
}
```

4. Click "Execute"

### Step 4: Login to Get Token

1. Find the **POST /auth/token** endpoint
2. Click "Try it out"
3. Enter credentials:
   - **username**: test@example.com (your email)
   - **password**: testpass123
4. Click "Execute"
5. **Copy the `access_token`** from the response

### Step 5: Authorize in Swagger

1. Look for the **🔒 Authorize** button at the top of the page
2. Click the "Authorize" button
3. In the popup, enter: `Bearer YOUR_ACCESS_TOKEN`
   - Replace `YOUR_ACCESS_TOKEN` with the token you copied
   - Make sure to include the word "Bearer" followed by a space
4. Click "Authorize"
5. Click "Close"

### Step 6: Test Protected Endpoints

Now you can test any protected endpoint:

- **GET /auth/me** - Get your user info
- **POST /todos/** - Create a new todo
- **GET /todos/** - Get all your todos

### 🎯 Example Token Format

```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### ❗ Troubleshooting

**Problem: "Not authenticated" error**

- Solution: Make sure you clicked the "Authorize" button and entered the token correctly

**Problem: "Token has expired"**

- Solution: Login again to get a new token (tokens expire after 30 minutes)

**Problem: "Invalid token format"**

- Solution: Make sure you included "Bearer " (with space) before your token

### 🔧 Testing with curl (Alternative)

```bash
# 1. Register
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "username": "testuser", "password": "testpass123"}'

# 2. Login (save the token)
curl -X POST "http://localhost:8000/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=test@example.com&password=testpass123"

# 3. Use token for protected endpoints
curl -X GET "http://localhost:8000/auth/me" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
```
