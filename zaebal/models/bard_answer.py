"""
    Provides Bard answer of question model.
"""
from typing import Any, List
from dataclasses import dataclass


@dataclass
class BardAnswerChoice:
    """
    Provides choices from BardAnswer.
    :param int id: ID of choice
    :param str content: Content of choice
    """
    id: int
    content: str


@dataclass
class BardAnswer:
    """
    Provides Bard answer data.
    """
    # NOTE: Types can be wrong, because this model is not tested yet.
    content: str
    conversation_id: str
    response_id: str
    factualityQueries: list
    textQuery: str
    choices: List[BardAnswerChoice]
    images: set
