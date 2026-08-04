from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastmcp.utilities.lifespan import combine_lifespans

from src.mcp import mcp_app


@asynccontextmanager
async def fastapi_lifespan(app: FastAPI):
    print("Starting the fastapi application")
    yield
    print("Shutting down the fastapi application")


app = FastAPI(
    title="MCP Sandbox",
    lifespan=combine_lifespans(fastapi_lifespan, mcp_app.lifespan),
)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.mount("/mcp", mcp_app)
