import logging


class PathResolver():
    def __init__(self, nodes_mapping):
        self.nodes_mapping = nodes_mapping
        self.paths = []
        self.tmp_path = []

    def resolve_paths(self, i, j, max_number_of_paths):
        paths = []
        tmp_path = []
        self.__resolve_paths(i, j, max_number_of_paths, paths, tmp_path)
        return paths

    def __resolve_paths(self, i, j, max_number_of_paths, paths, tmp_path):
        tmp_path.append((i, j))
        if i == 0 and j == 0:
            paths.append(list(tmp_path))
            tmp_path.pop()
            return
        parent_nodes = self.nodes_mapping[(i, j)]
        for parent_node in parent_nodes:
            if max_number_of_paths != 0 and max_number_of_paths == len(paths):
                logging.debug('Maximum number of paths found. Aborting further resolving')
                return
            self.__resolve_paths(parent_node[0], parent_node[1], max_number_of_paths, paths, tmp_path)
        tmp_path.pop()
