import os
import json
from typing import Dict, Any
from src.base.config_creator import ConfigCreator
from src.utils.node_finder.mac import NodeFinderMac
from src.utils.logger import get_logger

# Create a logger for this module
logger = get_logger(__name__)

class ClaudeCodeMacMCPConfigEditor(ConfigCreator):
    CONFIG_FILE_PATH = "~/.claude.json"

    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.node_finder = NodeFinderMac()

    @property
    def app_name(self) -> str:
        return "Claude Code"
  
    @property
    def config_file_path(self) -> str:
        logger.debug("config_file_path property called")
        return os.path.expanduser(self.CONFIG_FILE_PATH)
    
    def update_config(self) -> bool:
        super().update_config()

        # read config file
        with open(self.config_file_path, 'r') as f:
            config = json.load(f)

        # go over all the projects (which is a dictionary)
        for project_path, project_config in config['projects'].items():
            if 'mcpServers' in project_config:
                # Move mcpServers content to mintMcpServers
                if 'mintMcpServers' not in project_config:
                    project_config['mintMcpServers'] = {}
                
                # Merge existing mcpServers into mintMcpServers
                project_config['mintMcpServers'].update(project_config['mcpServers'])
                
                # Remove the original mcpServers
                del project_config['mcpServers']

        # write config file
        with open(self.config_file_path, 'w') as f:
            json.dump(config, f, indent=4)

        return True
    
    def restore_config(self) -> bool:
        super().restore_config()

        # read config file
        with open(self.config_file_path, 'r') as f:
            config = json.load(f)

        # go over all the projects (which is a dictionary)
        for project_path, project_config in config['projects'].items():
            if 'mintMcpServers' in project_config:
                # Move mintMcpServers content back to mcpServers
                if 'mcpServers' not in project_config:
                    project_config['mcpServers'] = {}
                
                # Merge existing mintMcpServers into mcpServers
                project_config['mcpServers'].update(project_config['mintMcpServers'])
                
                # Remove the mintMcpServers
                del project_config['mintMcpServers']

        # write config file
        with open(self.config_file_path, 'w') as f:
            json.dump(config, f, indent=4)

        return True