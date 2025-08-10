from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from ..domain.entities import User
from ..domain.repositories import UserRepository
from ..domain.exceptions import UserAlreadyExistsError, InvalidCredentialsError


class AuthService:
    def __init__(self, user_repository: UserRepository, secret_key: str, algorithm: str = "HS256"):
        self.user_repository = user_repository
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def register_user(self, email: str, username: str, password: str) -> User:
        # Check if user already exists
        existing_user = await self.user_repository.get_user_by_email(email)
        if existing_user:
            raise UserAlreadyExistsError("User with this email already exists")

        # Hash password and create user
        hashed_password = self.get_password_hash(password)
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password
        )

        return await self.user_repository.create_user(user)

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.user_repository.get_user_by_email(email)
        if not user or not self.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password")
        return user

    async def get_current_user(self, token: str) -> User:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise InvalidCredentialsError("Could not validate credentials")
        except JWTError:
            raise InvalidCredentialsError("Could not validate credentials")

        user = await self.user_repository.get_user_by_id(UUID(user_id))
        if user is None:
            raise InvalidCredentialsError("Could not validate credentials")
        return user
