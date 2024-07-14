"""
Sentiment response pydantic class implementation
"""

from pydantic.main import BaseModel
from pydantic.main import List
from typing import Optional


class SubfedditResponse(BaseModel):
    """
    Sentiment response  pydantic class implementation

    Args:
        :param BaseModel: BaseModel
    """
    
    id: int
    comments: List
    observations: Optional[str]


PREDICTION_RESPONSES_TYPES = {
    200: {
        "id": "id",
        "label": "label",
        "status": "200"
    },
    400: {"detail": "Expected a valid json message"},
    500: {"detail": "Internal Server Error"},
}
