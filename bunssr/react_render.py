import os
import json
from typing import Any, Dict, Optional
from .client import UnixSocketHttpClient  # Assuming client.py holds the class


class SSRRenderError(Exception):
    """Custom exception for SSR rendering errors."""


class ReactSSRRenderer:
    def __init__(self, socket_path: Optional[str] = None):
        """
        Initialize the renderer with the path to the Bun SSR server socket.
        Args:
            socket_path (str): Path to the Unix socket for the Bun SSR server.
                Defaults to the environment variable BUN_RENDER_SOCKET or a default path.
        Raises:
            ValueError: If the socket path is not provided and the environment variable is not set.
        """
        self.socket_path = socket_path or os.getenv(
            "BUN_RENDER_SOCKET", "/tmp/bun_render_socket"
        )
        self.client = UnixSocketHttpClient(self.socket_path)

    def render_component(
        self,
        component_path: str,
        props: Optional[Dict[str, Any]] = None,
        static: bool = False,
    ) -> str:
        """
        Render a React component by sending its path and props to the Bun SSR server.

        Args:
            component_path (str): Absolute or relative path to the .tsx/.jsx component.
            props (dict): Props to pass into the component.

        Returns:
            str: The rendered HTML.

        Raises:
            SSRRenderError: If there's a problem with the rendering or server response.
        """
        payload = {
            "componentPath": component_path,
            "props": props or {},
            "static": static,
        }

        status_code, response_body = self.client.request(
            url="/",
            method="POST",
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        if status_code != 200:
            raise SSRRenderError(
                f"Non-200 response from Bun SSR: {status_code} — {response_body}"
            )

        try:
            response = json.loads(response_body)
        except json.JSONDecodeError:
            raise SSRRenderError(f"Invalid JSON returned: {response_body}")

        if "error" in response:
            raise SSRRenderError(f"SSR error: {response['error']}")

        return response.get("html", "")
