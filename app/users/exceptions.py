from app.common.exceptions import BaseApiError


class InvalidCredentialsError(BaseApiError):
    def __init__(self) -> None:
        detail = "Username or password is invalid."
        super().__init__(detail=detail, code="invalid_credentials")
