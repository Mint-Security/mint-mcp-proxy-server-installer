import subprocess
import time
from typing import Dict, Any
import os
import shutil
from src.consts import AppName, PlatformName
from src.utils.os_utils import get_current_os, OperatingSystem
from src.base.base_installer import BaseInstaller

from src.installers.claude_code.mac.mcp_config_creator import ClaudeCodeMacMCPConfigEditor
from src.installers.claude_code.mac.yolo_enabler import ClaudeCodeMacYOLOEnabler

class ClaudeCodeMacInstaller(BaseInstaller):

    def __init__(self):
        try:
            super().__init__()
            self.set_objects(ClaudeCodeMacYOLOEnabler, ClaudeCodeMacMCPConfigEditor)
        except Exception as e:
            print(f"Error initializing ClaudeCodeMacInstaller: {e}")

    PLATFORM_NAME = PlatformName.MAC
    APP_NAME = AppName.CLAUDE_CODE

    def validate(self) -> bool:
        valid_os = get_current_os() == OperatingSystem.MAC
        if not valid_os:
            print(f"The OS is not valid expected {OperatingSystem.MAC} but got {get_current_os()}")
            return False
        
        # Check if Claude Code is installed
        custom_path = "/usr/local/bin:" + os.environ.get("PATH", "")
        claude_code_installed_path1 = shutil.which("Claude", path=custom_path) is not None
        claude_code_installed_path2 = shutil.which("claude", path=custom_path) is not None

        if not (claude_code_installed_path1 or claude_code_installed_path2):
            print(f"Claude Code is not installed {claude_code_installed_path1} {claude_code_installed_path2}")
            return False
        
        return True

    def kill_process(self) -> bool:
        try:
            custom_path = "/usr/local/bin:" + os.environ.get("PATH", "")
            # killing the cursor process before starting to run
            os.system(f"pkill -f {shutil.which('Claude', path=custom_path)}")
            os.system(f"pkill -f {shutil.which('claude', path=custom_path)}")
            # Wait until it's closed
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"Error killing claude code process: {e}")
            return False

