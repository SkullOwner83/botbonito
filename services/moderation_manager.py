import os
from threading import Lock
from models.protection import Protection
from config.moderation import get_protections
from utilities import *
from myapp import MyApp

class ModerationManager():
    def __init__(self):
        self._lock = Lock()
        self.protections: dict[str, Protection] = {}
        self.banned_words: dict[str, Protection] = {}
        self.load_protections()

    # Read the stored file and load them into the dictionary of protections
    def load_protections(self) -> None:
        with self._lock:
            self.protections = get_protections()

            try:
                stored_config = File.open(MyApp.moderation_path)
            except FileNotFoundError:
                stored_config = {}
                File.save(MyApp.moderation_path, stored_config)

            if stored_config:
                loaded_protections: dict = stored_config.get('protection', {})

                for name, data in loaded_protections.items():
                    protection = self.protections.get(name)

                    for attr, val in data.items():
                        if hasattr(protection, attr):
                            setattr(protection, attr, val)

                self.banned_words = { 
                    name: Protection(**data) 
                    for name, data in stored_config.get('banned_words', {}).items() 
                }

    # Convert the commands to a dictionary and save them to the file
    def save_protections(self) -> None:
        with self._lock:
            dictionary = {
                    'protection': {
                        name: data.__dict__
                        for name, data in self.protections.items()
                    },

                    'banned_words': {
                        name: data.__dict__
                        for name, data in self.banned_words.items()
                    }
            }

            File.save(os.path.join(MyApp.moderation_path), dictionary)