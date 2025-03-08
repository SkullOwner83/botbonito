import os

class MyApp:
    project_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(project_path, "config")
    credentials_path = os.path.join(config_path, "credentials.json")
    botconfig_path = os.path.join(config_path, "botconfig.json")
    command_registry = {}

    @staticmethod
    def register_command(name):
        def decorator(func):
            MyApp.command_registry[name.lower()] = func
            return func
        return decorator
    
    @staticmethod
    def bind_commands(instance):
        """Recorre el registro de comandos y los vincula a la instancia correspondiente."""
        for command_name, unbound_func in MyApp.command_registry.items():
            if hasattr(instance, unbound_func.__name__):
                bound_func = getattr(instance, unbound_func.__name__)
                MyApp.command_registry[command_name] = bound_func