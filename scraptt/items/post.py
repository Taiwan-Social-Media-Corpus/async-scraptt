from typing import Dict, List
from pydantic import BaseModel


class PostItem(BaseModel):
    """
    The PostItem object keeps track of an item in inventory.
    """

    board: str
    post_id: str
    date: str
    title: str
    author: str
    body: str
    post_vote: Dict[str, int]
    comments: List[Dict[str, str]]
