import unittest
from bio import solve
from bio import get_allignments


class SolveTest(unittest.TestCase):
    def test_laboratory_example(self):
        seq1 = 'SMART'
        seq2 = 'MARS'
        score_matrix, _ = solve(seq1, seq2, -2, -5, 5)
        self.assertEqual(9, score_matrix[-1, -1])

    def test_scoring_different(self):
        diff_score = -5
        # big other penalites so algorithm will choose diagonal path
        score_matrix, _ = solve('S', 'M', -100, diff_score, 100)
        self.assertEqual(0, score_matrix[0, 0])
        self.assertEqual(diff_score, score_matrix[1, 1])

    def test_scoring_same(self):
        same_score = 42
        # big other penalites so algorithm will choose diagonal path
        score_matrix, _ = solve('S', 'S', -100, -100, same_score)
        self.assertEqual(0, score_matrix[0, 0])
        self.assertEqual(same_score, score_matrix[1, 1])

    def test_scoring_gap(self):
        gap_score = 42
        # big other penalites so algorithm will choose diagonal path
        score_matrix, _ = solve('S', 'S', gap_score, -100, 42)
        self.assertEqual(0, score_matrix[0, 0])
        self.assertEqual(gap_score, score_matrix[1, 0])
        self.assertEqual(gap_score, score_matrix[0, 1])

    def test_every_node_has_parent(self):
        seq1 = 'SMART'
        seq2 = 'MARS'
        _, nodes_mapping = solve(seq1, seq2, -2, -5, 5)
        for i in range(len(seq1)):
            for j in range(len(seq2)):
                # every node except root
                if (i, j) != (0, 0):
                    self.assertTrue(len(nodes_mapping[(i, j)]) >= 1)

    def test_diagonal_allignment(self):
        a1, a2 = get_allignments([(1, 1), (0, 0)], 'S', 'M')
        self.assertEqual(a1, 'S')
        self.assertEqual(a2, 'M')

    def test_top_left_allignment(self):
        a1, a2 = get_allignments([(1, 1), (0, 1), (0, 0)], 'S', 'M')
        self.assertEqual(a1, '-S')
        self.assertEqual(a2, 'M-')

    def test_left_top_allignment(self):
        a1, a2 = get_allignments([(1, 1), (1, 0), (0, 0)], 'S', 'M')
        self.assertEqual(a1, 'S-')
        self.assertEqual(a2, '-M')

    def test_empty_path(self):
        a1, a2 = get_allignments([(0, 0)], 'S', 'M')
        self.assertEqual(a1, '')
        self.assertEqual(a2, '')

    def test_reversing_traversal_order(self):
        a1, a2 = get_allignments([(2, 2), (1, 1), (0, 0)], 'SM', 'SM')
        self.assertEqual(a1, 'SM')
        self.assertEqual(a2, 'SM')


if __name__ == '__main__':
    unittest.main()
