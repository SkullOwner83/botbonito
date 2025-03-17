from typing import Optional, List
from twitchio import Message
from twitchio.ext.commands import Bot
from modules.api import Api

class Protection:
    def __init__(self,
        name: str = None,
        enable: bool = False,
        penalty: Optional[str] = None,
        reason: Optional[str] = None,
        exclude: Optional[str] = 'no_one',
        words: Optional[List[str]] = None,
        duration: Optional[int] = 0,
        strikes: Optional[int] = 0
    ):

        self.name = name
        self.enable = enable
        self.penalty = penalty
        self.reason = reason
        self.exclude = exclude
        self.words = words
        self.duration = duration
        self.strikes = strikes

    def __repr__(self):
        return f'<Protection "{self.name}": penalty="{self.penalty}" enable="{self.enable}">'
    
    async def apply_penalty(self, ctx: Message, bot: Bot, penalty: Optional[str] = None) -> None:
        user = ctx.author.name
        message = ctx.message
        penalty = penalty or self.penalty
        api = Api(bot.token, bot.client_id)
        user_data = api.get_user(user)
        broadcaster_data = api.get_user(message.channel.name)
        moderator_data = api.get_user(bot.name)

        user_id = user_data['id']
        broadcaster_id = broadcaster_data['id']
        moderator_id = moderator_data['id']
        message_id = message.tags['id']

        match(penalty):
            case 'delete_message': 
                api.delete_message(broadcaster_id, moderator_id, message_id)
                if self.reason: await ctx.send(f"Se ha eliminado el mensaje de @{user}. {self.reason}")
            
            case 'timeout': api.set_timeout(broadcaster_id, moderator_id, user_id, self.duration, self.reason)
            case 'ban_user': api.set_ban(broadcaster_id, moderator_id, self.user_id, self.reason)