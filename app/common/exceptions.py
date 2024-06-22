from rest_framework.exceptions import ValidationError


class BaseApiError(ValidationError):
    def __init__(self, detail: str, code: str) -> None:
        content = {"error": detail, "code": code}
        super().__init__(detail=content)
