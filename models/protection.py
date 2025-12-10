from dataclasses import dataclass
from typing import List
from twitchio.ext.commands import Cog, Context
from utilities.api import Api
from utilities.enums import PenaltyType, UserLevel

@dataclass
class Protection:
    name: str = None
    description: str = ''
    enable: bool = True
    penalty: str = ''
    announce_penalty: bool = True
    mark_strike: bool = True
    reason: str = ''
    exclude: str = UserLevel.NO_ONE
    words: List[str] = None
    threshold: float = 0
    duration: int = 0
    
    async def apply_penalty(self, ctx: Context, cog: Cog, moderator: str) -> None:
        user = ctx.author.name
        message = ctx.message
        penalty = self.penalty
        MAX_STRIKES = 3

        if not cog.bot.level_check(ctx, self.exclude):
            api = Api(cog.bot.token, cog.bot.client_id)
            user_id = (api.get_user(user) or {}).get('id')
            broadcaster_id = (api.get_user(message.channel.name) or {}).get('id')
            moderator_id = (api.get_user(moderator) or {}).get('id')
            message_id = message.tags.get('id')

            # Change the penalty if the user exceed the allowed strikes
            if self.penalty != PenaltyType.BAN_USER and MAX_STRIKES > 0:
                if cog.user_strikes.get(user, 0) >= MAX_STRIKES:
                    penalty = PenaltyType.BAN_USER

            match(penalty):
                case PenaltyType.DELETE_MESSAGE: api.delete_message(broadcaster_id, moderator_id, message_id)
                case PenaltyType.TIME_OUT: api.set_timeout(broadcaster_id, moderator_id, user_id, self.duration, self.reason)
                case PenaltyType.BAN_USER: api.set_ban(broadcaster_id, moderator_id, user_id, self.reason)
            
            if self.announce_penalty: await ctx.send(self.reason)

    def __repr__(self):
        return f'<Protection "{self.name}": penalty="{self.penalty}" enable="{self.enable}" id={id(self)}>'