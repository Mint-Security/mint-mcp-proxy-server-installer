APPLICATION_DIR_NAME = ".mint/mcp_proxy/"
APPLICATION_NAME = "mint-mcp-proxy-server"

# Folders to remove during uninstallation
UNINSTALL_FOLDERS = [
   APPLICATION_DIR_NAME
]

class PlatformName:
    MAC = "mac"
    LINUX = "linux"
    WINDOWS = "windows"

class AppName:
    CURSOR = "cursor"
    CLAUDE_CODE = "claude-code"
    CLAUDE_DESKTOP = "claude-desktop"
    WINDSURF = "windsurf"

PACKAGE_VERSION = "1.0.0"
PACKAGE_NAME = f"mint-mcp-proxy-server-{PACKAGE_VERSION}.tgz"

DOWNLOAD_URLS = {
    PlatformName.MAC: f"https://wsrzmzgrflfrgovxedjl.supabase.co/storage/v1/object/public/storage/{PACKAGE_NAME}",
    PlatformName.LINUX: "UNSUPPORTED",
    PlatformName.WINDOWS: "UNSUPPORTED"
}
