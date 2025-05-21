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
    
    @abstractmethod
    def _mint_proxy_already_installed(self) -> bool:
        pass

    @abstractmethod
    def update_config(self) -> bool:
        pass
    
    @abstractmethod
    def restore_config(self) -> bool:
        pass