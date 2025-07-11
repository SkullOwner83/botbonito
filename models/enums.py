from enum import Enum

class UserLevel(str, Enum):
    NO_ONE = 'no_one'
    EVERYONE = 'everyone'
    FOLLOWER = 'follower'
    MODERATOR = 'moderator'
    SUBSCRIBER = 'subscriber'
    BROADCASTER = 'broadcaster'
    VIP = 'vip'

class AccountType(str, Enum):
    BOT = 'bot'
    USER = 'user'

class ResponseType(str, Enum):
    SAY = 'say'
    REPLY = 'reply'
    MENTION = 'mention'

class PenaltyType(str, Enum):
    DELETE_MESSAGE = 'delete_message'
    TIME_OUT = 'time_out'
    BAN_USER = 'ban_user'
