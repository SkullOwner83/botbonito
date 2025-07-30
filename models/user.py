from dataclasses import dataclass
from typing import Optional
from models.credentials import Credentials

@dataclass
class User:
    id: int
    email: str
    username: str
    display_name: str
    profile_image: str
    broadcaster_type: str
    credentials: Credentials
    account_type: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = None