from abc import ABC, abstractmethod

class NodeFinderBase(ABC):
    """
    Base class for Node.js finders across different operating systems.
    Defines the required interface for finding and validating Node.js installations.
    """

    @abstractmethod
    def get_node_path(self) -> str:
        pass

    @abstractmethod
    def is_node_installed(self) -> bool:
        pass

    @abstractmethod
    def get_node_version(self) -> str:
        pass
