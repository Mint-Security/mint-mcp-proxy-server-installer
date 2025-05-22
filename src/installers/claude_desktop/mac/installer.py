import subprocess
import time
from typing import Dict, Any
import os
from src.consts import AppName, PlatformName
from src.utils.os_utils import get_current_os, OperatingSystem
from src.base.base_installer import BaseInstaller

from src.installers.claude_desktop.mac.mcp_config_creator import ClaudeDesktopMacMCPConfigCreator
from src.installers.claude_desktop.mac.yolo_enabler import ClaudeDesktopMacYOLOEnabler

class ClaudeDesktopMacInstaller(BaseInstaller):

    def __init__(self):
        try:
            super().__init__()
            self.set_objects(ClaudeDesktopMacYOLOEnabler, ClaudeDesktopMacMCPConfigCreator)
        except Exception as e:
            print(f"Error initializing ClaudeDesktopMacInstaller: {e}")

    PLATFORM_NAME = PlatformName.MAC
    APP_NAME = AppName.CLAUDE_DESKTOP
    CONFIG_FILE_PATH = "~/Library/Application Support/Claude/claude_desktop_config.json"

    def validate(self) -> bool:
        is_valid = super().validate()
        if not is_valid:
            return False
        
        # Check if Claude Desktop is installed
        claude_app_path = "/Applications/Claude.app"
        claude_installed = os.path.exists(claude_app_path)
        if not claude_installed:
            print("Claude Desktop is not installed")
            return False
        
        return True

    def kill_process(self) -> bool:
        try:
            # killing the claude process before starting to run
            os.system("osascript -e 'quit app \"Claude\"'")
            # Wait until it's closed
            while subprocess.run(["pgrep", "-x", "Claude"], stdout=subprocess.DEVNULL).returncode == 0:
                time.sleep(1)

            # Wait until it's closed
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"Error killing claude desktop process: {e}")
            return False