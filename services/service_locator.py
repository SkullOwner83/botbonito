from threading import Lock

class ServiceLocator():
    _services = {}
    _lock = Lock()

    @classmethod
    def register(cls, name: str, service: object):
        with cls._lock:
            cls._services[name] = service
    
    @classmethod
    def get(cls, name):
        with cls._lock:
            return cls._services.get(name)