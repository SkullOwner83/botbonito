from dataclasses import dataclass, field
from typing import Optional, List
from utilities import *

@dataclass
class AppConfig:
    name: Optional[str] = 'BotBonito'
    prefix: Optional[str] = '!'
    channels: Optional[List[str]] = field(default_factory=list)
    redirect_uri: Optional[str] = ''
    client_id: Optional[str] = ''
    client_secret: Optional[str] = ''
    theme: Optional[str] = 'light'
    language: Optional[str] = 'español'

    always_ontop: Optional[bool] = False
    start_with_windows: Optional[bool] = False
    start_in_background: Optional[bool] = False
    run_bot_mode = None # (on startup, on stream online, manually)

    bot_language: Optional[str] = 'español'
    help_word: Optional[str] = 'help'
    enable_word: Optional[str] = 'enable'
    disable_word: Optional[str] = 'disable'
    start_word: Optional[str] = 'start'
    finish_word: Optional[str] = 'finish'
    speak_volume: Optional[float] = 1
    sounds_volume: Optional[float] = 1
    social_media: Optional[dict[str, str]] = field(default_factory=lambda: {
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