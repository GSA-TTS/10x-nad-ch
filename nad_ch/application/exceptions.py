class NadChError(Exception):
    """Base class for application exceptions with a message."""

    def __init__(self, message=None):
        if message is not None:
            self.message = message
        super().__init__(self.message)


class InvalidEmailDomainError(NadChError):
    """Exception raised when the email domain is not permitted."""

    def __init__(self, message="Invalid email domain."):
        super().__init__(message)


class InvalidEmailError(NadChError):
    """Exception raised when an invalid email is provided."""

    def __init__(self, message="Invalid email address provided."):
        super().__init__(message)


class OAuth2TokenError(NadChError):
    """Exception raised when an OAuth2 token cannot be retrieved."""

    def __init__(self, message="OAuth2 token retrieval failed."):
        super().__init__(message)
