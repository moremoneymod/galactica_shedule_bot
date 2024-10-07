import json
from typing import Dict, Union, Any, List, Type

JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]


def json_converter(dict_to_convert: Dict | List) -> JSON:
    json_dict = json.dumps(dict_to_convert, ensure_ascii=False)
    return json_dict


def save_json(json_file: JSON, file_name="schedule.json") -> None:
    with open(file_name, 'w') as outfile:
        outfile.write(json_file)
