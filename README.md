# FastAPI Hexagonal Todo

Todo list REST API built with FastAPI using Hexagonal Architecture (Clean Architecture).

## Features

- 🚀 User registration and authentication with JWT
- ✅ CRUD operations for todos
- 🏗️ Clean architecture with hexagonal design
- ⚡ FastAPI with Pydantic models
- 🔐 JWT authentication for login/register
- 📦 UV for virtual environment management
- 🗄️ SQLite database with SQLAlchemy
- 🔄 Database migrations with Alembic

## Architecture

This project follows Hexagonal Architecture principles:

```
app/
├── domain/          # Business logic and entities
│   ├── entities.py      # Domain entities (User, Todo)
│   ├── repositories.py  # Repository interfaces
│   └── exceptions.py    # Domain exceptions
├── application/     # Use cases and application services
│   ├── auth_service.py  # Authentication logic
│   └── todo_service.py  # Todo business logic
├── infrastructure/ # External adapters (database, etc.)
│   ├── database.py      # Database configuration
│   ├── models.py        # SQLAlchemy models
│   ├── user_repository.py
│   └── todo_repository.py
└── interfaces/     # API interfaces and controllers
    ├── schemas.py       # Pydantic schemas
    ├── auth_controller.py
    └── todo_controller.py
```

## Quick Setup

### Prerequisites

- Python 3.8+
- UV package manager

#### Install UV (if not already installed):

**Windows:**

```powershell
curl -LsSf https://astral.sh/uv/install.ps1 | powershell
```

**Linux/Mac:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or visit: https://docs.astral.sh/uv/getting-started/installation/

### Automatic Setup

**Windows:**

```batch
# Run the PowerShell setup script
powershell -ExecutionPolicy Bypass -File setup.ps1
```

**Linux/Mac:**

```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup

1. **Create virtual environment with UV:**

```bash
uv venv
```

2. **Install dependencies with UV:**

```bash
uv pip install -e .
```

3. **Create .env file:**

```bash
# Copy example and edit as needed
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

4. **Create database tables:**

```bash
uv run python create_db.py
```

### Running the Application

#### Option 1: Using UV (Recommended)

```bash
# Production mode
uv run python run.py

# Development mode with hot reload
uv run uvicorn app.main:app --reload
```

#### Option 2: Using batch scripts

**Windows:**

```batch
# Setup (first time only)
powershell -ExecutionPolicy Bypass -File setup.ps1

# Start application
start.bat

# Development mode with hot reload
dev.bat
```

**Linux/Mac:**

```bash
# Setup (first time only)
chmod +x setup.sh && ./setup.sh

# Start application
chmod +x start.sh && ./start.sh

# Development mode with hot reload
chmod +x dev.sh && ./dev.sh
```

#### Option 3: Traditional way

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Run application
python run.py
```

## API Documentation

Once running, visit:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 🔐 Authentication in Swagger UI

1. **Register a user** via `/auth/register`
2. **Login** via `/auth/token` to get access token
3. **Click the 🔒 Authorize button** at the top of Swagger UI
4. **Enter:** `Bearer YOUR_ACCESS_TOKEN`
5. **Now you can test protected endpoints!**

> 📖 **Detailed Guide:** See [SWAGGER_AUTH_GUIDE.md](SWAGGER_AUTH_GUIDE.md) for complete instructions

## API Endpoints

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/token` - Login (get JWT token)
- `GET /auth/me` - Get current user info

### Todos

- `POST /todos/` - Create new todo
- `GET /todos/` - Get user's todos
- `GET /todos/{id}` - Get specific todo
- `PUT /todos/{id}` - Update todo
- `DELETE /todos/{id}` - Delete todo

## Example Usage

### 1. Register a new user

```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "username": "johndoe",
       "password": "secret123"
     }'
```

### 2. Login to get JWT token

```bash
curl -X POST "http://localhost:8000/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user@example.com&password=secret123"
```

### 3. Create a todo (use token from step 2)

```bash
curl -X POST "http://localhost:8000/todos/" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Learn FastAPI",
       "description": "Study hexagonal architecture with FastAPI"
     }'
```

## Testing

Run tests:

```bash
pytest
```

## Project Structure Explanation

### Domain Layer

- **Entities**: Core business objects (User, Todo)
- **Repository Interfaces**: Abstract definitions for data access
- **Exceptions**: Domain-specific exceptions

### Application Layer

- **Services**: Business logic and use cases
- **Auth Service**: Handles authentication, password hashing, JWT
- **Todo Service**: Manages todo operations

### Infrastructure Layer

- **Database**: SQLAlchemy configuration
- **Repository Implementations**: Concrete data access implementations
- **Models**: SQLAlchemy ORM models

### Interface Layer

- **Controllers**: FastAPI route handlers
- **Schemas**: Pydantic models for request/response
- **Dependencies**: FastAPI dependency injection

## Environment Variables

Create a `.env` file with:

```env
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./todolist.db
DEBUG=True
```

## Development

### Database Migrations

Initialize Alembic (first time):

```bash
alembic init alembic
```

Create migration:

```bash
alembic revision --autogenerate -m "Create tables"
```

Apply migration:

```bash
alembic upgrade head
```

### Adding New Features

1. **Add Domain Entity** (if needed): Create in `domain/entities.py`
2. **Add Repository Interface**: Define in `domain/repositories.py`
3. **Implement Repository**: Create in `infrastructure/`
4. **Add Service Logic**: Create in `application/`
5. **Add API Endpoints**: Create controller in `interfaces/`
6. **Add Tests**: Create test files in `tests/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
