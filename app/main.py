from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .interfaces.auth_controller import router as auth_router
from .interfaces.todo_controller import router as todo_router

app = FastAPI(
    title="Todo List API",
    description="""
    A Todo List REST API built with FastAPI using Hexagonal Architecture.

    ## Authentication

    1. **Register a new user** using `/auth/register`
    2. **Get access token** using `/auth/token`
    3. **Click the 'Authorize' button** and enter your token as: `Bearer YOUR_TOKEN`
    4. Now you can access protected endpoints like `/todos/`

    ## Features

    * **User Registration & Authentication** with JWT
    * **Todo CRUD Operations** with user isolation
    * **Clean Architecture** with hexagonal design
    """,
    version="1.0.0",
    openapi_tags=[
        {
            "name": "authentication",
            "description": "User registration and authentication operations"
        },
        {
            "name": "todos",
            "description": "Todo management operations (requires authentication)"
        }
    ]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(todo_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Todo List API with Hexagonal Architecture"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
