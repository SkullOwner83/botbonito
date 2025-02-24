import os
import json

class File:
    @staticmethod
    def open(path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
    
    @staticmethod
    def save(path, data):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)