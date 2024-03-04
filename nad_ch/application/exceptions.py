class InvalidEmailDomainError(Exception):
    """Exception raised when the email domain is not permitted."""

    pass


class OAuth2TokenError(Exception):
    """Exception raised when an OAuth2 token cannot be retrieved."""

    pass
