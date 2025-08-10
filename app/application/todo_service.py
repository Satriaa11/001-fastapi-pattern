from typing import List, Optional
from uuid import UUID

from ..domain.entities import Todo
from ..domain.repositories import TodoRepository
from ..domain.exceptions import TodoNotFoundError, UnauthorizedError


class TodoService:
    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    async def create_todo(self, title: str, description: Optional[str], user_id: UUID) -> Todo:
        todo = Todo(
            title=title,
            description=description,
            user_id=user_id
        )
        return await self.todo_repository.create_todo(todo)

    async def get_user_todos(self, user_id: UUID) -> List[Todo]:
        return await self.todo_repository.get_todos_by_user_id(user_id)

    async def get_todo_by_id(self, todo_id: UUID, user_id: UUID) -> Todo:
        todo = await self.todo_repository.get_todo_by_id(todo_id)
        if not todo:
            raise TodoNotFoundError("Todo not found")

        if todo.user_id != user_id:
            raise UnauthorizedError("Not authorized to access this todo")

        return todo

    async def update_todo(self, todo_id: UUID, user_id: UUID, title: Optional[str] = None,
                         description: Optional[str] = None, completed: Optional[bool] = None) -> Todo:
        todo = await self.get_todo_by_id(todo_id, user_id)

        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        if completed is not None:
            todo.completed = completed

        return await self.todo_repository.update_todo(todo)

    async def delete_todo(self, todo_id: UUID, user_id: UUID) -> bool:
        todo = await self.get_todo_by_id(todo_id, user_id)
        return await self.todo_repository.delete_todo(todo_id)
