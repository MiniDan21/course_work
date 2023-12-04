from .solver import Solver
from .graph import *


# Укладка графа на плоскости (определить способ определения для класса Graph)
class Planarity(Solver):
    def __init__(self) -> None:
        super().__init__()
        self.vertex_degree_gt_3 = []
        self.vertex_degree_gt_2 = []
        self.visited = []
    def solve(self, graph: Graph, *args, **kwargs):
        planarited = True
        while len(graph.info()) > 4:
            if self.define_K_3_3(graph):
                planarited = False
                break
            elif self.define_K_5(graph):
                planarited = False
                break
            for node in graph.define_minimal_adjects_count():
                if len(node.adjects) == 0:
                    graph._del_node(node)
                else:
                    graph.tight_edge(node, node._random_adject())

        return planarited

    # def graph_traversal(self, node: Node, directed: bool = False) -> None:
    #     self.visited.append(node)
    #     if directed:
    #         if len(node.adjects.keys()) + len(node._reverse_adjects) > 2:
    #             self.vertex_degree_gt_2.append(node)
    #         if len(node.adjects.keys()) + len(node._reverse_adjects) > 3:
    #             self.vertex_degree_gt_3.append(node)
    #     else:
    #         if len(node.adjects.keys()) > 2:
    #             self.vertex_degree_gt_2.append(node)
    #         if len(node.adjects.keys()) > 3:
    #             self.vertex_degree_gt_3.append(node)
        
    #     for n in node.adjects:
    #         if n not in self.visited:
    #             self.graph_traversal(n, directed)

        
    def define_K_3_3(self, graph: Graph) -> bool:
        if len(graph.info()) != 6:
            return False
        left = set()
        right = set()
        for node in graph.info().keys():
            if len(node.adjects) != 3:
                return False
            if node.name in left or node.name in right:
                continue
            left.add(node.name)
            [right.add(n.name) for n in node.adjects.keys() if n.name not in right]
        if len(left) != 3 or len(right) != 3:
            return False
        return True
    
    def define_K_5(self, graph: Graph) -> bool:
        if len(graph.info()) != 5:
            return False
        added = set()
        for node in graph.info().keys():
            if len(node.adjects) != 4:
                return False
            if node.name in added:
                continue
            added.add(node.name)
            [added.add(n.name) for n in node.adjects.keys() if n.name not in added]
        if len(added) != 5:
            return False
        return True