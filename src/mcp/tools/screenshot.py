import io

import pyautogui

from mcp.server.fastmcp.utilities.types import Image
from src.mcp import mcp


@mcp.tool()
def capture_screenshot() -> Image:
    """
    Use this tool when the user asks you to take a screenshot for his screen
    Returns:
        Image: the screenshot for the user current screen
    """
    buffer = io.BytesIO()
    screenshot = pyautogui.screenshot()
    screenshot.convert("RGB").save(buffer, format="JPEG", quality=60, optimize=True)
    return Image(data=buffer.getvalue(), format="jpeg")
