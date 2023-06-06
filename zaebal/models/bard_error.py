"""
    Provides dataclass for Bard error response.
"""
from dataclasses import dataclass

@dataclass
class BardError:
    """
    Provides Bard error data.
    :param str content: Content of Bard response.
    :param int status_code: Status code of Bard response.
    """
    content: str
    status_code: int
