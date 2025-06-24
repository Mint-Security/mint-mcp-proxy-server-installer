import sys
import argparse
import shutil
from datetime import datetime
from src.utils.os_utils import get_current_os, OperatingSystem
from src.utils.node_finder.mac import NodeFinderMac, NodeNotFoundError
from src.installers.cursor.mac.installer import CursorMacInstaller
from src.installers.claude_desktop.mac.installer import ClaudeDesktopMacInstaller
from src.installers.claude_code.mac.installer import ClaudeCodeMacInstaller
from src.installers.windsurf.mac.installer import WindsurfMacInstaller
from src.base.base_installer import BaseInstaller
from src.utils.logger import configure_logger, LogLevel, get_logger
from src.consts import DOWNLOAD_URLS, PlatformName, PACKAGE_NAME, PACKAGE_VERSION
import os
# Create a logger for this module
logger = get_logger(__name__)

def print_welcome():
    print(f"\n=== Mint Security Proxy Installer ({PACKAGE_VERSION}) ===\n")

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

def print_client_menu(title, show_install_all=False):
    print(f"\n{title}")
    print("1. Cursor")
    print("2. Claude Desktop")
    print("3. Claude Code")
    print("4. Windsurf")
    if show_install_all:
        print("5. Install on All")

def get_client_selection(show_install_all=False):
    options = {"1": "Cursor", "2": "Claude Desktop", "3": "Claude Code", "4": "Windsurf"}
    if show_install_all:
        options["5"] = "Install on All"
    
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
        
    # Uninstall application
    BaseInstaller.uninstall_application()

    # Then proceed with application uninstallation
    for app, os_map in installer_objects.items():
        try:
            installer = os_map.get(os_key)
            if installer:
                print(f"Uninstalling {app.replace('-', ' ').title()}...")
                if not installer.is_client_installed():
                    print(f"{app.replace('-', ' ').title()} is not installed, skipping uninstallation")
                    continue
                if installer.run_client_uninstallation():
                    print(f"Successfully uninstalled {app.replace('-', ' ').title()}")
                    print(f" >>> NOTE: In order for the uninstallation to take effect, restart {installer.APP_NAME}. <<<")
                else:
                    print(f"Failed to uninstall {app.replace('-', ' ').title()}")
        except Exception as e:
            print(f"Error uninstalling {app}: {e}")

    # Remove the installation folders
    if BaseInstaller.remove_installation_folders():
        print("Installation folders removed successfully")
    else:
        print("Failed to remove installation folders")



def get_backup_info(backup_path):
    """Get backup file creation time information."""
    try:
        if os.path.exists(backup_path):
            # Get file modification time
            mtime = os.path.getmtime(backup_path)
            backup_date = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            return backup_date
        return None
    except Exception as e:
        logger.error(f"Error getting backup info: {e}")
        return None

def revert_client(os_type):
    """Revert a client configuration from backup."""
    print("\n=== Revert Client Configuration ===\n")
    
    print_client_menu("Which client would you like to revert?")
    selection = get_client_selection()
    if not selection:
        sys.exit(1)
    
    os_key = os_type.name.lower()
    app_key = selection.lower().replace(' ', '-')
    installer = installer_objects.get(app_key, {}).get(os_key)
    
    if not installer:
        print(f"No installer available for {selection} on {os_type.name}")
        return
    
    # Get backup file path
    config_path = installer.config_creator.config_file_path
    config_dir = os.path.dirname(config_path)
    config_filename = os.path.basename(config_path)
    backup_path = os.path.join(config_dir, f"{config_filename}.backup")
    
    # Check if backup exists
    if not os.path.exists(backup_path):
        print(f"No backup file found for {selection}")
        print("Cannot proceed with revert.")
        return
    
    # Get backup creation date
    backup_date = get_backup_info(backup_path)
    if backup_date:
        print(f"\nNOTE: The revert will restore the config file from backup created on {backup_date}")
    else:
        print(f"\nNOTE: The revert will restore the config file from the available backup")
    
    # Ask for user confirmation
    confirm = input("Do you want to proceed with the revert? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Revert operation cancelled.")
        return
    
    try:
        # Check if currently installed and uninstall if needed
        if installer.is_client_installed():
            print(f"Uninstalling {selection} first...")
            if not installer.run_client_uninstallation():
                print(f"Failed to uninstall {selection}")
                return
            print(f"Successfully uninstalled {selection}")
        else:
            print(f"{selection} is not currently installed")
        
        # Copy backup file to override the original config
        print(f"Restoring config file from backup...")
        shutil.copy2(backup_path, config_path)
        print(f"Successfully restored config file from backup")
        print(f"Config file reverted to state from {backup_date if backup_date else 'backup'}")
        
        # Remove the backup file after successful revert
        os.remove(backup_path)
        
        print(f"\n >>> NOTE: Please restart {installer.APP_NAME} for changes to take effect. <<<")
        
    except Exception as e:
        print(f"Error during revert operation: {e}")
        logger.error(f"Revert error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Mint Security Proxy Installer')
    parser.add_argument('--uninstall', action='store_true', help='Uninstall all applications')
    parser.add_argument('--revert', action='store_true', help='Revert a client configuration from backup')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--download', action='store_true', help='Download the package from the remote URL (default: use local package)')
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
        
        if args.revert:
            revert_client(os_type)
            return

        find_node(os_type)
        print_client_menu("What would you like to install?", show_install_all=True)
        selection = get_client_selection(show_install_all=True)
        if not selection:
            sys.exit(1)
        os_key = os_type.name.lower()
        
        # Download or use local application package
        if args.download:
            package_path = BaseInstaller.download_application(DOWNLOAD_URLS[PlatformName.MAC])
            logger.info(f"Downloaded package to: {package_path}")
        else:

            package_path = os.path.abspath(PACKAGE_NAME)
            if not os.path.exists(package_path):
                print(f"Local package {package_path} not found.")
                sys.exit(1)
            logger.info(f"Using local package: {package_path}")
        if not package_path:
            sys.exit(1)

        # Install the application (npm package of mint-mcp-proxy-server)
        BaseInstaller.install_application(package_path)

        #"Install on All" option removed as there's only one option now
        if selection == "Install on All":
            for app, os_map in installer_objects.items():
                try:
                    installer = os_map.get(os_key)
                    if installer:
                        if installer.is_client_installed():
                            print(f"{app.replace('-', ' ').title()} is already installed, skipping installation. Please uninstall it first.")
                            continue
                        print(f"Running installation for {app.replace('-', ' ').title()} on {os_type.name}")
                        installer.run_client_installation()
                        print(f"Installation for {app.replace('-', ' ').title()} on {os_type.name} completed")
                        print(f" >>> NOTE: In order for the installation to take effect, restart {installer.APP_NAME}. <<<")
                except Exception as e:
                    print(f"Error installing {app} on {os_type.name}: {e}")
        else:
            try:
                app_key = selection.lower().replace(' ', '-')
                installer = installer_objects.get(app_key, {}).get(os_key)
                if installer:
                    if installer.is_client_installed():
                        print(f"{selection} is already installed, skipping installation. Please uninstall it first.")
                        return
                    print(f"Running installation for {selection} on {os_type.name}")
                    installer.run_client_installation()
                    print(f"Installation for {selection} on {os_type.name} completed")
                    print(f" >>> NOTE: In order for the installation to take effect, restart {installer.APP_NAME}. <<<")
                else:
                    print(f"No installer available for {selection} on {os_type.name}")
            except Exception as e:
                print(f"Error installing {selection} on {os_type.name}: {e}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


