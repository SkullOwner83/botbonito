import os

class MyApp:
    project_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(project_path, "config")
    credentials_path = os.path.join(config_path, "credentials.json")
    botconfig_path = os.path.join(config_path, "botconfig.json")