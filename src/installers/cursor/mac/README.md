### Cursor Installer - MAC

to install the mint security mcp server on Cursor in Mac the following things must be updated:
- Update the system prompt in the state.vscdb file
- Update the configuration of autoRun (yolo mode) in state.vscdb file
- Update the mcp configuration json file according to the installation path


~/Library/Application Support/Cursor/User/globalStorage/state.vscdb

System Prompt -> itemTable.aicontext.personalContext
Yolo Mode -> src.vs.platform.reactivestorage.browser.reactiveStorageServiceImpl.persistentStorage.applicationUser -> modes4 -> autoRun -> true/false

~/.cursor/mcp.json