import os
from threading import Lock
from utilities.file import File
from models.commands import CommandConfig
from config.commands import get_default_commands
from myapp import MyApp

class CommandsManager():
    def __init__(self):
        self._lock = Lock()
        self.default_commands: dict[str, CommandConfig] = {}
        self.custom_commands: dict[str, CommandConfig] = {}
        self.load_commands()

        self.custom_alias = { 
            alias: key 
            for key, value in self.custom_commands.items()
            for alias in value.alias 
        }

    # Read the stored file and load them into the dictionary of commands
    def load_commands(self) -> None:
        with self._lock:
            commands_config: dict = File.open(os.path.join(MyApp.commands_path))
            self.default_commands = get_default_commands()

            if commands_config:
                loaded_default_commands: dict = commands_config.get('default_commands', {})

                for name, data in loaded_default_commands.items():
                    if name in self.default_commands:
                        command = self.default_commands[name]
                        
                        for attr, val in data.items():
                            setattr(command, attr, val)

                self.custom_commands = { 
                    name: CommandConfig(**data) 
                    for name, data in commands_config.get('custom_commands', {}).items() 
                }

    # Convert the commands to a dictionary and save them to the file
    def save_commands(self) -> None:
        with self._lock:
            dictionary = {
                    'default_commands': {
                        name: data.__dict__
                        for name, data in self.default_commands.items()
                    },

                    'custom_commands': {
                        name: data.__dict__
                        for name, data in self.custom_commands.items()
                    }
            }

            File.save(os.path.join(MyApp.config_path, 'commands.json'), dictionary)