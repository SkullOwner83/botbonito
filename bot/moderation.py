import os
import re
from typing import List, Optional
from twitchio.ext import commands
from twitchio.ext.commands import Context
from modules.file import File
from modules.api import Api
from myapp import MyApp
from models.protection import Protection

class Moderation():
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        MyApp.bind_commands(self)
        self.moderation_config = File.open(os.path.join(MyApp.config_path, 'moderation.json'))  
        self.protection = { name: Protection(**data) for name, data in self.moderation_config.get("protection", {}).items() }
        self.banned_words = { name: Protection(**data) for name, data in self.moderation_config.get("banned_words", {}).items() }
        self.repeated_messages = self.protection.get('repeated_messages')
        self.links_protection = self.protection.get('links')

        self.user_messages = {}
        self.user_strikes = {
            "links": {},
            "repeated_messages": {},
            "banned_words": {}
        }

    async def message_filter(self, ctx: Context) -> None:
        message = ctx.message
        user = message.author.name
        penalty = None

        # Save the user messages and check if it is a repeated message to detect spam
        if self.repeated_messages.enable:
            if self.user_messages.get(user) and self.user_messages[user] == message.content:
                self.user_strikes['repeated_messages'][user] = self.user_strikes['repeated_messages'].get(user, 0) + 1

            self.user_messages[user] = message.content

            if self.user_strikes['repeated_messages'].get(user, 0) >= strikes:
                penalty = self.repeated_messages

        # Check if the links protection is enable to delete the message if it contains a link
        if self.links_protection.enable:
            strikes = self.links_protection.strikes

            for word in message.content.split():
                if re.search(MyApp.link_pattern, word):
                    self.user_strikes['links'][user] = self.user_strikes['links'].get(user, 0) + 1
                    penalty = self.links_protection
                    break

        # Check if the group is enable and is not a excluded user for each group
        for group in self.banned_words.values():
            if group.enable:
                target_words = group.words
                strikes = group.strikes

                # Check if the message matches the banned words and apply the penalty
                if any(word in message.content for word in target_words):
                    self.user_strikes['banned_words'][user] = self.user_strikes['banned_words'].get(user, 0) + 1
                    penalty = group

        # Check if the user has an exception or not to aply the penalty
        if penalty and not self.bot.level_check(ctx, penalty.exclude):
            await penalty.apply_penalty(ctx, self.bot)

        # Check if the user has an exception or not to aply the penalty
        # if not self.bot.level_check(ctx, exclude) and penalty != 'none':
        #     if penalty != 'ban_user' and strikes > 0:
        #         for filter_strikes in self.user_strikes.values():
        #             if filter_strikes.get(user, 0) >= strikes:
        #                 penalty = 'ban_user'

    # Remove strikes from the specified user
    @MyApp.register_command("strikes")
    async def remove_strikes(self, ctx: Context, user_target: str = None) -> None:
        if await self.bot.check_command_access(ctx, "strikes") and user_target:
            for filter_strikes in self.user_strikes.values():
                if user_target in filter_strikes: 
                    filter_strikes[user_target] = 0