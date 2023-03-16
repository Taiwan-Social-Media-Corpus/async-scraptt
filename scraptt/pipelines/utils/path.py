from datetime import datetime
from pathlib import Path
from typing import (
    Any,
    Dict,
)


def make_file_path(item: Dict[str, Any], data_dir: str) -> str:
    """The make_file_path function makes the file path.

    Args:
        item (dict): the extracted data
        data_dir (str): the data directory
    Returns:
        a str
    """

    board = item["board"]
    date = datetime.fromtimestamp(int(item["date"]))
    formatted_date = date.strftime("%Y%m%d_%H%M")
    year = date.year
    dir_path = f"{data_dir}/{board}/{year}"
    file_path = f"{dir_path}/{formatted_date}_{item['post_id']}"
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    return file_path
