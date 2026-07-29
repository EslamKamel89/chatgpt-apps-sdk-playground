from fastmcp import FastMCP

mcp = FastMCP("MCP Sandbox")


@mcp.tool
def add(a: int, b: int) -> int:
    """
    Add two numbers.
    """
    return a + b


@mcp.tool
def subtract(a: int, b: int) -> int:
    """
    Subtract two numbers.
    """
    return a - b


mcp_app = mcp.http_app(path="/")
