from enum import Enum

class UserLevel(str, Enum):
    NO_ONE = 'no one'
    EVERYONE = 'everyone'
    FOLLOWER = 'follower'
    VIP = 'vip'
    MODERATOR = 'moderator'
    SUBSCRIBER = 'subscriber'
    BROADCASTER = 'broadcaster'

class AccountType(str, Enum):
    BOT = 'bot'
    USER = 'user'

class ResponseType(str, Enum):
    SAY = 'say'
    REPLY = 'reply'
    MENTION = 'mention'

class PenaltyType(str, Enum):
    DELETE_MESSAGE = 'delete message'
    TIME_OUT = 'time out'
    BAN_USER = 'ban user'