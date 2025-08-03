import subprocess
from setuptools.command.install import install as _install
from setuptools import setup


class InstallBunDependencies(_install):
    def run(self):
        _install.run(self)  # Run the standard install

        # Now run bun install
        try:
            print("Running bun install for JS dependencies...")
            subprocess.check_call(["bun", "install"], cwd="bunssr/server")
        except Exception as e:
            print(f"Warning: bun install failed: {e}")


setup(
    cmdclass={
        "install": InstallBunDependencies,
    }
)
