# Read each line and split in two parts by iqual character adn save in a dictionary
def ReadDictionary(Path):
    with open(Path, "r") as File:
        Lines = File.readlines()
        Dictionary = {}

        for Line in Lines:
            Parts = Line.replace("\n","").split("=")
            Dictionary[Parts[0]] = Parts[1]

    return Dictionary

def WriteDictionary(Path, Dictionary):
    with open(Path, "w") as File:
        for Key, Value in Dictionary.items():
            Line = f"{Key}={Value}\n"
            File.write(Line)