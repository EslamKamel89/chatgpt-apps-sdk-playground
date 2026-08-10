from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastmcp.utilities.lifespan import combine_lifespans

from src.auth import AuthenticationMiddleware
from src.core import settings
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


@app.get("/.well-known/oauth-protected-resource")
async def oauth_protected_resource():
    metadata = {
        "authorization_servers": [settings.scalekit_authorization_server],
        "bearer_methods_supported": ["header"],
        "resource": settings.mcp_resource_url,
        "resource_documentation": f"{settings.mcp_resource_url}docs",
        "scopes_supported": [],
    }
    return JSONResponse(metadata)


app.add_middleware(AuthenticationMiddleware)
app.mount("/mcp", mcp_app)
