import os
from modules.file import File
from modules.api import Api
from myapp import MyApp

class Moderation():
    def __init__(self, bot):
        self.bot = bot
        self.moderation_config = File.open(os.path.join(MyApp.config_path, 'moderation.json'))
        self.banned_words = self.moderation_config.get('banned_words')

    async def message_filter(self, ctx):
        message = ctx.message
        user = message.author.name

        # Check if the group is enable and is not a excluded user for each group
        for group in self.banned_words.values():
            if group.get('enable', False) and not self.bot.level_check(ctx, group.get('exclude', 'no_one')):
                target_words = group.get('words', [])
                penalty = group.get('penalty', 'delete_message')
                reason = group.get('reason', '')
                duration = group.get('duration', 0)
                api = Api(self.bot.token, self.bot.client_id)

                user_data = api.get_user(user)
                broadcaster_data = api.get_user(message.channel.name)
                moderator_data = api.get_user(self.bot.name)

                user_id = user_data['id']
                broadcaster_id = broadcaster_data['id']
                moderator_id = moderator_data['id']
                message_id = message.tags['id']
                
                # Check if the message matches the banned words and apply the penalty
                if any(word in message.content for word in target_words):
                    match(penalty):
                        case 'delete_message': 
                            api.delete_message(broadcaster_id, moderator_id, message_id)
                            if reason: await self.bot.send_message(f"Se ha eliminado el mensaje de @{user}. {reason}")
                            
                        case 'timeout':
                            api.ban_user(broadcaster_id, moderator_id, user_id=user_id, duration=duration, timeout=True)
                            if reason: await self.bot.send_message(f"El usuario @{user} ha recibido una penalización de {duration}s. {reason}")

                        case 'ban_user':
                            api.ban_user(broadcaster_id, moderator_id, user_id=user_id)
                            if reason: await self.bot.send_message(f"El usuario @{user} ha sido baneado. {reason}")
