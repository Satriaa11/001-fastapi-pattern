from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from .entities import User, Todo


class UserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        pass


class TodoRepository(ABC):
    @abstractmethod
    async def create_todo(self, todo: Todo) -> Todo:
        pass

    @abstractmethod
    async def get_todos_by_user_id(self, user_id: UUID) -> List[Todo]:
        pass

    @abstractmethod
    async def get_todo_by_id(self, todo_id: UUID) -> Optional[Todo]:
        pass

    @abstractmethod
    async def update_todo(self, todo: Todo) -> Todo:
        pass

    @abstractmethod
    async def delete_todo(self, todo_id: UUID) -> bool:
        pass
