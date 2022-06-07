import json


def dump_json(file_name: str, data: list):
    """
    dump json to file
    """
    with open(f'tmp/{file_name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f'Successfully loaded {file_name}')

def load_json(file_path: str):
    """
    loads json from file
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    print(f'Successfully loaded {file_path}')
    return data


def sanitize_str(data: str) -> str:
    """
    removes all whitespaces and lowercase string
    """
    return ''.join(data.split()).lower()
