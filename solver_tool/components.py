from .solver import Solver
from .graph import *


# Поиск компонентов сильной связности
class Components(Solver):
    def solve(self, graph: Graph, *args, **kwargs):
        temp = set()
        for node in graph.nodes.values():
            print(node.adjects)
            if not node in temp:
                last = self.direct_transitive_closure(node) & self.reverse_transitive_closure(node)
                temp |= last
                yield list(last)
