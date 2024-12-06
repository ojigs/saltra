class UserAlreadyExistsException(Exception):
    """Raise this exception when attempting to create a user with an existing email."""
    def __init__(self, message: str = "User with that email already exists"):
        super().__init__(message)