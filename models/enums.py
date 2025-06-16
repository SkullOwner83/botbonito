from enum import Enum

class UserLevel(str, Enum):
    EVERYONE = 'everyone'
    FOLLOWER = 'follower'
    MODERATOR = 'moderator'
    SUSCRIPTOR = 'suscriptor'
    BROADCASTER = 'broadcaster'
    VIP = 'vip'