import linecache
import re
from tokenTKOM import Token


class Error(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class ParserError(Error):
    def __init__(self, message, currentToken) -> None:
        message += f"\nInstead got {currentToken.type} at position {currentToken.position}"
        super().__init__(message)