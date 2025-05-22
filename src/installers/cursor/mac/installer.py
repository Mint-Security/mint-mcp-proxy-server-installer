import time
from typing import Dict, Any
import os
import subprocess
import shutil
from src.utils.os_utils import get_current_os, OperatingSystem
from src.base.base_installer import BaseInstaller

from src.installers.cursor.mac.mcp_config_creator import CursorMacMCPConfigEditor
from src.installers.cursor.mac.yolo_enabler import CursorMacYOLOEnabler
from src.consts import PlatformName, AppName

class CursorMacInstaller(BaseInstaller):

    def __init__(self):
        try:
            super().__init__()
            self.set_objects(CursorMacYOLOEnabler, CursorMacMCPConfigEditor)
        except Exception as e:
            print(f"Error initializing CursorMacInstaller: {e}")

    PLATFORM_NAME = PlatformName.MAC
    APP_NAME = AppName.CURSOR
    CONFIG_FILE_PATH = "~/.cursor/mcp.json"

    def validate(self) -> bool:
        is_valid = super().validate()
        if not is_valid:
            return False
        
        custom_path = "/usr/local/bin:" + os.environ.get("PATH", "")
        cursor_installed_path = shutil.which("Cursor", path=custom_path) is not None
        # Check if Claude Desktop is installed
        cursor_app_path = "/Applications/Cursor.app"
        cursor_installed = os.path.exists(cursor_app_path)
        if not (cursor_installed_path or cursor_installed):
            print("Cursor is not installed")
            return False
        
        return True

    def kill_process(self) -> bool:
        try:
            os.system("osascript -e 'quit app \"Cursor\"'")
            # Wait until it's closed
            while subprocess.run(["pgrep", "-x", "Cursor"], stdout=subprocess.DEVNULL).returncode == 0:
                time.sleep(1)
            return True
        except Exception as e:
            print(f"Error killing cursor process: {e}")
            return False

       