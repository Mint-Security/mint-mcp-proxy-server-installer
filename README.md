# Mint MCP Proxy Server Installer

A utility for installing and configuring the Mint Security MCP proxy server.

## Overview

This tool simplifies the process of integrating the Mint MCP (Model Context Protocol) Proxy Server. It handles:

- Installation of required dependencies
- Configuration of relevant client to use the Mint MCP proxy
- Enabling secure communication between the client and Mint Security services
- Uninstallation process

## Supported clients:

- Claude Desktop

## Installation

### Prerequisites

- Python 3.9+
- Node.js
- Claude Desktop installed

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/your-org/mint-mcp-proxy-server-installer.git
   cd mint-mcp-proxy-server-installer
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the installer with:

```
python main.py
```

For debugging information:

```
python main.py -d
```

To revert configuration changes (Override the current configuration with a backup file):

```
python main.py --revert
```

To uninstall:

```
python main.py --uninstall
```
