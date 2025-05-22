import sys
import argparse
from src.utils.os_utils import get_current_os, OperatingSystem
from src.utils.node_finder.mac import NodeFinderMac, NodeNotFoundError
from src.installers.cursor.mac.installer import CursorMacInstaller
from src.installers.claude_desktop.mac.installer import ClaudeDesktopMacInstaller
from src.installers.claude_code.mac.installer import ClaudeCodeMacInstaller
from src.installers.windsurf.mac.installer import WindsurfMacInstaller
from src.consts import UNINSTALL_FOLDERS
from src.utils.logger import configure_logger, LogLevel, get_logger

# Create a logger for this module
logger = get_logger(__name__)

def print_welcome():
    print("\n=== Mint Security Supervisor Installer ===\n")

installer_objects = {
    "cursor": {
        "mac": CursorMacInstaller(),
        "linux": None,
        "windows": None
    },
    "claude-desktop": {
        "mac": ClaudeDesktopMacInstaller(),
        "linux": None,
        "windows": None
    },
    "claude-code": {
        "mac": ClaudeCodeMacInstaller(),
        "linux": None,
        "windows": None
    },
    "windsurf": {
        "mac": WindsurfMacInstaller(),
        "linux": None,
        "windows": None
    }
}

def detect_os():
    try:
        os_type = get_current_os()
        print(f"Detected OS: {os_type.name}")
        return os_type
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

def find_node(os_type):
    if os_type == OperatingSystem.MAC:
        node_finder = NodeFinderMac()
    else:
        print("Node.js detection for this OS is not implemented yet.")
        sys.exit(1)
    try:
        node_path = node_finder.get_node_path()
        print(f"Node.js found at: {node_path}")
        return node_path
    except NodeNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

def print_menu():
    print("\nWhat would you like to install?")
    print("1. Cursor")
    print("2. Claude Desktop")
    print("3. Claude Code")
    print("4. Windsurf")
    print("5. Install on All")

def get_user_selection():
    options = {"1": "Cursor", "2": "Claude Desktop", "3": "Claude Code", "4": "Windsurf", "5": "Install on All"}
    choice = input("Enter the number of your choice: ").strip()
    selected = options.get(choice)
    if selected:
        print(f"You selected: {selected}")
        return selected
    else:
        print("Invalid selection.")
        return None

def uninstall_all(os_type):
    os_key = os_type.name.lower()
    print("\nUninstalling all applications...")
        
    # Then proceed with application uninstallation
    for app, os_map in installer_objects.items():
        try:
            installer = os_map.get(os_key)
            if installer:
                print(f"Uninstalling {app.replace('-', ' ').title()}...")
                if installer.run_uninstallation():
                    print(f"Successfully uninstalled {app.replace('-', ' ').title()}")
                else:
                    print(f"Failed to uninstall {app.replace('-', ' ').title()}")
        except Exception as e:
            print(f"Error uninstalling {app}: {e}")

    # Remove the installation folders
    if installer.remove_installation_folders():
        print("Installation folders removed successfully")
    else:
        print("Failed to remove installation folders")

def main():
    parser = argparse.ArgumentParser(description='Mint Security Supervisor Installer')
    parser.add_argument('--uninstall', action='store_true', help='Uninstall all applications')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()

    # Configure logger
    if args.debug:
        configure_logger(LogLevel.DEBUG.value)
        logger.debug("Debug logging enabled")
    else:
        # Default is to keep logging off
        configure_logger(LogLevel.OFF.value)

    try:
        print_welcome()
        os_type = detect_os()
        
        if args.uninstall:
            uninstall_all(os_type)
            return

        find_node(os_type)
        print_menu()
        selection = get_user_selection()
        if not selection:
            sys.exit(1)
        os_key = os_type.name.lower()
        
        #"Install on All" option removed as there's only one option now
        if selection == "Install on All":
            for app, os_map in installer_objects.items():
                try:
                    installer = os_map.get(os_key)
                    if installer:
                        print(f"Running installation for {app.replace('-', ' ').title()} on {os_type.name}")
                        installer.run_installation()
                        print(f"Installation for {app.replace('-', ' ').title()} on {os_type.name} completed")
                except Exception as e:
                    print(f"Error installing {app} on {os_type.name}: {e}")
        else:
            try:
                app_key = selection.lower().replace(' ', '-')
                installer = installer_objects.get(app_key, {}).get(os_key)
                if installer:
                    print(f"Running installation for {selection} on {os_type.name}")
                    installer.run_installation()
                    print(f"Installation for {selection} on {os_type.name} completed")
                else:
                    print(f"No installer available for {selection} on {os_type.name}")
            except Exception as e:
                print(f"Error installing {selection} on {os_type.name}: {e}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


