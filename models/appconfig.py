from dataclasses import dataclass, fields
from typing import List, Optional

@dataclass
class AppConfig:
    name: Optional[str] = 'BotBonito',
    prefix: Optional[str] = '!',
    redirect_uri: Optional[str] = 'https://localhost:300',
    help_word: Optional[str] = 'help',
    enable_word: Optional[str] = 'enable',
    disable_word: Optional[str] = 'disable',
    start_word: Optional[str] = 'start',
    finish_word: Optional[str] = 'finish',

    @classmethod
    def open(cls, data: dict):
        class_properties = {f.name for f in fields(cls)} 
        filtered_data = {property: value for property, value in data.items() if property in class_properties}
        return cls(**filtered_data)