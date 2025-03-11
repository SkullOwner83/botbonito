import os
from modules.file import File
from modules.api import Api
from myapp import MyApp

class Moderation():
    def __init__(self, bot):
        self.bot = bot
        self.moderation_config = File.open(os.path.join(MyApp.config_path, 'moderation.json'))
        self.banned_words = self.words.get('filters')['words']

    async def message_filter(self, message):
        if any(word in message.content for word in self.banned_words):
            api = Api(self.bot.token, self.bot.client_id)

            broadcaster_data = api.get_user(message.channel.name)
            moderator_data = api.get_user(self.bot.name)

            broadcaster_id = broadcaster_data['id']
            moderator_id = moderator_data['id']
            
            message_id = message.tags['id']

            api.delete_message(broadcaster_id, moderator_id, message_id)