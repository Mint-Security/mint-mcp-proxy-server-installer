APPLICATION_DIR_NAME = ".mint"
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
    # CURSOR = "cursor"
    CLAUDE_CODE = "claude-code"
    CLAUDE_DESKTOP = "claude-desktop"
    # WINDSURF = "windsurf"

DOWNLOAD_URLS = {
    # AppName.CURSOR: {
    #     PlatformName.MAC: "https://wsrzmzgrflfrgovxedjl.supabase.co/storage/v1/object/public/storage//default.zip",
    #     PlatformName.LINUX: "cursor-linux.zip",
    #     PlatformName.WINDOWS: "cursor-windows.zip"
    # },
    AppName.CLAUDE_CODE: {
        PlatformName.MAC: "https://wsrzmzgrflfrgovxedjl.supabase.co/storage/v1/object/public/storage//mint-mcp-proxy-server-0.1.0.tgz",
        PlatformName.LINUX: "claude-code-linux.zip",
        PlatformName.WINDOWS: "claude-code-windows.zip"
    },
    AppName.CLAUDE_DESKTOP: {
        PlatformName.MAC: "https://wsrzmzgrflfrgovxedjl.supabase.co/storage/v1/object/public/storage//mint-mcp-proxy-server-0.1.0.tgz",
        PlatformName.LINUX: "mint-mcp-proxy-server-0.1.0.tgz",
        PlatformName.WINDOWS: "mint-mcp-proxy-server-0.1.0.tgz"
    },
    # AppName.WINDSURF: {
    #     PlatformName.MAC: "https://wsrzmzgrflfrgovxedjl.supabase.co/storage/v1/object/public/storage//default.zip",
    #     PlatformName.LINUX: "windsurf-linux.zip",
    #     PlatformName.WINDOWS: "windsurf-windows.zip"
    # }
}
