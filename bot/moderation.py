import os
import re
from modules.file import File
from modules.api import Api
from myapp import MyApp

class Moderation():
    def __init__(self, bot):
        self.bot = bot
        self.moderation_config = File.open(os.path.join(MyApp.config_path, 'moderation.json'))  
        self.banned_words = self.moderation_config.get('banned_words')
        self.protection = self.moderation_config.get('protection')
        self.user_messages = {}
        self.user_strikes = {
            "Links": {},
            "repeated_messages": {},
            "banned_words": {}
        }

    async def message_filter(self, ctx):
        message = ctx.message
        user = message.author.name
        api = Api(self.bot.token, self.bot.client_id)
        penalty = ''
        reason = ''
        exclude = 'no_one'
        duration = 0
        strikes = 0

        user_data = api.get_user(user)
        broadcaster_data = api.get_user(message.channel.name)
        moderator_data = api.get_user(self.bot.name)

        user_id = user_data['id']
        broadcaster_id = broadcaster_data['id']
        moderator_id = moderator_data['id']
        message_id = message.tags['id']

        # Save the user messages and check if it is a repeated message to detect spam
        if self.protection.get('repeated_messages', {}).get('enable'):
            strikes = self.protection['repeated_messages'].get('strikes', strikes)

            if self.user_messages.get(user) and self.user_messages[user] == message.content:
                self.user_strikes['repeated_messages'][user] = self.user_strikes['repeated_messages'].get(user, 0) + 1
            
            self.user_messages[user] = message.content

            if self.user_strikes['repeated_messages'].get(user, 0) >= strikes:
                penalty = self.protection['repeated_messages'].get('penalty')
                reason = self.protection['repeated_messages'].get("reason", '')
                exclude = self.protection['repeated_messages'].get('exclude', exclude)
                duration = self.protection['repeated_messages'].get('duration', 0)

        # Check if the links protection is enable to delete the message if it contains a link
        if self.protection.get('links', {}).get('enable'):
            strikes = self.protection['links'].get('strikes', strikes)

            for word in message.content.split():
                if re.search(MyApp.link_pattern, word):
                    self.user_strikes['links'][user] = self.user_strikes['links'].get(user, 0) + 1
                    penalty = self.protection['links'].get('penalty')
                    reason = self.protection['links'].get('reason')
                    exclude = self.protection['links'].get('exclude', exclude)
                    duration = self.protection['links'].get('duration', 0)

        # Check if the group is enable and is not a excluded user for each group
        for group in self.banned_words.values():
            if group.get('enable', False):
                target_words = group.get('words', [])
                strikes = group.get('strikes', strikes)

                # Check if the message matches the banned words and apply the penalty
                if any(word in message.content for word in target_words):
                    self.user_strikes['banned_words'][user] = self.user_strikes['banned_words'].get(user, 0) + 1
                    penalty = group.get('penalty', 'delete_message')
                    reason = group.get('reason', '')
                    exclude = group.get('exclude', exclude)
                    duration = group.get('duration', 0)

        # Check if the user has an exception or not to aply the penalty
        if not self.bot.level_check(ctx, exclude):
            if penalty != 'ban_user' and strikes > 0:
                for filter_strikes in self.user_strikes.values():
                    if filter_strikes.get(user, 0) >= strikes:
                        penalty = 'ban_user'

            match(penalty):
                case 'delete_message': 
                    api.delete_message(broadcaster_id, moderator_id, message_id)
                    if reason: await ctx.send(f"Se ha eliminado el mensaje de @{user}. {reason}")
                    
                case 'timeout': api.set_timeout(broadcaster_id, moderator_id, user_id, duration, reason)
                case 'ban_user': api.set_ban(broadcaster_id, moderator_id, user_id, reason)