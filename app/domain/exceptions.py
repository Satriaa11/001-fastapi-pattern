class DomainException(Exception):
    """Base exception for domain layer"""
    pass


class UserAlreadyExistsError(DomainException):
    """Raised when trying to create a user that already exists"""
    pass


class UserNotFoundError(DomainException):
    """Raised when user is not found"""
    pass


class TodoNotFoundError(DomainException):
    """Raised when todo is not found"""
    pass


class InvalidCredentialsError(DomainException):
    """Raised when credentials are invalid"""
    pass


class UnauthorizedError(DomainException):
    """Raised when user is not authorized to perform action"""
    pass
