class DatabaseConnectionException(Exception):
    """Raise this exception if there is a database connection issue."""
    def __init__(self, message: str = "Failed to connect to the database"):
        super().__init__(message)

class IndexCreationError(Exception):
    """Raise this exception when there is an error creating database indexes"""
    def __init__(self, message: str = "Failed to create database index"):
        self.message = message
        super().__init__(self.message)


class DatabaseCloseError(Exception):
    """Raise this exception when an error occurs while closing the database connection"""
    def __init__(self, message: str = "Failed to close database connection"):
        self.message = message
        super().__init__(self.message)
