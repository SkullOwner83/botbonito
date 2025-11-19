from threading import Lock
from models.eventsub import EventSub
from config.event_subs import get_event_subs
from myapp import MyApp
from utilities.file import File

class EventService():
    def __init__(self):
        self._lock = Lock()
        self.events: dict[str, EventSub] = {}
        self.load_events()

    # Read the stored file and load them into the dictionary of events
    def load_events(self) -> None:
        with self._lock:
            self.events = get_event_subs()

            try:
                stored_config: dict = File.open(MyApp.events_path)
            except FileNotFoundError:
                stored_config = {}
                File.save(MyApp.events_path, stored_config)

            for name, data in stored_config.items():
                command = self.events[name]
                    
                for attr, val in data.items():
                    if hasattr(command, attr):
                        setattr(command, attr, val)

    # Convert the events to a dictionary and save them to the file
    def save_events(self) -> None:
        with self._lock:
            dictionary = {
                name: data.__dict__
                for name, data in self.events.items()
            }

            File.save(MyApp.events_path, dictionary)