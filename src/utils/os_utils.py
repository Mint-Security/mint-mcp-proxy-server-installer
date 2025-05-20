import platform
from enum import Enum, auto

class OperatingSystem(Enum):
    """Enum representing supported operating systems"""
    WINDOWS = auto()
    LINUX = auto()
    MAC = auto()

def get_current_os() -> OperatingSystem:
    """
    Detects and returns the current operating system.
    
    Returns:
        OperatingSystem: The enum value representing the current operating system
        
    Raises:
        RuntimeError: If the current operating system is not supported
    """
    system = platform.system().lower()
    
    if system == "darwin":
        return OperatingSystem.MAC
    elif system == "linux":
        return OperatingSystem.LINUX
    elif system == "windows":
        return OperatingSystem.WINDOWS
    else:
        raise RuntimeError(f"Unsupported operating system: {system}") 