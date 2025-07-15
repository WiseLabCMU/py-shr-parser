class ShrFileParserException(Exception):
    """Base exception class for ShrFileParser errors"""
    pass


class FileNotOpenError(ShrFileParserException):
    """File not open error"""

    def __init__(self):
        super().__init__("File not open")
