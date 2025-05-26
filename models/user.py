from typing import Optional
from models.credentials import Credentials

class User:
    def __init__(
        self,
        id: int,
        name: str,
        email: str,
        profile_image: str,
        broadcaster_type: str,
        credentials: Credentials,
        description: Optional[str] = '',
        created_at: Optional[str] = ''
    ):
        self.id = id
        self.name = name
        self.email = email
        self.profile_image = profile_image
        self.broadcaster_type = broadcaster_type
        self.credentials = credentials
        self.description = description
        self.created_at = created_at