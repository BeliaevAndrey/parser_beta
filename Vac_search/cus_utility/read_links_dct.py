import json


def read_json(file_name: str) -> dict[str, str]:
    with open(file_name, 'r', encoding='utf-8') as f_in:
        out_dict = json.load(f_in)
    return out_dict
