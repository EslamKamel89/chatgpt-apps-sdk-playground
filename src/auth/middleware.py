from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.core import settings

PROTECTED_PATHS = ["/mcp"]


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        for path in PROTECTED_PATHS:
            if request.url.path.startswith(path):
                return await self.handle_authentication(request, call_next)

        return await call_next(request)

    async def handle_authentication(
        self, request: Request, call_next: Callable
    ) -> Response:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
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
        return await call_next(request)
