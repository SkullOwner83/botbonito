import os

class MyApp:
    project_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(project_path, "config")
    credentials_path = os.path.join(config_path, "credentials.json")
    botconfig_path = os.path.join(config_path, "botconfig.json")
    colors = {
            "blue": "#0000FF",
            "BlueViolet": "#8A2BE2",
            "CadetBlue": "#5F9EA0",
            "Chocolate": "#D2691E",
            "Coral": "#FF7F50",
            "DodgerBlue": "#1E90FF",
            "Firebrick": "#B22222",
            "GoldenRod": "#DAA520",
            "Green": "#008000",
            "HotPink": "#FF69B4",
            "OrangeRed": "#FF4500",
            "Red": "#FF0000",
            "SeaGreen": "#2E8B57",
            "SpringGreen": "#00FF7F",
            "YellowGreen": "#9ACD32"
        }