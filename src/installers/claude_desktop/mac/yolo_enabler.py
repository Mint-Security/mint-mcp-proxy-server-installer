import os
import json
from typing import Dict, Any
from src.base.auto_run_enabler import AutoRunEnabler

class ClaudeDesktopMacYOLOEnabler(AutoRunEnabler):
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        
    def enable_auto_run(self) -> bool:
        # TODO: Implement this
        return True
    
    def disable_auto_run(self) -> bool:
        # TODO: Implement this
        return True