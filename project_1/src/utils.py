import json
from pathlib import Path


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_fasta_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return ''.join(f.readlines()[1:]).strip()


def save_output(path, seq1, seq2, config, allignments, score_matrix):
    Path(path).parent.mkdir(exist_ok=True, parents=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({
            'seq1': seq1,
            'seq2': seq2,
            'config': config,
            'allignments': allignments,
            'score_matrix': score_matrix.tolist()
        }, f, indent=2)


def save_output2(path, data):
    Path(path).parent.mkdir(exist_ok=True, parents=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
