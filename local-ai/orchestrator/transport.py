"""Loopback-only HTTP transport for the local LM Studio server (standard library only)."""

from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import ProxyHandler, Request, build_opener

from .config import LOOPBACK_HOST


class TransportError(RuntimeError):
    """A local HTTP exchange failed, or the server returned something other than a JSON object."""


# An empty proxy map keeps requests to 127.0.0.1 from being routed through a system proxy.
_OPENER = build_opener(ProxyHandler({}))


class LoopbackHttpTransport:
    """Send JSON requests to LM Studio on 127.0.0.1 and refuse every other host before connecting."""

    def request(self, *, method: str, url: str, payload: dict[str, Any] | None, timeout: int) -> dict[str, Any]:
        parsed = urlparse(url)
        if parsed.scheme != "http" or parsed.hostname != LOOPBACK_HOST:
            raise TransportError(f"only http://{LOOPBACK_HOST} may be contacted; refused {parsed.scheme}://{parsed.hostname}")
        headers = {"Accept": "application/json"}
        data = None
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = Request(url, data=data, method=method, headers=headers)
        try:
            with _OPENER.open(request, timeout=timeout) as response:
                body = response.read().decode("utf-8")
        except HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            raise TransportError(f"HTTP {error.code} from local server: {detail[:500]}") from error
        except (URLError, TimeoutError, OSError) as error:
            raise TransportError(f"local server unreachable: {error}") from error
        try:
            decoded = json.loads(body)
        except json.JSONDecodeError as error:
            raise TransportError("local server returned content that is not JSON") from error
        if not isinstance(decoded, dict):
            raise TransportError("local server returned JSON that is not an object")
        return decoded
