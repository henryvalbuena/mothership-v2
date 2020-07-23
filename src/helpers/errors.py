"""Custom errors goes here"""


class Error(Exception):
    """Base error class"""

    pass


class InvalidUserInput(Error):
    """Exception raised for invalid user input"""

    pass
