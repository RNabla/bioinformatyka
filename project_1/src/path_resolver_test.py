import unittest

from path_resolver import PathResolver


class PathResolvingTest(unittest.TestCase):
    @staticmethod
    # path from laboratory example (MARS vs SMART)
    def get_nodes_mapping():
        return {(0, 1): [(0, 0)],
                (0, 2): [(0, 1)],
                (0, 3): [(0, 2)],
                (0, 4): [(0, 3)],
                (0, 5): [(0, 4)],
                (1, 0): [(0, 0)],
                (1, 1): [(0, 0)],
                (1, 2): [(0, 1)],
                (1, 3): [(0, 2), (1, 2)],
                (1, 4): [(0, 3)],
                (1, 5): [(0, 4)],
                (2, 0): [(1, 0)],
                (2, 1): [(1, 0)],
                (2, 2): [(1, 1), (1, 2)],
                (2, 3): [(1, 2)],
                (2, 4): [(2, 3)],
                (2, 5): [(1, 4), (2, 4)],
                (3, 0): [(2, 0)],
                (3, 1): [(2, 0)],
                (3, 2): [(2, 1)],
                (3, 3): [(2, 3)],
                (3, 4): [(2, 3)],
                (3, 5): [(3, 4)],
                (4, 0): [(3, 0)],
                (4, 1): [(3, 0), (3, 1)],
                (4, 2): [(3, 1)],
                (4, 3): [(3, 2), (3, 3)],
                (4, 4): [(3, 4)],
                (4, 5): [(3, 5), (4, 4)]}

    def test_path_resolving_from_top_left(self):
        nodes_mapping = PathResolvingTest.get_nodes_mapping()
        path_resolver = PathResolver(nodes_mapping)
        paths = path_resolver.resolve_paths(0, 0)
        self.assertEqual(len(paths), 1)

    def test_path_resolving_from_top_right(self):
        nodes_mapping = PathResolvingTest.get_nodes_mapping()
        path_resolver = PathResolver(nodes_mapping)
        paths = path_resolver.resolve_paths(0, 5)
        self.assertEqual(len(paths), 1)

    def test_path_resolving_from_bottom_left(self):
        nodes_mapping = PathResolvingTest.get_nodes_mapping()
        path_resolver = PathResolver(nodes_mapping)
        paths = path_resolver.resolve_paths(4, 0)
        self.assertEqual(len(paths), 1)

    def test_path_resolving_from_bottom_right(self):
        nodes_mapping = PathResolvingTest.get_nodes_mapping()
        path_resolver = PathResolver(nodes_mapping)
        paths = path_resolver.resolve_paths(4, 5)
        self.assertEqual(len(paths), 2)

    def test_path_resolving_from_bottom_right_with_restrictions(self):
        max_number_of_paths = 1
        nodes_mapping = PathResolvingTest.get_nodes_mapping()
        path_resolver = PathResolver(nodes_mapping)
        paths = path_resolver.resolve_paths(4, 5, max_number_of_paths)
        self.assertEqual(len(paths), max_number_of_paths)


if __name__ == '__main__':
    unittest.main()
