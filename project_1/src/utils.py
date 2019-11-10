import json
from pathlib import Path


def assert_required_keys(dict_obj, required_keys):
    for key in required_keys:
        if key not in dict_obj:
            raise KeyError(f'config must have \'{key}\' value specified')


def load_config_from_json_file(path, required_keys=[]):
    with open(path, 'r', encoding='utf-8') as f:
        config = json.load(f)
        assert_required_keys(config, required_keys)
        return config


def load_fasta_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return ''.join(f.readlines()[1:]).strip().replace('\n', '')


def save_output(path, data):
    Path(path).parent.mkdir(exist_ok=True, parents=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
