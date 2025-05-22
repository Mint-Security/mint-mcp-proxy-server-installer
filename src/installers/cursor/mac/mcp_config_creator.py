import os
import json
from typing import Dict, Any
from src.base.config_creator import ConfigCreator
from src.utils.node_finder.mac import NodeFinderMac
from src.utils.logger import get_logger

# Create a logger for this module
logger = get_logger(__name__)

class CursorMacMCPConfigEditor(ConfigCreator):

    CONFIG_FILE_PATH = "~/.cursor/mcp.json"

    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.node_finder = NodeFinderMac()

    @property
    def config_file_path(self) -> str:
        logger.debug("config_file_path property called")
        return os.path.expanduser(self.CONFIG_FILE_PATH)


