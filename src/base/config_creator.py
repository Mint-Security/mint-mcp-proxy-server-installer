from abc import ABC, abstractmethod
import shutil
import os
import json
from src.utils.logger import get_logger
from src.consts import APPLICATION_NAME

# Create a logger for this module
logger = get_logger(__name__)

class ConfigCreator(ABC):
    """
    Base class for creating the configuraiton of the target software,
    to include the new MCP servers we want to add.
    """

    @property
    @abstractmethod
    def app_name(self) -> str:
        """Name of the application. Must be implemented by subclasses."""
        pass

    @property
    @abstractmethod
    def config_file_path(self) -> str:
        """Path to the application's config file. Must be implemented by subclasses."""
        pass
    
    def _create_backup(self) -> bool:
        """Create a backup of the config file before modifying it."""
        try:
            config_dir = os.path.dirname(self.config_file_path)
            config_filename = os.path.basename(self.config_file_path)
            
            # Create backup filename
            backup_filename = f"{config_filename}.backup"
            backup_path = os.path.join(config_dir, backup_filename)
            
            # If backup already exists, remove it first
            if os.path.exists(backup_path):
                os.remove(backup_path)
                logger.debug(f"Removed existing backup file: {backup_path}")
            
            # Copy the original config file to backup
            shutil.copy2(self.config_file_path, backup_path)
            logger.info(f"Created backup of config file at: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating backup of config file: {e}")
            logger.exception("Exception details:")
            return False
    
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
            
            # Create backup before modifying the config
            logger.info("Creating backup of config file...")
            if not self._create_backup():
                logger.warning("Failed to create backup, but continuing with installation")
            
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
                    "MCP_CONFIG_PATH": self.config_file_path,
                    "MCP_CLIENT_NAME": self.app_name
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