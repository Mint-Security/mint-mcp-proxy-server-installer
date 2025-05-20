from abc import ABC, abstractmethod


class AutoRunEnabler(ABC):
    """
    Base class for enabling our MCP server to auto-run in the target application
    we are trying to install on. eg. Enabling YOLO mode in cursor.
    """

    @abstractmethod
    def enable_auto_run(self) -> bool:
        return True
    
    @abstractmethod
    def disable_auto_run(self) -> bool:
        return True