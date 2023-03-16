# pylint: disable=no-name-in-module
from pydantic import BaseModel


class CommentsValidator(BaseModel):
    """
    The CommentsValidator object keeps track of an item in inventory, including `type`,
    `author`, `content` and `order`.
    """

    type: str
    author: str
    content: str
    order: int
