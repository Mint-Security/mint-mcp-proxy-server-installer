import os
import shutil
from src.consts import AppName, PlatformName
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
    CONFIG_FILE_PATH = "~/.claude.json"

    def validate(self) -> bool:
        is_valid = super().validate()
        if not is_valid:
            return False
        
        # Check if Claude Code is installed
        custom_path = "/usr/local/bin:" + os.environ.get("PATH", "")
        claude_code_installed_path1 = shutil.which("Claude", path=custom_path) is not None
        claude_code_installed_path2 = shutil.which("claude", path=custom_path) is not None

        if not (claude_code_installed_path1 or claude_code_installed_path2):
            print(f"Claude Code is not installed {claude_code_installed_path1} {claude_code_installed_path2}")
            return False
        
        return True

