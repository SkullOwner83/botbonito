import os
import re
from typing import Callable

class MyApp:
    project_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(project_path, "config")
    credentials_path = os.path.join(config_path, "credentials.json")
    botconfig_path = os.path.join(config_path, "botconfig.json")
    command_registry: dict[str, Callable] = {}

    link_pattern = re.compile(
        r'^(https?://)?'
        r'([\w.-]+)\.'
        r'([a-zA-Z]{2,})'
        r'(/[\w./?=&-]*)?$'
    )

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