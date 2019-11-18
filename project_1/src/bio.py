import numpy as np
import sys
import json
import logging
from argparse import ArgumentParser
from pprint import pformat
from utils import load_fasta_file
from utils import load_config_from_json_file
from utils import save_output
from path_resolver import PathResolver


def get_init_score_matrix(len1, len2, gap_score):
    score_matrix = np.zeros((len1, len2))
    nodes_mapping = {}
    for i in range(1, len1):
        score_matrix[i, 0] = gap_score * i
        nodes_mapping[(i, 0)] = [(i-1, 0)]
    for i in range(1, len2):
        score_matrix[0, i] = gap_score * i
        nodes_mapping[(0, i)] = [(0, i-1)]
    return score_matrix, nodes_mapping


def solve(seq1, seq2, gap_score, diff_score, same_score):
    len1 = len(seq1) + 1
    len2 = len(seq2) + 1
    logging.info('Solving score matrix for:')
    logging.info('Sequence 1: %s' % seq1)
    logging.info('Sequence 2: %s' % seq2)
    score_matrix, nodes_mapping = get_init_score_matrix(len1, len2, gap_score)
    for depth in range(1, len1 + len2):
        for i in range(1, len1):
            j = depth - i
            if j in range(1, len2):
                diag = score_matrix[i - 1, j - 1] + (same_score if seq1[i - 1] == seq2[j - 1] else diff_score)
                up = score_matrix[i - 1, j] + gap_score
                left = score_matrix[i, j - 1] + gap_score
                best_score = max(diag, up, left)
                parent_nodes = []
                if diag == best_score:
                    parent_nodes.append((i-1, j-1))
                if up == best_score:
                    parent_nodes.append((i-1, j))
                if left == best_score:
                    parent_nodes.append((i, j-1))
                nodes_mapping[(i, j)] = parent_nodes
                score_matrix[i, j] = best_score

    return score_matrix, nodes_mapping


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
    logging.info('User args: %s' % pformat(args))
    config = load_config_from_json_file(args.config, ['gap', 'same', 'diff', 'max_number_of_paths', 'max_sequence_length'])
    logging.info('Config is: \n%s' % pformat(config))

    seq1 = load_fasta_file(args.input1)
    seq2 = load_fasta_file(args.input2)
    if config['max_sequence_length'] != 0 and max(len(seq1), len(seq2)) > config['max_sequence_length']:
        raise ValueError('Sequence exceeded max_sequence_length ')

    score_matrix, nodes_mapping = solve(seq1, seq2, config['gap'], config['diff'], config['same'])

    logging.debug('Score matrix: \n%s' % pformat(score_matrix))
    logging.debug('Nodes mapping: (target_node): [(parent_node),...]\n%s' % pformat(nodes_mapping))
    logging.info('Alignments score: %s' % score_matrix[len(seq1), len(seq2)])

    paths = PathResolver(nodes_mapping).resolve_paths(len(seq1), len(seq2), config['max_number_of_paths'])

    allignments = [get_allignments(path, seq1, seq2) for path in paths]

    for (allignment_1, allignment_2), i in zip(allignments, range(len(allignments))):
        logging.info('[A%04d] %s' % (i, allignment_1))
        logging.info('[A%04d] %s' % (i, allignment_2))

    if args.output:
        save_output(args.output, {
            'seq1': seq1,
            'seq2': seq2,
            'config': config,
            'allignments': allignments,
            'score_matrix': score_matrix.tolist()
        })
        logging.info('Saved output to %s' % args.output)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input1', type=str, default='../data/in1.txt', help='Path to the file where first sequence is stored.')
    parser.add_argument('--input2', type=str, default='../data/in2.txt', help='Path to the file where second sequence is stored.')
    parser.add_argument('--config', type=str, default='../configs/config.json', help='Path to the config file. Format must be json.')
    parser.add_argument('--output', type=str, default=None, help='Path to the output file. Format will be json.')
    parser.add_argument('--logging', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Set the logging level', default='INFO')
    args = parser.parse_args(sys.argv[1:])
    try:
        main(args)
    except Exception as ex:
        logging.critical(ex)
