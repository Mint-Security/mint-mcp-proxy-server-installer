from src.base.auto_run_enabler import AutoRunEnabler
from typing import Dict, Any

class WindsurfMacYOLOEnabler(AutoRunEnabler):

    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config

    def enable_auto_run(self) -> bool:
        return True

    def disable_auto_run(self) -> bool:
        return True
            
