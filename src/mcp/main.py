from fastmcp import FastMCP

mcp = FastMCP("MCP Sandbox")


mcp_app = mcp.http_app(path="/")
