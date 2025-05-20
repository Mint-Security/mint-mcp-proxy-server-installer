import os
import json
from typing import Dict, Any
from src.base.auto_run_enabler import AutoRunEnabler

class ClaudeCodeMacYOLOEnabler(AutoRunEnabler):
    REQUIRED_PERMISSIONS = [
        "mcp__supervisor-server__supervisor_server",
        "supervisor_server",
        "supervisor-server__supervisor_server"
    ]

    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        
    def enable_auto_run(self) -> bool:
        try:
            # Get path to settings.json
            settings_path = os.path.expanduser("~/.claude/settings.json")
            settings_local_path = os.path.expanduser("~/.claude/settings.local.json")
            settings_paths = [settings_path, settings_local_path]

            for settings_path in settings_paths:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(settings_path), exist_ok=True)

                # Read existing settings or create new
                settings = {"permissions": {"allow": [], "deny": []}}
                if os.path.exists(settings_path):
                    with open(settings_path, 'r') as f:
                        settings = json.load(f)

                # Ensure permissions structure exists
                if "permissions" not in settings:
                    settings["permissions"] = {"allow": [], "deny": []}
                if "allow" not in settings["permissions"]:
                    settings["permissions"]["allow"] = []

                # Add any missing required permissions
                modified = False
                for perm in self.REQUIRED_PERMISSIONS:
                    if perm not in settings["permissions"]["allow"]:
                        settings["permissions"]["allow"].append(perm)
                        modified = True

                # Write back if modified
                if modified:
                    with open(settings_path, 'w') as f:
                        json.dump(settings, f, indent=2)

            return True

        except Exception as e:
            print(f"Error enabling YOLO mode: {str(e)}")
            return False
        
    def disable_auto_run(self) -> bool:
        try:
            # Get path to settings.json
            settings_path = os.path.expanduser("~/.claude/settings.json")
            settings_local_path = os.path.expanduser("~/.claude/settings.local.json")
            settings_paths = [settings_path, settings_local_path]

            for settings_path in settings_paths:
                if not os.path.exists(settings_path):
                    continue

                # Read existing settings
                with open(settings_path, 'r') as f:
                    settings = json.load(f)

                # Skip if no permissions section
                if "permissions" not in settings or "allow" not in settings["permissions"]:
                    continue

                # Remove required permissions from allow list
                modified = False
                for perm in self.REQUIRED_PERMISSIONS:
                    if perm in settings["permissions"]["allow"]:
                        settings["permissions"]["allow"].remove(perm)
                        modified = True

                # Write back if modified
                if modified:
                    with open(settings_path, 'w') as f:
                        json.dump(settings, f, indent=2)

            return True

        except Exception as e:
            print(f"Error disabling YOLO mode: {str(e)}")
            return False