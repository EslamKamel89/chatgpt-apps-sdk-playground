from fastapi import FastAPI

from src.mcp import mcp_app

app = FastAPI(
    title="MCP Sandbox",
    lifespan=mcp_app.lifespan,
)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.mount("/mcp", mcp_app)
