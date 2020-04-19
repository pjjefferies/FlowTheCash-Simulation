"""Functions to read and write JSON files."""
import json


def load_json(fileName):
    """Load file from JSON file."""
    try:
        f = open(fileName, "r")
    except OSError:
        raise OSError
        return
    try:
        jsonData = json.load(f)
    except ValueError:
        raise ValueError
        return
    f.close()
    return jsonData


def write_json(databaseFile, listOfCarData):
    """Write data to JSON file."""
    try:
        f = open(databaseFile, "w")
        jsonCarData = json.dumps(listOfCarData, indent="\t", sort_keys=True)
        f.write(jsonCarData)
        f.close()
        return
    except OSError:
        return
