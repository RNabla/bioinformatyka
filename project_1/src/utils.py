import json
from pathlib import Path


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_fasta_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return ''.join(f.readlines()[1:]).strip().replace('\n', '')


def save_output(path, data):
    Path(path).parent.mkdir(exist_ok=True, parents=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
