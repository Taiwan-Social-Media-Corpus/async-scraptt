import json
from typing import Callable


def handle_exception(io_func: Callable):
    """The handle_exception function is a decorator that catches the error.

    Args:
        io_func (Callable): an io function.
    Returns:
        the io function if there is no error, log message otherwise.
    """

    def wrapper(file_path: str, content: str):
        try:
            return io_func(file_path, content)
        except Exception as error:
            post_id = file_path.split("_")[-1]
            print(f"error msg: {error}")
            print(f"error html file: {post_id}")

    return wrapper


@handle_exception
async def write_html(file_path: str, content: str):
    with open(f"{file_path}.html", "wb") as file:
        return file.write(content)


@handle_exception
async def write_json(file_path: str, content: str):
    with open(f"{file_path}.json", "w", encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False)


@handle_exception
async def write_tei(file_path: str, content: str):
    with open(f"{file_path}.xml", "w") as file:
        file.write(content)
