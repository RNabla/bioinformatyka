from argparse import ArgumentParser
from pprint import pformat
from pathlib import Path
import numpy as np
import sys
import json
import logging

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_flat_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


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


def solve(seq1, seq2, config):
    len1 = len(seq1) + 1
    len2 = len(seq2) + 1
    logging.info('Solving score matrix for:')
    logging.info('Sequence 1: %s' % seq1)
    logging.info('Sequence 2: %s' % seq2)
    score_matrix = np.zeros((len1, len2))
    nodes_mapping = {}
    for i in range(1, len1):
        score_matrix[i, 0] = config['gap'] * i
        nodes_mapping[(i, 0)] = [(i-1, 0)]
    for i in range(1, len2):
        score_matrix[0, i] = config['gap'] * i
        nodes_mapping[(0, i)] = [(0, i-1)]

    for depth in range(1, len1 + len2):
        for i in range(1, len1):
            j = depth - i
            if j in range(1, len2):
                diag = score_matrix[i - 1, j - 1] + config['same'] if seq1[i - 1] == seq2[j - 1] else config['diff']
                up = score_matrix[i - 1, j] + config['gap']
                right = score_matrix[i, j - 1] + config['gap']
                best_option = max(diag, up, right)
                parent_nodes = []
                if diag == best_option:
                    parent_nodes.append((i-1, j-1))
                if up == best_option:
                    parent_nodes.append((i-1, j))
                if right == best_option:
                    parent_nodes.append((i, j-1))
                nodes_mapping[(i, j)] = parent_nodes
                score_matrix[i, j] = best_option

    # for depth in range(1, len1 + len2):
    #     for i in range(1, len1):
    #         # TODO: remove j loop
    #         for j in range(1, len2):
    #             if i + j == depth:
    #                 diag = score_matrix[i - 1, j - 1] + config['same'] if seq1[i - 1] == seq2[j - 1] else config['diff']
    #                 up = score_matrix[i - 1, j] + config['gap']
    #                 right = score_matrix[i, j - 1] + config['gap']
    #                 best_option = max(diag, up, right)
    #                 parent_nodes = []
    #                 if diag == best_option:
    #                     parent_nodes.append((i-1, j-1))
    #                 if up == best_option:
    #                     parent_nodes.append((i-1, j))
    #                 if right == best_option:
    #                     parent_nodes.append((i, j-1))
    #                 nodes_mapping[(i, j)] = parent_nodes
    #                 score_matrix[i, j] = best_option

    return score_matrix, nodes_mapping


class PathResolver():
    def __init__(self, nodes_mapping, max_number_of_paths):
        self.nodes_mapping = nodes_mapping
        self.paths = []
        self.tmp_path = []
        self.max_number_of_paths = max_number_of_paths

    def resolve_path(self, i, j):
        self.tmp_path.append((i, j))
        if i == 0 and j == 0:
            self.paths.append(list(self.tmp_path))
            self.tmp_path.pop()
            return
        parent_nodes = self.nodes_mapping[(i, j)]
        for node in parent_nodes:
            if self.max_number_of_paths != 0 and self.max_number_of_paths == len(self.paths):
                logging.debug('Maximum number of paths found. Aborting further resolving')
                return
            self.resolve_path(node[0], node[1])
        self.tmp_path.pop()


def get_allignments(path, seq1, seq2):
    alignment_1 = []
    alignment_2 = []
    logging.debug('Resolving alignment for path %s' % path)
    for to_node, from_node in zip(path, path[1:]):
        if from_node[0] + 1 == to_node[0] and from_node[1] + 1 == to_node[1]:
            alignment_1.append(seq1[from_node[0]])
            alignment_2.append(seq2[from_node[1]])
            logging.debug('Moving left and up and appending %s and %s' % (seq1[from_node[0]], seq2[from_node[1]]))
        elif from_node[0] + 1 == to_node[0]:
            logging.debug('Moving up and appending %s and %s' % (seq1[from_node[0]], '-'))
            alignment_1.append(seq1[from_node[0]])
            alignment_2.append('-')
        elif from_node[1] + 1 == to_node[1]:
            logging.debug('Moving left and appending %s and %s' % ('-', seq2[from_node[1]]))
            alignment_1.append('-')
            alignment_2.append(seq2[from_node[1]])
    return ''.join(reversed(alignment_1)), ''.join(reversed(alignment_2))


def main(args):
    logging.basicConfig(level=logging.getLevelName(args.logging))
    config = load_json(args.config)
    logging.info('User args: %s' % pformat(args))
    logging.info('Config is: \n%s' % pformat(config))

    seq1 = load_flat_file(args.input1)
    seq2 = load_flat_file(args.input2)
    if min(len(seq1), len(seq2)) > config['max_sequence_length']:
        raise ValueError('Sequence exceeded max_sequence_length ')

    score_matrix, nodes_mapping = solve(seq1, seq2, config)

    logging.debug('Score matrix: \n%s' % pformat(score_matrix))
    logging.debug('Nodes mapping: (target_node): [(parent_node),...]\n%s' % pformat(nodes_mapping))
    logging.info('Alignments score: %s' % score_matrix[len(seq1), len(seq2)])

    path_resolver = PathResolver(nodes_mapping, config['max_number_of_paths'])
    path_resolver.resolve_path(len(seq1), len(seq2))

    allignments = [get_allignments(path, seq1, seq2) for path in path_resolver.paths]

    for (allignment_1, allignment_2), i in zip(allignments, range(len(allignments))):
        logging.info('[A%04d] %s' % (i, allignment_1))
        logging.info('[A%04d] %s' % (i, allignment_2))

    if args.output:
        save_output(args.output, seq1, seq2, config, allignments, score_matrix)
        logging.info('Saved output to %s' % args.output)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input1', type=str, default='../data/in1.txt', help='Path to the file where first sequence is stored.')
    parser.add_argument('--input2', type=str, default='../data/in2.txt', help='Path to the file where second sequence is stored.')
    parser.add_argument('--config', type=str, default='../configs/config.json', help='Path to the config file. Format must be json.')
    parser.add_argument('--output', type=str, default=None, help='Path to the output file. Format will be json.')
    parser.add_argument('--logging', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Set the logging level', default='INFO')
    args = parser.parse_args(sys.argv[1:])
    main(args)

