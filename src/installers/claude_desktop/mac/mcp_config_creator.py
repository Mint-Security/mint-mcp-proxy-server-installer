import os
import json
from typing import Dict, Any
from src.base.config_creator import ConfigCreator
from src.utils.node_finder.mac import NodeFinderMac
from src.consts import  APPLICATION_NAME
from src.utils.logger import get_logger

# Create a logger for this module
logger = get_logger(__name__)

class ClaudeDesktopMacMCPConfigCreator(ConfigCreator):

    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.node_finder = NodeFinderMac()
        logger.debug("ClaudeDesktopMacMCPConfigCreator initialized")
        
    @property
    def config_file_path(self) -> str:
        logger.debug("config_file_path property called")
        return os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")

    def _mint_proxy_already_installed(self) -> bool:
        logger.debug(f"Checking if mint proxy is already installed in: {self.config_file_path}")
        try:
            with open(self.config_file_path, 'r') as f:
                config = json.load(f)
            logger.debug(f"Config contents: {config}")
            installed = APPLICATION_NAME in config.get('mcpServers', {})
            logger.debug(f"Mint proxy already installed: {installed}")
            return installed
        except Exception as e:
            logger.error(f"Error checking if mint proxy is installed: {e}")
            logger.exception("Exception details:")
            return False

    def update_config(self) -> bool:
        logger.info("Starting update_config method")
        # check if the config file exists
        try:
            logger.debug(f"Found config path: {self.config_file_path}")

            if not os.path.exists(self.config_file_path):
                logger.warning(f"Config file does not exist at: {self.config_file_path}")
                return False
            
            # check if the MCP proxy server is already installed
            if self._mint_proxy_already_installed():
                logger.info("MCP proxy already installed, skipping update")
                return False
            
            logger.info("Updating config file with our MCP server")
            # read the config file
            with open(self.config_file_path, 'r') as f:
                config = json.load(f)

            # Store original mcpServers as backup
            config['mintMcpServers'] = config.get('mcpServers', {})
            config['mcpServers'] = {}

            mint_mcp_proxy_server = {
                "command": APPLICATION_NAME,
                "env": {
                    "MCP_CONFIG_PATH": self.config_file_path
                }
            }
            logger.debug(f"Created mint_mcp_proxy_server config with path: {self.config_file_path}")
            
            config['mcpServers'][APPLICATION_NAME] = mint_mcp_proxy_server

            # Overwrite the config file with the new config
            logger.debug(f"Writing new config to: {self.config_file_path}")
            with open(self.config_file_path, 'w') as f:
                json.dump(config, f, indent=4)
            logger.info("Successfully wrote config file")

            return True
        except Exception as e:
            logger.error(f"Error in update_config: {e}")
            logger.exception("Exception details:")
            return False
        
    def restore_config(self) -> bool:
        logger.info("Starting restore_config method")
        try:
            # check if the MCP proxy server is already installed
            if not self._mint_proxy_already_installed():
                logger.info("MCP proxy not installed, skipping removal")
                return False

            # read the config file
            with open(self.config_file_path, 'r') as f:
                config = json.load(f)

            # Remove mintMcpServers property entirely instead of setting it to {}
            if 'mintMcpServers' in config:
                # restore the original config file
                config['mcpServers'] = config['mintMcpServers']
                del config['mintMcpServers']
                
            # Write the updated config back to the file
            with open(self.config_file_path, 'w') as f:
                json.dump(config, f, indent=4)
            logger.info("Successfully restored config file")

            return True
            
        except Exception as e:
            logger.error(f"Error removing uninstall config from Claude Desktop: {str(e)}")
            return False
        