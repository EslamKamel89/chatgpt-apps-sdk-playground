from typing import Callable

from fastapi import Request, Response
from scalekit import ScalekitClient
from scalekit.common.scalekit import TokenValidationOptions
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.core import settings

PROTECTED_PATHS = ["/mcp"]

scalekit_client = ScalekitClient(
    env_url=settings.scalekit_environment_url,
    client_id=settings.scalekit_client_id,
    client_secret=settings.scalekit_client_secret,
)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        for path in PROTECTED_PATHS:
            if request.url.path.startswith(path):
                return await self.handle_authentication(request, call_next)

        return await call_next(request)

    async def handle_authentication(
        self, request: Request, call_next: Callable
    ) -> Response:
        # print("=" * 80)
        # print("MCP AUTH REQUEST")
        # print("METHOD:", request.method)
        # print("PATH:", request.url.path)
        # print("AUTHORIZATION:", request.headers.get("Authorization"))
        # print("USER-AGENT:", request.headers.get("User-Agent"))
        # print("=" * 80)
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            # print("AUTH RESULT: Missing Bearer token")
            return Response(
                content='{"error":"Missing Bearer token"}',
                status_code=401,
                headers={
                    "WWW-Authenticate": (
                        f'Bearer realm="OAuth", '
                        f'resource_metadata="{settings.mcp_resource_metadata_url}"'
                    ),
                    "Cache-Control": "no-store",
                },
                media_type="application/json",
            )
        token = auth_header.split("Bearer ", 1)[1].strip()
        if not token:
            return Response(
                content='{"error":"Missing Bearer token"}',
                status_code=401,
                headers={
                    "WWW-Authenticate": (
                        f'Bearer realm="OAuth", '
                        f'resource_metadata="{settings.mcp_resource_metadata_url}"'
                    )
                },
                media_type="application/json",
            )
        options = TokenValidationOptions(
            issuer=settings.scalekit_environment_url,
            audience=[settings.mcp_resource_url],
        )
        try:
            is_valid = scalekit_client.validate_access_token(
                token,
                options=options,
            )
            if not is_valid:
                raise ValueError("Invalid token")
        except Exception as e:
            print(f"Token validation failed: {type(e).__name__}: {e}")
            return Response(
                content='{"error":"Token validation failed"}',
                status_code=401,
                headers={
                    "WWW-Authenticate": (
                        f'Bearer realm="OAuth", '
                        f'resource_metadata="{settings.mcp_resource_metadata_url}"'
                    )
                },
                media_type="application/json",
            )

        return await call_next(request)
