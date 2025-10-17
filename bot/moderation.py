import os
import re
from twitchio.ext import commands
from twitchio.ext.commands import Context, Cog
from services.session_service import SessionService
from services.moderation_manager import ModerationManager
from services.service_locator import ServiceLocator
from utilities.enums import UserLevel
from myapp import MyApp
from models.protection import Protection

class Moderation(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        MyApp.bind_commands(self)

        moderation_manager: ModerationManager = ServiceLocator.get('moderation')
        self.session_service: SessionService = ServiceLocator.get('session')
        self.protections: dict[str, dict] = moderation_manager.protections
        self.banned_words: dict[str, dict] = moderation_manager.banned_words

        self.repeated_messages: Protection = self.protections.get('repeated_messages')
        self.long_messages: Protection = self.protections.get('long_messages')
        self.links_protection: Protection = self.protections.get('links')
        self.caps_protection: Protection = self.protections.get('excess_caps')
        self.symbols_protection: Protection = self.protections.get('excess_symbols')
        self.emotes_protection: Protection = self.protections.get('excess_emotes')

        self.user_messages: dict[str, str] = {}
        self.user_strikes: dict[str, dict] = {
            'links': {},
            'repeated_messages': {},
            'long_message': {},
            'banned_words': {},
            'excess_caps': {},
            'excess_symbols': {},
            'excess_emotes': {}
        }

    # Remove strikes from the specified user
    @MyApp.register_command("strikes")
    async def remove_strikes(self, ctx: Context, user: str = None) -> None:
        if await self.bot.check_command_access(ctx, "strikes") and user:
            for filter_strikes in self.user_strikes.values():
                if user in filter_strikes: 
                    filter_strikes[user] = 0

    async def message_filter(self, ctx: Context) -> None:
        if not self.bot.level_check(ctx, UserLevel.BROADCASTER):
            await self._spam_filter(ctx)
            await self._links_filter(ctx)
            await self._words_filter(ctx)
            await self._caps_filter(ctx)
            await self._symbols_filter(ctx)
            await self._emotes_filter(ctx)
            await self._long_message_filter(ctx)

    # Save the user messages and check if it is a repeated message to detect spam
    async def _spam_filter(self, ctx: Context) -> None:
        message = ctx.message
        user = message.author.name

        if self.repeated_messages.enable:
            if self.user_messages.get(user) and self.user_messages[user] == message.content:
                self.user_strikes['repeated_messages'][user] = self.user_strikes['repeated_messages'].get(user, 0) + 1

            self.user_messages[user] = message.content

            if self.user_strikes['repeated_messages'].get(user, 0) >= self.repeated_messages.strikes:
                await self.repeated_messages.apply_penalty(ctx, self, self.session_service.bot_account.username)

    # Check if the message contains a link
    async def _links_filter(self, ctx: Context) -> None:
        message: str = ctx.message.content
        user: str = ctx.message.author.name

        if self.links_protection.enable:
            for word in message.split():
                if re.search(MyApp.link_pattern, word):
                    self.user_strikes['links'][user] = self.user_strikes['links'].get(user, 0) + 1
                    await self.links_protection.apply_penalty(ctx, self, self.session_service.bot_account.username)
                    break

    # Check if the message lenght is greater than the maximum allowed
    async def _long_message_filter(self, ctx: Context) -> None:
        message: str = ctx.message.content
        user: str = ctx.message.author.name

        if self.long_messages.enable:
            if len(message) > self.long_messages.threshold:
                self.user_strikes['long_message'][user] = self.user_strikes['long_message'].get(user, 0) + 1
                await self.long_messages.apply_penalty(ctx, self, self.session_service.bot_account.username)

    # Check if the message contains excess of uppercase
    async def _caps_filter(self, ctx: Context) -> None:
        message: str = ctx.message.content
        user: str = ctx.message.author.name

        if self.caps_protection.enable:
            letters = [c for c in message if c.isalpha()]
            total_letters = len(letters)
            uppercase_count = sum(1 for c in letters if c.isupper())

            if total_letters > 5 and uppercase_count > 200:
                caps_ratio = uppercase_count / total_letters

                if caps_ratio >= self.caps_protection.threshold:
                    self.user_strikes['excess_caps'][user] = self.user_strikes['excess_caps'].get(user, 0) + 1
                    await self.caps_protection.apply_penalty(ctx, self, self.session_service.bot_account.username)

    # Check if the message contains excess of symbols or special characters
    async def _symbols_filter(self, ctx: Context) -> None:
        message: str = ctx.message.content
        user: str = ctx.message.author.name

        if self.symbols_protection.enable:
            total_letters = len(message)
            symbols_count = sum(1 for c in message if not c.isalnum())

            if total_letters > 5 and symbols_count > 0:
                caps_ratio = symbols_count / total_letters

                if caps_ratio >= self.symbols_protection.threshold:
                    self.user_strikes['excess_symbols'][user] = self.user_strikes['excess_symbols'].get(user, 0) + 1
                    await self.symbols_protection.apply_penalty(ctx, self, self.session_service.bot_account.username)

    # Check if the message contains excess of twitch emotes
    async def _emotes_filter(self, ctx: Context) -> None:
        message = ctx.message
        user: str = ctx.message.author.name

        if self.emotes_protection.enable:
            emotes_tag: str = message.tags.get('emotes')
            emote_count = 0

            if emotes_tag:
                parts = emotes_tag.split('/')

                for part in parts:
                    if ':' in part:
                        emote_range = part.split(':')[1]
                        emote_count += len(emote_range.split(','))

                if emote_count > self.emotes_protection.threshold:
                    self.user_strikes['excess_emotes'][user] = self.user_strikes['excess_emotes'].get(user, 0) + 1
                    await self.symbols_protection.apply_penalty(ctx, self, self.session_service.bot_account.username)

    # Check if the group is enable and is not a excluded user for each group
    async def _words_filter(self, ctx: Context) -> None:
        message: str = ctx.message.content
        user: str = ctx.message.author.name

        for group in self.banned_words.values():
            if group.enable:
                if any(word in message for word in group.words):
                    self.user_strikes['banned_words'][user] = self.user_strikes['banned_words'].get(user, 0) + 1
                    await group.apply_penalty(ctx, self, self.session_service.bot_account.username)
