import asyncio
import threading
from typing import Dict
from bot.bot import Bot

class BotService():
    def __init__(self):
        self.bot_instance: Bot = None
        self.bot_credentials: dict = {}
        self.botconfig: dict = {}
        self._thread = None
        self._loop = None

    # Create a new thread to run the bot in the background
    def start(self, bot_credentials: Dict, botconfig: Dict) -> None:
        if self.bot_instance is None and not self._thread:
            self.botconfig = botconfig
            self.bot_credentials = bot_credentials

            self._thread = threading.Thread(target=self._create_bot)
            self._thread.daemon = True
            self._thread.start()

    # Stop the bot excecution and their thread and event loop
    def stop(self) -> None:
        if self._thread and self._loop and self.bot_instance:
            asyncio.run_coroutine_threadsafe(self.bot_instance.close(), self._loop)
            self._loop.call_soon_threadsafe(self._loop.stop)
            self.bot_instance = None
            self._loop = None
            self._thread = None
            print("bot has been stopped.")

    def delete_command(self, command_name) -> bool:
        if self.bot_instance:
            try:
                self.bot_instance.remove_command(command_name)
                return True
            except Exception as e:
                pass
            
        return False
    
    # def modify_command(self, command_name):
    #     if self.bot_instance:


    # Create a event loop in the new thread and instance the bot into this loop
    def _create_bot(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self.bot_instance = Bot(self.botconfig, self.bot_credentials)
        self._loop.create_task(self.bot_instance.start())
        self._loop.run_forever()