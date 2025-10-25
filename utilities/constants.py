
class Constants():
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
        raise TypeError("The Constants class cannot be instantiated.")