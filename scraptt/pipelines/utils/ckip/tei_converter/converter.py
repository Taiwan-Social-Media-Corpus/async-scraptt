import asyncio
from datetime import datetime
from typing import Dict, Union
from dataclasses import dataclass
from .tags import create_tei_tags
from ..segmenter import segment_text
from .mandarin_extractor import extract_mandarin

# --------------------------------------------------------------------
# helper functions


def create_datetime(post_time: Union[int, str]) -> datetime:
    if isinstance(post_time, str):
        post_time = int(post_time)

    date_time = datetime.fromtimestamp(post_time)
    return (str(date_time.year), str(date_time.month), str(date_time.day))


def create_tei_template(
    author: str,
    id: str,
    year: str,
    board: str,
    title: str,
    segmented_title: str,
    body: str,
    comments: str,
) -> str:
    return f"""<TEI.2>
    <teiHeader>
        <metadata name="media">ptt</metadata>
        <metadata name="board">{board}-ptt</metadata>
        <metadata name="post_id">{id}</metadata>
        <metadata name="author">{author}</metadata>
        <metadata name="year">{year}</metadata>
        <metadata name="title">{title}</metadata>
    </teiHeader>
    <text>
        <title author="{author}">
        <s>
        {segmented_title}
        </s>
        </title>
        <body author="{author}">
                {body}
        </body>
        {comments}
    </text>
</TEI.2>"""


# --------------------------------------------------------------------
# public interface


@dataclass
class TeiConverter:
    """
    The TeiConverter object converts the post data to tei tags.
    """

    post_data: Dict[str, Union[str, int]]

    async def create_multiple_tei_tags(self):
        filtered_body = extract_mandarin(self.post_data["body"])

        return await asyncio.gather(
            create_tei_tags(await segment_text(self.post_data["title"]), "title"),
            create_tei_tags(await segment_text(filtered_body), "body"),
            create_tei_tags(await segment_text(self.post_data["comments"]), "comments"),
        )

    def convert(self):
        post_id = self.post_data["post_id"]
        post_author = self.post_data["author"]
        post_board = self.post_data["board"]
        post_title = self.post_data['title']
        year, month, day = create_datetime(self.post_data["date"])
        segmented_title, body, comments = asyncio.run(self.create_multiple_tei_tags())

        return create_tei_template(
            author=post_author,
            id=post_id,
            year=year,
            board=post_board,
            title=post_title, 
            segmented_title=segmented_title,
            body=body,
            comments=comments,
        )
