import os
import subprocess
from pathlib import Path
from .node_finder_base import NodeFinderBase

class NodeNotFoundError(Exception):
    """Raised when Node.js is not found on the system"""
    pass

class NodeFinderMac(NodeFinderBase):

    def __init__(self):
        self.common_paths = [
            "/usr/local/bin/node",
            "/usr/bin/node",
            "/opt/homebrew/bin/node",
            "/opt/local/bin/node",
            str(Path.home() / ".nvm" / "versions" / "node"),  # NVM installations
            str(Path.home() / ".nodenv" / "versions"),        # nodenv installations
        ]

    def is_node_installed(self) -> bool:
        """
        Check if Node.js is installed on the system.
        Attempts multiple methods to detect Node.js:
        1. Check PATH for node executable
        2. Check common installation locations
        3. Try running node --version
        
        Returns:
            bool: True if Node.js is installed, False otherwise
        """
        try:
            self.get_node_path()
            return True
        except NodeNotFoundError:
            return False

    def get_node_path(self) -> str:
        try:
            which_result = subprocess.run(
                ["which", "node"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if which_result.returncode == 0:
                node_path = which_result.stdout.strip()
                if os.path.isfile(node_path) and os.access(node_path, os.X_OK):
                    return node_path
        except subprocess.SubprocessError:
            pass

        for path in self.common_paths:
            if "versions" in path:
                if os.path.isdir(path):
                    # Look for the latest version in version manager directories
                    try:
                        versions = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
                        if versions:
                            latest = sorted(versions)[-1]
                            node_path = os.path.join(path, latest, "bin", "node")
                            if os.path.isfile(node_path) and os.access(node_path, os.X_OK):
                                return node_path
                    except (OSError, IndexError):
                        continue
            else:
                # Direct path check
                if os.path.isfile(path) and os.access(path, os.X_OK):
                    return path

        try:
            brew_result = subprocess.run(
                ["brew", "--prefix", "node"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if brew_result.returncode == 0:
                node_path = os.path.join(brew_result.stdout.strip(), "bin", "node")
                if os.path.isfile(node_path) and os.access(node_path, os.X_OK):
                    return node_path
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

        raise NodeNotFoundError("Node.js not found on the system")

    def get_node_version(self) -> str:
        try:
            result = subprocess.run(
                ["node", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            raise NodeNotFoundError("Unable to determine Node.js version")
