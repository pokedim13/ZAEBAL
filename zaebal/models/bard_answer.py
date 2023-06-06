"""
    Provides Bard answer of question model.
"""
from typing import Any, List, Dict
from dataclasses import dataclass


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
    choices: List[Dict[str, Any]]
    images: set
