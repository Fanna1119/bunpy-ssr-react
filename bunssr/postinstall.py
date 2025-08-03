import subprocess
import os


def run():
    print("[bunssr] Installing JS dependencies with `bun install`...")
    server_dir = os.path.join(os.path.dirname(__file__), "server")
    try:
        subprocess.check_call(["bun", "install"], cwd=server_dir)
        print("[bunssr] JS dependencies installed successfully.")
    except Exception as e:
        print(f"[bunssr] Failed to run `bun install`: {e}")
