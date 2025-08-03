from .client import UnixSocketHttpClient
from .runtime import start_bun_server, is_bun_installed
from .react_render import ReactSSRRenderer, SSRRenderError

# import os
# import subprocess


# def ensure_bun_packages_installed():
#     if not is_bun_installed():
#         raise RuntimeError("Bun is not installed or not found in PATH")

#     server_dir = os.path.join(os.path.dirname(__file__), "server")
#     node_modules = os.path.join(server_dir, "node_modules")
#     if not os.path.exists(node_modules):
#         print("Installing JS dependencies with Bun...")
#         subprocess.check_call(["bun", "install"], cwd=server_dir)


# # Optional: run during import
# ensure_bun_packages_installed()
