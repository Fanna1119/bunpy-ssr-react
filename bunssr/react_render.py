import os
import asyncio
import atexit
from typing import Optional, Dict, Any

import httpx
from runtime import start_bun_server


class SSRRenderError(Exception):
    pass


class AsyncReactSSRRendererSingleton:
    _instance = None
    _serve = None
    _client = None
    _socket_path = None

    def __new__(cls, socket_path: Optional[str] = None, start_server: bool = False):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._socket_path = socket_path or os.getenv(
                "BUN_RENDER_SOCKET", "/tmp/bun_render_socket"
            )

            if start_server:
                cls._serve = start_bun_server(cls._socket_path)

            cls._client = httpx.AsyncClient(
                transport=httpx.AsyncHTTPTransport(uds=cls._socket_path),
                base_url="http://bunssr",
                timeout=10.0,
            )

            # Register cleanup on normal exit
            atexit.register(cls._cleanup)

        return cls._instance

    @classmethod
    def _cleanup(cls):
        if cls._serve:
            cls._serve.terminate()
            cls._serve.wait()
            print("Bun SSR server terminated.")

        if cls._client:
            # Properly close async client; run in event loop if available
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(cls._client.aclose())
                else:
                    loop.run_until_complete(cls._client.aclose())
            except RuntimeError:
                # no event loop, ignore or handle appropriately
                pass

    async def render_component(
        self,
        component_path: str,
        props: Optional[Dict[str, Any]] = None,
        static: bool = False,
    ) -> str:
        payload = {
            "componentPath": component_path,
            "props": props or {},
            "static": static,
        }

        response = await self._client.post("/", json=payload)
        if response.status_code != 200:
            raise SSRRenderError(
                f"Non-200 response from Bun SSR: {response.status_code} — {response.text}"
            )

        data = response.json()
        if "error" in data:
            raise SSRRenderError(f"SSR error: {data['error']}")

        return data.get("html", "")
