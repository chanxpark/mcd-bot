import json


def dump_json(file_name: str, data: list):
    with open(f'tmp/{file_name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f'Successfully loaded {file_name}')


def sanitize_str(data: str) -> str:
    """
    removes all whitespaces and lowercase string
    """
    return ''.join(data.split()).lower()
