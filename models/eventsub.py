from dataclasses import dataclass

@dataclass
class EventSub:
    name: str = ''
    description: str = ''
    enable: bool = True
    response: str = ''
    announce_response: bool = False
    effect = None