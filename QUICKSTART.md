# 🚀 Quick Start Guide

## 1. Install UV (if not already installed)

**Windows:**

```powershell
curl -LsSf https://astral.sh/uv/install.ps1 | powershell
```

**Linux/Mac:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 2. Setup Project

**Windows:**

```batch
powershell -ExecutionPolicy Bypass -File setup.ps1
```

**Linux/Mac:**

```bash
chmod +x setup.sh && ./setup.sh
```

## 3. Start Application

**Option A: Using UV (Recommended)**

```bash
uv run python run.py
```

**Option B: Using Scripts**

Windows: `start.bat`
Linux/Mac: `chmod +x start.sh && ./start.sh`

## 4. Access API

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 5. Test API

1. **Register a user:**

```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com",
       "username": "testuser",
       "password": "testpass123"
     }'
```

2. **Login to get token:**

```bash
curl -X POST "http://localhost:8000/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=test@example.com&password=testpass123"
```

3. **Create a todo (replace YOUR_TOKEN):**

```bash
curl -X POST "http://localhost:8000/todos/" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "My First Todo",
       "description": "Testing the API"
     }'
```

## Development Mode

For hot reload during development:

```bash
uv run uvicorn app.main:app --reload
```

Or use: `dev.bat` (Windows) / `dev.sh` (Linux/Mac)

## Troubleshooting

**Error: UV not found**

- Install UV using the commands in step 1

**Error: Virtual environment not found**

- Run the setup script first

**Error: Database not found**

- Run: `uv run python create_db.py`

**Error: Permission denied (Linux/Mac)**

- Make scripts executable: `chmod +x *.sh`
