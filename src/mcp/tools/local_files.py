from src.mcp import mcp


@mcp.tool()
def add_note_to_file(content: str) -> bool:
    """
    Append content to the user notes
    Args:
        content (str): the text content to append
    Returns:
        str: returns True if the operation is successful and False if something went wrong
    """
    filename = "./docs/notes.txt"
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write("\n" + content + "\n")
            return True
    except:
        return False


@mcp.tool()
def read_note_from_file() -> str | None:
    """
    read the content of the user notes
    Returns:
        str | None: returns content of the user notes if the read is successful else returns None
    """
    filename = "./docs/notes.txt"
    try:
        with open(filename, "r") as f:
            return f.read()
    except Exception as e:
        return None
