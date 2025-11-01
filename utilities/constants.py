import flet as ft
from utilities.enums import UserLevel, PenaltyType

class Constants():
    PENALTY_ICONS = {
        PenaltyType.DELETE_MESSAGE: ft.Icons.MESSAGE_ROUNDED,
        PenaltyType.TIME_OUT: ft.Icons.WATCH_LATER_ROUNDED,
        PenaltyType.BAN_USER: ft.Icons.BLOCK_ROUNDED
    }

    USER_LEVEL_ICONS = {
        UserLevel.NO_ONE: 'user levels/everyone.png',
        UserLevel.EVERYONE: 'user levels/everyone.png',
        UserLevel.FOLLOWER: 'user levels/follower.png',
        UserLevel.MODERATOR: 'user levels/moderator.png',
        UserLevel.SUBSCRIBER: 'user levels/subscriber.png',
        UserLevel.BROADCASTER: 'user levels/broadcaster.png',
        UserLevel.VIP: 'user levels/vip.png',
    }

    BOT_SCOPES = [
        'chat:read',
        'user:read:subscriptions',
        'chat:edit',
        'moderator:read:followers',
        'moderator:manage:chat_messages',
        'moderator:manage:banned_users',
        'channel:read:goals',
        'user:read:email'
    ]

    USER_SCOPES = [
        'user:read:email',
        'channel:read:goals',
        'moderator:read:followers',
        'channel:read:subscriptions'
    ]

    def __new__(cls):
        raise TypeError('The Constants class cannot be instantiated.')