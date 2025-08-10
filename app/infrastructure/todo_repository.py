from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..domain.entities import Todo
from ..domain.repositories import TodoRepository
from .models import TodoModel


class SQLAlchemyTodoRepository(TodoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_todo(self, todo: Todo) -> Todo:
        db_todo = TodoModel(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            user_id=todo.user_id,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )
        self.session.add(db_todo)
        await self.session.commit()
        await self.session.refresh(db_todo)

        return Todo.model_validate(db_todo)

    async def get_todos_by_user_id(self, user_id: UUID) -> List[Todo]:
        result = await self.session.execute(
            select(TodoModel).where(TodoModel.user_id == user_id)
        )
        db_todos = result.scalars().all()

        return [Todo.model_validate(todo) for todo in db_todos]

    async def get_todo_by_id(self, todo_id: UUID) -> Optional[Todo]:
        result = await self.session.execute(
            select(TodoModel).where(TodoModel.id == todo_id)
        )
        db_todo = result.scalar_one_or_none()

        if db_todo:
            return Todo.model_validate(db_todo)
        return None

    async def update_todo(self, todo: Todo) -> Todo:
        result = await self.session.execute(
            select(TodoModel).where(TodoModel.id == todo.id)
        )
        db_todo = result.scalar_one()

        db_todo.title = todo.title
        db_todo.description = todo.description
        db_todo.completed = todo.completed
        db_todo.updated_at = todo.updated_at

        await self.session.commit()
        await self.session.refresh(db_todo)

        return Todo.model_validate(db_todo)

    async def delete_todo(self, todo_id: UUID) -> bool:
        result = await self.session.execute(
            select(TodoModel).where(TodoModel.id == todo_id)
        )
        db_todo = result.scalar_one_or_none()

        if db_todo:
            await self.session.delete(db_todo)
            await self.session.commit()
            return True
        return False
