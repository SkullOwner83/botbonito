from typing import Optional, List
from twitchio import Message
from twitchio.ext.commands import Bot, Cog
from twitchio.ext import commands
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
    
    async def apply_penalty(self, ctx: Message, cog: Cog) -> None:
        user = ctx.author.name
        message = ctx.message
        penalty = self.penalty 

        if not cog.bot.level_check(ctx, self.exclude):
            api = Api(cog.bot.token, cog.bot.client_id)
            user_id = (api.get_user(user) or {}).get('id')
            broadcaster_id = (api.get_user(message.channel.name) or {}).get('id')
            moderator_id = (api.get_user(cog.bot.name) or {}).get('id')
            message_id = message.tags.get('id')

            # Change the penalty if the user exceed the allowed strikes
            if self.penalty != 'ban_user' and self.strikes > 0:
                for filter_strikes in cog.user_strikes.values():
                    if filter_strikes.get(user, 0) >= self.strikes:
                        penalty = 'ban_user'

            match(penalty):
                case 'delete_message': 
                    api.delete_message(broadcaster_id, moderator_id, message_id)
                    if self.reason: await ctx.send(f"Se ha eliminado el mensaje de @{user}. {self.reason}")
                
                case 'timeout': api.set_timeout(broadcaster_id, moderator_id, user_id, self.duration, self.reason)
                case 'ban_user': api.set_ban(broadcaster_id, moderator_id, user_id, self.reason)