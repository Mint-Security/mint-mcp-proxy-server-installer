import os
from src.consts import AppName, PlatformName
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