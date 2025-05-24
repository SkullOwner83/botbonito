import asyncio
import threading
import time
from typing import Dict
from myapp import MyApp
from bot.bot import Bot
from modules.file import File

class BotService():
    def __init__(self):
        self.bot_instance = None
        self.credentials = {}
        self.botconfig = {}

        self._thread = None
        self._loop = None

    # Create a new thread to run the bot in the background
    def start(self, botconfig: Dict, credentials: Dict) -> None:
        if self.bot_instance is None and not self._thread:
            self.botconfig = botconfig
            self.credentials = credentials

            self._thread = threading.Thread(target=self._create_bot)
            self._thread.daemon = True
            self._thread.start()

    # Create a event loop in the new thread and instance the bot into this loop
    def _create_bot(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self.bot_instance = Bot(self.botconfig, self.credentials)
        self._loop.run_until_complete(self.bot_instance.start())