import os
import json
from typing import Dict, Any
from src.base.config_creator import ConfigUpdater
from src.utils.node_finder.mac import NodeFinderMac

class WindsurfMacMCPConfigEditor(ConfigUpdater):

    WINDSURF_CONFIG_FILE_PATH = "~/.codeium/windsurf/mcp_config.json"

    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.node_finder = NodeFinderMac()

    def _mint_proxy_already_installed(self) -> bool:
        pass

    def update_config(self) -> bool:
        pass

    def update_config(self) -> bool:
        # # Expand the home directory in the path
        # config_path = os.path.expanduser(self.WINDSURF_CONFIG_FILE_PATH)
        
        # # check if the file exists
        # if not os.path.exists(config_path):
        #     # Create directory if it doesn't exist
        #     os.makedirs(os.path.dirname(config_path), exist_ok=True)
        #     with open(config_path, "w") as file:
        #         json.dump({}, file)

        # with open(config_path, "r") as file:
        #     try:
        #         file_config = json.load(file)
        #     except json.JSONDecodeError:
        #         file_config = {}

        # # Create mcpServers key if it doesn't exist
        # if "mcpServers" not in file_config:
        #     file_config["mcpServers"] = {}

        # installation_path = self.config.get("installation_path", "")
        # if not installation_path:
        #     return False

        # supervisor_config = {
        #     "command": self.node_finder.get_node_path(),
        #     "args": [
        #         os.path.join(installation_path + "/compiled/dist/", "server.js"),
        #     ],
        #     "env": {
        #         "AGENT_ID": f"windsurf_{AGENT_ID}"
        #     }
        # }

        # # Insert supervisor-server as the first key in mcpServers
        # from collections import OrderedDict
        # mcp_servers = file_config["mcpServers"]
        # new_mcp_servers = OrderedDict()
        # new_mcp_servers["supervisor-server"] = supervisor_config
        # for k, v in mcp_servers.items():
        #     if k != "supervisor-server":
        #         new_mcp_servers[k] = v
        # file_config["mcpServers"] = new_mcp_servers

        # # write the config
        # with open(config_path, "w") as file:
        #     json.dump(file_config, file, indent=4)

        return True
        
    def restore_config(self) -> bool:
        # # Expand the home directory in the path
        # config_path = os.path.expanduser(self.WINDSURF_CONFIG_FILE_PATH)
        
        # # check if the file exists
        # if not os.path.exists(config_path):
        #     return False
        
        # # read the config
        # with open(config_path, "r") as file:
        #     try:
        #         file_config = json.load(file)
        #     except json.JSONDecodeError:
        #         file_config = {}
        
        # # remove the supervisor-server from the config
        # if "mcpServers" in file_config and "supervisor-server" in file_config["mcpServers"]:
        #     del file_config["mcpServers"]["supervisor-server"]
        
        # # write the config
        # with open(config_path, "w") as file:
        #     json.dump(file_config, file, indent=4)
        
        return True
            