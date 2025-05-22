import time
from typing import Dict, Any
import os
import subprocess
import shutil
from src.utils.os_utils import get_current_os, OperatingSystem
from src.base.base_installer import BaseInstaller

from src.installers.windsurf.mac.mcp_config_creator import WindsurfMacMCPConfigEditor
from src.installers.windsurf.mac.yolo_enabler import WindsurfMacYOLOEnabler
from src.consts import PlatformName, AppName

class WindsurfMacInstaller(BaseInstaller):

    def __init__(self):
        try:
            super().__init__()
            self.set_objects(WindsurfMacYOLOEnabler, WindsurfMacMCPConfigEditor)
        except Exception as e:
            print(f"Error initializing WindsurfMacInstaller: {e}")

    PLATFORM_NAME = PlatformName.MAC
    APP_NAME = AppName.WINDSURF
    CONFIG_FILE_PATH = "~/.codeium/windsurf/mcp_config.json"

    def validate(self) -> bool:
        is_valid = super().validate()
        if not is_valid:
            return False
        
        custom_path = "/usr/local/bin:" + os.environ.get("PATH", "")
        windsurf_installed_path = shutil.which("windsurf", path=custom_path) is not None
        # Check if Windsurf is installed
        windsurf_app_path = "/Applications/Windsurf.app"
        windsurf_installed = os.path.exists(windsurf_app_path)
        if not (windsurf_installed_path or windsurf_installed):
            print("Windsurf is not installed")
            return False
        
        return True

    # Todo - fix to be generic and work on all OS
    def kill_process(self) -> bool:
        try:
            # killing the windsurf process before starting to run
            os.system("osascript -e 'quit app \"Windsurf\"'")
            # Wait until it's closed
            while subprocess.run(["pgrep", "-x", "Windsurf"], stdout=subprocess.DEVNULL).returncode == 0:
                time.sleep(1)
            return True
        except Exception as e:
            print(f"Error killing windsurf process: {e}")
            return False
        