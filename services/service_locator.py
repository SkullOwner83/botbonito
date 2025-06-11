from threading import Lock

class ServiceLocator():
    _services = {}
    _instance = None
    _lock = Lock()

    @staticmethod
    def register(name: str, service: object):
        ServiceLocator._services[name] = service
    
    @staticmethod
    def get(name):
        return ServiceLocator._services.get(name)
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        
        return cls._instance