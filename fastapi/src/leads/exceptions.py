class LeadAlreadyExistsException(Exception):
    """Raise this exception when attempting to create a lead with an existing email."""
    def __init__(self, message: str = "Lead with that email already exists"):
        super().__init__(message)