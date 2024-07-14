"""
Sentiment pydantic class implementation
"""

from pydantic.main import BaseModel
from pydantic.main import List
from typing import Optional


class Subfeddit(BaseModel):
    """
      pydantic class implementation

    Args:
        :param BaseModel: BaseModel
    """
    subfeddit_id: int
    comments_start_time: Optional[str]
    comments_end_time: Optional[str]
    sort_polarity_comments: Optional[bool]

    def get_subfeddit_id(self) -> str:
        """
        Function to get subfeddit_id .

        Args:
            :param
        Returns:
            subfeddit_id
        """
        subfeddit_id = self.subfeddit_id
        return str(subfeddit_id)