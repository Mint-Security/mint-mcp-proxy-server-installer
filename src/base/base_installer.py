import time
import os
import json
from abc import ABC 
from typing import Dict, Any
from .auto_run_enabler import AutoRunEnabler
from .config_creator import ConfigCreator
from src.consts import PlatformName, AppName, APPLICATION_DIR_NAME, APPLICATION_NAME, UNINSTALL_FOLDERS
from pathlib import Path
from src.utils.downloader import download_file
import subprocess
from src.utils.logger import get_logger
import shutil
from src.utils.os_utils import get_current_os, OperatingSystem

# Create a logger for this module
logger = get_logger(__name__)

class BaseInstaller(ABC):
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.auto_run_enabler = None
        self.config_creator = None

        logger.debug(f"Initialized BaseInstaller with empty config")

    PLATFORM_NAME: PlatformName
    APP_NAME: AppName
    CONFIG_FILE_PATH: str

    def set_objects(self, auto_run_enabler: AutoRunEnabler, config_creator: ConfigCreator):
        try:
            logger.debug(f"Setting objects in BaseInstaller - auto_run_enabler: {auto_run_enabler}, config_creator: {config_creator}")
            self.auto_run_enabler = auto_run_enabler(self.config)
            logger.debug(f"Created auto_run_enabler instance: {self.auto_run_enabler}")
            self.config_creator = config_creator(self.config)
            logger.debug(f"Created config_creator instance: {self.config_creator}")
        except Exception as e:
            logger.error(f"Error setting objects: {e}")
            logger.exception("Exception details:")
        


    def validate(self) -> bool:
        vlaid_os = get_current_os() == OperatingSystem.MAC
        if not vlaid_os:
            print(f"the os is not valid expected {OperatingSystem.MAC} but got {get_current_os()}")
            return False
        return True

    @staticmethod
    def uninstall_application() -> bool:
        if BaseInstaller.is_application_installed():
            try:
                # install the application
                logger.info(f"Uninstalling application: {APPLICATION_NAME}")
                subprocess.run(["npm", "uninstall", "-g", APPLICATION_NAME])

                # check if the application is installed
                return not BaseInstaller.is_application_installed()
            except Exception as e:
                logger.error(f"Error uninstalling {APPLICATION_NAME}: {e}")
                return False


    @staticmethod
    def download_application(download_url: str) -> str:
        try:
            logger.debug(f"Starting download application")
            logger.debug(f"Download URL: {download_url}")
            application_name = download_url.split("/")[-1]
            logger.debug(f"Application name from URL: {application_name}")
            download_dir = os.path.join(str(Path.home()), APPLICATION_DIR_NAME)
            logger.debug(f"Download directory: {download_dir}")

            if not os.path.exists(download_dir):
                logger.debug(f"Creating download directory: {download_dir}")
                os.makedirs(download_dir, exist_ok=True)
            
            # download the application
            download_file_path = os.path.join(download_dir, application_name)
            logger.info(f"Downloading application to: {download_file_path}")
            if not download_file(download_url, download_file_path):
                logger.error("Download failed")
                return ""
            logger.info(f"Download successful")

            return download_file_path
                
        except Exception as e:
            logger.error(f"Error downloading application: {e}")
            logger.exception("Exception details:")
            return ""

    @staticmethod
    def install_application(file_path: str) -> bool:
        try:
            if not os.path.exists(file_path):
                logger.error(f"File path does not exist: {file_path}")
                return False
            
            # install the application
            logger.info(f"Installing application from: {file_path}")
            result = subprocess.run(["npm", "install", "-g", file_path], capture_output=True, text=True)
            logger.debug(f"Installation result: {result.returncode}")
            logger.debug(f"Installation stdout: {result.stdout}")
            logger.debug(f"Installation stderr: {result.stderr}")

            # check if the application is installed
            is_installed = BaseInstaller.is_application_installed()
            logger.debug(f"Application is installed: {is_installed}")
            return is_installed
        except Exception as e:
            logger.error(f"Error installing {file_path}: {e}")
            logger.exception("Exception details:")
            return False

    @staticmethod
    def is_application_installed() -> bool:
        try:
            logger.debug(f"Checking if {APPLICATION_NAME} is installed")
            whereis_result = subprocess.run(["whereis", APPLICATION_NAME], capture_output=True, text=True)
            # whereis returns app_name: /path/to/app if found
            logger.debug(f"whereis result: {whereis_result.stdout}")
            if ":" in whereis_result.stdout and len(whereis_result.stdout.split(":")[1].strip()) > 0:
                logger.debug(f"{APPLICATION_NAME} is installed")
                return True
            else:
                logger.debug(f"{APPLICATION_NAME} is not installed")
                return False
        except Exception as e:
            logger.error(f"Error checking if {APPLICATION_NAME} is installed: {e}")
            logger.exception("Exception details:")
            return False

    def is_client_installed(self) -> bool:
        #Check is mint-mcp-proxy-server is installed in config file
        config_file_path = os.path.expanduser(self.CONFIG_FILE_PATH)
        if not os.path.exists(config_file_path):
            logger.debug(f"{self.APP_NAME} is not installed")
            return False
        
        #Check if the config file is valid
        with open(config_file_path, "r") as f:
            config = json.load(f)
        
        # Check if our main proxy exists in mcpServers
        if APPLICATION_NAME in config.get("mcpServers", {}):
            logger.debug(f"{self.APP_NAME} is installed")
            return True
        
        logger.debug(f"{self.APP_NAME} is not installed")
        return False

    def run_client_installation(self) -> bool:
        logger.info(f"Starting installation for {self.APP_NAME} on {self.PLATFORM_NAME}")

        # validate the application
        if not self.validate():
            logger.error("Validation failed. Cannot proceed with installation.")
            raise ValueError("Validation failed. Cannot proceed with installation.")
        
        # update the config json of the target application
        logger.info("Creating configuration...")
        try:
            config_result = self.config_creator.update_config()
            logger.debug(f"Configuration creation result: {config_result}")
        except Exception as e:
            logger.error(f"Error creating configuration: {e}")
            logger.exception("Exception details:")
            raise
        
        time.sleep(0.5)
        
        # enable auto-run to make our mcp server autostart in the target application
        logger.info("Enabling auto-run...")
        try:
            autorun_result = self.auto_run_enabler.enable_auto_run()
            logger.debug(f"Auto-run enabling result: {autorun_result}")
        except Exception as e:
            logger.error(f"Error enabling auto-run: {e}")
            logger.exception("Exception details:")
            raise
        
        time.sleep(0.5)
        logger.info("Installation completed successfully")
        return True
    
    def run_client_uninstallation(self) -> bool:
        logger.info(f"Starting uninstallation for {self.APP_NAME} on {self.PLATFORM_NAME}")
        
        # disable auto-run to make our mcp server autostart in the target application
        logger.info("Disabling auto-run...")
        self.auto_run_enabler.disable_auto_run()
        time.sleep(0.5)

        # restore the config
        logger.info("Restoring configuration...")
        self.config_creator.restore_config()
        time.sleep(0.5)
        
        logger.info("Uninstallation completed successfully")
        return True

    @staticmethod
    def remove_installation_folders() -> bool:
        logger.info("\nRemoving installation folders...")
        for folder in UNINSTALL_FOLDERS:
            try:
                # Expand the path to handle ~
                dir_path_to_remove = os.path.join(str(Path.home()), folder)
                if os.path.exists(dir_path_to_remove):
                    shutil.rmtree(dir_path_to_remove)
                    logger.info(f"Successfully removed {folder}")
                else:
                    logger.info(f"Folder {dir_path_to_remove} does not exist, skipping...")
            except Exception as e:
                logger.error(f"Error removing {dir_path_to_remove}: {e}")
                return False
        logger.info("Installation folders removed successfully")
        return True
