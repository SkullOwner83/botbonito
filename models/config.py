import os
from utilities.file import File
from models.commands import CommandConfig
from myapp import MyApp

from threading import Lock

class ConfigManager():
    _instance = None
    _lock = Lock()

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.__commands_config = File.open(os.path.join(MyApp.config_path, "commands.json"))

            self.default_commands = { 
                name: CommandConfig(**data) 
                for name, data in self.__commands_config.get("default_commands", {}).items() 
            }

            self.custom_commands = { 
                name: CommandConfig(**data) 
                for name, data in self.__commands_config.get("custom_commands", {}).items() 
            }

            self.custom_alias = { 
                alias: key 
                for key, value in self.custom_commands.items()
                for alias in value.alias }
            
    def save_commands(self) -> None:
        self.dictionary = {
                "default_commands": {
                    name: data.__dict__
                    for name, data in self.default_commands.items()
                },

                "custom_commands": {
                    name: data.__dict__
                    for name, data in self.custom_commands.items()
                }
        }

        File.save(os.path.join(MyApp.config_path, "commands.json"), self.dictionary)
            
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        
        return cls._instance