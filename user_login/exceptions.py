class UserNotFoundException(Exception):
    """Raised when the user is not found in the database."""
    pass

class PasswordMissMatchException(Exception):
    """Raised when the provided password does not match the stored password."""
    pass
