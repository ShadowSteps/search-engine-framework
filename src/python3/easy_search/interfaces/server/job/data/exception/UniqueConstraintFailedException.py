from .....base.exception.BasicException import BasicException


class UniqueConstraintFailedException(BasicException):
    def __init__(self, message: str, prev: Exception = None, code: int = 0) -> None:
        super().__init__(message, prev, code)