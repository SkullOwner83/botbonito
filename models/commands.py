from typing import List, Optional

class CommandConfig:
    def __init__(
        self,
        name: str,
        enable: bool = True,
        alias: Optional[List[str]] = None,
        cooldown: Optional[int] = 0,
        max_length: Optional[int] = 0,
        user_level: Optional[str] = 'everyone',
        response: Optional[str] = None,
        response_type: Optional[str] = 'say'
    ):

        self.name = name
        self.enable = enable
        self.alias = alias or []
        self.cooldown = cooldown
        self.max_length = max_length
        self.user_level = user_level
        self.response = response
        self.response_type = response_type

    def __repr__(self):
        return f'<Command "{self.name}": enabled="{self.enable}">'