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

        self.user_messages: dict[str, str] = {}
        self.spam_strikes: dict[str, str] = {}
        self.user_strikes: dict[str, dict] = {}

    # Process the message with diferent protection filters
    async def message_filter(self, ctx: Context) -> None:
        if not self.bot.level_check(ctx, UserLevel.BROADCASTER):
            if await self._spam_filter(ctx): return
            if await self._links_filter(ctx): return
            if await self._words_filter(ctx): return
            if await self._caps_filter(ctx): return
            if await self._symbols_filter(ctx): return
            if await self._emotes_filter(ctx): return
            if await self._long_message_filter(ctx): return

    # Save the user messages and check if it is a repeated message to detect spam
    async def _spam_filter(self, ctx: Context) -> bool:
        repeated_messages: Protection = self.protections.get('repeated_messages')
        message: str = ctx.message.content
        user: str = ctx.message.author.name

        if not repeated_messages.enable:
            return False

        if self.user_messages.get(user) and self.user_messages[user] == message:
            self.spam_strikes[user] = self.spam_strikes.get(user, 0) + 1
        else:
            self.spam_strikes[user] = 0

        self.user_messages[user] = message

        if self.spam_strikes.get(user, 0) >= repeated_messages.threshold - 1:
            self.user_strikes[user] = self.user_strikes.get(user, 0) + 1
            await repeated_messages.apply_penalty(ctx, self, self.session_service.bot_account.username)
            return True

        return False

    # Check if the message contains a link
    async def _links_filter(self, ctx: Context) -> bool:
        links_protection: Protection = self.protections.get('links')
        message: str = ctx.message.content
        user: str = ctx.message.author.name

        if not links_protection.enable:
            return False
        
        for word in message.split():
            if re.search(MyApp.link_pattern, word):
                if links_protection.mark_strike:
                    self.user_strikes[user] = self.user_strikes.get(user, 0) + 1

                await links_protection.apply_penalty(ctx, self, self.session_service.bot_account.username)
                return True
        
        return False

    # Check if the message lenght is greater than the maximum allowed
    async def _long_message_filter(self, ctx: Context) -> bool:
        long_messages: Protection = self.protections.get('long_messages')
        message: str = ctx.message.content
        user: str = ctx.message.author.name

        if not long_messages.enable:
            return False 
        
        if len(message) > long_messages.threshold:
            if long_messages.mark_strike:
                self.user_strikes[user] = self.user_strikes.get(user, 0) + 1

            await long_messages.apply_penalty(ctx, self, self.session_service.bot_account.username)
            return True
        
        return False

    # Check if the message contains excess of uppercase
    async def _caps_filter(self, ctx: Context) -> bool:
        caps_protection: Protection = self.protections.get('excess_caps')
        message: str = ctx.message.content
        user: str = ctx.message.author.name

        if not caps_protection.enable:
            return False

        letters = [c for c in message if c.isalpha()]
        uppercase_count = sum(1 for c in letters if c.isupper())

        if uppercase_count > caps_protection.threshold:
            if caps_protection.mark_strike:
                self.user_strikes[user] = self.user_strikes.get(user, 0) + 1

            await caps_protection.apply_penalty(ctx, self, self.session_service.bot_account.username)
            return True
            
        return False

    # Check if the message contains excess of symbols or special characters
    async def _symbols_filter(self, ctx: Context) -> bool:
        symbols_protection: Protection = self.protections.get('excess_symbols')
        message: str = ctx.message.content
        user: str = ctx.message.author.name

        if not symbols_protection.enable:
            return False

        symbols_count = sum(1 for c in message if not c.isalnum() and not c.isspace())

        if symbols_count > symbols_protection.threshold:
            if symbols_protection.mark_strike:
                self.user_strikes[user] = self.user_strikes.get(user, 0) + 1

            await symbols_protection.apply_penalty(ctx, self, self.session_service.bot_account.username)
            return True
        
        return False

    # Check if the message contains excess of twitch emotes
    async def _emotes_filter(self, ctx: Context) -> bool:
        emotes_protection: Protection = self.protections.get('excess_emotes')
        message = ctx.message
        user: str = ctx.message.author.name

        if not emotes_protection.enable:
            return False

        emotes_tag: str = message.tags.get('emotes')
        emote_count = 0

        if emotes_tag:
            parts = emotes_tag.split('/')

            for part in parts:
                if ':' in part:
                    emote_range = part.split(':')[1]
                    emote_count += len(emote_range.split(','))

            if emote_count > emotes_protection.threshold:
                if emotes_protection.mark_strike:
                    self.user_strikes[user] = self.user_strikes.get(user, 0) + 1

                await emotes_protection.apply_penalty(ctx, self, self.session_service.bot_account.username)
                return True
        
        return False

    # Check if the group is enable and is not a excluded user for each group
    async def _words_filter(self, ctx: Context) -> bool:
        message: str = ctx.message.content
        user: str = ctx.message.author.name

        for group in self.banned_words.values():
            if group.enable:
                if any(word in message for word in group.words):
                    self.user_strikes['banned_words'][user] = self.user_strikes['banned_words'].get(user, 0) + 1
                    await group.apply_penalty(ctx, self, self.session_service.bot_account.username)
                    return True
                
        
        return False
