from dataclasses import dataclass, field
from typing import List, Optional
from utilities.enums import ResponseType, UserLevel

@dataclass
class CommandConfig:
    name: str
    description: str = ''
    enable: bool = True
    alias: List[str] = field(default_factory=list)
    cooldown: int = 0
    max_length: int = 0
    user_level: str = UserLevel.EVERYONE.value
    response: str = ''
    response_type: str = ResponseType.SAY.value

    def __repr__(self):
        return f'<Command "{self.name}": enabled="{self.enable}", id="{id(self)}">'