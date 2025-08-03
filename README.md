# 🌀 bunssr

A reusable Python package for React Server-Side Rendering (SSR) powered by a Bun-based SSR server communicating over a Unix socket.

## 🚀 Features

- ✅ Native communication over Unix domain socket (no HTTP server needed)
- ✅ Lightweight: Python talks directly to Bun
- ✅ Custom component path and props support
- ✅ Clean Python API: `ReactSSRRenderer`

---

## ⚙️ Installation

Make sure [**Bun**](https://bun.sh/) is installed and available in your system path.

Then install the package:

```bash
pip install bunssr
```

> On first use, JS dependencies will be installed automatically.

---

## 🧠 Usage Example

```python
from bunssr import start_bun_server, ReactSSRRenderer

# 1. Start Bun server (you can also use a context manager if you prefer)
proc = start_bun_server()

# 2. Create the renderer
renderer = ReactSSRRenderer()

# 3. Render a React component
html = renderer.render_component(
    component_path="/absolute/path/to/MyComponent.tsx",
    props={"title": "Hello from Python!"}
)

print(html)

# 4. Clean up when done
proc.terminate()
```

---

## 📦 Python API

### `start_bun_server() -> subprocess.Popen`

Starts the bundled Bun SSR server and returns the `subprocess` handle.

### `ReactSSRRenderer(socket_path: Optional[str] = None)`

- Uses `BUN_RENDER_SOCKET` env var or defaults to `/tmp/bun_render_socket`.
- Handles request/response cycle for SSR.

### `render_component(component_path: str, props: dict) -> str`

Renders the provided React component using the Bun server and returns the resulting HTML string.

Raises `SSRRenderError` on:

- Bun socket errors
- Component import/render failures
- Invalid JSON or malformed responses

---

## 📁 Project Layout

```
bunssr/
├── __init__.py
├── server/                  # Bun server implementation
│   ├── index.ts             # SSR entry server
│   └── package.json         # Dependencies (e.g., react, react-dom, vite)
└── render.py                # Python client code
```

---

## TODO

- Add support for other frameworks (e.g. Vue via `pip install bunssr[vue]`)
- Add logging, async rendering, or socket health checks
