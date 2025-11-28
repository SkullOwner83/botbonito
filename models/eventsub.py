from dataclasses import dataclass, field
from typing import List

@dataclass
class EventSub:
    name: str = ''
    description: str = ''
    enable: bool = True
    response: str = ''
    announce_response: bool = False
    params: List[str] = field(default_factory=list)
    effect = None