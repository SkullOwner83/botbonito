from typing import Optional, List

from twitchio.ext.commands import Bot, Cog, Context
from utilities.api import Api
from utilities.enums import PenaltyType

class Protection:
    def __init__(self,
        name: str = None,
        description: str = None,
        enable: bool = True,
        penalty: Optional[str] = None,
        announce_penalty: Optional[bool] = True,
        reason: Optional[str] = None,
        exclude: Optional[str] = 'no_one',
        words: Optional[List[str]] = None,
        threshold: Optional[float] = 0,
        duration: Optional[int] = 0,
        strikes: Optional[int] = 0
    ):

        self.name = name
        self.description = description
        self.enable = enable
        self.penalty = penalty
        self.announce_penalty = announce_penalty
        self.reason = reason
        self.exclude = exclude
        self.words = words
        self.threshold = threshold
        self.duration = duration
        self.strikes = strikes
    
    async def apply_penalty(self, ctx: Context, cog: Cog) -> None:
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
            if self.penalty != PenaltyType.BAN_USER and self.strikes > 0:
                for filter_strikes in cog.user_strikes.values():
                    if filter_strikes.get(user, 0) >= self.strikes:
                        penalty = PenaltyType.BAN_USER

            match(penalty):
                case PenaltyType.DELETE_MESSAGE: api.delete_message(broadcaster_id, moderator_id, message_id)
                case PenaltyType.TIME_OUT: api.set_timeout(broadcaster_id, moderator_id, user_id, self.duration, self.reason)
                case PenaltyType.BAN_USER: api.set_ban(broadcaster_id, moderator_id, user_id, self.reason)
            
            if self.announce_penalty: 
                await ctx.send(self.reason)

    def __repr__(self):
        return f'<Protection "{self.name}": penalty="{self.penalty}" enable="{self.enable}">'