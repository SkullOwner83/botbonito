import os
import json

class File:
    @staticmethod
    def open(path: str) -> dict:
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file could not be found in the path {path}.")

        with open(path, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                raise ValueError("The file is not a valid format.")

        return None
    
    @staticmethod
    def save(path: str, data: dict) -> None:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)