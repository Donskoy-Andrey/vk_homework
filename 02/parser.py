import json
from typing import List, Callable


def parse_json(
        json_str: str = "",
        required_fields: List = None,
        keywords: List = None,
        keyword_callback: Callable = None
):
    if (
            (required_fields is None) or
            (keywords is None) or
            (keyword_callback is None)
    ):
        return

    try:
        json_doc = json.loads(json_str)
    except json.decoder.JSONDecodeError:
        return

    json_doc = {key: values.split() for key, values in json_doc.items()}
    for field in required_fields:
        if field in json_doc:
            for index, word in enumerate(json_doc.get(field)):
                if word in keywords:
                    keyword_callback(field, word)