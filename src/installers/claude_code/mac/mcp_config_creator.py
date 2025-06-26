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
    
    def _wrap_mcp_server_with_proxy(self, server_config: Dict[str, Any], client_name: str = "Claude Code") -> Dict[str, Any]:
        """
        Wrap an existing MCP server configuration with our proxy.
        """
        return {
            "command": "mint-mcp-proxy-server",
            "env": {
                "MCP_CONFIG_PATH": self.config_file_path,
                "MCP_CLIENT_NAME": client_name,
                "NO_TOOLS": "true"
            },
            "inner": server_config
        }
    
    def _is_wrapped_by_proxy(self, server_config: Dict[str, Any]) -> bool:
        """
        Check if a server config is already wrapped by our proxy.
        """
        return (
            server_config.get("command") == "mint-mcp-proxy-server" and
            "inner" in server_config and
            server_config.get("env", {}).get("NO_TOOLS") == "true"
        )
    
    def _is_our_main_proxy(self, server_config: Dict[str, Any]) -> bool:
        """
        Check if a server config is our main proxy (without NO_TOOLS).
        """
        return (
            server_config.get("command") == "mint-mcp-proxy-server" and
            "inner" not in server_config and
            server_config.get("env", {}).get("NO_TOOLS") != "true"
        )
    
    def update_config(self) -> bool:
        super().update_config()

        # read config file
        with open(self.config_file_path, 'r') as f:
            config = json.load(f)

        # Handle global mcpServers (if they exist)
        if 'mcpServers' in config:
            for server_name, server_config in list(config['mcpServers'].items()):
                # Skip if already wrapped by our proxy or if it's our main proxy
                if not self._is_wrapped_by_proxy(server_config) and not self._is_our_main_proxy(server_config):
                    config['mcpServers'][server_name] = self._wrap_mcp_server_with_proxy(server_config)
        
        # Add our main proxy to global mcpServers if it doesn't exist
        if 'mcpServers' not in config:
            config['mcpServers'] = {}
        
        # Check if our main proxy already exists
        main_proxy_exists = any(self._is_our_main_proxy(server_config) for server_config in config['mcpServers'].values())
        
        if not main_proxy_exists:
            config['mcpServers']['mint-mcp-proxy-server'] = {
                "command": "mint-mcp-proxy-server",
                "env": {
                    "MCP_CONFIG_PATH": self.config_file_path,
                    "MCP_CLIENT_NAME": "Claude Code"
                }
            }

        # Handle project-specific mcpServers
        for project_path, project_config in config['projects'].items():
            if 'mcpServers' in project_config:
                for server_name, server_config in list(project_config['mcpServers'].items()):
                    # Skip if already wrapped by our proxy or if it's our main proxy
                    if not self._is_wrapped_by_proxy(server_config) and not self._is_our_main_proxy(server_config):
                        project_config['mcpServers'][server_name] = self._wrap_mcp_server_with_proxy(
                            server_config, 
                            client_name="Claude Code"
                        )

        # write config file
        with open(self.config_file_path, 'w') as f:
            json.dump(config, f, indent=4)

        return True
    
    def restore_config(self) -> bool:
        super().restore_config()

        # read config file
        with open(self.config_file_path, 'r') as f:
            config = json.load(f)

        # Handle global mcpServers restoration
        if 'mcpServers' in config:
            servers_to_remove = []
            for server_name, server_config in list(config['mcpServers'].items()):
                if self._is_wrapped_by_proxy(server_config):
                    # Restore the original server config from the 'inner' key
                    config['mcpServers'][server_name] = server_config['inner']
                elif self._is_our_main_proxy(server_config):
                    # Mark our main proxy for removal
                    servers_to_remove.append(server_name)
            
            # Remove our main proxy
            for server_name in servers_to_remove:
                del config['mcpServers'][server_name]

        # Handle project-specific mcpServers restoration
        for project_path, project_config in config['projects'].items():
            if 'mcpServers' in project_config:
                for server_name, server_config in list(project_config['mcpServers'].items()):
                    if self._is_wrapped_by_proxy(server_config):
                        # Restore the original server config from the 'inner' key
                        project_config['mcpServers'][server_name] = server_config['inner']

        # write config file
        with open(self.config_file_path, 'w') as f:
            json.dump(config, f, indent=4)

        return True