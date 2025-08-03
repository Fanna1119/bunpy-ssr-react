# bunssr

A reusable Python package to perform React Server-Side Rendering (SSR) by communicating with a Bun-based SSR server over a Unix socket.

## Features

- Starts Bun SSR server shipped inside the package.
- Sends component path and props to Bun server.
- Receives server-rendered HTML.
- Uses pycurl for efficient Unix socket HTTP communication. This means no need for a separate HTTP server in Python.

## Usage

```python
from bunssr import UnixSocketHttpClient, start_bun_server

# Start Bun server (make sure Bun is installed)
proc = start_bun_server()

client = UnixSocketHttpClient("/tmp/bun_render_socket")

status, html = client.request(
    "/",
    method="POST",
    headers={"Content-Type": "application/json"},
    data={
        "componentPath": "/path/to/your/ReactComponent.tsx",
        "ssp": False,
        "props": {"message": "Hello from SSR!"},
    }
)

print(html)

# Stop server if needed
proc.terminate()
```
