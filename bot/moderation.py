import os
import re
from twitchio.ext import commands
from twitchio.ext.commands import Context, Cog
from modules.file import File
from myapp import MyApp
from models.protection import Protection

class Moderation(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        MyApp.bind_commands(self)
        self.moderation_config = File.open(os.path.join(MyApp.config_path, 'moderation.json'))  
        self.protection = { name: Protection(**data) for name, data in self.moderation_config.get("protection", {}).items() }
        self.banned_words = { name: Protection(**data) for name, data in self.moderation_config.get("banned_words", {}).items() }
        self.repeated_messages = self.protection.get('repeated_messages')
        self.long_messages = self.protection.get('long_messages')
        self.links_protection = self.protection.get('links')

        self.user_messages: dict[str, str] = {}
        self.user_strikes: dict[str, dict] = {
            "links": {},
            "repeated_messages": {},
            "long_message": {},
            "banned_words": {}
        }

    # Remove strikes from the specified user
    @MyApp.register_command("strikes")
    async def remove_strikes(self, ctx: Context, user: str = None) -> None:
        if await self.bot.check_command_access(ctx, "strikes") and user:
            for filter_strikes in self.user_strikes.values():
                if user in filter_strikes: 
                    filter_strikes[user] = 0

    async def message_filter(self, ctx: Context) -> None:
        if not self.bot.level_check(ctx, 'broadcaster'):
            await self.__spam_filter(ctx)
            await self.__links_filter(ctx)
            await self.__words_filter(ctx)
            await self.__long_message_filter(ctx)

    # Save the user messages and check if it is a repeated message to detect spam
    async def __spam_filter(self, ctx: Context) -> None:
        message = ctx.message
        user = message.author.name

        if self.repeated_messages.enable:
            if self.user_messages.get(user) and self.user_messages[user] == message.content:
                self.user_strikes['repeated_messages'][user] = self.user_strikes['repeated_messages'].get(user, 0) + 1

            self.user_messages[user] = message.content

            if self.user_strikes['repeated_messages'].get(user, 0) >= self.repeated_messages.strikes:
                await self.repeated_messages.apply_penalty(ctx, self)

    # Check if the links protection is enable to delete the message if it contains a link
    async def __links_filter(self, ctx: Context) -> None:
        message = ctx.message
        user = message.author.name

        if self.links_protection.enable:
            for word in message.content.split():
                if re.search(MyApp.link_pattern, word):
                    self.user_strikes['links'][user] = self.user_strikes['links'].get(user, 0) + 1
                    await self.links_protection.apply_penalty(ctx, self)
                    break

    # Check if the message lenght is greater than the maximum allowed
    async def __long_message_filter(self, ctx: Context):
        message = ctx.message
        user = message.author.name

        if self.long_messages.enable:
            if len(message.content) > self.long_messages.max_length:
                self.user_strikes['long_message'][user] = self.user_strikes['long_message'].get(user, 0) + 1
                await self.long_messages.apply_penalty(ctx, self)

    # Check if the group is enable and is not a excluded user for each group
    async def __words_filter(self, ctx: Context) -> None:
        message = ctx.message
        user = message.author.name

        for group in self.banned_words.values():
            if group.enable:
                if any(word in message.content for word in group.words):
                    self.user_strikes['banned_words'][user] = self.user_strikes['banned_words'].get(user, 0) + 1
                    await group.apply_penalty(ctx, self)
