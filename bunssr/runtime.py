import subprocess
from contextlib import contextmanager
import os
import shutil

BUN_PATH = shutil.which("bun") or "/usr/local/bin/bun"


def is_bun_installed():
    return shutil.which("bun") is not None


def start_bun_server(socket_path="/tmp/bun_render_socket"):
    if not is_bun_installed():
        raise RuntimeError("Bun is not installed or not found in PATH")

    server_dir = os.path.join(os.path.dirname(__file__), "server")
    server_entry = os.path.join(server_dir, "index.ts")

    return subprocess.Popen(
        [BUN_PATH, "run", server_entry],
        cwd=server_dir,
        env={**os.environ, "BUN_RENDER_SOCKET": socket_path},
    )


@contextmanager
def bun_server_context(socket_path="/tmp/bun_render_socket"):
    """
    Context manager to start and stop the Bun SSR server.
    """
    # Remove socket file if it exists before starting
    if os.path.exists(socket_path):
        os.remove(socket_path)

    process = start_bun_server(socket_path)
    try:
        yield process
    finally:
        process.terminate()
        process.wait()
        if os.path.exists(socket_path):
            os.remove(socket_path)
        print("Bun SSR server stopped and socket removed.")
