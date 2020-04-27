"""Functions to read and write JSON files."""
import json


def load_json(fileName: str) -> None:
    """Load file from JSON file."""
    try:
        f = open(fileName, "r")
    except OSError:
        raise OSError
        return
    try:
        json_data = json.load(f)
    except ValueError:
        raise ValueError
        return
    f.close()
    return json_data


def write_json(file_name: str, data: list) -> None:
    """Write data to JSON file."""
    try:
        f = open(file_name, "w")
        json_data = json.dumps(data, indent="\t", sort_keys=True)
        f.write(json_data)
        f.close()
        return
    except OSError:
        return
