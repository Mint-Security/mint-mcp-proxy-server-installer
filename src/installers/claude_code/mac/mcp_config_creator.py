import os
import json
from typing import Dict, Any
from src.base.config_creator import ConfigUpdater
from src.utils.node_finder.mac import NodeFinderMac

class ClaudeCodeMacMCPConfigEditor(ConfigUpdater):
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.node_finder = NodeFinderMac()
        
    def _find_config_file(self):
        # Common locations to check
        config_path = os.path.expanduser("~/.claude.json")
        if not os.path.exists(config_path):
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, "w") as file:
                json.dump({}, file)

        return config_path

    def _mint_proxy_already_installed(self) -> bool:
        pass
    
    def update_config(self) -> bool:
        pass
    
    def update_config(self) -> bool:
        # config_path = self._find_config_file()

        try:
        #     # Read the config file
        #     with open(config_path, 'r') as f:
        #         config = json.load(f)
            
        #     # Create or update MCP servers configuration
        #     if 'mcpServers' not in config:
        #         config['mcpServers'] = {}
            
        #     installation_path = self.config.get("installation_path", "")
        #     if not installation_path:
        #         return False

        #     # Add our supervisor tool server
        #     supervisor_config = {
        #         "command": self.node_finder.get_node_path(),
        #         "args": [
        #             os.path.join(installation_path + "/compiled/dist/", "server.js"),
        #         ],
        #         "env": {
        #             "AGENT_ID": f"claude_code_{AGENT_ID}"
        #         }
        #     }
            
        #     # Insert supervisor-server as the first key in mcpServers
        #     from collections import OrderedDict
        #     mcp_servers = config['mcpServers']
        #     new_mcp_servers = OrderedDict()
        #     new_mcp_servers["supervisor-server"] = supervisor_config
        #     for k, v in mcp_servers.items():
        #         if k != "supervisor-server":
        #             new_mcp_servers[k] = v
        #     config['mcpServers'] = new_mcp_servers
            
        #     # Write the updated config back
        #     with open(config_path, 'w') as f:
        #         json.dump(config, f, indent=4)
                
            return True
            
        except Exception as e:
            print(f"Error updating Claude Code MCP configuration: {str(e)}")
            return False 
        

    def restore_config(self) -> bool:
        # config_path = self._find_config_file()

        try:
            # # Read the config file
            # with open(config_path, 'r') as f:
            #     config = json.load(f)
            
            # # Remove supervisor server if it exists
            # if 'mcpServers' in config and "supervisor-server" in config['mcpServers']:
            #     del config['mcpServers']["supervisor-server"]
            
            # # Write the updated config back
            # with open(config_path, 'w') as f:
            #     json.dump(config, f, indent=4)
                
            return True
            
        except Exception as e:
            print(f"Error removing supervisor config from Claude Desktop: {str(e)}")
            return False
        