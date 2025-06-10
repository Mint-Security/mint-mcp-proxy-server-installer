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

DOWNLOAD_URLS = {
    PlatformName.MAC: "https://wsrzmzgrflfrgovxedjl.supabase.co/storage/v1/object/public/storage//mint-mcp-proxy-server-0.1.0.tgz",
    PlatformName.LINUX: "UNSUPPORTED",
    PlatformName.WINDOWS: "UNSUPPORTED"
}
