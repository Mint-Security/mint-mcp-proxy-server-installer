import os
import sqlite3
import json
from src.base.auto_run_enabler import AutoRunEnabler
from typing import Dict, Any
class CursorMacYOLOEnabler(AutoRunEnabler):

    DATABASE_FILE_PATH = os.path.join(os.path.expanduser("~/Library/Application Support/Cursor/User/globalStorage"), "state.vscdb")
    STORAGE_KEY = 'src.vs.platform.reactivestorage.browser.reactiveStorageServiceImpl.persistentStorage.applicationUser'

    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        
    def disable_auto_run(self) -> bool:
        # we don't know what was there before, so we just return true
        return True

    def enable_auto_run(self) -> bool:
        try:
            if not os.path.exists(self.DATABASE_FILE_PATH):
                raise FileNotFoundError(f"Database file not found at {self.DATABASE_FILE_PATH}")
            conn = sqlite3.connect(self.DATABASE_FILE_PATH)
            cursor = conn.cursor()
            
            # Read current value
            cursor.execute("SELECT value FROM ItemTable WHERE key = ?", (self.STORAGE_KEY,))
            row = cursor.fetchone()
            
            if not row:
                print("No row found for key:", self.STORAGE_KEY)
                return False
                
            # Parse the JSON value
            settings = json.loads(row[0])
            
            # Ensure composerState exists
            if 'composerState' not in settings:
                settings['composerState'] = {}
            
            # Update the autoRun setting for agent mode
            if 'modes4' not in settings['composerState']:
                settings['composerState']['modes4'] = []
            
            # Find and update the agent mode
            agent_mode_found = False
            for mode in settings['composerState']['modes4']:
                if mode.get('id') == 'agent':
                    agent_mode_found = True
                    mode['autoRun'] = True
                    break
            
            if not agent_mode_found:
                # Add agent mode if it doesn't exist
                settings['composerState']['modes4'].append({
                    'id': 'agent',
                    'autoRun': True
                })
            
            # Convert back to JSON string
            updated_value = json.dumps(settings)
            
            # Insert or replace the value
            cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", 
                         (self.STORAGE_KEY, updated_value))
            
            conn.commit()
            conn.close()
            
            return True
            
        except sqlite3.Error as e:
            print(f"Error enabling auto run for Cursor: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return False
        except Exception as e:
            print(f"Error enabling auto run for Cursor: {e}")
            return False