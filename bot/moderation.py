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
        self.user_strikes = {}
        self.user_messages = {}

        self.user_repeated_strikes ={}

    async def message_filter(self, ctx):
        message = ctx.message
        user = message.author.name
        api = Api(self.bot.token, self.bot.client_id)

        user_data = api.get_user(user)
        broadcaster_data = api.get_user(message.channel.name)
        moderator_data = api.get_user(self.bot.name)

        user_id = user_data['id']
        broadcaster_id = broadcaster_data['id']
        moderator_id = moderator_data['id']
        message_id = message.tags['id']

        if self.protection.get("repeated_messages", {}).get('enable'):
            strikes = self.protection["repeated_messages"].get("strikes")
            reason = self.protection["repeated_messages"].get("reason")

            if self.user_messages.get(user) and self.user_messages[user] == message.content:
                self.user_repeated_strikes[user] = self.user_repeated_strikes.get(user, 0) + 1
            
            self.user_messages[user] = message.content

            if self.user_repeated_strikes.get(user, 0) >= strikes:
                api.set_ban(broadcaster_id, moderator_id, user_id, reason)

        # Check if the links protection is enable to delete the message if it contains a link
        if self.protection.get('links', {}).get('enable'):
            for word in message.content.split():
                if re.search(MyApp.link_pattern, word):
                    api.delete_message(broadcaster_id, moderator_id, message_id)
                    await ctx.send('Por seguridad, no esta permitido enviar links.')

        # Check if the group is enable and is not a excluded user for each group
        for group in self.banned_words.values():
            if group.get('enable', False) and not self.bot.level_check(ctx, group.get('exclude', 'no_one')):
                target_words = group.get('words', [])
                penalty = group.get('penalty', 'delete_message')
                reason = group.get('reason', '')
                duration = group.get('duration', 0)
                strikes = group.get('strikes', 0)

                # Check if the message matches the banned words and apply the penalty
                if any(word in message.content for word in target_words):
                    if penalty != 'ban_user' and strikes > 0:
                        if user in self.user_strikes:
                            self.user_strikes[user] += 1
                        else:
                            self.user_strikes[user] = 1

                        if self.user_strikes[user] >= strikes:
                            penalty = 'ban_user'

                    match(penalty):
                        case 'delete_message': 
                            api.delete_message(broadcaster_id, moderator_id, message_id)
                            if reason: await ctx.send(f"Se ha eliminado el mensaje de @{user}. {reason}")
                            
                        case 'timeout': api.set_timeout(broadcaster_id, moderator_id, user_id, duration, reason)
                        case 'ban_user': api.set_ban(broadcaster_id, moderator_id, user_id, reason)
