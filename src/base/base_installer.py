import time
import os
from abc import ABC, abstractmethod
from typing import Dict, Any
from .auto_run_enabler import AutoRunEnabler
from .config_creator import ConfigCreator
from src.consts import PlatformName, AppName, DOWNLOAD_URLS, APPLICATION_DIR_NAME, APPLICATION_NAME, UNINSTALL_FOLDERS
from pathlib import Path
from src.utils.downloader import download_file
import subprocess
from src.utils.logger import get_logger
import shutil

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
        

    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def kill_process(self) -> bool:
        pass

    def uninstall_application(self) -> bool:
        try:
            # install the application
            logger.info(f"Uninstalling application: {APPLICATION_NAME}")
            subprocess.run(["npm", "uninstall", "-g", APPLICATION_NAME])

            # check if the application is installed
            return not self.is_application_installed()
        except Exception as e:
            logger.error(f"Error uninstalling {APPLICATION_NAME}: {e}")
            return False

    def download_application(self) -> str:
        try:
            logger.debug(f"Starting download of application - APP_NAME: {self.APP_NAME}, PLATFORM_NAME: {self.PLATFORM_NAME}")
            download_url = DOWNLOAD_URLS[self.APP_NAME][self.PLATFORM_NAME]
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

    def install_application(self, download_file_path: str) -> bool:
        try:
            # install the application
            logger.info(f"Installing application from: {download_file_path}")
            result = subprocess.run(["npm", "install", "-g", download_file_path], capture_output=True, text=True)
            logger.debug(f"Installation result: {result.returncode}")
            logger.debug(f"Installation stdout: {result.stdout}")
            logger.debug(f"Installation stderr: {result.stderr}")

            # check if the application is installed
            is_installed = self.is_application_installed()
            logger.debug(f"Application is installed: {is_installed}")
            return is_installed
        except Exception as e:
            logger.error(f"Error installing {download_file_path}: {e}")
            logger.exception("Exception details:")
            return False

    def is_application_installed(self) -> bool:
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

    def run_installation(self) -> bool:
        logger.info(f"Starting installation for {self.APP_NAME} on {self.PLATFORM_NAME}")

        # validate the application
        if not self.validate():
            logger.error("Validation failed. Cannot proceed with installation.")
            raise ValueError("Validation failed. Cannot proceed with installation.")
        
        # DO THIS ONE TIME FOR ALL APPLICATIONS (SINCE ALL USES THE SAME PACKAGE)
        # TODO: REFACTOR THIS TO BE A SINGLE INSTALLATION FOR ALL APPLICATIONS
        if not self.is_application_installed():
            # download the application
            download_file_path = self.download_application()
            if not download_file_path:
                logger.error("Download failed. Cannot proceed with installation.")
                raise ValueError("Download failed. Cannot proceed with installation.")

            # install the application
            if not self.install_application(download_file_path):
                logger.error("Installation failed. Cannot proceed with installation.")
                raise ValueError("Installation failed. Cannot proceed with installation.")

        # kill the process to make sure it's not running
        if not self.kill_process():
            logger.error("Could not kill the process. Cannot proceed with installation.")
            raise ValueError("Could not kill the process. Cannot proceed with installation.")
        
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
    
    def run_uninstallation(self) -> bool:
        logger.info(f"Starting uninstallation for {self.APP_NAME} on {self.PLATFORM_NAME}")
        if not self.kill_process():
            logger.error("Could not kill the process. Cannot proceed with uninstallation.")
            raise ValueError("Could not kill the process. Cannot proceed with uninstallation.")
        
        # disable auto-run to make our mcp server autostart in the target application
        logger.info("Disabling auto-run...")
        self.auto_run_enabler.disable_auto_run()
        time.sleep(0.5)

        # restore the config
        logger.info("Restoring configuration...")
        self.config_creator.restore_config()
        time.sleep(0.5)
        
        # uninstall the application
        if self.is_application_installed():
            logger.info("Uninstalling application...")
            self.uninstall_application()
        
        logger.info("Uninstallation completed successfully")
        return True

    def remove_installation_folders(self) -> bool:
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
