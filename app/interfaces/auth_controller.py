from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import os

from ..infrastructure.database import get_async_session
from ..infrastructure.user_repository import SQLAlchemyUserRepository
from ..application.auth_service import AuthService
from ..domain.exceptions import UserAlreadyExistsError, InvalidCredentialsError
from .schemas import UserCreate, UserResponse, Token

router = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    description="Enter your email and password to get an access token"
)

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


async def get_auth_service(session: AsyncSession = Depends(get_async_session)) -> AuthService:
    user_repository = SQLAlchemyUserRepository(session)
    return AuthService(user_repository, SECRET_KEY, ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        return await auth_service.get_current_user(token)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/register", response_model=UserResponse, summary="Register a new user")
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user account.

    - **email**: Valid email address (will be used for login)
    - **username**: Display name for the user
    - **password**: Strong password for the account
    """
    try:
        user = await auth_service.register_user(
            email=user_data.email,
            username=user_data.username,
            password=user_data.password
        )
        return UserResponse.model_validate(user)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/token", response_model=Token, summary="Login for access token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Login to get an access token.

    **How to use the token:**
    1. Copy the `access_token` from the response
    2. Click the 'Authorize' button at the top of this page
    3. Enter: `Bearer YOUR_ACCESS_TOKEN`
    4. Click 'Authorize'

    **Login credentials:**
    - **username**: Your email address
    - **password**: Your password
    """
    try:
        user = await auth_service.authenticate_user(form_data.username, form_data.password)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserResponse, summary="Get current user info")
async def read_users_me(current_user = Depends(get_current_user)):
    """
    Get information about the currently authenticated user.

    **Requires authentication:**
    - Include your access token in the Authorization header
    - Or use the 'Authorize' button at the top of this page
    """
    return UserResponse.model_validate(current_user)
