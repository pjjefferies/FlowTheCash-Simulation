"""Functions to read and write JSON files."""
import json


def load_json(file_name: str) -> None:
    """Load file from JSON file."""
    with open(file_name) as f:
        json_data = json.load(f)

    return json_data


def write_json(file_name: str, data: list) -> None:
    """Write data to JSON file."""
    json_data = json.dumps(data, indent='\t', sort_keys=True)

    with open(file_name, 'w') as f:
        f.write(json_data)
