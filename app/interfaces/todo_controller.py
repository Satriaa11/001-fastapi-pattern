from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..infrastructure.database import get_async_session
from ..infrastructure.todo_repository import SQLAlchemyTodoRepository
from ..application.todo_service import TodoService
from ..domain.exceptions import TodoNotFoundError, UnauthorizedError
from .auth_controller import get_current_user
from .schemas import TodoCreate, TodoUpdate, TodoResponse

router = APIRouter(prefix="/todos", tags=["todos"])


async def get_todo_service(session: AsyncSession = Depends(get_async_session)) -> TodoService:
    todo_repository = SQLAlchemyTodoRepository(session)
    return TodoService(todo_repository)


@router.post("/", response_model=TodoResponse, summary="Create a new todo")
async def create_todo(
    todo_data: TodoCreate,
    current_user = Depends(get_current_user),
    todo_service: TodoService = Depends(get_todo_service)
):
    """
    Create a new todo item.

    **Required authentication:**
    - You must be logged in to create todos
    - Each user can only see and manage their own todos

    **Parameters:**
    - **title**: Short description of the todo (required)
    - **description**: Detailed description (optional)
    """
    todo = await todo_service.create_todo(
        title=todo_data.title,
        description=todo_data.description,
        user_id=current_user.id
    )
    return TodoResponse.model_validate(todo)


@router.get("/", response_model=List[TodoResponse], summary="Get all user's todos")
async def get_todos(
    current_user = Depends(get_current_user),
    todo_service: TodoService = Depends(get_todo_service)
):
    """
    Get all todos for the authenticated user.

    **Returns:** List of all todos belonging to the current user
    """
    todos = await todo_service.get_user_todos(current_user.id)
    return [TodoResponse.model_validate(todo) for todo in todos]


@router.get("/{todo_id}", response_model=TodoResponse, summary="Get a specific todo")
async def get_todo(
    todo_id: UUID,
    current_user = Depends(get_current_user),
    todo_service: TodoService = Depends(get_todo_service)
):
    """
    Get a specific todo by ID.

    **Parameters:**
    - **todo_id**: UUID of the todo to retrieve

    **Note:** You can only access your own todos
    """
    try:
        todo = await todo_service.get_todo_by_id(todo_id, current_user.id)
        return TodoResponse.model_validate(todo)
    except TodoNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    except UnauthorizedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this todo"
        )


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: UUID,
    todo_data: TodoUpdate,
    current_user = Depends(get_current_user),
    todo_service: TodoService = Depends(get_todo_service)
):
    try:
        todo = await todo_service.update_todo(
            todo_id=todo_id,
            user_id=current_user.id,
            title=todo_data.title,
            description=todo_data.description,
            completed=todo_data.completed
        )
        return TodoResponse.model_validate(todo)
    except TodoNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    except UnauthorizedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this todo"
        )


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: UUID,
    current_user = Depends(get_current_user),
    todo_service: TodoService = Depends(get_todo_service)
):
    try:
        deleted = await todo_service.delete_todo(todo_id, current_user.id)
        if deleted:
            return {"message": "Todo deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
    except TodoNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    except UnauthorizedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this todo"
        )
