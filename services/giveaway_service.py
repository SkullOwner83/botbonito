from typing import List

class GiveawayService():
    def __init__(self):
        self.giveaway_active = False
        self.participants: List[str] = []

    def add_user(self, user: str):
        self.participants.append(user)