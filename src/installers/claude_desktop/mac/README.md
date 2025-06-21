# Claude Desktop Mac Installer

This module contains the installation tools for integrating the Mint MCP proxy server with Claude Desktop on macOS.

## Components

- `ClaudeDesktopMacInstaller`: Main installer class for Claude Desktop on macOS
- `ClaudeDesktopMacMCPConfigCreator`: Copy Claude Desktop's configuration for the Mint MCP Proxy to use and update the original configuration file to include Mint MCP Proxy
- `ClaudeDesktopMacYOLOEnabler`: Enables auto-run capabilities for the proxy tool by updating permissions

## Requirements

- macOS operating system
- Claude Desktop installed in /Applications/Claude.app

## Implementation Details

The installer targets Claude Desktop configuration files at:
- `~/Library/Application Support/Claude/claude_desktop_config.json` for MCP configuration