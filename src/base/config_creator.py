from abc import ABC, abstractmethod
import shutil
import os
import json
from src.utils.logger import get_logger

# Create a logger for this module
logger = get_logger(__name__)

class ConfigCreator(ABC):
    """
    Base class for creating the configuraiton of the target software,
    to include the new MCP servers we want to add.
    """

    @property
    @abstractmethod
    def config_file_path(self) -> str:
        """Path to the application's config file. Must be implemented by subclasses."""
        pass
    
    @property
    def mint_config_file_path(self) -> str:
        """Path to the Mint backup config file. Must be implemented by subclasses."""
        logger.debug("mint_config_file_path property called")
        # Ensure we access the property, not try to call it as a function
        config_path = self.config_file_path
        logger.debug(f"config_file_path value: {config_path}")
        result = config_path + ".mint"
        logger.debug(f"mint_config_file_path returning: {result}")
        return result

    def _duplicate_config_file(self):
        logger.debug("_duplicate_config_file called")
        try:
            config_path = self._find_config_file()
            mint_path = self.mint_config_file_path
            logger.debug(f"Copying from {config_path} to {mint_path}")
            shutil.copy(config_path, mint_path)
            logger.debug("Copy successful")
        except Exception as e:
            logger.error(f"Error in _duplicate_config_file: {e}")
            logger.exception("Exception details:")
            raise

    def _find_config_file(self):
        logger.debug("_find_config_file called")
        try:
            # Common locations to check
            config_path = os.path.expanduser(self.config_file_path)
            logger.debug(f"Expanded config path: {config_path}")
            if not os.path.exists(config_path):
                logger.debug(f"Config path doesn't exist, creating directory: {os.path.dirname(config_path)}")
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                logger.debug(f"Creating empty config file: {config_path}")
                with open(config_path, "w") as file:
                    json.dump({}, file)
                logger.debug("Empty config file created")

            return config_path
        except Exception as e:
            logger.error(f"Error in _find_config_file: {e}")
            logger.exception("Exception details:")
            raise

    @abstractmethod
    def _mint_proxy_already_installed(self) -> bool:
        pass

    @abstractmethod
    def create_config(self) -> bool:
        pass
    
    @abstractmethod
    def restore_config(self) -> bool:
        pass