import os
import json
from typing import Dict, Any
from src.base.config_creator import ConfigCreator
from src.utils.node_finder.mac import NodeFinderMac
import shutil
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
            installed = "mint-mcp-proxy-server" in config.get('mcpServers', {})
            logger.debug(f"Mint proxy already installed: {installed}")
            return installed
        except Exception as e:
            logger.error(f"Error checking if mint proxy is installed: {e}")
            logger.exception("Exception details:")
            return False

    def create_config(self) -> bool:
        logger.info("Starting create_config method")
        # check if the config file exists
        try:
            config_path = self._find_config_file()
            logger.debug(f"Found config path: {config_path}")

            if not os.path.exists(config_path):
                logger.warning(f"Config file does not exist at: {config_path}")
                return False

            # duplicate the config file - for the MCP proxy server to use
            logger.info("Duplicating config file")
            self._duplicate_config_file()

            # update the config file with the MCP server
            logger.info("Updating config file with MCP server")
            result = self._update_config()
            logger.debug(f"Update config result: {result}")

            return result
        except Exception as e:
            logger.error(f"Error in create_config: {e}")
            logger.exception("Exception details:")
            return False
        
    def _update_config(self) -> bool:
        logger.debug("Starting _update_config method")
        try:
            # check if the MCP proxy server is already installed
            if self._mint_proxy_already_installed():
                logger.info("MCP proxy already installed, skipping update")
                return False

            # Create a new config object
            config = {}
            logger.debug("Created new config object")

            # Create or update MCP servers configuration
            config['mcpServers'] = {}
            
            mint_mcp_proxy_server = {
                "command": "mint-mcp-proxy-server",
                "env": {
                    "MCP_CONFIG_PATH": self.mint_config_file_path
                }
            }
            logger.debug(f"Created mint_mcp_proxy_server config with path: {self.mint_config_file_path}")
            
            config['mcpServers']['mint-mcp-proxy-server'] = mint_mcp_proxy_server

            # Overwrite the config file with the new config
            logger.debug(f"Writing new config to: {self.config_file_path}")
            with open(self.config_file_path, 'w') as f:
                json.dump(config, f, indent=4)
            logger.info("Successfully wrote config file")
                
            return True
            
        except Exception as e:
            logger.error(f"Error updating Claude Desktop MCP configuration: {str(e)}")
            try:
                # restore the original config file
                logger.debug(f"Restoring original config from: {self.mint_config_file_path} to {self.config_file_path}")
                shutil.copy(self.mint_config_file_path, self.config_file_path)
                # delete the mint config file
                logger.debug(f"Removing mint config file: {self.mint_config_file_path}")
                os.remove(self.mint_config_file_path)
            except Exception as cleanup_error:
                logger.error(f"Error during cleanup: {cleanup_error}")
                logger.exception("Exception details:")
            return False

    def restore_config(self) -> bool:
        logger.info("Starting restore_config method")
        try:
            # check if the MCP proxy server is already installed
            if not self._mint_proxy_already_installed():
                logger.info("MCP proxy not installed, skipping removal")
                return False

            # restore the original config file
            logger.debug(f"Restoring original config from: {self.mint_config_file_path} to {self.config_file_path}")
            shutil.copy(self.mint_config_file_path, self.config_file_path)
            # delete the mint config file
            logger.debug(f"Removing mint config file: {self.mint_config_file_path}")
            os.remove(self.mint_config_file_path)
            logger.info("Successfully removed uninstall config from Claude Desktop")

            return True
            
        except Exception as e:
            logger.error(f"Error removing uninstall config from Claude Desktop: {str(e)}")
            return False
        