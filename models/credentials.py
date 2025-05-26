from typing import Optional

class Credentials:
    def __init__(
        self,
        access_token: str,
        refresh_token: str,
        client_id: Optional[str] = "",
        client_secret: Optional[str] = "",
    ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret