from dataclasses import dataclass
from typing import Optional

@dataclass
class Credentials:
    access_token: str
    refresh_token: str
    client_id: str = ''
    client_secret: str = ''