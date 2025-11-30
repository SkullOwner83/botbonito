from dataclasses import dataclass, field
from typing import List
from utilities import *

@dataclass
class AppConfig:
    name: str = 'BotBonito'
    prefix: str = '!'
    channels: List[str] = field(default_factory=list)
    redirect_uri: str = ''
    client_id: str = ''
    client_secret: str = ''
    theme: str = 'light'
    language: str = 'español'

    always_ontop: bool = False
    start_with_windows: bool = False
    start_in_background: bool = False
    run_bot_mode = None # (on startup, on stream online, manually)

    bot_language: str = 'español'
    help_word: str = 'help'
    enable_word: str = 'enable'
    disable_word: str = 'disable'
    start_word: str = 'start'
    finish_word: str = 'finish'
    
    announce_speaker: bool = True
    speak_cooldown: int = 3
    speak_volume: float = 1
    sounds_volume: float = 1
    social_media: dict[str, str] = field(default_factory=lambda: {
        'facebook': '',
        'twitter': '',
        'discord': '',
        'instagram': '',
        'tiktok': ''
    })

    # Open the stored configuration file
    def open(self, path: str) -> None:
        stored_config = File.open(path)

        if stored_config:
            for key, value in stored_config.items():
                if hasattr(self, key) and not callable(getattr(self, key)):
                    setattr(self, key, value)
    
    # Save the configuration in the specified path
    def save(self, path: str) -> None:
        File.save(path, self.__dict__)

    # Set the default values for the configuration
    def restore_defaults(self):
        new_instance = AppConfig()
        
        for field in self.__dataclass_fields__:
            setattr(self, field, getattr(new_instance, field))