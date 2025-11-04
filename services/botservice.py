import asyncio
from threading import Thread
from bot.bot import Bot
from models.appconfig import AppConfig

class BotService():
    def __init__(self):
        self.bot_instance: Bot = None
        self.bot_credentials: dict[str, str] = None
        self.app_config: AppConfig = None
        self.is_running: bool = False
        self._thread = None
        self._loop = None

    # Create a new thread to run the bot in the background
    def start(self) -> None:
        if self.bot_instance is None and not self._thread:
            self._thread = Thread(target=self._create_bot, daemon=True)
            self._thread.start()

    # Stop the bot excecution and their thread and event loop
    def stop(self) -> None:
        if self._thread and self._loop and self.bot_instance:
            asyncio.run_coroutine_threadsafe(self.bot_instance.close(), self._loop)
            self._loop.call_soon_threadsafe(self._loop.stop)
            self.bot_instance = None
            self.is_running = False
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

    # Create a event loop in the new thread and instance the bot into this loop
    def _create_bot(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self.bot_instance = Bot(self.app_config, self.bot_credentials)
        self.is_running = True
        self._loop.create_task(self.bot_instance.start())
        self._loop.run_forever()