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
            if len(graph.info()) == 6:
                # Основано на авторском алгоритме, где из 6 вершин находится подграф К3,3
                if self.define_K_3_3(graph):
                    planarited = False
                    break
            elif self.define_K_5(graph):
                planarited = False
                break

            # ИСПРАВИТЬ КОСТЫЛЬ ДЛЯ ДВУДОЛЬНЫХ ГРАФОВ
            node = graph.define_minimal_adjects_count()[-1]
            if len(node.adjects) == 0:
                graph._del_node(node)
            else:                    
                graph.tight_edge(node, node._random_adject())

        return planarited

    def define_K_3_3(self, graph: Graph) -> bool:
        if len(graph.info()) != 6:
            return False
        left = set()
        right = set()
        # Если у кого-то 5 вершин, то по сути он со всеми связан, неважно в какую долю его запихивать, пока других не распределим
        five_edges = set()
        for node in graph.info().keys():
            if len(node.adjects) < 3:
                return False
            
            if node.name in left or node.name in right:
                continue

            if len(node.adjects) == 5:
                five_edges.add(node.name)
                continue
            left.add(node.name)
            for n in node.adjects.keys():
                if n.name not in right and len(n.adjects) != 5:
                    right.add(n.name)
                elif len(n.adjects) == 5:
                    five_edges.add(n.name)

        for five in five_edges:
            if five not in right and five not in left:
                min(left, right, key=len).add(five)
        if len(left) != 3 or len(right) != 3:
            return False
        
        # Проверка на то, что все вершины из противоположной доли являются смежными текущей вершине
        for node in graph.info().keys():
            adjects = set(node.adjects.keys())
            result = set()
            if node in left:
                result = right - adjects
            if node in right:
                result = left - adjects
            if len(result) > 0:
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